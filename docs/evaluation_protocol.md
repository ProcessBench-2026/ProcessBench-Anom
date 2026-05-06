# Evaluation Protocol

## Default public scoring mode

- score against the public `eval` split
- keep all eval rows by default
- count invalid rows such as `INVALID`, `ERROR`, and `MISSING_FRAME` as incorrect unless `--valid-only` is used
- report:
  - overall micro accuracy
  - task macro accuracy
  - source macro accuracy
  - per-task accuracy
  - per-source accuracy

## Prompt serialization

### Standard multiple-choice

```text
{question}

A: {choice_A}
B: {choice_B}
...

Choose exactly one option label.

Output protocol:
- You may include brief reasoning before the final answer.
- The final line must be exactly: <ANSWER>A</ANSWER>
- Do not output anything after </ANSWER>.
```

### `T8` temporal ordering

```text
You are shown 3 frames from a robot manipulation task.
The frames are labeled X, Y, Z (these labels are arbitrary identifiers, not positional, and not time-ordered).
Determine the correct chronological order of these frames (from earliest to latest).
Choose exactly one 3-letter permutation.
```

### `T9` temporal priority

```text
A single comparison image shows two labeled robot-manipulation panels from the same episode.
The left-right placement of the panels and the labels are arbitrary identifiers and do not indicate temporal order.
Which labeled panel happened earlier in the real manipulation sequence, X or Y?
Choose exactly one label: X or Y.
```

## Baselines

- random baseline = `1 / num_choices`
- majority baseline = most frequent answer option on the public eval split