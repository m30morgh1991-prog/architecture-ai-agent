# Architecture Regulation Sources — Register

This register records user-provided architecture regulation references for later structured ingestion and validation.

## Source register
| ID | Document | Pages | Status | Coverage |
|---|---|---:|---|---|
| AR-SRC-001 | آموزش ضوابط طراحی معماری.pdf | 67 | Uploaded in conversation; reference text not binary in repo yet | Definitions; parking/ramp; stair/elevator; daylighting; projections; fire/egress; accessibility; structure/columns; spatial standards |
| AR-SRC-002 | ضوابط پارکینگ.pdf | 27 | Uploaded in conversation; reference text not binary in repo yet | Parking-specific criteria |
| AR-SRC-003 | User-supplied supplemental Persian architecture rule summary | — | USER_SUPPLIED; OFFICIAL_EDITION_NOT_VERIFIED | Summary topics are captured in docs/reference/architecture-regulations.md; not independently verified or executable. |

## User-supplied supplemental summary
The user supplied an additional Persian summary in the conversation covering:
- Stair/elevator core dimensions and unit-count guidance
- Light-well/patio area, minimum dimensions, and facing-window distances
- Parking dimensions, adjacent bay widths, maneuvering, entrances, ramp widths/slope, parking counts
- Clear-height notes for residential, parking, pilotis, basement, commercial, entrance, roof stair head, elevator pit, and basement daylight
- Window area, courtyard width, balcony projection, kitchen/bedroom/living/landing widths

See `docs/reference/architecture-regulations.md` for the captured rule summary and fail-closed integration requirements.

## Handling caveats
- User-supplied summaries and PDFs are references, not automatically current/official legal authority.
- Validate edition, jurisdiction, applicability, and conflicts before implementation or declaring compliance.
- The actual PDF binaries are not committed by this change; the current connector supports UTF-8 file creation, not a verified binary upload workflow. Preserve the original PDFs in the conversation/library and later add them through a normal Git upload if desired.


## Additional municipal source — pending retrieval
| ID | Document | Pages | Status | Coverage |
|---|---|---:|---|---|
| AR-SRC-004 | ضوابط و مقررات بازنگری طرح تفصیلی شهر شیراز (filename: `zavabemogararatbaznegari.pdf`) | Unknown | Official Shiraz Municipality transparency-site URL supplied by the user; direct retrieval attempted through web and PDF scraping, but both failed at the network/proxy layer. Content not yet inspected. | Pending document inspection; do not infer provisions from the filename or third-party summaries. |

Direct source URL: https://shaffaf.shiraz.ir/ImageGallery/FileManager/FilesForManager/taTafzil/zavabemogararatbaznegari.pdf
Information page: https://shaffaf.shiraz.ir/RContent/AXM7Q6C-%D8%A7%D8%B7%D9%84%D8%A7%D8%B9%D8%A7%D8%AA-%D8%B7%D8%B1%D8%AD-%D8%AA%D9%81%D8%B5%DB%8C%D9%84%DB%8C.aspx

Retrieval note: a failed fetch is not evidence that the URL is invalid or that the user lacks permission. Retry later. Until the actual PDF bytes/text are obtained, AR-SRC-004 must remain SOURCE_REQUIRED / NOT_INGESTED and must not produce compliance PASS results.


## Article 100 / 99 judicial-source register — 2026-11-19

