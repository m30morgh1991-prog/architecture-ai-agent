# Shiraz Building-Regulation Authorities and Update Acquisition Plan

Research status: initial discovery, 2026-11-19. This is an authority map and collection plan, not a legal opinion. URLs and legal effect must be re-verified before any rule is promoted to enforceable compliance logic.

## 1. Authority and responsibility map

| Body / channel | Role in the building lifecycle | What to collect | Initial evidence / caveat |
|---|---|---|---|
| Shiraz Municipality — Urban Planning & Architecture / municipal transparency portal | Local planning rules, parcel-specific planning information, permit workflow, approved drawings, municipal circulars and service requirements | Detailed-plan text/maps, zoning and use tables, building permit checklists, urban design guidelines, amendments, committee decisions published by municipality | User supplied the municipality's transparency page and direct PDF for the revised detailed plan. PDF retrieval failed at the network/proxy layer; source registered as AR-SRC-004 and remains NOT_INGESTED. |
| Fars Province Article 5 Commission; secretariat associated with Fars Road & Urban Development Department | Reviews and approves detailed urban plans and their amendments within its legal remit | Signed resolutions, meeting minutes, technical committee recommendations, amendment maps, notification letters, effective dates and parcel/zone scope | Article 5 legal framework identifies the provincial commission and its membership. Individual resolutions must be obtained in signed/official form; press reports are leads only. |
| Fars General Department of Roads & Urban Development; Ministry of Roads & Urban Development; Supreme Council of Urban Planning and Architecture | Provincial secretariat / national policy and approval oversight for urban plans, depending on matter and materiality | Official circulars, approved plan documents, approvals/ratifications, national planning instructions, building-regulation notices | Article 5 process and review path indicate this is a primary route for obtaining commission records. |
| Fars Construction Engineering Organization (Fars Nezam) and national Construction Engineering Organization | Professional practice, design/review/supervision service procedures, professional circulars and implementation guidance; not the general legislator of Shiraz zoning | Design review checklists, engineering service circulars, professional directives, technical notices, discipline-specific requirements | A Fars professional channel surfaced a notice about mandatory alignment of approved drawings with National Building Regulations; use the organization’s official portal and signed notices as primary sources. |
| Ministry of Roads & Urban Development — National Building Regulations Office | National technical baseline for design, calculations, construction, supervision, operation and maintenance | Current editions and errata of National Building Regulations, formal interpretations, circulars and effective dates | National technical requirements can apply even where a municipal drawing has been approved; preserve both rule sets and detect conflict rather than assuming permit approval overrides national requirements. |
| Shiraz Fire & Safety Organization / municipal fire authority | Fire safety review and operational clearance where required | Fire access, escape, compartmentation, alarm/suppression, façade and parking safety requirements; review checklists and circulars | Exact current public document portal and current submission workflow still need verification. |
| Fars Cultural Heritage, Tourism and Handicrafts Department; Shiraz historic-area heritage bases | Heritage protection, registered property boundaries, historic fabric and buffer-zone controls | Registered monument and buffer maps, historic fabric rules, design approvals, conservation guidelines and case-specific approvals | A 2026 report says the integrated historic Shiraz protection/development regulations were registered in national archival records. Obtain the actual registered document and map annexes; do not rely on the news report as the rule text. |
| Fars Department of Environment and relevant national environmental bodies | Environmental permits and constraints where a project/activity triggers them | Environmental assessment decisions, protected-area maps, noise/pollution requirements and project-specific conditions | Applicability is project- and location-dependent; not a universal building-plan gate. |
| Shiraz City Council and relevant commissions | Municipal policy, fees, local resolutions and oversight; may approve municipal rules within statutory authority | Public council resolutions, approved fee schedules, commissions' published decisions and meeting records | Distinguish council resolutions from Article 5 planning approvals and from individual permit decisions. |
| Utility providers (electricity, gas, water/sewer, telecom) | Service connection, easements, safety clearances and infrastructure constraints | Service standards, connection requirements, utility maps, written technical clearances | Collect only where relevant to the parcel/building and record the issuing utility and validity period. |
| Governorate / provincial coordination bodies and Administrative Justice Court | Provincial coordination and legal review; court rulings may invalidate or interpret decisions | Official notifications, court judgments, annulments, binding legal interpretations | Track court decisions that annul a rule or decision; never treat a press summary as the operative judgment. |

## 2. High-value acquisition channels

