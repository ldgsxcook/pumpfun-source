# Mayhem O0076 SweepFees: remaining operand triage

This is a reconstruction work item, **not** a new byte match.

## Starting point

The retained [address-selection control](../mayhem-current436-sweep-address-selection-20261028/README.md)
already matches the original O0076 function length (8,400 bytes), all 189 CFG
blocks, opcodes, register fields, 51 callee positions and 13 Source values.
It reports 1,047/1,050 normalized instruction words equal.

| Relative byte offset | Original address operand | Candidate operand | Hypothesis to test |
| ---: | ---: | ---: | --- |
| 776 | 176 | 520 | Different base pointer / stack-slot lifetime |
| 808 | 232 | 576 | Same base-pointer choice as previous load |
| 1176 | 344 | 0 | Address calculation folded into a different base register |

The retained analysis says each pair selects the same field address, but
**equivalent effective addresses are not identical instruction bytes**.
Do not mask these operands, patch the ELF, or count O0076 as matched.

## Next source-only experiment

1. Restore the retained 67-file source snapshot from
   `research/mayhem-current436-sweep-address-selection-20261028/sweep/source.tar.gz`.
2. Locate the SweepFees AccountInfo bindings and the Rent / data-length locals.
3. Change **one** Rust ownership/lifetime choice at a time. Record source diff.
4. Build twice with the recorded compiler/linker recipe, and run the retained
   `verify.py` plus strict O0076 matcher without relaxing comparison rules.
5. Record the three operand values, raw body equality, normalized-window count,
   direct-call closure and local signed replay status separately.
6. Promote only a candidate that preserves the qualified 436/141/429 baseline
   and passes newly run runtime tests. If no improvement, retain as experiment.

## Reproduce retained baseline

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -B research/mayhem-current436-sweep-address-selection-20261028/verify.py
```

No rebuild or runtime test has been performed for this triage note.
The qualified composition remains 436/441 matched; five bodies remain.
