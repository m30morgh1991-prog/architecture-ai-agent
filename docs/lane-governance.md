# Architecture AI Agent — Lane Governance, Priority & Acceptance

## Purpose

این سند سه لایه را یکپارچه می‌کند:

1. وضعیت اجرای Laneها و وابستگی‌های آن‌ها.
2. اولویت و Stop Gateهای سراسری.
3. معیار پذیرش عینی برای هر Lane.

اصل حاکم:
`Implement → CI Run/Status → Verify → Sync Project State → Continue`

هیچ Lane با ادعا، تست محلی، یا نتیجه شبیه‌سازی‌شده به `PASS` ارتقا نمی‌یابد.

## Unified Lane Status Model

هر Lane فقط یکی از این وضعیت‌ها را دارد:

- `NOT_STARTED`: هنوز اجرا نشده.
- `READY`: پیش‌نیازها برقرار و آماده اجرا.
- `IN_PROGRESS`: در حال اجرا.
- `BLOCKED`: یک Stop Gate فعال است.
- `NEEDS_REVIEW`: خروجی قابل ادامه است ولی نیاز به بررسی انسانی/شواهد بیشتر دارد.
- `VERIFIED_PASS`: معیار پذیرش Lane و CI واقعی تأیید شده.
- `VERIFIED_FAIL`: معیار پذیرش یا CI شکست خورده و باید اصلاح شود.

تفاوت مهم:
- `PASS` در سطح قرارداد/Logical با `VERIFIED_PASS` در Runtime واقعی یکی نیست.
- Real Runtime/Visual فقط وقتی `VERIFIED_PASS` می‌گیرد که اجرای واقعی، شواهد ورودی/خروجی و Stop Gateهای مربوطه تأیید شده باشند.

## Global Stop Gates

هرکدام از موارد زیر می‌تواند Lane مربوطه و هر Lane وابسته را متوقف کند:

### SG-01 — CI Gate
اگر CI واقعی شکست بخورد یا وضعیت آن ناشناخته باشد:
- Merge متوقف.
- Lane وابسته متوقف.
- فقط Laneهای مستقل مجاز به ادامه‌اند.

### SG-02 — Source Identity Gate
اگر source hash / model identity / source document قابل اثبات نباشد:
- PlanModel approval متوقف.
- Controlled Editing متوقف.
- Final PASS ممنوع.

### SG-03 — Fixed-Element Safety Gate
هر Fixed Element با وضعیت `UNKNOWN` یا corroboration ناکافی:
- promotion به `LOCKED` ممنوع.
- تغییر هندسی وابسته متوقف.
- نتیجه فقط `UNKNOWN`/`NEEDS_REVIEW`/ `BLOCKED`.

### SG-04 — Scale Gate
scale/unit ناشناخته یا متناقض:
- عملیات وابسته به اندازه/فاصله متوقف.
- conflict صریح → `BLOCKED`.

### SG-05 — Impact Gate
هر اثر مستقیم یا BIM-indirect روی عنصر LOCKED/UNKNOWN/CONDITIONAL حل‌نشده:
- ApprovedChangePlan صادر نمی‌شود.
- execution ممنوع.

### SG-06 — Approval Gate
بدون `ApprovedChangePlan` معتبر:
- Controlled Editing اجرا نمی‌شود.

### SG-07 — Mutation Guard Gate
اگر امکان mutation روی LOCKED element یا خارج از target scope وجود داشته باشد:
- execution باید fail-closed شود.

### SG-08 — Post-Edit Evidence Gate
اگر after-state دوباره detect/validate نشده باشد:
- PostEditDiff معتبر نیست.
- Final Validation ممنوع.

### SG-09 — Audit Gate
اگر source identity، change request، approval، execution، diff و validation قابل ردیابی نباشند:
- Release/Final PASS ممنوع.

## Priority Order

### P0 — Safety / Source of Truth
اولویت مطلق:
1. Native DWG evidence + entity inventory
2. Fixed-element corroboration
3. Scale/unit evidence
4. PlanModel validity
5. BIM semantics + ConstraintMap

### P1 — Dependency / Impact
پس از P0:
6. BIM relation-aware Impact Analysis
7. ApprovedChangePlan / Controlled Editing guards

