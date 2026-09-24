# Research Evidence Baseline — Controlled Architectural Floor-Plan Editing

Date: 2026-09-24
Status: ADDED / ARCHITECTURE BASELINE
Project: Architecture AI Agent — MVP

## Purpose
Translate current research evidence into explicit design requirements for the Architecture AI Agent without replacing the frozen MVP contracts.

## Evidence-backed findings
1. Floor-plan AI research increasingly represents plans through geometry, semantics, spatial relations and vector/symbolic structures rather than pixels alone.
2. Recent work demonstrates natural-language floor-plan generation/editing and localized editing, but precise architectural validity and controllability remain active research problems.
3. 2026 CVPR work (HouseMind) demonstrates multimodal understanding, generation and editing using symbolic room-instance tokens, reinforcing the value of a structured plan representation.
4. Research on architectural evaluation notes that generic image/statistical metrics do not adequately capture architectural functionality, flow and professional validity.

## Project Research Gap
The project focuses on a control layer that is not the same as image generation/editing:
- explicit protection of LOCKED elements;
- EDITABLE / CONDITIONAL permissions;
- Change Proposal before execution;
- dependency-aware Impact Analysis;
- uncertainty propagation and fail-closed behavior;
- deterministic Rule/Validation gates;
- Post-Edit Diff against the logical Plan Model;
- architectural/regulatory validation after editing;
- traceable explanation of what changed and why.

## Design Principle
AI/Visual models provide interpretation, detection assistance and candidate visual output only.
They must never bypass the deterministic Architecture Core.

Allowed path:
Request → Understanding → Plan Model → Constraints → Rules → Proposal → Conflict/Impact → Validation → Approved Change Plan → Controlled Editing → Post-Edit Detection/Diff → Final Validation → Version/Audit

Forbidden path:
Prompt → Image Editor → Final Plan

## Regression implications
Research findings are incorporated without invalidating prior tests:
- H20 release gate remains the accepted baseline.
- Existing Locked/Furniture/Impact/Unknown/Post-Edit tests remain mandatory.
- New research-driven checks must be additive and must not weaken existing guards.
- H20 PASS is preserved; no previous PASS is reclassified.

## Next implementation direction
H21: Research-Gap Controlled-Editing Contract.
Scope:
- formalize permission semantics;
- formalize uncertainty/abstention semantics;
- expose ImpactAnalysis dependencies to the execution contract;
- add regression coverage for fail-closed behavior;
- preserve all existing H15-H20 contracts and gates.

## Primary sources
- Qin, Weber & Lu, CVPR 2026, “Tokenization Allows Multimodal Large Language Models to Understand, Generate and Edit Architectural Floor Plans.”
- Qiu et al., Automation in Construction, 2025, “LLM-based framework for automated and customized floor plan design.”
- Zeng et al., Automation in Construction, 2025, “Automated residential layout generation and editing using natural language and images.”
- Lin, Xia & Zhang, 2025, “A Diffusion-Based Approach for Generating Floor Plans with Adjustable Area Constraints.”
- Wang et al., Journal of Computing in Civil Engineering, 2025, “Enhanced Semantic Recognition of Architectural Floor Plan Recognition Using CLIP and Advanced Sampling Strategy.”
- Yin et al., ACL 2025, “FloorPlan-LLaMa: Aligning Architects’ Feedback and Domain Knowledge in Architectural Floor Plan Generation.”

## Governance
Execute → Verify → Sync Notion → Continue
