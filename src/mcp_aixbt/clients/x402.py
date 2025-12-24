"""x402 payment protocol handler for pay-per-request endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Any, Optional

import httpx
from pydantic import BaseModel

from mcp_aixbt.config import Settings
from mcp_aixbt.utils.errors import AIXBTError, BudgetExceededError

logger = logging.getLogger(__name__)

# Base chain ID
BASE_CHAIN_ID = 8453

# USDC contract on Base
USDC_TOKEN_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"


class PaymentChallenge(BaseModel):
    """Parsed 402 payment challenge."""

    amount: str
    currency: str
    token_address: str
    recipient: str
    chain_id: int


class SpendTracker:
    """Track daily x402 spending."""

    def __init__(self, daily_limit_usdc: float) -> None:
        self._daily_limit = daily_limit_usdc
        self._current_spend = 0.0
        self._reset_date = datetime.now().date()

    def _maybe_reset(self) -> None:
        """Reset spend counter at midnight."""
        today = datetime.now().date()
        if today > self._reset_date:
            self._current_spend = 0.0
            self._reset_date = today

    def can_spend(self, amount_usdc: float) -> bool:
        """Check if spending amount is within budget."""
        self._maybe_reset()
        return (self._current_spend + amount_usdc) <= self._daily_limit

    def record_spend(self, amount_usdc: float) -> None:
        """Record a spend."""
        self._maybe_reset()
        self._current_spend += amount_usdc

    @property
    def remaining_budget(self) -> float:
        """Get remaining daily budget."""
        self._maybe_reset()
        return max(0, self._daily_limit - self._current_spend)


def parse_402_response(response_data: dict[str, Any]) -> PaymentChallenge:
    """Parse payment challenge from 402 response."""
    payment = response_data.get("payment", {})
    return PaymentChallenge(
        amount=payment.get("amount", "0"),
        currency=payment.get("currency", "USDC"),
        token_address=payment.get("token_address", USDC_TOKEN_ADDRESS),
        recipient=payment.get("recipient", ""),
        chain_id=payment.get("chain_id", BASE_CHAIN_ID),
    )


def amount_to_usdc(amount_str: str) -> float:
    """Convert amount string to USDC (6 decimals)."""
    try:
        return int(amount_str) / 1_000_000
    except (ValueError, TypeError):
        return 0.0


class X402Handler:
    """Handler for x402 payment protocol."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._spend_tracker = SpendTracker(settings.max_spend_per_day_usdc)
        self._has_wallet = settings.evm_private_key is not None

    def _get_private_key(self) -> str:
        """Get private key from settings."""
        if not self._settings.evm_private_key:
            raise AIXBTError("EVM_PRIVATE_KEY not configured for x402 payments")
        return self._settings.evm_private_key.get_secret_value()

    def _sign_payment(self, challenge: PaymentChallenge) -> str:
        """Sign payment challenge with EIP-712."""
        try:
            from eth_account import Account
            from eth_account.messages import encode_typed_data
        except ImportError:
            raise AIXBTError(
                "eth-account package required for x402. Install with: pip install eth-account"
            )

        # EIP-712 typed data structure for x402
        typed_data = {
            "types": {
                "EIP712Domain": [
                    {"name": "name", "type": "string"},
                    {"name": "version", "type": "string"},
                    {"name": "chainId", "type": "uint256"},
                ],
                "Payment": [
                    {"name": "recipient", "type": "address"},
                    {"name": "amount", "type": "uint256"},
                    {"name": "token", "type": "address"},
                ],
            },
            "primaryType": "Payment",
            "domain": {
                "name": "x402",
                "version": "1",
                "chainId": challenge.chain_id,
            },
            "message": {
                "recipient": challenge.recipient,
                "amount": int(challenge.amount),
                "token": challenge.token_address,
            },
        }

        private_key = self._get_private_key()
        account = Account.from_key(private_key)
        signed = account.sign_typed_data(typed_data["domain"], typed_data["types"], typed_data["message"])

        return f"type=exact; signature={signed.signature.hex()}"

    def validate_challenge(self, challenge: PaymentChallenge) -> None:
        """Validate payment challenge before signing."""
        # Check chain ID
        if challenge.chain_id != BASE_CHAIN_ID:
            raise AIXBTError(
                f"Unexpected chain_id {challenge.chain_id}, expected {BASE_CHAIN_ID} (Base)"
            )

        # Check per-request limit
        amount_usdc = amount_to_usdc(challenge.amount)
        if amount_usdc > self._settings.max_price_per_call_usdc:
            raise BudgetExceededError(
                f"Request cost ${amount_usdc:.4f} exceeds per-call limit "
                f"${self._settings.max_price_per_call_usdc:.2f}",
                limit_type="per_call",
            )

        # Check daily budget
        if not self._spend_tracker.can_spend(amount_usdc):
            raise BudgetExceededError(
                f"Request cost ${amount_usdc:.4f} would exceed daily budget. "
                f"Remaining: ${self._spend_tracker.remaining_budget:.2f}",
                limit_type="daily",
            )

    async def fetch_with_payment(
        self,
        client: httpx.AsyncClient,
        method: str,
        url: str,
        **kwargs: Any,
    ) -> httpx.Response:
        """Make request with automatic x402 payment handling."""
        if not self._has_wallet:
            raise AIXBTError("EVM_PRIVATE_KEY required for x402 endpoints")

        # Initial request
        response = await client.request(method, url, **kwargs)

        # Handle 402 Payment Required
        if response.status_code == 402:
            try:
                challenge_data = response.json()
                challenge = parse_402_response(challenge_data)

                # Validate before signing
                self.validate_challenge(challenge)

                # Sign payment
                payment_header = self._sign_payment(challenge)

                # Retry with payment
                headers = kwargs.get("headers", {}).copy()
                headers["X-Payment"] = payment_header
                kwargs["headers"] = headers

                response = await client.request(method, url, **kwargs)

                # Record successful payment
                if response.status_code == 200:
                    amount_usdc = amount_to_usdc(challenge.amount)
                    self._spend_tracker.record_spend(amount_usdc)
                    logger.info(
                        "x402 payment successful",
                        extra={
                            "amount_usdc": amount_usdc,
                            "remaining_budget": self._spend_tracker.remaining_budget,
                        },
                    )

            except Exception as e:
                if isinstance(e, (AIXBTError, BudgetExceededError)):
                    raise
                logger.error(f"x402 payment failed: {e}")
                raise AIXBTError(f"x402 payment failed: {e}")

        return response

    def parse_refund(self, response_data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Parse refund information from error response."""
        data = response_data.get("data", {})
        refund = data.get("refund")
        if refund and refund.get("successful"):
            logger.info(
                "x402 refund received",
                extra={
                    "tx_hash": refund.get("transactionHash"),
                    "reason": refund.get("reason"),
                },
            )
        return refund