| ID | Document | Status / verification | Coverage / caution |
|---|---|---|---|
| AR-SRC-005 | قانون شهرداری، ماده ۱۰۰ (متن تجمیعی بازنشرشده) | OFFICIAL_SECONDARY; current consolidated official Gazette/Parliament copy still required | Permit-before-construction rule; municipal stop-work power; notes and amendments. Do not treat this mirror as the final primary artifact. |
| AR-SRC-006 | دادنامه ۱۴۰۳۳۱۳۹۰۰۰۱۸۲۹۵۸۷ مورخ ۱۴۰۳/۰۸/۰۱ — ابطال بند ۳ بخشنامه ۲۳۹۰۲۴ | COURT_PRIMARY text reproduced by secondary legal host; official Gazette/judiciary copy pending | Annuls clause 3's categorical demolition direction for unroofed structures. |
| AR-SRC-007 | دادنامه ۱۴۰۵۳۱۳۹۰۰۰۰۵۴۷۳۵۰ مورخ ۱۴۰۵/۰۳/۰۵ — بند ۱۱ بخشنامه ۲۳۹۰۲۴ | COURT_PRIMARY text reproduced by secondary legal host; official Gazette/judiciary copy pending | Does not annul clause 11; concerns demolition as consequence of non-payment of fines under notes 2 and 3 and subsequent payment. |
| AR-SRC-008 | دادنامه ۱۴۰۴۳۱۳۹۰۰۰۰۶۴۶۸۶۵ مورخ ۱۴۰۴/۰۳/۱۳ | COURT_PRIMARY text reproduced by secondary legal host; official publication copy pending | Commercial activity in non-commercial zone; jurisdiction distinction. Must be read narrowly with later interpretation. |
| AR-SRC-009 | نظریه مشورتی ۷/۱۴۰۴/۶۸۱ مورخ ۱۴۰۴/۱۰/۲۸ | OFFICIAL_SECONDARY reproduction / primary signed copy pending | Interpretation following judgment 646865; do not generalize beyond its precise conclusion. |

Links discovered:
- Article 100 text: https://lawlex.ir/laws/shahrdari/100
- Judgment 1403/08/01 (clause 3): https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D8%A8%D9%86%D8%AF-%DB%B3-%D8%A8%D8%AE%D8%B4%D9%86%D8%A7%D9%85%D9%87-%D8%A7%D9%86%D8%AA%D8%B8%D8%A7%D9%85-%D8%A8%D8%AE%D8%B4%DB%8C-%D8%A8%D9%87-%D9%81%D8%B1%D8%A2%DB%8C%D9%86%D8%AF%D9%87%D8%A7-%D9%88-%D8%B9%D9%85%D9%84%DA%A9%D8%B1%D8%AF-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%87%D8%A7%DB%8C-%D9%85%D8%A7%D8%AF%D9%87-140331390001829587
- Judgment 1405/03/05 (clause 11): https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D8%A8%D9%86%D8%AF-%DB%B1%DB%B1-%D8%A8%D8%AE%D8%B4%D9%86%D8%A7%D9%85%D9%87-%D8%A7%D9%86%D8%AA%D8%B8%D8%A7%D9%85-%D8%A8%D8%AE%D8%B4%DB%8C-%D8%A8%D9%87-%D9%81%D8%B1%D8%A2%DB%8C%D9%86%D8%AF%D9%87%D8%A7-%D9%88-%D8%B9%D9%85%D9%84%DA%A9%D8%B1%D8%AF-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%87%D8%A7%DB%8C-%D9%85%D8%A7%D8%AF%D9%87-140531390000547350
- Judgment 1404/03/13 (646865): https://amagestate.com/legal/article-100-commission-ruling/
- Advisory opinion 7/1404/681: https://www.hoshyarvakil.ir/opinion/7-1404-681/

Register policy: These are research leads and reproductions, not a substitute for official Gazette/judiciary artifacts. Keep each clause's status independent. Clause 3 is ANNULLED; clause 11 was NOT ANNULLED by the located judgment; remaining circular clauses are UNKNOWN pending review. Article 99 jurisdiction must be separately determined from parcel location.


## Regulatory watch update — 2026-11-19 (baseline)

The prior report for this monitoring series was not available, so this is the initial baseline, not a change comparison.

