# Tasks: Add x402 Payment Protocol Handler

## 1. Configuration
- [ ] 1.1 Add `EVM_PRIVATE_KEY` to Settings (optional, SecretStr)
- [ ] 1.2 Add `MAX_PRICE_PER_CALL_USDC` setting (default: 1.0)
- [ ] 1.3 Add `MAX_SPEND_PER_DAY_USDC` setting (default: 10.0)
- [ ] 1.4 Add `BASE_RPC_URL` setting (default: https://mainnet.base.org)

## 2. Payment Challenge Parser
- [ ] 2.1 Create `src/mcp_aixbt/clients/x402.py`
- [ ] 2.2 Define `PaymentChallenge` Pydantic model
- [ ] 2.3 Implement `parse_402_response()` function
- [ ] 2.4 Extract amount, recipient, token_address, chain_id

## 3. EIP-712 Signing
- [ ] 3.1 Define EIP-712 typed data structure for x402
- [ ] 3.2 Implement `sign_payment()` using eth-account
- [ ] 3.3 Generate `X-Payment` header string
- [ ] 3.4 Handle signature encoding (hex format)

## 4. Budget Controls
- [ ] 4.1 Implement per-request amount validation
- [ ] 4.2 Create daily spend tracker (in-memory or file-based)
- [ ] 4.3 Reject payments exceeding limits
- [ ] 4.4 Add `BudgetExceededError` exception

## 5. x402 Client Wrapper
- [ ] 5.1 Implement `fetch_with_x402()` function
- [ ] 5.2 Handle 402 response → sign → retry flow
- [ ] 5.3 Parse refund information from 404/500 responses
- [ ] 5.4 Log payment transactions (amount, tx hash if available)

## 6. Surging Projects Tool
- [ ] 6.1 Add `POST /tools/get-surging-projects` endpoint
- [ ] 6.2 Call `/x402/v1/projects` with payment handling
- [ ] 6.3 Support limit and minScore filters

## 7. Validation
- [ ] 7.1 Unit test EIP-712 signing with known test vectors
- [ ] 7.2 Unit test budget validation logic
- [ ] 7.3 Integration test with mocked 402 responses
- [ ] 7.4 Test refund parsing from error responses
- [ ] 7.5 Verify private key is never logged

## 8. Security Review
- [ ] 8.1 Ensure private key only accessed via SecretStr
- [ ] 8.2 Validate challenge amounts before signing
- [ ] 8.3 Verify chain_id matches expected (8453 for Base)
- [ ] 8.4 Add warning log when approaching daily limit
