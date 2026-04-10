# Evaluation Payload Schema

File: `schemas/evaluation-payload.schema.json`

This schema defines the normalized input object for KPT-aligned candidate-output evaluation.

It exists to ensure that candidate-output evaluation begins from a consistent governed structure before decision assignment, enforcement mapping, and trace emission.

## Required top-level fields

- `input_ref`
- `output_ref`
- `candidate_output`
- `context`
- `provenance`
- `policy`

## Design intent

The schema separates:

- the candidate output itself;
- governed context;
- provenance and verification state;
- policy pinning.

This supports the KPT 2.3 principle that decisioning must occur on a normalized evaluation object before influence or execution.

## Notes

- This schema validates structure, not truthfulness.
- This schema does not itself assign decision state.
- Execution authorization must not be inferred from schema validity alone.
- Further schemas should define decision result and trace objects separately.
