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


## Regulatory watch update — 2026-11-19 (baseline)

The prior report for this monitoring series was not available, so this is the initial baseline, not a change comparison.

### Correction to AR-SRC-007
The previously recorded interpretation of the docket number as a ruling dated 1405/03/05 is not supported. The secondary page currently displays **1406/03/05**, which is future-dated relative to 1405/08/28, and the docket-year prefix does not match the displayed date. Treat the result as **UNVERIFIED / UNKNOWN**; it cannot establish whether circular clause 11 was annulled or upheld. Do not delete the historic record; this correction supersedes its legal-status note.

### New source entries
| ID | Document | Status | Verification / level | Notes |
|---|---|---|---|---|
| AR-SRC-010 | General Board judgment No. 1404313900001295686, 1404/05/28 | EFFECTIVE for similar cases | COURT_PRIMARY text reproduced; official copy pending | Change of use is distinguished from building/extra area; Art.100 fine is not a standalone change-of-use sanction; Art.5 land-use-change authority. |
| AR-SRC-011 | Advisory opinion 7/1405/261, 1405/06/22 | ANNOUNCED | OFFICIAL_SECONDARY reproduction; signed primary copy SOURCE_REQUIRED | Final demolition decisions; execution limits and no enlargement of demolition footprint. |
| AR-SRC-012 | Advisory opinion 7/1405/231, 1405/06/15 | ANNOUNCED | OFFICIAL_SECONDARY reproduction; signed primary copy SOURCE_REQUIRED | Art.100 does not decide subdivision; only separately unpermitted construction operations. |
| AR-SRC-013 | Topic 24 national building regulation, first edition 1404; notification 1404/07/27 | NOTIFIED; EFFECTIVE by six-month clause as of this report; exact day UNKNOWN | OFFICIAL_SECONDARY host, primary text reproduced | Height/density/coverage/floor area/massing/placement/adjacency/cityscape; source PDF hash not obtained. |
| AR-SRC-014 | Fars Article-5 residential floor-height change to 350 cm; press 1405/08/17 | ANNOUNCED; legal effect UNKNOWN | PRESS_LEAD | Resolution and applicability details missing. |
| AR-SRC-015 | Unified historic Shiraz protection/development plan; reported registration 1404/12/01 | ANNOUNCED; plan/maps SOURCE_REQUIRED | PRESS_LEAD | Actual plan, official catalogue record and map attachments not retrieved. |
| AR-SRC-016 | General Board judgment No. 1403313900001065297, 1403/05/09 (Art.99) | EFFECTIVE in the case; holding not to be generalized | COURT_PRIMARY text reproduced; official copy pending | Art.99 outside city harem; do not import Art.100 three-principle demolition test automatically. |

### Links
- Topic 24 PDF copy: https://qsce.ir/uploads/%D9%85%D8%A8%D8%AD%D8%AB%20%D8%A8%DB%8C%D8%B3%D8%AA%20%D9%88%20%DA%86%D9%87%D8%A7%D8%B1%D9%85%20%D9%85%D9%82%D8%B1%D8%B1%D8%A7%D8%AA%20%D9%85%D9%84%D9%8A.pdf
- Fars 350-cm height press lead (Tasnim): https://newsmedia.tasnimnews.ir/fa/news/1405/08/17/3743048/%D9%85%D8%AC%D9%88%D8%B2-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%85%D8%A7%D8%AF%D9%87-5-%D8%A8%D8%B1%D8%A7%DB%8C-%D8%A7%D9%81%D8%B2%D8%A7%DB%8C%D8%B4-%D8%A7%D8%B1%D8%AA%D9%81%D8%A7%D8%B9-%D8%B7%D8%A8%D9%82%D8%A7%D8%AA-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%AA%D8%A7-3-5-%D9%85%D8%AA%D8%B1
- Fars 350-cm height press lead (Mehr): https://mehrnews.com/x3dycs
- Judgment 1295686: https://hoghogh.ai/case-law/%D8%B1%D8%A7%DB%8C-%D9%88%D8%AD%D8%AF%D8%AA-%D8%B1%D9%88%DB%8C%D9%87-%D9%87%DB%8C%D8%A7%D8%AA-%D8%B9%D9%85%D9%88%D9%85%DB%8C-%D8%AF%DB%8C%D9%88%D8%A7%D9%86-%D8%B9%D8%AF%D8%A7%D9%84%D8%AA-%D8%A7%D8%AF%D8%A7%D8%B1%DB%8C-%D8%AF%D8%B1%D8%A8%D8%A7%D8%B1%D9%87-%D8%AA%DA%A9%D9%84%DB%8C%D9%81-%DA%A9%D9%85%DB%8C%D8%B3%DB%8C%D9%88%D9%86-%D9%87%D8%A7%DB%8C-%D9%85%D8%A7%D8%AF%D9%87-%DB%B1%DB%B0%DB%B0-%D8%AF%D8%B1
- Opinion 7/1405/261: https://telegram.me/s/vvakil?before=31018
- Opinion 7/1405/231: https://tg.me/hoghoogh_amlaak/4061
- Article-99 judgment 1065297: https://hoghogh.ai/case-law/%D8%A7%D8%B9%D9%84%D8%A7%D9%85-%D8%AA%D8%B9%D8%A7%D8%B1%D8%B6-%D8%A8%DB%8C%D9%86-%D8%B1%D8%A7%DB%8C-%D8%B4%D9%85%D8%A7%D8%B1%D9%87-%DB%B1%DB%B4%DB%B0%DB%B2%DB%B3%DB%B1%DB%B3%DB%B9%DB%B0%DB%B0%DB%B0%DB%B3%DB%B8%DB%B0%DB%B6%DB%B3%DB%B3-%D9%85%D9%88%D8%B1%D8%AE-%DB%B1%DB%B4%DB%B0%DB%B2-%DB%B2-%DB%B1%DB%B9-%D8%B5%D8%A7%D8%AF%D8%B1%D9%87-%D8%A7%D8%B2-140331390001065297
- Historic Shiraz plan report: https://www.tasnimnews.ir/fa/news/1404/12/01/3521507/%D8%B7%D8%B1%D8%AD-%D8%B6%D9%88%D8%A7%D8%A8%D8%B7-%DB%8C%DA%A9%D9%BE%D8%A7%D8%B1%DA%86%D9%87-%D8%A8%D8%A7%D9%81%D8%AA-%D8%AA%D8%A7%D8%B1%DB%8C%D8%AE%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%AF%D8%B1-%D8%A7%D8%B3%D9%86%D8%A7%D8%AF-%D9%85%D9%84%DB%8C-%D8%AB%D8%A8%D8%AA-%D8%B4%D8%AF

Official-source retrieval failures remain logged; none of the above press leads or secondary copies are promoted to executable rules.
