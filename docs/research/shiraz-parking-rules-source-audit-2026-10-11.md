# Shiraz Parking Rules and Architectural Execution-Detail Source Audit
Date: 2026-10-11
Status: RESEARCH ONLY — NOT A VERIFIED CURRENT CODE BASELINE

## Purpose and boundaries

This research record feeds the existing Architecture AI Agent knowledge/evidence and future Rule/Validation layers. It does not replace or alter PlanModel, ConstraintMap, ApprovedChangePlan, H100 Golden Understanding gates, or the existing Iranian drawing-language work. No runtime code or Golden DWG asset is changed by this document.

Core invariant: understand the plan before generating or editing it. External documents and downloadable CAD details are evidence sources, not automatic authorities.

## Source inventory

### S1 — “ضوابط پارکینگ شیراز”, Hamyar Saze
URL: https://hamyarsaze.com/ضوابط-پارکینگ/
Observed page: https://hamyarsaze.com/ضوابط-پارکینگ/
Source class: secondary web transcription of a local parking guideline.
Confidence: useful discovery / candidate extraction only; current legal force and edition not verified.
The page says the Shiraz architectural-plan control guidelines were approved by the Article 5 Commission in 1383 and discusses parking design. This is historical context, not proof that every displayed number remains in force today.

The page publishes candidate values/rules including:
- access / entrance width differentiated by parking size;
- straight and curved ramp widths; inner radius for curved ramps;
- vehicle waiting/level area before ramp;
- ramp maximum slope and level transition area slope;
- clearance heights differentiated by parking size/type;
- accessible parking count/location, width, and slope;
- parking bay dimensions and maneuver aisle width;
- column grid / bay width constraints;
- pedestrian separation and exits.
It displays values such as 15% maximum ramp slope, 3 m straight ramp, 3.5 m curved ramp, 3 m inner radius, 5% waiting-area slope, and various parking bay/aisle/clearance dimensions. These are **unverified candidate values transcribed from a secondary source**. Do not encode them as current PASS/FAIL thresholds until the official applicable edition and any later amendments are found and cross-checked.

### S2 — IranDWG listing: concrete parking ramp execution detail
URL: https://t.me/s/IranDWG?q=%23DWG
Source class: downloadable CAD-detail listing (DWG), discovered through a Telegram channel listing.
Use: visual/geometry example for recognizing ramp sections, slope notes, transitions, and detail annotations after lawful download and inspection.
Limit: not a regulatory source; authorship, design conditions, revision, and accuracy must be checked. Never infer a general rule from a single detail.

### S3 — “نقشه دیتیل و جزییات اجرایی معماری ساختمان”, Farafile listing
URL: https://filenet.farafile.ir/file/40721/نقشه-دیتیل-و-جزییات-اجرایی-معماری-ساختمان
Source class: paid DWG package listing.
Described coverage includes ramps, parking, stairs/rails, doors/windows, floors, roofs, drains, site work, and MEP-related details.
Use: candidate source for a later licensed/manual review of drawing conventions and detail structure.
Limit: listing metadata is not proof of the file's quality, code compliance, or license for redistribution. Do not download or ingest paid material automatically.

### S4 — “پلان پارکینگ 3 طبقه”, KabookArc
URL: https://kabookarc.com/contents/view/5cc3d4d9-aa06-4857-06a2-08d7c78bd399
Source class: publicly listed DWG example; the listing describes it as a free three-level parking plan.
Use: candidate for layout/topology regression examples if the file can be accessed and its terms permit use.
Limit: illustrative geometry only; not a code source. Check license and provenance before adding to repository.

### S5 — “جزئیات محوطه‌سازی”, VrayGroup
URL: https://vraygroup.blogfa.com/post/128
Source class: secondary listing of DWG details described as public-program construction details.
Use: possible broader detail-reading reference (site/landscape) after source and license verification.
Limit: old listing; current file availability, integrity, and reuse terms not verified.

### S6 — User-provided book ZIP
Archive observed in the current work context: `کتاب.zip` (123 images: 97 in “نقشه کشی مهارت فنی درجه۲” and 26 in “کتاب ازمون نظام مهندسی”).
Contact-sheet review identified parking layouts, vehicle bays, circulation, ramp/stair drawings, dimensions, grids/columns, levels/sections, and drafting symbols.
Status: visually categorized at contact-sheet level; this is not a complete OCR/page-by-page transcription. Exact printed page numbers and text must be read from the original image before quoting a rule.