1. Municipal transparency portal and official Shiraz Municipality site: retrieve the full detailed-plan PDF, zoning maps, appendices, later amendments, parcel-specific inquiry outputs and permit checklists.
2. Fars Road & Urban Development Department: request the complete signed Article 5 resolution, minutes, technical committee report, attachments/maps and notification/implementation date for every Shiraz amendment.
3. Fars Article 5 Commission secretariat: maintain a chronological decision register and request a searchable archive or official access route.
4. Fars Construction Engineering Organization: monitor official circulars, technical notices, review checklists and design/supervision service instructions.
5. National Building Regulations Office: monitor new editions, corrections, interpretations and effective dates of the national مباحث.
6. Fire authority and heritage authority: request official review checklists, maps, standard conditions and current approval process.
7. City Council public records: collect approved fee schedules and resolutions relevant to building permit and urban development.
8. National Library / National Archives: use archival catalogue records to locate historic-area and older planning documents; request copies from the responsible archive when not downloadable.
9. Freedom-of-information / official correspondence route: where no public download exists, submit a narrowly scoped written request for public decisions and annexes, citing title/date/subject and requesting searchable PDF plus maps. Record request number, date, recipient and response.

## 3. Initial verified leads

- Article 5 law: the provincial commission examines and approves detailed urban plans and changes. The law describes the provincial governor as chair (or deputy for civil affairs in absence), with the mayor and representatives of relevant ministries/agencies and the city council; the provincial engineering organization representative in architecture or urban planning participates without voting rights. Verify the current consolidated law before encoding membership or procedure.
- Shiraz residential floor-height amendment: a Tasnim report dated 17 Aban 1405 quotes the Fars urban-planning director-general as saying the Article 5 Commission agreed to allow residential storey height up to 3.50 m under an amendment to Shiraz detailed-plan rules. This is a high-priority lead only. Obtain the signed resolution, exact clause, effective date, zones/building types covered, transitional rules and whether the 3.50 m is floor-to-floor or another measurement before changing any rule.
- Historic Shiraz: a Tasnim report dated 1 Esfand 1404 states the integrated historic-area protection/management/development regulation was registered in national archival records. Retrieve the registered document and all maps/annexes from the National Library/Archives or responsible heritage authority.
- National Building Regulations: a published notice/report dated 1404/08/11 refers to the requirement to align approved drawings with National Building Regulations. Retrieve the original ministry circular and current legal status before using it as a compliance rule.

## 4. Mandatory evidence record for every collected rule

Each source/rule record must include:
- issuing_authority, issuing_unit, document_title, document_number, issue_date, publication_date, effective_from, effective_until (if known)
- source_url, official_file_hash, retrieved_at, original_language, page/section/clause, attachments/maps
- jurisdiction (national/province/city/zone/parcel), land-use class, building-use, height/storey/area thresholds, exemptions and transitional provisions
- legal_status: DRAFT / ANNOUNCED / APPROVED / NOTIFIED / EFFECTIVE / AMENDED / REPEALED / ANNULLED / UNKNOWN
- verification_level: OFFICIAL_PRIMARY / OFFICIAL_SECONDARY / PRESS_LEAD / USER_SUPPLIED / UNVERIFIED
- supersedes, amended_by, annulled_by, conflict_group
- applicability and required project inputs

## 5. Fail-closed integration policy

- A press article, social post, search snippet or unsigned draft is a discovery lead, not a rule capable of producing PASS.
- Only an official primary document with traceable issuer, number/date, clause and applicable geography can become a verified rule candidate.
- Even official rules remain NEEDS_REVIEW when parcel/zone, building use, date, threshold or annex/map applicability is unknown.
- Keep national technical rules, provincial planning approvals, municipal parcel rules, fire/heritage conditions and utility requirements as separate authorities and evaluate them cumulatively where applicable.
- Preserve superseded rules for audit, but never apply them as current without an explicit historical/as-of-date query.
- A conflict between a municipal approved plan and national technical regulation must be flagged for review; do not silently choose one or declare compliance.

## 6. Next research actions

1. Obtain the actual AR-SRC-004 PDF from the municipal portal through a working retrieval route and inspect every page and annex.
2. Locate the official signed Article 5 decision behind the reported 3.50 m residential floor-height amendment.
3. Locate the official registered integrated historic Shiraz regulations and their map appendices.
4. Verify official portals and downloadable document indexes for Fars Nezam, Fars Road & Urban Development, Shiraz Municipality, Fire Organization and Fars Heritage.
5. Add exact document links and hashes to the source registry; only then derive candidate rules and tests.


## 7. Article 100 — focused legal research update (2026-11-19)

This section records a preliminary legal-source review. The reproduced judgments below are secondary-host copies of court texts; obtain the official Gazette / judiciary publication before treating the source artifact as primary. The legal propositions are recorded narrowly and must not be generalized beyond each judgment's holding.

### 7.1 Statutory baseline

