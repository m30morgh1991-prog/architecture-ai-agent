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
