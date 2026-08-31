# DockSure

DockSure is a freight SLA escrow protocol, not a tracking-page classifier. A customer funds a shipment promise, the named carrier accepts it, and the carrier later submits public tracking, port, weather, or destination records. GenLayer validators independently re-fetch those sources and agree on one bounded verdict plus the exact evidence indexes supporting an exception. Deterministic code moves the escrow only after consensus.

## Lifecycle and settlement

1. `open_shipment` creates a unique lane agreement and locks native GEN.
2. `accept_shipment` is restricted to the named carrier. Before acceptance, only the customer can cancel and recover escrow.
3. `submit_delivery` requires at least two HTTPS sources. Every validator executes the same fetch-and-evaluate function independently.
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

- Contract: `0x65852186084288ab89133679051b9f3076629F06`
- Deploy tx: `0x19f4aca50305ac3949b6a8da40dfc7a4e4439d13b108771ad38d45bc015c0a69`
- Live app: `https://docksure.pages.dev/`

## Proven StudioNet lifecycle

- Fund shipment: `0x0e08c705edd7e8d950a9d138bfe3451063ba7cbe77fd0f388ae83b68254372c2`
- Carrier acceptance: `0xdcf97984573cad4ccf8008156cbd659e1e8e37346fb4aad2d6c563d1b31e23c3`
- Evidence consensus and ON_TIME settlement: `0x51f264aa80f9f2d26abc17abd0d03b5cf8046c2372cb27991d34b247d0b0280b`
