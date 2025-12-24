# Change: Add x402 Payment Protocol Handler

## Why
The x402 protocol enables pay-per-request access to premium AIXBT endpoints without requiring API keys. This proposal implements the payment handshake flow including EIP-712 signature generation, budget controls, and automatic retry with payment headers.

## What Changes
- Create `src/mcp_aixbt/clients/x402.py` with payment handler
- Implement EIP-712 typed data signing using eth-account
- Add budget controls (per-request limit, daily cap)
- Create `get_surging_projects` tool using x402 endpoint
- Add spend tracking and refund handling

## Impact
- Affected specs: `x402-payments` (new capability)
- Affected code: `src/mcp_aixbt/clients/x402.py`, `src/mcp_aixbt/routers/tools.py`
- Dependencies: Requires `001-scaffold-project` and `004-add-mcp-tools`
- **Security Note:** Requires EVM private key management

## Sequence
**Proposal 5 of 7** - Depends on proposals 001-004. Optional feature (can be skipped if not using x402).

## References
- `ApplicationSpecificationFinal.md` Section 3.2 (x402 Payment Protocol)
- `ApplicationSpecificationFinal.md` Section 6.3 (x402 Payment Handler)
- `openspec/project.md` (x402 Payment Flow)