### Correction to AR-SRC-007
The earlier uncertainty arose from a conflicting date rendering on a secondary page. A further retrieval on 2026-11-19 located the full reproduced judgment text with matching docket number **140531390000547350** and date **1405/03/05**. The reproduced General Board judgment expressly rejects annulment of clause 11. Update the clause status to **NOT ANNULLED in the scope of this judgment**; the original court/Gazette copy remains SOURCE_REQUIRED. The holding is limited to demolition issued as a consequence of non-payment under notes 2 and 3 and subsequent payment/settlement; it is not a blanket right to retain every violation.

### New source entries
| ID | Document | Status | Verification / level | Notes |
|---|---|---|---|---|
| AR-SRC-010 | General Board judgment No. 1404313900001295686, 1404/05/28 | EFFECTIVE for similar cases | COURT_PRIMARY text reproduced; official copy pending | Change of use is distinguished from building/extra area; Art.100 fine is not a standalone change-of-use sanction; Art.5 land-use-change authority. |
| AR-SRC-011 | Advisory opinion 7/1405/261, 1405/06/22 | ANNOUNCED | OFFICIAL_SECONDARY reproduction; signed primary copy SOURCE_REQUIRED | Final demolition decisions; execution limits and no enlargement of demolition footprint. |
| AR-SRC-012 | Advisory opinion 7/1405/231, 1405/06/15 | ANNOUNCED | OFFICIAL_SECONDARY reproduction; signed primary copy SOURCE_REQUIRED | Art.100 does not decide subdivision; only separately unpermitted construction operations. |
| AR-SRC-013 | مبحث 24 مقررات ملی ساختمان، ویرایش اول 1404 — انطباق شهری ساختمان؛ ابلاغ 1404/07/27 | NOTIFIED; EFFECTIVE date calculated as 1405/01/27 (16 Apr 2026), official-host confirmation pending | OFFICIAL_SECONDARY; Ministry letter/text reproduced on non-official host; binary/hash not obtained | Rechecked text defines high-rise as ≥27 m OR ≥8 floors including ground OR highest usable floor >23 m above average ground. Coverage: 40% general high-rise limit; 20% only for specified point-landmark high-rises of at least 12 floors. Plan detail takes precedence. |
| AR-SRC-014 | خبر موافقت کمیسیون ماده 5 فارس با ارتفاع طبقات مسکونی شیراز تا 350 سانتی‌متر — 1405/08/17 | ANNOUNCED; legal effect UNKNOWN | PRESS_LEAD | Resolution and applicability details missing. |
| AR-SRC-015 | Unified historic Shiraz protection/development plan; reported registration 1404/12/01 | ANNOUNCED; plan/maps SOURCE_REQUIRED | PRESS_LEAD | Actual plan, official catalogue record and map attachments not retrieved. |
| AR-SRC-016 | General Board judgment No. 1403313900001065297, 1403/05/09 (Art.99) | EFFECTIVE in the case; holding not to be generalized | COURT_PRIMARY text reproduced; official copy pending | Art.99 outside city harem; do not import Art.100 three-principle demolition test automatically. |

