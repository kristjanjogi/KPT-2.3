# Examples Surface

**Author:** Kristjan Jõgi  
**Status:** Public example surface note

This directory contains **public example materials** for KPT 2.3.

It does not imply that every file here is a live runtime export or a full implementation artifact.

## File roles

### `trace-valid-example.json`
A **schema-valid public trace example**.

Its purpose is to show what a valid KPT trace object can look like under the public schema surface.

This file is also used by public reference-engine demo and conformance-validation utilities.

### `trace-invalid-example.json`
An **intentionally invalid negative schema example**.

Its purpose is to demonstrate a trace object that should fail schema validation.

This file is also used by public reference-engine validation utilities.

### `appendix/kpt-2_3_multicase_boundary_audit_companion.md`
A **reconstructed audit companion**.

It is an appendix-style example surface and must not be read as a live append-only runtime export.

## Interpretation rule

Read this directory as:
1. example surface
2. schema / validation fixture surface
3. appendix / companion surface where explicitly marked

Do not treat these files as stronger than:
- `docs/core-standard.md`
- `docs/quickstart.md`
- `schemas/trace.schema.json`