## Authority and evidence policy

Use source classes separately:
1. Current official national building regulations and amendments.
2. Current official Shiraz municipality / local planning and building-control instructions, including the applicable approved edition and date.
3. Authoritative professional/engineering guidance where applicable.
4. Textbooks and educational examples.
5. CAD/DWG details and example plans.
6. Secondary web transcriptions and informal posts.

If an official current source cannot be located, the value remains `SOURCE_REQUIRED` / `UNKNOWN`; do not silently promote S1 or any sample DWG to an official rule. For every rule candidate, retain source URL, source title/issuer, edition/date, page/clause, jurisdiction, occupancy/parking type, units, effective status, extraction method, confidence, and review status.

## Proposed source-to-module mapping (design-only; no code change claimed)

| Evidence / rule family | Existing destination boundary | Candidate validation / acceptance evidence |
|---|---|---|
| Parking bay geometry and bay count | DrawingEvidence → CandidateFact → canonical PlanModel; later Rule/Validation | Verify dimensions and vehicle envelopes; distinguish measured geometry from inferred bay classification; conflicting dimensions stay UNKNOWN |
| Aisles, maneuvering and turning | Relations / Geometry-Topology / ImpactAnalysis | Swept-path or conservative maneuver-envelope checks; test dead ends, tight turns, blocked access and column collisions |
| Ramp width, slope, radius and transitions | PlanModel geometry + level/elevation evidence + Rule/Validation | Recompute slope from source-supported run/rise; test missing levels, curved ramps, slope breaks, and unit ambiguity; no PASS if elevations or dimensions are missing |
| Clear height / beams / services | Cross-view coordination and evidence reconciliation | Check the lowest obstruction, not only nominal floor-to-floor height; missing section/MEP evidence remains SOURCE_REQUIRED |
| Accessible parking and pedestrian route | Rule/Validation and accessibility evidence | Check location, dimensions, slope, route continuity and applicable current local/national rule; do not assume old 2% value is current |
| Columns and structural grid | Locked-element/structural evidence boundary | Parking optimization cannot move columns or outer boundary; any conflict becomes a ChangeProposal/Conflict, not automatic geometry editing |
| Stairs, exits, fire and pedestrian separation | Existing stair/level/section semantics + rules layer | Validate cross-view consistency and applicable fire/accessibility requirements; distinguish architectural drafting evidence from code conclusion |
| Execution details (ramp section, drainage, joints, curb, finish) | Detail-library/reference index; later controlled-editing proposals only | Keep detail source/version and material/system conditions; no generic detail promoted as universally applicable |

## Recommended implementation order

1. **Official-source verification first:** locate the current official Shiraz municipal / approved local parking rules and the applicable current national regulations. Record issuer, edition, amendments, clauses, and effective date.
2. **Build a machine-readable rule catalog** with rule IDs, applicability predicates, dimensions/units, source traceability, status, and test fixtures. Keep old values as historical candidates until verified.
3. **Extract the user ZIP at page level:** orient/deskew images; OCR Persian text where possible; visually verify each extracted number, unit, diagram, and page label. Store page-image provenance.
4. **Build parking-specific adversarial tests:** missing dimensions, conflicting units, inaccessible bays, insufficient aisle, impossible turning, slope without reliable levels, low beam/duct, column blocking a bay, and mismatch between plan and section.
5. **Review downloadable DWG/PDF examples** only after access/license checks. Treat them as labeled examples, not normative rules; avoid committing copyrighted paid packs or unlicensed datasets.
6. **Integrate through existing evidence and Rule/Validation contracts.** No new semantic graph; no edits to PlanModel/ConstraintMap architecture; no changes to the H100 gate or immutable Golden DWGs without a separate approved implementation PR.

## Acceptance criteria for a future implementation PR

- Every enforced numeric threshold references a verified applicable source and clause.
- Unit, version, jurisdiction, parking type, and applicability are explicit.
- Secondary sources and sample details cannot independently produce regulatory PASS.
- Unknown or conflicting source evidence produces UNKNOWN / SOURCE_REQUIRED / NEEDS_REVIEW, never PASS.
- Regression tests cover valid, invalid, boundary, missing-evidence, contradictory-evidence, and stale-rule cases.
- Existing H100 gates and Golden DWG immutability remain intact; exact-head REAL CI, Runtime Tests, Mandatory Bug Hunt, and required regression must pass before merge.