### Links
- Topic 24 PDF copy: https://qsce.ir/uploads/%D9%85%D8%A8%D8%AD%D8%AB%20%D8%A8%DB%8C%D8%B3%D8%AA%20%D9%88%20%DA%86%D9%87%D8%A7%D8%B1%D9%85%20%D9%85%D9%82%D8%B1%D8%B1%D8%A7%D8%AA%20%D9%85%D9%84%D9%8A.pdf
- Fars 350-cm height press lead (Tasnim): https://newsmedia.tasnimnews.ir/fa/news/1405/08/17/3743048/%D9%85%D8%AC%D9%88%D8%B2-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%85%D8%A7%D8%AF%D9%87-5-%D8%A8%D8%B1%D8%A7%DB%8C-%D8%A7%D9%81%D8%B2%D8%A7%DB%8C%D8%B4-%D8%A7%D8%B1%D8%AA%D9%81%D8%A7%D8%B9-%D8%B7%D8%A8%D9%82%D8%A7%D8%AA-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%AA%D8%A7-3-5-%D9%85%D8%AA%D8%B1
- Fars 350-cm height press lead (Mehr): https://mehrnews.com/x3dycs
- Judgment 1295686: https://hoghogh.ai/case-law/%D8%B1%D8%A7%DB%8C-%D9%88%D8%AD%D8%AF%D8%AA-%D8%B1%D9%88%DB%8C%D9%87-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%85%D9%88%D9%85%DB%8C-%D8%AF%DB%8C%D9%88%D8%A7%D9%86-%D8%B9%D8%AF%D8%A7%D9%84%D8%AA-%D8%A7%D8%AF%D8%A7%D8%B1%DB%8C-%D8%AF%D8%B1%D8%A8%D8%A7%D8%B1%D9%87-%D8%AA%DA%A9%D9%84%DB%8C%D9%81-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%87%D8%A7%DB%8C-%D9%85%D8%A7%D8%AF%D9%87-%DB%B1%DB%B0%DB%B0-%D8%AF%D8%B1
- Opinion 7/1405/261: https://telegram.me/s/vvakil?before=31018
- Opinion 7/1405/231: https://tg.me/hoghoogh_amlaak/4061
- Article-99 judgment 1065297: direct URL not verified in this run; use the exact judgment number/title for official retrieval.
- Historic Shiraz plan report: https://www.tasnimnews.ir/fa/news/1404/12/01/3521507/%D8%B7%D8%B1%D8%AD-%D8%B6%D9%88%D8%A7%D8%A8%D8%B7-%DB%8C%DA%A9%D9%BE%D8%A7%D8%B1%DA%86%D9%87-%D8%A8%D8%A7%D9%81%D8%AA-%D8%AA%D8%A7%D8%B1%DB%8C%D8%AE%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%AF%D8%B1-%D8%A7%D8%B3%D9%86%D8%A7%D8%AF-%D9%85%D9%84%DB%8C-%D8%AB%D8%A8%D8%AA-%D8%B4%D8%AF

Official-source retrieval failures remain logged; none of the above press leads or secondary copies are promoted to executable rules.


## Article 99 follow-up — 2026-11-19

| ID | Document | Status | Source level | Holding / scope |
|---|---|---|---|---|
| AR-SRC-017 | General Board judgment 1403313900001065343, 1403/05/09; circular 145016 dated 1401/07/19 | EFFECTIVE; specific clauses annulled | COURT_PRIMARY text reproduced; official copy pending | Annuls clauses 7 and 8 (demolition deadline/execution procedure), 9 (50–70% fine formula), 10 (re-referral for demolition after non-payment), and 14 (allocation/use of collected funds) of the cited Article-99 guideline. Does not annul the whole guideline or Article 99. |
| AR-SRC-018 | Advisory opinion 7/1403/747, 1403/10/30 | ANNOUNCED; non-binding | OFFICIAL_SECONDARY reproduction | Jurisdiction follows the legal boundary status at the date of violation: if construction occurred while outside city harem, Article-99 commission remains competent even if the parcel later enters city limits/harem; construction after entry is Article-100. |

Links:
- Judgment 1065343: https://amagestate.com/legal/article-99-building-demolition-ruling/
- Opinion 7/1403/747: https://hoshyarvakil.ir/opinion/7-1403-747/

This follow-up materially qualifies the earlier simple boundary note: **jurisdiction must be determined by parcel location and the date of the alleged violation**, using official boundary/harem records. Do not use the parcel's current status alone.


## Source-link and status correction — AR-SRC-016
The direct link saved for AR-SRC-016 could not be opened/verified during this run. Keep the reproduced judgment in the register, but do not treat its URL as validated. Use the exact judgment number 1403313900001065297 and title to retrieve it from the official court/Gazette or a stable legal database.