### P2 — Real Runtime Verification
8. Golden DWG regression
9. Controlled Editing real-runtime E2E
10. Post-Edit Detection + Diff

### P3 — Release Integrity / Visual
11. Final Validation + Audit
12. Real Visual Runtime / visual adapter verification

### P4 — Expansion / Knowledge
13. BIM/AutoCAD/Revit interoperability hardening
14. Standards/rules expansion and evidence registry
15. Research-gap / controlled-editing contract expansion

قانون موازی‌سازی:
- Laneهای یک Priority می‌توانند موازی باشند اگر dependency ندارند.
- Lane با Priority پایین‌تر می‌تواند مستقل از Lane بالاتر اجرا شود، اما حق bypass کردن Stop Gate بالاتر را ندارد.
- هیچ Lane نباید وضعیت Lane دیگری را جعل یا green کند.

## Lane Dependency Graph

`Source → Evidence → Detection → PlanModel → BIM Semantics → ConstraintMap → Scale → Impact → Approval → Controlled Edit → Post-Edit Detection/Diff → Final Validation → Audit → Release`

Visual Runtime از Source/Evidence/Detection/Scale و Controlled Editing/Validation شواهد می‌گیرد.

## Lane Acceptance Criteria

### L1 — Native DWG
**هدف:** تبدیل DWG واقعی به evidence-backed architectural candidates.

پذیرش:
- source identity/hash ثبت شود.
- entity inventory واقعی تولید شود.
- candidate IDs پایدار باشند.
- هر candidate دارای evidence IDs باشد.
- promotion بدون شواهد کافی ممکن نباشد.
- contradiction → BLOCKED.
- regression روی DWG واقعی اجرا شود.
- CI واقعی سبز باشد.

### L2 — Fixed-Element Corroboration
پذیرش:
- COLUMNS/WALLS/DOORS/WINDOWS/OUTER_BOUNDARY/OVERALL_PLAN_FORM پوشش داده شوند.
- یک signal به‌تنهایی LOCKED نکند.
- corroboration مستقل طبق contract اعمال شود.
- contradiction → BLOCKED.
- unknown → fail-closed.
- CI سبز.

### L3 — Scale / Unit
پذیرش:
- حداقل دو signal مستقل → PASS/scale_known.
- یک signal → NEEDS_REVIEW.
- نبود signal → UNKNOWN.
- conflict explicit/header → BLOCKED.
- evidence IDs حفظ شوند.
- CI سبز.

### L4 — PlanModel + BIM Semantics
پذیرش:
- PlanModel Source of Truth باقی بماند.
- BIM identity و relations معتبر باشند.
- relation/identity conflict → BLOCKED.
- mapping LOCKED/EDITABLE/CONDITIONAL/UNKNOWN deterministic باشد.
- missing identity/binding → fail-closed.
- CI سبز.

### L5 — ConstraintMap
پذیرش:
- source element و evidence provenance حفظ شود.
- missing binding → NEEDS_REVIEW.
- semantic/state conflict → BLOCKED.
- unknown/unmapped → fail-closed.
- خروجی deterministic باشد.
- CI سبز.

### L6 — Impact + BIM Relations
پذیرش:
- direct impact محاسبه شود.
- BIM relation neighbors در impact وارد شوند.
- protected indirect → BLOCKED.
- unknown indirect → BLOCKED/NEEDS_REVIEW طبق contract.
- conditional indirect unresolved → BLOCKED.
- graph فقط impact authority بدهد، نه edit authority.
- CI سبز.

### L7 — ApprovedChangePlan / Controlled Editing
پذیرش:
- فقط targetهای مجاز قابل اجرا باشند.
- LOCKED/UNKNOWN/unsafe targets اجرا نشوند.
- source_sha256/model_id/approval/impact/visual readiness بررسی شوند.
- no approval → no execution.
- mutation خارج scope → fail-closed.
- CI سبز و runtime evidence ثبت‌شده.

### L8 — Golden DWG Regression
پذیرش:
- source SHA معتبر و قابل ردیابی باشد.
- entity/candidate inventory سازگار باشد.
- PlanModel/evidence/BIM graph معتبر باشند.
- fail-closed invariant برقرار باشد.
- candidate count با candidate IDs برابر باشد.
- duplicate IDs رد شوند.
- CI سبز.

