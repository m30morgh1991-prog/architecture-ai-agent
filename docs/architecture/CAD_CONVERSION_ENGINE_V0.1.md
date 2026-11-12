# CAD Conversion Engine v0.1 — Architecture and Safety Contract

## Purpose

Provide an optional, replaceable DWG-to-DXF conversion adapter for environments where AutoCAD is unavailable. This is a local orchestration layer around an installed CAD codec, not a newly reverse-engineered DWG codec and not a source of architectural truth.

## Current implementation

- The Python adapter invokes an installed ODA File Converter executable.
- Exactly one source DWG is copied into a private temporary input directory; the original directory is never passed to the converter.
- Recursive processing is disabled and a single-file filter is supplied.
- The process has a bounded timeout and is invoked without a shell.
- Existing outputs are never overwritten.
- Source SHA-256 is checked before and after conversion.
- Non-zero exit, missing/empty/ambiguous output, timeout, missing executable, or source mutation is rejected.
- The initial adapter supports DWG → DXF only. DXF → DWG is deferred until an independent DWG reopen/verification path is available.

## Evidence boundary

execution_status=COMPLETED means only that the external converter returned success and produced a non-empty file while the source remained unchanged.

fidelity_status=UNKNOWN and requires_review=true are mandatory in v0.1. The adapter does not claim preservation of entity inventories, layers, blocks, xrefs, proxy objects, dimensions, text/font encodings, layouts, coordinate systems, units, or plot scale. Independent DXF parsing, audit, semantic comparison, and where appropriate human review are required before use.

A converted DXF must not silently replace the original DWG. The original remains immutable and the converted file is a derived artifact with provenance.

## Engine selection

ODA File Converter is the first external local codec adapter because the Open Design Alliance documents a command-line interface with source directory, target directory, output version/type, recursion, and audit options. The executable must be installed separately by the deploying office; this repository does not redistribute it.

The codec's license and terms must be checked for the specific deployment and commercial use. This adapter does not grant redistribution rights.

## Deferred work

1. Independent DXF parse/audit and entity/layer/block/text/units/coordinates comparison.
2. Adapter for another legally compatible local codec, if required.
3. Optional CloudConvert provider for explicitly approved, non-confidential files only; never required for core operation.
4. DXF → DWG only after independent reopen and fidelity evidence can be collected.
5. Real Windows installation and execution tests after the user's Windows replacement and CAD software setup.

## Explicit non-goals

- No DWG write-back to the source.
- No automatic repair/audit by default (audit=false).
- No semantic promotion into PlanModel or ConstraintMap.
- No compliance verdict or visual equivalence claim.
- No mandatory cloud dependency.
