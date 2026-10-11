## Why

The developer deferred the proposed rule below on 2026-10-11 and will judge it later. Resume only when the developer asks to review or implement it. This proposal is not an active global instruction.

Proposed owner: Explanation, under Use the Most General Name That Stays Clear. The existing rules already require standard terms and understandable names; this proposal adds only clarification when multiple meanings affect the answer.

Proposed text: "When a term has multiple meanings relevant to the answer, name the layer it refers to."

Proposed reason: the reader can otherwise apply a correct statement to the wrong unit or system boundary. Scope: developer-facing explanations across projects, not just AI harnesses.

The approved harness definitions are already canonical in [Communication](../../rules/Communication.md#harness-vocabulary). This deferred task does not redefine them.

## Examples

First firing case: a response compares backend usage with a whole agent request. Bad: "A turn costs USD 0.10." Better: "The recorded provider turn costs an estimated USD 0.10; the budget applies to the whole harness turn." The qualifiers prevent the reader from treating one backend record as the complete request's cost. The number is illustrative, not a measurement.

Second firing case: a response discusses both conversation storage and program execution. Bad: "The thread contains 12 messages, and the worker runs on one thread." Better: "The chat thread contains 12 messages; the worker runs on one execution thread." The same word names different things in the two systems, so the qualifiers show which meaning each statement uses. The numbers are illustrative, not measurements.

Non-firing case: "The PNG image is 512 by 512 pixels." Nothing in this statement depends on two relevant meanings of a term, so adding a layer label would not help the reader.

## Step 1: Judge the proposed clarification

- [ ] #1 Review the trigger, examples, and overlap with existing Explanation rules
- [ ] #2 Decide whether to accept, revise, or reject the proposed rule
- [ ] #3 If accepted, update its canonical owner and check that the non-firing example stays unaffected
