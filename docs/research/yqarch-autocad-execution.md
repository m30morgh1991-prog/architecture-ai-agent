# YQArch / AutoCAD Execution Research

## Purpose

Research checkpoint for integrating useful YQArch/AutoCAD capabilities without weakening the Architecture AI Agent's evidence-backed, fail-closed architecture.

## Decision

YQArch is an **execution adapter candidate**, not a Plan Understanding engine and never a Source of Truth.

Source of Truth remains:

- PlanModel
- ConstraintMap
- ApprovedChangePlan

The intended boundary is:

`ApprovedChangePlan → Controlled Editing → AutoCAD/YQArch Adapter → PostEditDiff → Final Validation → Audit`

## Capabilities worth adopting as project concepts

The reviewed YQArch command registry exposes useful architectural primitives and drafting operations:

- walls: create, trim, thickness change, offset, line-to-wall
- columns: rectangular, circular, L/T/cross, axis arrangement
- openings: doors, windows, pocket doors, corner windows, move/replace/repair
- vertical circulation: stair plans/sections, elevators, escalators, banisters
- drawing semantics: axes, grids, dimensions, section/elevation markers, symbols
- annotation: text, leaders, title blocks, scale and drawing frame
- layer operations: create/current/on/off/freeze/lock/isolate/rename/merge
- measurement/listing helpers: areas, window/door lists, serials, bounding boxes
- transformation/repair operations: move, copy, mirror, repair

These are **capability candidates**. They do not become semantic truth merely because an execution backend supports them.

## Architectural Capability Registry

Adopt the idea of a provider-neutral capability registry rather than exposing raw YQArch commands to the model.

Example conceptual record:

```text
capability = DOOR.WIDTH.UPDATE
operation = UPDATE
object_type = DOOR
backend = AUTOCAD_YQARCH
backend_command = yq_width_windoor
required_evidence = door_identity + host_wall + current_width
risk = HIGH
requires_approval = true
```

The LLM should request a semantic capability. The controlled-editing layer resolves that capability to a backend command.

## Runtime safety contract

Never treat command dispatch or command launch as proof of edit success.

Recommended execution states:

```text
REQUESTED
DISPATCHED
STARTED
INTERACTIVE
EXECUTING
COMPLETED
VERIFIED
FAILED
UNKNOWN
```

Only `VERIFIED` may satisfy the execution-success side of the pipeline.

Interactive AutoCAD/LISP prompts must not silently become PASS.

## Security boundary

Do **not** expose arbitrary AutoLISP evaluation or arbitrary command strings to the model.

Execution should use an allowlisted capability registry with typed parameters, validation, approval requirements, and post-edit verification.

File-based IPC can be used as an implementation technique, but command/result envelopes must be bounded, source-bound, request-ID bound, and fail closed on timeout, malformed output, or unknown state.

## Layer semantics

YQArch's layer operations are useful evidence, but a layer name must never be treated as semantic truth by itself.

Semantic classification should combine:

```text
Layer Evidence
+ Geometry Evidence
+ Symbol Evidence
+ Text Evidence
+ Topology
+ BIM Relations
```

Contradictory or missing evidence remains UNKNOWN / NEEDS_REVIEW.

## PlanModel implications

YQArch reinforces the need for first-class semantic objects for:

- Wall
- Door
- Window
- Column
- Stair
- Grid / Axis
- Dimension
- Section Marker
- Elevation Marker
- Annotation
- Space

H100 already establishes evidence-backed drawing annotations and dimension semantics. Future controlled-editing work should consume these semantics rather than reverse-engineering them from raw CAD commands.

## Stair / vertical circulation implication

YQArch separates stair plan and section operations and exposes step/dimension-related operations. This supports a future VerticalCirculation semantic model containing:

- storey height
- riser
- tread
- flight count
- landing
- direction
- required step count
- plan representation
- section representation

This is especially relevant to level/elevation evidence and architectural stair validation.

## What is explicitly NOT adopted

- YQArch as Source of Truth
- direct LLM → AutoCAD command execution
- arbitrary LISP execution
- assuming `STARTED` or `DISPATCHED` means success
- trusting layer names as semantic truth
- proprietary YQArch-MCP licensing/runtime as a project dependency

## Backend strategy

Keep the adapter boundary provider-neutral:

```text
Controlled Editing
  ├── AutoCAD/YQArch Adapter
  ├── AutoCAD Native API Adapter (future)
  └── Other CAD/BIM adapters (future)
```

The semantic capability contract stays stable while backend implementations can change.

## Evidence status

This document records architectural research and design decisions. It does **not** declare a future H stage GREEN and does not replace real CI/runtime evidence.
