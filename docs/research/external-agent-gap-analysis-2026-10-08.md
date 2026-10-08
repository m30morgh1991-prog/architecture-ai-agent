# External Architecture-Agent Gap Analysis — 2026-10-08

## Purpose
Consolidate the newly reviewed architecture/BIM/plan-understanding systems into the Architecture AI Agent roadmap without creating a second semantic graph or changing the project's Source of Truth.

## Baseline finding
No reviewed project currently provides the complete combination of evidence-first architectural plan understanding, canonical PlanModel, ConstraintMap and ApprovedChangePlan, fail-closed uncertainty propagation, Iranian architectural drawing language, BIM-ready semantic identity/relations, deterministic validation, provider-neutral controlled editing, and repository-backed CI/bug-hunt/recovery governance.

Several projects are materially ahead in individual layers. They are references, benchmarks, or future adapters rather than copied dependencies.

## Reviewed systems and adoption decisions

### HarnessBIM
Strongest areas: BIM/IFC abstraction, verification-first workflows, schema/IDS/clash/structural/MEP/egress validation patterns, machine-checkable evidence and human approval boundaries.
Adopt verification architecture, explicit checker boundaries, and future Rule/Validation orchestration.
Do not adopt a multi-agent generation pipeline as an MVP dependency.

### IFC_AGENTS
Strongest areas: IFC-aware agent reasoning, issue normalization, deterministic tool execution, validation/evidence packaging, and human-approved correction workflows.
Adopt separation of LLM reasoning from deterministic BIM operations, issue/evidence lifecycle, and verification after mutation.
Do not give the model direct IFC mutation authority.

### Floor-plan vision pipelines
Strongest areas: wall/door/window/room segmentation, OCR, raster-to-geometry reconstruction, IFC/CAD bridging, and uncertainty-aware vision outputs.
Adopt Evidence Extraction and Semantic Candidate patterns, held-out evaluation/robustness testing, and conservative visual-to-geometry conversion.
Do not promote raster detections to authoritative geometry without PlanModel evidence and validation.

### CAD/BIM agent bridges
Strongest areas: semantic intent mapped to deterministic CAD/BIM operations, typed capabilities, query/measurement tooling, and execution verification.
Adopt Capability Registry, backend adapters, deterministic operation contracts, and post-edit verification.
Do not allow arbitrary LLM-generated CAD commands, LISP, or geometry.

### OpenTakeoff-style measurement/provenance patterns
Adopt explicit scale gates, measurement provenance, source/method/agent-human attribution, withheld/refusal states, and separation of human approval from agent verdict.

## New roadmap decisions

### H101 — Evidence & Provenance
Stable Evidence IDs; source binding for every semantic fact; evidence strength/confidence; measurement provenance; contradiction and missing-evidence propagation; fail-closed promotion rules.
Acceptance: no semantic fact becomes authoritative without traceable evidence.

### H102 — Relations & Topology
Wall-Door-Window-Space relations; adjacency; containment; connectivity; geometry/semantic consistency; canonical PlanModel/ConstraintMap integration.
Acceptance: relations are deterministic, source-linked, validated, and do not form a duplicate semantic graph.

### H103 — Drawing Set Graph
Sheet identity; floor/storey identity; plan/section/elevation/detail relationships; continuation/reference links; cross-sheet provenance.
Acceptance: evidence can be traced across the drawing set without guessing.

### H104 — Vertical Circulation
Level/elevation codes; storey heights; riser/tread; landing; flight count; direction; plan/section consistency.
Acceptance: stair/level inference is promoted only when evidence is explicit and internally consistent.

### H105 — Architectural Capability Registry
Semantic capability IDs; operation/object type; backend/provider; required evidence; risk; approval requirement; refusal/default behavior.
Example capability: DOOR.WIDTH.UPDATE.
Acceptance: the model can request a semantic operation but cannot bypass capability validation.

### H106 — Controlled Editing
Transaction boundary; rollback; execution lifecycle; provider-neutral adapter; no direct LLM-to-AutoCAD authority.
Acceptance: only approved semantic operations reach a backend adapter.

### H107 — Post-Edit Verification
Drawing diff; reopen/parity checks; geometry validation; semantic validation; before/after evidence.
Acceptance: execution is successful only when post-edit verification succeeds.

### H108 — Rule & Compliance Layer
Traceable rule packs; explicit/testable rules; Iran/local architectural rules; drafting standards; accessibility/MEP/structural checks where evidence supports them.
Acceptance: every rule result is traceable to a rule definition and its required evidence.

### H109 — End-to-End Plan Understanding
Target flow: Evidence → Semantic Candidates → PlanModel → Relations/Topology → ConstraintMap → Validation → Understanding Result.
Acceptance: the system explains what it understands, what evidence supports it, and what remains UNKNOWN/NEEDS_REVIEW/BLOCKED.

### H110 — Controlled Plan Generation
Only after H109 is Green.
Flow: Understanding → Design Intent → ChangeRequest → ImpactAnalysis → ApprovedChangePlan → Controlled Generation → Validation.
Acceptance: generation never becomes an alternative source of truth.

## Architectural invariant
Understand the plan before generating or editing the plan.
The roadmap therefore prioritizes understanding, provenance, relations, topology and validation before increasing execution power.