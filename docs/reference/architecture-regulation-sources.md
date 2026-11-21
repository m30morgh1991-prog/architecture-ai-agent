# Architecture Regulation Sources — Register

This register records user-provided architecture regulation references for later structured ingestion and validation.

## Source register
| ID | Document | Pages | Status | Coverage |
|---|---|---:|---|---|
| AR-SRC-001 | آموزش ضوابط طراحی معماری.pdf | 67 | Uploaded in conversation; reference text not binary in repo yet | Definitions; parking/ramp; stair/elevator; daylighting; projections; fire/egress; accessibility; structure/columns; spatial standards |
| AR-SRC-002 | ضوابط پارکینگ.pdf | 27 | Uploaded in conversation; reference text not binary in repo yet | Parking-specific criteria |

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


## Daily watch addendum — 2026-11-21

| ID | Document | Status | Source level / verification | Scope / caveat |
|---|---|---|---|---|
| AR-SRC-010 | Topic 24, first edition 1404, Urban Building Conformity; letter 140461/100/2 dated 1404/07/27 | NOTIFIED; EFFECTIVE after six months (calculated 1405/01/27) | OFFICIAL_SECONDARY; full PDF text read on non-official host; official-host copy/hash pending | M24 tall-building definition: ≥47 m OR ≥8 floors including ground OR highest usable floor >44 m above average ground. Prior 27/23-m note conflicts; do not attribute it to M24. |
| AR-SRC-011 | Topic 19, fifth edition (1404), initial notice | NOTIFIED; initial effective date reported 1404/10/19 | OFFICIAL_SECONDARY; IRCEO notice and linked 144-page PDF opened; minister letter metadata pending | Energy management; subsequent transition notice permits concurrent editions. |
| AR-SRC-012 | Extension of concurrent Topic 19 editions 4 (1399) and 5 (1404), 1404/10/20–1405/12/29 | AMENDED | OFFICIAL_SECONDARY; IRCEO announcement read; original ministerial letter pending | Both editions reportedly permitted through the stated period; one-day start-date discrepancy remains. |
| AR-SRC-013 | Topic 12, fifth edition: safety, occupational health and environment during construction; minister letter dated 1403/09/12 | NOTIFIED; EFFECTIVE as reported | OFFICIAL_SECONDARY; announcement read; full PDF/letter pending | No detailed clause extraction without full document. |
| AR-SRC-014 | General Board judgment 1405313900001131406 dated 1405/05/06; annulment of letter 134252/420 dated 1404/08/11 | EFFECTIVE (reported); target letter ANNULLED | OFFICIAL_SECONDARY; full judgment reproduced/read; official court copy pending | Narrowly annuls the Director-General letter on supervisor comparison/reporting of approved plans vs National Regulations. Not an exemption from design/execution duties. |
| AR-SRC-015 | Fars/Shiraz residential floor-height report up to 350 cm; Ministry news ID 237112, 1405/08/16–17 | ANNOUNCED; legal effect UNKNOWN | PRESS_LEAD; MRUD page timed out this run; Tasnim/Mehr reproductions found | Original Article-5 resolution, clause, height definition, zones/uses, notification and effective date SOURCE_REQUIRED. |

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