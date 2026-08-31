# DockSure

DockSure is a freight SLA escrow protocol, not a tracking-page classifier. A customer funds a shipment promise, the named carrier accepts it, and the carrier later submits public tracking, port, weather, or destination records. GenLayer validators independently re-fetch those sources and agree on one bounded verdict plus the exact evidence indexes supporting an exception. Deterministic code moves the escrow only after consensus.

## Lifecycle and settlement

1. `open_shipment` creates a unique lane agreement, locks native GEN, and binds two distinct customer-authorized HTTPS evidence origins before the carrier can act.
2. `accept_shipment` is restricted to the named carrier. Before acceptance, only the customer can cancel and recover escrow.
3. `submit_delivery` requires two distinct sources matching the customer's frozen policy. Every validator re-fetches the same records and agrees on their SHA-256 content digests as well as the bounded verdict.
4. `ON_TIME` and `EXCUSED` pay the carrier; `LATE` refunds the customer; `INSUFFICIENT` moves no funds and permits stronger evidence.
5. Transfers emit only on `finalized`, after the appeal-sensitive consensus phase.

The model never selects a recipient or amount. Evidence bodies are explicitly untrusted data. Expected, external, transient, and malformed-model errors are separated so validators cannot accidentally agree on unrelated failures.

## Product surface

The responsive operations desk supports wallet connection, funded shipment creation, carrier acceptance, evidence submission, receipt polling, contract reads, and a visible settlement manifest. All fields are editable; no workflow result is hardcoded.

## Verification

```bash
genvm-lint check contracts/contract.py
python -m pytest -q
```

The repository includes two transparent demo evidence records used for a real StudioNet lifecycle. Deployment metadata is in `deployment.json`.

## Deployment

- Contract: `0x699f116d8F138D6e9c0d96b77f3602B1364C95a0`
- Deploy tx: `0xe9999db532864acc73c138623001e8ce4e5151230b13b002514725f669bb9922`
- Live app: `https://docksure.pages.dev/`

## Proven StudioNet lifecycle

- Customer funding with two immutable authorized sources: `0x8e57c879846c4ccf63261daf14675c10f05c9787a29dfd2cb1a5b85d980fd02f`
- Named carrier acceptance from a different wallet: `0x22c80ead181d5b47d21d755682aa10e0dddb35f17558a7edf5603a98f871758b`
- Evidence consensus, two stored content digests and ON_TIME settlement: `0xc7d45677257c5ef210f18fbd4c60f931294ebab8dbeb8bcbeb48af2031260021`

The verification script also simulates a carrier submission from unauthorized origins and requires that it fail before the positive settlement path runs.