### L9 — Post-Edit Detection + Diff
پذیرش:
- before/after source identity حفظ شود.
- after-state دوباره detect شود.
- changed IDs دقیقاً قابل ردیابی باشند.
- هر تغییر LOCKED شناسایی و reject شود.
- unauthorized change → invalid/BLOCKED.
- absence of after-state → not PASS.
- CI سبز.

### L10 — Final Validation + Audit
پذیرش:
- approval معتبر باشد.
- post-edit validation معتبر باشد.
- source/model match برقرار باشد.
- audit complete باشد.
- هر missing prerequisite → false/fail-closed.
- CI سبز.

### L11 — Real Visual Runtime
پذیرش:
- واقعی بودن source ingestion اثبات شود.
- detector output با evidence قابل ردیابی باشد.
- scale و fixed-element safety gate پاس شود.
- editor guard verified باشد.
- post-edit detection موجود باشد.
- visual output با source/model/approved change سازگار باشد.
- هیچ uncertainty unresolved باقی نماند.
- Real Runtime/Visual evidence ثبت شود؛ Logical PASS به‌تنهایی کافی نیست.
- CI سبز.

### L12 — BIM / AutoCAD / Revit Interoperability
پذیرش:
- mapping بین native/BIM semantics و PlanModel deterministic باشد.
- source identity و external refs حفظ شوند.
- unknown semantics fail-closed باشند.
- round-trip یا import/export ادعا فقط با test واقعی پذیرفته شود.
- CI سبز.

### L13 — Standards / Rule Engine
پذیرش:
- source authority و evidence provenance ثبت شود.
- priority hierarchy رعایت شود.
- conflicting sources به‌صورت deterministic حل یا NEEDS_REVIEW شوند.
- absence of applicable rule → UNKNOWN.
- rule adapter nondeterministic → NEEDS_REVIEW.
- CI سبز.

### L14 — Research / Controlled-Editing Contract
پذیرش:
- research claim از implementation contract جدا باشد.
- هر claim منبع و provenance داشته باشد.
- gap به requirement قابل تست تبدیل شود.
- research commit بدون CI Green به‌عنوان runtime green ثبت نشود.
- CI/verification status مستقل ثبت شود.

## Release Gates

### Gate A — Safe Analysis
لازم:
L1 + L2 + L3 + L4 + L5

خروجی مجاز:
Analysis / Proposal فقط؛ execution هنوز ممنوع.

### Gate B — Safe Planning
لازم:
Gate A + L6 + L7

خروجی:
ApprovedChangePlan قابل اجرا، مشروط به runtime guards.

### Gate C — Real Editing
لازم:
Gate B + L8 + L9

خروجی:
Controlled Edit با before/after evidence.

### Gate D — Release
لازم:
Gate C + L10 + L11
و برای قابلیت‌های BIM/standards مربوطه، L12/L13.

## Current Operating Rule

در هر نوبت کاری:

1. وضعیت PR/CI واقعی بررسی شود.
2. PR سبز → Verify → Merge.
3. بعد از Merge، main CI دوباره Verify شود.
4. سپس Project State/Notion Sync شود.
5. Laneهای مستقل Priority فعلی موازی ادامه یابند.
6. هر Stop Gate فعال، Laneهای وابسته را متوقف کند.
7. هیچ `VERIFIED_PASS` بدون شواهد واقعی ثبت نشود.

## Current Known Lanes

- H86 / L1: Native DWG — IN_PROGRESS until PR/CI verification.
- Impact BIM / L6: IN_PROGRESS until PR/CI verification.
- Golden DWG / L8: IN_PROGRESS until PR/CI verification.
- Scale Runtime / L3: IN_PROGRESS until PR/CI verification.
- Controlled Editing / L7: requires real runtime verification.
- Post-Edit / L9: contract exists; real before/after detection still required.
- Final Validation/Audit / L10: contract exists; integrated runtime evidence still required.
- Real Visual / L11: NOT VERIFIED until full real-runtime chain passes.

