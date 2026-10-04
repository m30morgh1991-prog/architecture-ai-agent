# Architectural Design Exam Research — 2026-10-04

## Purpose
This checkpoint records the architectural-design exam resources identified during research and the project knowledge that should be extracted from them without turning exam-specific teaching methods into architectural law.

## Priority resources identified
1. **مبانی طراحی معماری — مهدی دریانی** — high-value areas: design fundamentals, housing design, urban apartments, case studies. Use for architectural problem-solving and spatial design knowledge. Older editions are not current-rule authorities.
2. **تشریح و طراحی سوالات آزمون‌های نظام مهندسی معماری — مهدی دریانی** — real exam problems, step-by-step design, parking, ramp, stairs, daylight, standard drawing. Use for problem decomposition and constraint interaction.
3. **تشریح و طراحی سوالات آزمون‌های نظام مهندسی معماری به روش پازل — مهدی بیات** — decomposition of a design problem into solvable parts, checklists, past exams, practice cases. The puzzle method is a teaching method, not a universal rule.
4. **آموزش آزمون طراحی معماری نظام مهندسی با تأکید بر مصورسازی منابع — هما ساداتی‌طباطبائی، زهرا فائز، حسن سالاری** — useful for converting textual provisions into visual/drawing decisions. Older edition; not a current-rule authority.
5. **ناگفته‌های آزمون معماری — طراحی — مهدی دریانی** — useful for ambiguity/interpretation traps and NEEDS_REVIEW cases.
6. **جزئیات اجرایی ساختمان — مهدی دریانی** — useful for plan/section/elevation/execution-detail relationships and Phase 2 understanding.
7. **آزمون‌های آزمایشی معماری — طراحی** — useful as diverse practice/regression cases after provenance is recorded.
8. **مجموعه سوالات/اسکیس‌های سال‌های گذشته** — useful for diversity of design problems and recognition of non-template solutions.

## Knowledge to carry into Architecture AI Agent
### A. Drawing Language vs Rule Core
Keep three layers separate: Architectural Drawing Language; Plan Understanding; Rule Core. Educational exam books may teach a solution strategy, but that strategy must not automatically become a Rule Core rule.

### B. Design-problem decomposition
Use the reasoning chain: Brief → Program/Spaces → Spatial Relations → Site/Boundary Constraints → Access/Circulation → Parking → Vertical Circulation → Ramp/Stair Geometry → Daylight/Ventilation Evidence → Dimensions → Drawing Set → Validation. This is a reasoning pattern, not a fixed residential template.

### C. Spatial relationships
Legitimate residential solutions include sequential rooms/corridors, central courtyard, lightwell, central circulation core, vertical stacking, split-level organization, narrow/deep lots, irregular lots, and varied parking/circulation arrangements. Do not reject a layout merely because it differs from a familiar template.

### D. Ramp understanding
A ramp is not one generic object. Semantic chain: Detect → Classify geometry → Measure → Understand context → Determine applicable rules → Evaluate. Candidate geometries: straight/uniform, 90-degree turn, curved/arc, U-turn/180-degree, spiral, multi-segment/compound, ramp with landing/transition, variable-slope segments. Evidence may include start/end levels, slope, width, radius, direction, transition/landing, and circulation context.

### E. Vertical levels
Preserve the distinction between Floor Designation and Elevation Code. One floor plan may contain multiple local elevations. Level annotations need semantic type/context such as floor finish, landing, ramp start/end, yard, street, roof, local level, or section level. Elevation numbers alone must not force a conclusion about stairs, ramps, or compliance.

### F. Phase 1 vs Phase 2
Phase 1 is design-stage; there is generally no expectation of door/window/material/room schedules. Phase 2 is execution-oriented and may include more sheets, finishes, wall build-ups, exact execution dimensions, details, schedules, and material information. Dimensions can change between phases. Latest issued drawing requires version/issue/supersession evidence, not date alone.

### G. Iranian drawing-language baseline
Vocational architectural drafting references, especially پایه دهم و یازدهم, remain important guidance for drawing language while regulations stay separate. Preserve: internal and external dimensions; scale/north in title frame; plan name under drawing; elevation annotations at stairs/landings and relevant site/ramp locations; section line with form/code/arrows/endpoints/cross-drawing relation; architectural axes in addition to structural framing; office-dependent title block; line types/weights and CAD layers as evidence/organization rather than absolute semantic truth; hatch meaning only with legend/annotation/context; revision history in project/document record.

## Source hierarchy for future extraction
Book/teaching statement → Extracted concept → Evidence classification → Compare with authoritative regulation/standard → Candidate rule or drawing-language fact.
Do not promote a book-specific recommendation to PASS/Rule Core without authoritative support.

## Physical-book ingestion plan
Do not OCR whole physical books by default.
1. Photograph table of contents.
2. Select only chapters/pages relevant to Plan Understanding, drawing language, spatial design, ramps, stairs, parking, levels, and execution drawings.
3. Photograph selected page ranges.
4. Extract concepts/evidence.
5. Cross-check against authoritative current sources.
6. Persist only useful structured knowledge and provenance.
The three highest-priority books are: مبانی طراحی معماری — مهدی دریانی; تشریح و طراحی سوالات آزمون‌های نظام مهندسی معماری — مهدی دریانی; تشریح و طراحی سوالات ... به روش پازل — مهدی بیات.

## Next work session
### Step 1 — Repository state
Verify current main and active PRs. Verify H99 exact-head CI before any merge decision. Never declare H99 GREEN without exact-head completed/success evidence.
### Step 2 — Architecture knowledge
Build/extend the Drawing Information + Annotation semantic model. Keep Floor Designation, Elevation Code, Section Marker, Axis, Dimension, Hatch, Title Block, Phase, Issue/Revision distinct. Add evidence/provenance fields where missing.
### Step 3 — Exam-book extraction
Begin with the table of contents of مبانی طراحی معماری — مهدی دریانی. Select only high-value sections. Do not wait for full-book digitization.
### Step 4 — Parallel design-case research
Continue collecting varied residential and circulation/ramp examples as exposure/reference. Do not create a new rigid taxonomy from these examples.
### Step 5 — Verification
Any implementation change follows: Implement → REAL CI → Verify → Regression → Persist → Continue. After any red test: Bug Hunt → root cause → fix → rerun → verify.