# Timeline

**RFP #MC-2026-0417 — Meridian Components Inventory Dashboard**
**Proposed duration:** 8 weeks from contract execution

---

## Phased Delivery Plan

| Week | Phase | Tech Lead | Frontend Dev | QA Engineer |
|------|-------|-----------|--------------|-------------|
| 1 | Kickoff & orientation | Codebase review, architecture mapping | Codebase review, Reports audit | Define critical flows with Meridian IT, begin test scaffolding |
| 2 | Foundation | R4 architecture doc draft | R1 filter wiring fixes | R3 tests for dashboard load and filters |
| 3 | Reports remediation | R4 architecture doc final | R1 i18n gaps + Options API migration | R3 tests for Reports page |
| 4 | Restocking — backend | R2 `/api/restocking` endpoint | R2 frontend scaffolding + routing | R3 smoke tests on R1 fixes |
| 5 | Restocking — frontend | R2 backend refinement | R2 view: table, budget input, totals | R3 tests for Restocking view |
| 6 | Integration & polish | End-to-end integration review | UI consistency pass across all views | Full test suite run, gap analysis |
| 7 | Buffer & optionals | D1/D2/D3 if selected | D1/D2/D3 if selected | Regression coverage, CI setup |
| 8 | Delivery | Final handoff package | Final fixes | Test coverage report, sign-off |

---

## Key Milestones

| Milestone | Target |
|-----------|--------|
| Kickoff complete, critical flows defined with IT | End of Week 1 |
| Architecture documentation delivered (R4) | End of Week 3 |
| Reports module remediated (R1) | End of Week 3 |
| Restocking view live (R2) | End of Week 5 |
| Full test suite passing (R3) | End of Week 6 |
| Final delivery and handoff | End of Week 8 |

---

## Notes

**Testing runs throughout, not at the end.** The QA Engineer begins in Week 1 and maintains coverage as each feature lands. By the time we reach final delivery, the test suite has been running for seven weeks — not assembled at the last minute.

**Week 7 is a deliberate buffer.** Real engagements encounter surprises. We would rather plan for them than promise a timeline that assumes nothing goes wrong.

**Desired items (D1–D3)** are scheduled in Week 7 if selected. Each is independent and can be added or dropped without affecting the required scope.

**Meridian IT dependency.** The kickoff session in Week 1 is the one hard external dependency. If it slips, we absorb it in Week 1 rather than pushing the delivery date — but we need it to happen.