## Clause 11 — verified text-reproduction correction (2026-11-19)

The full reproduced judgment No. 140531390000547350 dated 1405/03/05 was retrieved at https://hoghogh.ai/case-law/ (case title: ابطال بند ۱۱ بخشنامه انتظام‌بخشی...). The General Board **rejected the request to annul clause 11**. It reasoned that, under the relevant notes 2 and 3 of Article 100, demolition after non-payment is a substitute/guarantee for the original fine decision; once the fine is paid or otherwise settled, there is no remaining basis to execute that substitute demolition. This is a narrow clause-specific holding, not a general legalization or permission to retain unauthorized construction. Source level remains COURT_TEXT_REPRODUCED_BY_SECONDARY_HOST; official judiciary/Gazette copy and hash are still SOURCE_REQUIRED.


## Regulatory watch update — 2026-11-20

### AR-SRC-019 — Ministry of Roads and Urban Development news (official secondary)
- Title: ارتفاع طبقات مسکونی تا ۳۵۰ سانتی‌متر مجاز شد
- Article ID: 237112; date/time: 1405/08/16, 21:43
- URL: http://news.mrud.ir/news/237112/
- Source level: OFFICIAL_SECONDARY. Full news text retrieved and read on 1405/08/29.
- It reports that amendment of Shiraz detailed-plan clauses was considered and approved in Fars Article-5 commission and residential floor height up to 350 cm is permitted.
- Status: ANNOUNCED only for this evidence record; the original resolution, amended clause, measurement definition, zones/uses, conditions, notification and effective date are still SOURCE_REQUIRED. No legal threshold or runtime rule activation.

### AR-SRC-020 — Official INBR listing for Topic 24
- Page: https://inbr.ir/%D8%AF%D8%A7%D9%86%D9%84%D9%88%D8%AF-%D9%85%D8%A8%D8%AD%D8%AB-%D8%A8%DB%8C%D8%B3%D8%AA-%D9%88-%DA%86%D9%87%D8%A7%D8%B1%D9%85/
- The official-domain indexed result lists a download page for Topic 24; indexed snippet carries 1405/06/08. This verifies official listing metadata only, not a fresh edition or amendment.
- Status: UNKNOWN for the document's version/contents/effective date in this run. Direct page and PDF fetch were blocked (403); no hash.

### AR-SRC-021 — Topic 22 second-edition first draft
- Official indexed PDF URL: https://inbr.ir/wp-content/uploads/2025/10/%D9%85%D8%AA%D9%86-%D9%BE%DB%8C%D8%B4-%D9%86%D9%88%DB%8C%D8%B3-%D8%A7%D9%88%D9%84-%D9%88%DB%8C%D8%B1%D8%A7%DB%8C%D8%B4-%D8%AF%D9%88%D9%85-%D9%85%D8%A8%D8%AD%D8%AB-22-%D9%85%D9%82%D8%B1%D8%B1%D8%A7%D8%AA-%D9%85%D9%84%DB%8C-%D8%B3%D8%A7%D8%AE%D8%AA%D9%85%D8%A7%D9%86-06-08-1404.pdf
- Search index title identifies “پیش‌نویس اول ویرایش دوم مبحث 22” with file-date clue 1404/08/06. This is DRAFT, not an adopted/effective edition.
- Direct PDF retrieval blocked (403); contents, approval, notification, effective date, and hash not inspected.

No new verified Article-100/99 judgment, official Shiraz parking/fee/permit, fire, heritage, utility, or parcel-specific zoning document was surfaced by the targeted searches today. Search coverage is not exhaustive; this means no new verified change, not proof that no change exists.

## Daily watch addendum — 2026-11-21

