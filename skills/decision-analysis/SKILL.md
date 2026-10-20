---
name: decision-analysis
description: Rank options against weighted criteria that carry uncertainty ranges, and recommend one or return a tie as a preference question. Use only when the agent's own assessment cannot distinguish between two or more options (A, B, ...): each option wins on at least one material criterion and loses on another. Covers purchases and the choice of a library, vendor, tool, or architecture. Not for a question with one correct answer, and not when one option is better or equal on every material criterion.
---

# Decision Analysis

Summary: How does the agent rank options that its own judgement cannot separate? Gates, anchored scores, swing weights, score and weight ranges, and the rule that overlapping ranges are a tie.
Why: a weighted total shown without its uncertainty invents precision. In one laptop comparison, four machines spanned 0.08 on a 5-point scale while unverified scores could move each total by more than 0.1, and the result was still reported as an order.

## When Not to Run

- One option is better or equal on every material criterion. Pick it and name the criterion that decides.
- The question has one correct answer, such as whether an API supports a feature.

## 1. Elicit Requirements Before Criteria

Criteria and weights are the developer's preferences, not findings. Ask for them as concrete trade-offs in money or time, never as abstract weights. "How much does memory matter?" has no answer. "Would you pay 7,000,000 VND more for 32 GB instead of 16 GB?" has one.

Elicit at least: the planning horizon, the workloads in rank order, whether the budget ceiling is hard, the tolerance for warranty and support risk, and which weaknesses the developer can repair cheaply, because a weakness that is cheap to repair is not a weakness.

Record each input as confirmed by the developer or as the agent's assumption.

## 2. Derive Criteria From Requirements

Each criterion measures one property of an option that serves a requirement from step 1. A criterion that no requirement produced is invented: remove it, or ask the developer whether the requirement behind it exists.

For each criterion:
- Name the requirement it serves. For example, "runs an IDE, a browser, and several agents for 4 to 5 years" produces "installed RAM and maximum RAM", and "may play 3D games" produces "dedicated GPU memory".
- Make it measurable: name the quantity or observable property, and where its value is read, such as a manufacturer specification page or a benchmark. "Good performance" is not a criterion; "physical CPU cores, from the manufacturer page" is.
- Measure what cannot be repaired later. When a weakness can be repaired by a purchase, the criterion measures the repair cost, not the weakness itself. For example, a small SSD that a 2,000,000 VND drive replaces is worth at most that amount.

Then check the set:
- No two criteria measure the same capability, because the overlap would be counted twice. When one criterion can substitute for another, check whether the substitution is real at this budget. If it is, merge the two. For example, a fast USB-C port can host an external GPU, but the enclosure alone costs about 14,000,000 VND before any graphics card. At a 35,000,000 VND budget the substitution is not real, so "fast port" and "dedicated GPU" stay separate criteria.
- Every requirement from step 1 has at least one criterion. A requirement with no criterion is silently dropped from the ranking.

For software options, take the criteria from the material subcharacteristics in [software-quality](../software-quality/SKILL.md).

## 3. Separate Gates From Criteria

A gate rejects an option outright. A criterion scores it. Gate only on a defect that no purchase, workaround, or later decision can repair. Everything else is a low score.

Verify a gate's fact at its source before the gate fires. A search summary, an absence from a listing, or an empty result is not enough, because a gate removes the option without anyone seeing it. Re-check gates that depend on volatile facts, such as price and stock, on every run.

## 4. Write Anchors Before Scoring

Give every criterion 1-to-5 anchors before looking at any option. Anchors written afterwards only describe the options found.

Space the anchors by the real difference. For example, a laptop with no dedicated GPU cannot run a 3D game at all, while 6 GB versus 8 GB of VRAM changes little. So "no GPU" scores 1, "6 GB" scores 4 and "8 GB" scores 5, not 1, 3 and 5.

## 5. Weight by Swing

A criterion's weight is the value of moving an option from the worst score to the best score that any real option has on that criterion. Give the largest swing 100, judge each other swing against it, then normalise the weights so they sum to 100. A criterion on which every option scores the same has no swing, so it gets no weight.

## 6. Score With Ranges

Every cell holds a range `[low, high]`:
- A verified cell has `low == high`.
- An unverified cell covers every anchor that the evidence does not rule out. For example, a warranty listed as "12 or 24 months" with no source scores `[3, 4]`.

Before widening a range, try to verify the cell, because research is the agent's work. MUST NOT assume the favourable value.

## 7. Use Weight Ranges Only for Undecided Preferences

A weight is a single value. When the developer says that a preference itself is not yet decided, such as "I don't know whether I will do 3D work in two years", write one weight set for each possible answer, each summing to 100. For any other doubt about a weight, ask the developer a trade-off question instead of adding a range.

## 8. Compute and Compare

Compute with a script, and confirm that every weight set sums to 100:

```python
def total_range(cells: dict[str, tuple[int, int]], weight_sets: list[dict[str, float]]) -> tuple[float, float]:
    lows: list[float] = [sum(w[c] * cells[c][0] for c in w) / 100 for w in weight_sets]
    highs: list[float] = [sum(w[c] * cells[c][1] for c in w) / 100 for w in weight_sets]
    return min(lows), max(highs)
```

Option A ranks above option B only when A's low is above B's high. Ranges that overlap are a tie.

For example, laptop A totals 3.34 and has one unverified cell (weight 6, ±1), so its range is 3.28 to 3.40. Laptop B totals 3.26 and has three unverified cells, so its range is 3.08 to 3.32. The ranges overlap, so the two laptops tie, even though A has the higher total.

## 9. Narrow a Tie, Then Hand It Over

List the cells whose ranges cause the overlap, ordered by `weight × (high - low)`, and verify them first. When the overlap remains after the evidence is used up, turn the tie into a preference question: name what each option buys and what it costs, in the developer's terms. Do not break a tie with a number.

## 10. Report

- The ranking, with each option's range and a link to buy or adopt it.
- The score matrix, with unverified cells marked by their ranges.
- The weights, and the requirement each weight came from.
- Rejected options, with the gate that fired.
- The check date of every volatile fact.
