# DockSure

DockSure is a freight SLA escrow protocol, not a tracking-page classifier. A customer funds a shipment promise, the named carrier accepts it, and the carrier later submits public tracking, port, weather, or destination records. GenLayer validators independently re-fetch those sources and agree on one bounded verdict plus the exact evidence indexes supporting an exception. Deterministic code moves the escrow only after consensus.

## Lifecycle and settlement

1. `open_shipment` creates a unique lane agreement, locks native GEN, and binds two distinct customer-authorized HTTPS evidence origins before the carrier can act.
2. `accept_shipment` is restricted to the named carrier. Before acceptance, only the customer can cancel and recover escrow.
3. `submit_delivery` requires two distinct sources matching the customer's frozen policy. Every validator re-fetches the same records and agrees on their SHA-256 content digests as well as the bounded verdict.
4. `ON_TIME` and `EXCUSED` pay the carrier; `LATE` refunds the customer; `INSUFFICIENT` moves no funds and permits stronger evidence.
5. `recover_unsettled` gives the customer an explicit recovery transition after carrier acceptance and before settlement.
6. Transfers emit only on `finalized`, after the appeal-sensitive consensus phase.

Evidence authorization parses HTTPS scheme, hostname, port and normalized path. Hostname-prefix tricks, encoded traversal, ambiguous overlapping slots and multiple records reusing one authorized slot are rejected before any web fetch.

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

- Contract: `0x90E1d13152213D765Dcc6a5072ed434151033435`
- Deploy tx: `0x46203926b1267206abdcc12f0ca8ec56df35322f62ff0b7bb91390caf3b2de40`
- Live app: `https://docksure.pages.dev/`

## Proven StudioNet lifecycle

- Customer funding with two immutable authorized source slots: `0x8dd300c49c7e728d1bb3a7fb77bbc830ae99b6ab660cdffb8ba044878289e08f`
- Named carrier acceptance from a different wallet: `0xdc78121b6aa5a1677023a3f6db2de9a400c5e72d18505ffa852d49ce37fbcf66`
- Evidence consensus, two stored content digests and ON_TIME settlement: `0x7c3ae3ed2e5a4413f525bc98515a55832093ee9e1e764cdefb4e630e5d292ef3`
- Recovery flow funding: `0xf32e59b0b00dfd841cc69faec75ae34fa49da4280d378132edc032d2778fb0f7`
- Recovery flow carrier acceptance: `0x18d516a968cc71a7ce7917cb3d78df1f2921c351eafd3e2c5fed1a1c65f0f07c`
- Customer escrow recovery after acceptance: `0x04d0453df7e5a43e0b7f318c17012b4ce1aca857f10efa3cefc7b5f3c569cf79`

The verification script also requires hostname-prefix bypass and same-slot evidence simulations to fail before the positive settlement path runs. Direct behavioral regression tests cover both attacks and fund recovery.