- Article 100 of the Municipalities Law applies to land and properties within the city limits or its legal buffer (حریم): owners must obtain a municipal permit before construction, land development or subdivision; the municipality may stop construction without a permit or contrary to the permit.
- The consolidated text reproduced by Lawlex identifies Article 100 as added 1345/11/27 and shows the first paragraph and amendments to its initial notes. The full current consolidated text, all notes (تبصره‌ها), subsequent amendments and official publication history still need a primary-source copy.
- Article 99 must be analyzed separately for areas outside the city limits and within the legally defined rural/urban jurisdiction. Do not infer that every parcel outside the built-up boundary is automatically governed by Article 99: determine its exact legal location (حدود شهر، حریم، خارج از حریم) and the relevant statutory authority first.

### 7.2 Judicial decisions and interpretations found

| Record | Date / identifier | Narrow holding from reproduced text | Status for project |
|---|---|---|---|
| Article 100 circular, clause 3 | Judgment 140331390001829587, 1403/08/01 | Annulled clause 3 of Ministry of Interior circular 239024 dated 1402/11/14 insofar as it required Article 100 commissions to order demolition for unroofed structures by relying on definition 4-2 of National Building Regulation Part 4. The court held the Ministry lacked authority to impose that binding direction on the statutory commission. | ANNULLED (clause 3); COURT_PRIMARY text still to be obtained from official publication. Never encode the annulled clause as a mandatory demolition rule. |
| Article 100 circular, clause 11 | Judgment 140531390000547350, 1405/03/05 | Did not annul clause 11. The court reasoned that where a demolition order was issued as the consequence of non-payment of a fine under notes 2 or 3, payment of the original fine means the demolition order no longer has a remaining basis for execution. | NOT_ANNULLED / binding effect stated under Article 93 of the Administrative Justice Court Law in reproduced text; official publication still required. Do not generalize to demolition orders based on independent substantive grounds. |
| Commercial use in non-commercial zone | Judgment 140431390000646865, 1404/03/13 | Reversed the earlier general precedent and upheld a branch decision finding the Article 100 commission lacked competence to impose a fine or demolition for operating a shop/business in a non-commercial zone contrary to the permit; the reproduced text distinguishes this from construction operations in a commercial zone. | Scope-sensitive; must be read with later advisory opinion 7/1404/681 and official judgment copy. Do not convert to a blanket rule that all commercial-use violations escape Article 100. |
| Interpretation after judgment 646865 | Advisory opinion 7/1404/681, dated 1404/10/28 | Records differing interpretations: whether judgment 646865 is limited to operating a business in a non-commercial zone (where closure under clause 24 of Article 55 may be relevant), while construction contrary to permit to create commercial premises in a commercial zone may remain within notes to Article 100. | OFFICIAL_SECONDARY reproduction / interpretation lead. Obtain the full official advisory response and use its exact conclusion before rule encoding. |

### 7.3 Circular 239024 (1402/11/14): handling rule

The circular contains 29 clauses. It must be represented clause-by-clause, not as one all-valid document. At minimum:
- Clause 3: annulled by judgment 140331390001829587 (1403/08/01); do not enforce its categorical unroofed-structure demolition instruction.
- Clause 11: not annulled by judgment 140531390000547350 (1405/03/05); its reproduced holding concerns the consequential demolition order following non-payment of a fine under notes 2 and 3, and subsequent payment of that fine.
- Other clauses: status UNKNOWN until individually checked against the complete circular and later judgments. Do not infer their validity from the treatment of clauses 3 and 11.
- Verify whether any later decision, amendment, stay or official interpretation changes the above status.

### 7.4 Implications for architectural plan checking

Article 100 is primarily an enforcement / adjudication framework for construction violations, not a substitute for design standards or a permit. Keep two separate layers:
1. **Preventive design compliance:** zoning, permit conditions, national technical rules, fire/heritage/utility requirements and verified municipal planning rules.
2. **Post-violation legal workflow:** jurisdiction, violation classification, commission procedure, notice and opportunity to respond, decision, appeal, execution, fine payment and judicial review.

The plan checker may flag potential exposure (e.g., construction beyond permit, use mismatch, parking shortfall, setback/height/area deviation) only where the relevant design/permit rule is verified. It must not predict a specific Article 100 fine or demolition outcome without the complete legal criteria, current tariff/base, case facts and competent decision.

### 7.5 Acquisition queue