| ID | Document | Status | Source level / verification | Scope / caveat |
|---|---|---|---|---|
| AR-SRC-013 | مبحث 24 مقررات ملی ساختمان، ویرایش اول 1404 — انطباق شهری ساختمان؛ ابلاغ 1404/07/27 | NOTIFIED; EFFECTIVE date calculated as 1405/01/27; official-host confirmation pending | OFFICIAL_SECONDARY; full PDF text read on non-official host; official-host copy/hash pending | Correct text: high-rise ≥27 m OR ≥8 floors including ground OR highest usable floor >23 m above average ground. General high-rise coverage max 40%; special point-landmark high-rise: max 20% and min 12 floors. No 47/44 m or 24% rule in the rechecked text. |
| AR-SRC-022 | مبحث ۱۹ مقررات ملی ساختمان، ویرایش پنجم ۱۴۰۴ — مدیریت انرژی در ساختمان | NOTIFIED; initial effective date reported 1404/10/19 | OFFICIAL_SECONDARY; IRCEO notice and linked 144-page PDF opened; minister letter metadata pending | Energy management; subsequent transition notice permits concurrent editions. |
| AR-SRC-023 | تمدید اجرای همزمان ویرایش چهارم و پنجم مبحث ۱۹ تا پایان ۱۴۰۵ | AMENDED | OFFICIAL_SECONDARY; IRCEO announcement read; original ministerial letter pending | Both editions reportedly permitted through the stated period; one-day start-date discrepancy remains. |
| AR-SRC-024 | مبحث ۱۲ مقررات ملی ساختمان، ویرایش پنجم — ایمنی، بهداشت‌کار و محیط‌زیست در حین اجرا | NOTIFIED; EFFECTIVE as reported | OFFICIAL_SECONDARY; announcement read; full PDF/letter pending | No detailed clause extraction without full document. |
| AR-SRC-025 | دادنامه هیأت عمومی 1405313900001131406 مورخ 1405/05/06 — ابطال نامه 134252/420 مورخ 1404/08/11 | EFFECTIVE (reported); target letter ANNULLED | OFFICIAL_SECONDARY; full judgment reproduced/read; official court copy pending | Narrowly annuls the Director-General letter on supervisor comparison/reporting of approved plans vs National Regulations. Not an exemption from design/execution duties. |
| AR-SRC-014 | خبر موافقت کمیسیون ماده 5 فارس با ارتفاع طبقات مسکونی شیراز تا 350 سانتی‌متر — 1405/08/17 | ANNOUNCED; legal effect UNKNOWN | PRESS_LEAD; MRUD page timed out this run; Tasnim/Mehr reproductions found | Original Article-5 resolution, clause, height definition, zones/uses, notification and effective date SOURCE_REQUIRED. |

### Direct source links
- Topic 24 official download page (access restricted this run): https://inbr.ir/دانلود-مبحث-بیست-و-چهارم/
- Topic 24 reproduced text PDF: https://atnasr.ir/wp-content/uploads/2025/11/Mabhas24-v1.0-1404-ATNasr.ir.pdf
- Topic 19 fifth-edition notice: https://irceo.ir/fa/news/36052/ابلاغ-ویرایش-پنجم-مبحث-نوزدهم
- Topic 19 fifth-edition PDF: https://static0.irceo.ir/servev2/OGNkNAT8Ewpf/lgax4Op8x6k5CUTWbZszXbbJmCHlw5ISu1nbqwkXWZy6TtQwfVyWBCMwERybPv4CM9_AR0Jt85wcIyAAhsJNNA,,/file.pdf
- Topic 19 transition extension: https://irceo.ir/fa/news/36375/تمدید-اجرای-همزمان-ویرایش-چهارم
- Topic 12 fifth-edition notice: https://irceo.ir/fa/news/35804/ابلاغ-ویرایش-پنجم-مبحث-دوازدهم
- Judgment 1405313900001131406: https://hoghogh.ai/case-law/ابطال-نامه-شماره-134252-420-مورخ-1404-8-11-مدیرکل-دفتر-مقررات-ملی-140531390001131406
- MRUD news ID 237112 (timeout): http://news.mrud.ir/news/237112/
- Tasnim height lead: https://newsmedia.tasnimnews.ir/fa/news/1405/08/17/3743048/

