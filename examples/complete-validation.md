# Complete example: evidence supports only the next stage

## User input

> I offer a fictional invoice-follow-up service for freelancers. I attached payment receipts and an anonymized use log: eight unrelated freelancers each paid $25, six used it again, and the median delivery time was 28 minutes per customer. All eight came from one partner who introduced the service to 40 qualified leads. Should I build the full automated product?

The example assumes the agent inspected the attached receipts and log. Without those artifacts, the same claims would be `User statement`, not `Verified`.

## Decision

`Expand in stages`.

Approve automating one bounded delivery step for the next cohort. Do not approve a full product build or broad paid acquisition yet.

## One-sentence rationale

Verified payment and repeat use support another stage, while acquisition beyond one partner and scalable delivery quality remain unknown.

## Evidence ledger

| Claim or decision point | Source | State | What it supports | What is missing |
|---|---|---|---|---|
| Eight unrelated freelancers paid $25 | Inspected receipts | `Verified` | Real payment from the stated buyer | Will new cohorts pay? |
| Six of eight used it again | Inspected use log | `Verified` | Early repeat-use behavior | Longer retention and renewal |
| Median delivery time was 28 minutes | Inspected time log | `Verified` | Current delivery-cost baseline | Support burden after automation |
| Eight buyers came from 40 partner leads | Inspected referral and payment records | `Verified` | One partner can deliver qualified leads | Whether that channel repeats or another channel works |
| A full automated product will be profitable | No model or cost evidence | `Unknown` | Nothing yet | Hosting, support, failure, and acquisition costs |

## Business assessment

| Dimension | Current judgment | Evidence | Next validation |
|---|---|---|---|
| Demand | A costly problem exists for this cohort | Verified payment and repeat use | Test a second cohort |
| Buyer | Freelancers paid directly | Inspected receipts | Confirm the same payer profile repeats |
| Distribution | One partner works; repeatability is unknown | Eight payments from 40 qualified introductions | Repeat the partner cohort before testing another channel |
| Payment | Strong for a small cohort | Eight inspected payments | Test the same offer without founder novelty effects |
| Delivery economics | Measurable but still founder-heavy | 28-minute median delivery | Measure time and correction burden after one automation step |
| Compounding value | Workflow automation may compound | `External inference` from the repeated process | Confirm reused automation actually reduces work |
| Ceiling | `Unable to judge` | One partner and one cohort | Estimate reachable qualified buyers only after channel repeatability |
| Risk | Incorrect reminders and partner concentration | Workflow review plus current channel mix | Keep customer messages and channel expansion human-gated |

## Smallest decisive experiment

- **Hypothesis:** Automating reminder setup can reduce founder delivery time without lowering the verified 6/8 repeat-use result.
- **Target payer:** One new cohort matching the eight verified freelancer buyers.
- **Minimum deliverable:** Automate reminder setup only; keep review and sending manual.
- **Reach action:** Ask the same partner for one comparable cohort before adding a new acquisition channel.
- **Costly behavior:** Payment for the same offer and repeat use after first delivery.
- **Pass line:** Maintain at least the verified 6/8 repeat-use result and reduce median founder time below 20 minutes. `20 minutes is a provisional test value, not market evidence`; it represents a first meaningful reduction from the verified 28-minute baseline and needs founder confirmation.
- **Stop line:** Pause automation if repeat use falls below the current 6/8 baseline, any incorrect reminder reaches a customer, or median founder time does not fall.
- **Time cap:** `10 founder hours is a provisional test value, not market evidence`; it bounds one implementation-and-delivery cycle and needs founder confirmation.
- **Money cap:** `$100 is a provisional test value, not market evidence`; it prevents tooling spend beyond the value of this learning stage and needs founder confirmation.
- **Human approval:** Require confirmation before purchasing tools or sending any external reminder.

## Next three actions

1. Confirm the provisional time and money caps against the founder's actual economics.
2. Automate reminder setup only and run one comparable partner cohort.
3. Inspect payment, repeat use, errors, and founder-time evidence before deciding on another stage.