1. Obtain official Gazette / official judiciary copies for judgments 140331390001829587, 140531390000547350 and 140431390000646865.
2. Obtain the complete 29-clause circular 239024 dated 1402/11/14 and build a clause-by-clause judicial status matrix.
3. Obtain the full official text of advisory opinion 7/1404/681 and any later advisory opinions on commercial-use change, unpermitted additions, parking and fine installment/payment.
4. Obtain a current official consolidated Article 100 and Article 99 text with amendment history from the Parliament Research Center / Official Gazette.
5. Obtain Shiraz-specific written procedure, forms, fine calculation bases, current council-approved tariffs, appeal workflow and enforcement practices. Treat informal municipal practice as unverified until supported by an official circular, resolution or published legal instrument.
6. Map parcel jurisdiction precisely (city limits / city buffer / outside both) before selecting Article 100 or Article 99 workflow.



## 8. Product-priority boundary — design optimization comes first (2026-11-19)

This regulation research is a supporting knowledge layer. It must not displace or harden the primary product workflow into a permit-enforcement tool.

### Primary product priorities
1. Understand the architectural plan reliably: geometry, spaces, walls, openings, columns, dimensions, levels and relationships, each with evidence and uncertainty.
2. Find design problems and opportunities: inefficient/circulation-heavy layouts, weak adjacency, unusable or leftover areas, spatial conflicts, poor furniture fit, daylight/ventilation concerns where evidence permits, privacy and functional-zoning issues.
3. Propose useful alternatives and explain trade-offs rather than merely flagging failures.
4. Analyze change impact on neighboring spaces, dimensions, circulation, structure and other constraints before controlled editing.
5. Preserve architect control: suggestions are advisory until selected and approved; uncertain observations remain visible as uncertain.

### How regulations support this workflow
- Regulations are consulted when relevant to the project, location, use, permit and design stage; they are not the default ranking function for every design suggestion.
- Separate hard, verified constraints from conditional requirements, design guidance and unknowns. A regulation with incomplete scope or source evidence must not block an otherwise useful design alternative.
- When a candidate design appears to conflict with a verified mandatory requirement, explain the exact evidence, affected element and possible compliant alternatives. Do not silently discard the design or claim legal approval.
- Article 100 research is limited to identifying preventable sources of construction/permit mismatch (for example, unapproved additions or changes from approved drawings). The product is not to adjudicate cases, calculate penalties, predict demolition, or automate commission decisions.
- Some risks are detectable only during construction or by comparing the as-built building with the approved permit set; mark these as outside drawing-only detection rather than pretending the plan checker can detect them.

### Priority rule
If work competes for implementation time, prioritize plan understanding, design-quality diagnosis, alternative generation, impact analysis and controlled editing over expanding legal-procedure analysis. Continue collecting high-value official regulations in parallel, but do not let that research block the design-optimization core.


## 9. Daily regulatory watch — 2026-11-24

### 9.1 New judicial and interpretive records
- Added the full reproduced judgment 140531390001131406 (1405/05/06) annulling letter 134252/420. Separate the plan-checking/design responsibility from the supervisor's execution-stage inspection duties; do not infer that national code requirements are waived.
- Added Shiraz judgments 140531390000237503 (1405/02/08), 140531390000547136 (1405/03/05), and 140531390000879392 (1405/04/09). Their exact annulled objects and limitations are recorded in the source register.
- Added advisory opinions 7/1405/55, 7/1404/722, 7/1405/231, 7/1405/261, 7/1404/727 and 7/1404/817. They clarify the Article 99/100/101 boundary, enforcement, demolition scope, partial payment and parking-fine refund. They remain advisory interpretations, not statutes or binding judgments.
- Reconfirmed the exact distinction in advisory 7/1404/681 after judgment 646865: operating a business in a residential/noncommercial space is different from physically constructing a commercial building there.

### 9.2 New planning and height leads
- A Ministry-news reproduction reports stage-one approval of the Shiraz master-plan framework at the 16th Supreme Council meeting (1405/08/26). The detailed-plan process is to follow; no parcel-level maps or signed resolution were obtained.
- A press report dated 1405/08/17 says the Article 5 Fars Commission approved a 350 cm maximum residential floor height. Measurement basis, scope, exceptions, resolution number, maps and effective date remain SOURCE_REQUIRED.

### 9.3 Primary-source acquisition gaps
- The official consolidated Article 100 page at the Majlis Research Center timed out; a secondary consolidated text was reviewed but is not sufficient for a final legal baseline.
- The official Ministry/INBR M24 binary and SHA-256 were not obtained; the six-month effective date is a calculation from the reproduced letter, not an independently confirmed official effective-date notice.
- The original Fars Article 5 resolution, current Shiraz detailed-plan maps, historic-fabric integrated rules and maps, current council tariff attachments, fire-service requirements and utility-specific building rules remain pending.
- No new rule was added to the executable registry and no rule was promoted to PASS.