### Topic 24 source correction
The reproduced first-edition text (section 2-4 definitions, PDF page around 27) defines a tall building as 47 m or more, or 8 floors or more including ground, or a highest usable floor more than 44 m above average ground. Prior 27 m / 23 m figures are not supported by this reproduced M24 text. Keep them as a source conflict and do not attribute them to M24; the 47/44 m values remain source-gated because the official-host PDF was not obtained. The text also describes density increases for 8+ floors as requiring high-rise zone/axis context rather than an isolated building and states a 24% coverage limit for high-rise buildings. Applicability to a Shiraz parcel must be checked against the detailed plan and primary source.

### Topic 24 effective-date discrepancy
The reproduced letter dated 1404/07/27, No. 140461/100/2, says effectiveness six months after notification. Calendar calculation yields 1405/01/27. A secondary summary says “from Ordibehesht 1405”; retain this conflict pending official-host verification.

### Topic 19 transition
The initial fifth-edition notice reports mandatory application from 1404/10/19. The later IRCEO announcement states concurrent use of fourth (1399) and fifth (1404) editions from 1404/10/20 through 1405/12/29. Preserve version selection and evidence per project; do not force v5-only checks during the reported transition. The one-day start discrepancy and original minister letter metadata remain SOURCE_REQUIRED.

### Judgment 1131406
The judgment annuls letter 134252/420, not National Building Regulations themselves and not general duties of designers, executors, permit issuers, or supervisors arising from other statutes/regulations. Its reproduced reasoning says no express supervisor duty to compare approved plans with National Regulations is stated in the cited rules, while another phrase appears to refer to such a duty. Retain this textual tension and obtain the official judgment before definitive legal interpretation.

Retrieval time: 1405/08/30, 09:43 Asia/Tehran. SHA-256 not calculated; PDF binary download failed.

**Source provenance correction:** the full M24 text/thresholds were read from the ATNasr-hosted PDF. The letter number/date were found in a search-indexed QSCE PDF result, but its exact direct URL could not be verified. Do not imply that the ATNasr PDF itself contains the ministerial letter. Official-host PDF and hash remain pending.


## Additional source records — integrated 2026-11-21

| ID | Document | Verification / status | Notes |
|---|---|---|---|
| AR-SRC-022 | مبحث ۱۹ مقررات ملی ساختمان، ویرایش پنجم ۱۴۰۴ — مدیریت انرژی در ساختمان | OFFICIAL_SECONDARY; IRCEO notice and linked PDF opened; minister letter metadata pending | Initial effective date reported 1404/10/19; later transition extension permits editions 4 and 5 through 1405/12/29. |
| AR-SRC-023 | تمدید اجرای همزمان ویرایش چهارم و پنجم مبحث ۱۹ تا پایان ۱۴۰۵ | OFFICIAL_SECONDARY; IRCEO announcement read; original ministerial letter pending | Reported concurrent use from 1404/10/20 to 1405/12/29; one-day discrepancy remains SOURCE_REQUIRED. |
| AR-SRC-024 | مبحث ۱۲ مقررات ملی ساختمان، ویرایش پنجم — ایمنی، بهداشت‌کار و محیط‌زیست در حین اجرا | OFFICIAL_SECONDARY; IRCEO announcement read; full PDF/letter not obtained | Effectiveness reported from 1403/09/12; no clause-level implementation until full source is obtained. |
| AR-SRC-025 | دادنامه هیأت عمومی 1405313900001131406 مورخ 1405/05/06 — ابطال نامه 134252/420 مورخ 1404/08/11 | Full judgment reproduced by secondary host; official court/Gazette copy pending | Narrow annulment of the cited letter only; no general exemption from code/design/execution duties. |
