# Architectural Client Brief & Requirements Analysis

## Status
- Status: accepted product requirement; documentation-only proposal in this PR.
- Implementation: not implemented in runtime. No capability is claimed as operational.
- Placement: architecture understanding and requirements-analysis layer, upstream of PlanModel construction and design/change proposals.

## Purpose
Capture what the client actually needs before design begins, reduce avoidable redesign, expose missing information and contradictory requests, and preserve approved decisions as traceable project inputs. This is not a form-only feature and does not replace architectural judgement, code compliance checks, engineering coordination, or site verification.

## Four-stage workflow
1. **Client Intake** — plain-language, client-friendly questionnaire. Ask relevant questions and support UNKNOWN / NOT DECIDED / NOT APPLICABLE; allow evidence uploads and reference images where useful.
2. **Architectural Analysis** — normalize answers into candidate requirements; identify omissions, ambiguities, contradictions, dependencies, risks, and evidence gaps. Ask focused follow-up questions rather than silently guessing.
3. **Designer Brief** — separate professional questionnaire/workspace for site analysis, spatial relationships, area/program decisions, orientation/climate response, regulations, structure/MEP coordination, materials, landscape constraints, constructability, and design strategy.
4. **Architectural Design Brief** — consolidated, versioned brief with requirement IDs, source/provenance, status/confidence, priorities, dependencies, unresolved issues, and explicit client/designer approvals. Design proceeds from the approved brief, not unverified assumptions.

## Client questionnaire — minimum topic coverage
- Project type, location, site documents, survey and known legal/planning constraints.
- Desired gross/net area, number of floors, room/space list, capacity and occupancy patterns.
- Site orientation, access, topography, views, privacy, neighbors/adjacencies and surrounding land uses.
- Existing trees, vegetation, structures and site elements; what must remain, may be altered, or may be removed.
- Desired plan organization (open/closed/mixed), privacy gradients, circulation and room relationships.
- Architectural character, massing/form preferences, and whether plan form and facade expression may differ.
- Material and color preferences, including limits such as a restricted material palette.
- Landscape, parking, outdoor living, shading and water features.
- Climate comfort expectations, accessibility and special user needs.
- Budget range, phasing, schedule, deliverables and approval process.
- Reference images and examples, with a note about what the client likes or dislikes in each.

## Designer questionnaire — professional analysis
- Verify survey, north/orientation, dimensions, levels, access, boundaries and neighboring context.
- Separate verified facts, client statements, designer assumptions and externally sourced evidence.
- Reconcile buildable envelope, setbacks, coverage/FAR/height and applicable jurisdictional rules; do not infer legal compliance from incomplete evidence.
- Develop area schedule, occupancy, adjacency matrix, circulation, privacy and zoning logic.
- Evaluate climate, solar exposure, prevailing wind evidence, shading, thermal envelope and landscape preservation.
- Record structural grid/system constraints, shafts, wet cores, MEP routes, fire/life safety and accessibility coordination.
- Evaluate material performance, maintenance, availability, cost and construction feasibility.
- Record risks, alternatives, trade-offs, decisions, review owners and evidence needed.

## Requirement and evidence model
Every captured item should retain:
- stable requirement ID and concise statement;
- category and affected spaces/elements/site zones;
- source type and provenance (CLIENT, SITE_SURVEY, REGULATION, DESIGNER, CONSULTANT, REFERENCE);
- source/evidence reference and timestamp/version where available;
- priority (MUST, SHOULD, COULD, WON'T or equivalent);
- certainty/status (CONFIRMED, PROVISIONAL, UNKNOWN, SOURCE_REQUIRED, NEEDS_REVIEW, CONFLICT);
- dependencies, rationale, owner and approval state;
- change history and links to superseded decisions.

Client preference is not automatically a verified site fact or a regulatory rule. Conflicting sources must remain visible and unresolved until reviewed.

## Integration with the existing architecture pipeline
Client Intake → Requirement Records + Evidence → Architectural Analysis → Designer Brief → Approved Architectural Design Brief → PlanModel → ConstraintMap → ImpactAnalysis / Rules → ChangeProposal → Conflict → Validation → ApprovedChangePlan → Controlled Editing → PostEditDiff → Final Validation → Audit

- Approved brief requirements become traceable inputs to PlanModel and relevant ConstraintMap entries.
- Site facts and regulatory constraints retain source provenance and jurisdiction/version.
- Unknown or contradictory requirements remain UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW / BLOCKED; they must never be promoted to PASS by inference.
- Requirement changes after approval create a new brief version and trigger impact analysis; prior approvals remain auditable.
- The brief does not authorize edits. Existing approval, validation, fail-closed and controlled-editing gates remain mandatory.

## Conflict and completeness checks
Examples include:
- large openings requested toward an overlooked neighboring property;
- desired floor area exceeding the verified buildable envelope;
- retaining a tree conflicting with the proposed footprint or access;
- requested room relationships conflicting with circulation, privacy or structure;
- material preference conflicting with climate performance, maintenance or budget;
- client sketch/reference image conflicting with measured site evidence.

The system should explain the conflict, identify missing evidence, and ask the smallest useful follow-up. It must not silently choose a side.

## Interaction rules
- Begin every architectural design request with Client Intake before proposing a design.
- Ask conversationally by default; use a compact questionnaire only when several independent details are best gathered together.
- Do not ask clients professional technical questions they cannot reasonably know; route those to Designer Brief.
- Carry forward already-confirmed information and ask only for missing or changed items.
- Clearly label assumptions and request confirmation before treating them as decisions.
- Do not generate final presentation renders before the brief, site constraints, plan and massing have been reviewed and accepted.

## Acceptance criteria for future implementation
1. Client and designer questionnaires are distinct experiences with role-appropriate language.
2. Partial answers and explicit unknown/not-decided states are supported.
3. Analysis identifies missing, contradictory and dependent requirements with traceable explanations.
4. Requirement/evidence provenance and version history are preserved.
5. Approval creates an immutable/versioned approved brief snapshot.
6. Approved requirements can be traced into PlanModel and ConstraintMap without bypassing validation.
7. Requirement changes trigger impact analysis and never silently overwrite approved decisions.
8. Tests prove fail-closed behavior for unknown, conflicting and unsupported requirements.
9. No compliance PASS is produced without authoritative, applicable evidence and existing validation gates.

## Scope boundary
This PR records the product requirement only. It does not add runtime forms, AI inference, PlanModel fields, ConstraintMap logic, BIM functionality, regulatory automation, CAD editing, or render-generation code.
