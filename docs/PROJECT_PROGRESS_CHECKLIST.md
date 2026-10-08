# Architecture AI Agent — Master Progress Checklist

> This file is the persistent cross-chat project checklist. When asked "کجای پروژه هستیم؟" or "مرحله بعد چیست؟", use this file together with GitHub PR/CI status and `PROJECT_STATE.md` as the source of truth.

## Governance Gate — ALWAYS ACTIVE

- [ ] Implement
- [ ] REAL CI run/status
- [ ] Verify exact HEAD
- [ ] Regression when applicable
- [ ] Persist State
- [ ] Continue immediately when Green
- [ ] If Red: Bug Hunt → root cause → fix → REAL CI again
- [ ] Never treat queued/in_progress/no-CI as Green
- [ ] Never bypass Fail-Closed
- [ ] No-Wait Rule: prepare/debug in parallel while CI runs, without bypassing the gate

## Current master sequence

- [x] Architecture Agent feature-to-file matrix defined (PR #65)
- [x] Plan Understanding Semantic Chain defined
- [ ] PR #65 — CI + Bug Hunt Green
- [ ] PR #65 — Merge
- [ ] Post-merge main REAL CI Green
- [ ] Persist State after merge
- [ ] H100 — Drawing Semantics + Dimension/Annotation Evidence
- [ ] H100 — Semantic Chain fully wired and validated
- [ ] H100 — REAL CI + Bug Hunt Green
- [ ] H101 — Architectural Intent + Program + Plan Generation + deterministic geometry/layout
- [ ] H101 — REAL CI + Bug Hunt Green
- [ ] H102 — Architecture IR + lint/diagnostics
- [ ] H103 — Deterministic Drawing Compiler + SVG/DXF
- [ ] H104 — Dimensions/annotations/views + drawing standards
- [ ] H105 — Sections + elevations
- [ ] H106 — Details + schedules + sheets
- [ ] H107 — Multi-output sync + BIM export boundary
- [ ] H108 — Multi-agent roles/orchestration
- [ ] H109 — Iterative propose → inspect → revise
- [ ] H110 — Cross-format round-trip validation
- [ ] H111 — Production documentation/release gate

## H100 — Semantic/Drawing Evidence checklist

- [ ] Door/window symbols + opening direction
- [ ] Line type/thickness/weight
- [ ] Layer semantics
- [ ] Dimensions + extension lines
- [ ] Elevation/level codes
- [ ] Room/space labels
- [ ] Section markers + direction lines
- [ ] Elevation markers + direction
- [ ] Hatch semantics
- [ ] Column/structural symbols
- [ ] Element ↔ wall/space relations
- [ ] Floor/level semantics
- [ ] Stairs/landings and stair-count inference only with explicit consistent evidence
- [ ] Scale/unit evidence
- [ ] Title-block/drawing metadata evidence
- [ ] Evidence IDs/provenance bound to semantic facts
- [ ] UNKNOWN / NEEDS_REVIEW / BLOCKED propagation
- [ ] Contradiction detection
- [ ] Missing-evidence detection
- [ ] Golden DWG regression

## Plan Understanding — target semantic chain

Source Evidence
→ Element Identity
→ Geometry
→ Topology
→ Spatial Relation
→ Architectural Semantics
→ BIM Semantics
→ Rule Context

Rule: Detection is not Understanding. Do not create a second PlanModel or second BIM evidence graph. Preserve provenance continuity into the existing canonical model.

## H101 — Plan Generation checklist

- [ ] Architectural Intent contract
- [ ] Program/room requirements
- [ ] Prompt → plan proposal
- [ ] Deterministic layout/geometry
- [ ] Adjacency + circulation
- [ ] Opening connectivity
- [ ] Structural/regulatory constraints
- [ ] ConstraintMap integration
- [ ] Generated PlanModel
- [ ] Validation + conflict handling
- [ ] Fail-closed behavior
- [ ] Normal + ambiguous/failure tests
- [ ] Golden/regression coverage
- [ ] Exact-head REAL CI Green

## Feature-to-file matrix milestones

- F01–F02 → Intent + Program (H101)
- F03–F04 → Plan Generation + deterministic geometry (H101)
- F05–F06 → Architecture IR + validation (H102)
- F07–F10 → Drawing compiler/backends (H103–H104)
- F11–F18 → Phase-2 documentation (H104–H106)
- F19–F20 → Output sync + BIM export (H107)
- F21–F23 → Multi-agent + iterative design (H108–H109)
- F24–F26 → Semantic/BIM/evidence continuity (H100+ continuous)
- F27–F28 → Iran/architectural drawing standards + symbols/layers (H100/H104+)
- F29 → Round-trip (H110)
- F30 → Production readiness (H111)

## Status rules

- **PLANNED** = listed in matrix, not implemented.
- **IMPLEMENTED** = code exists, but exact-head REAL CI is not Green.
- **IMPLEMENTED + GREEN** = code + exact-head REAL CI success.
- **MERGED + VERIFIED** = merged to main + required post-merge verification Green.

## Source of truth

1. GitHub main/PR state and exact-head REAL CI
2. `PROJECT_STATE.md`
3. `MASTER_HANDOFF.md`
4. This checklist
5. Feature-to-file matrix / research docs as supporting planning documents

Notion is not a governance or Green-Gate source of truth.
