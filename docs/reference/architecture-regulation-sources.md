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


## 2026-11-24 daily source addendum

**Received/reviewed:** 2026-11-24 09:35:19 Asia/Tehran. No binary hash was computed in this run. The complete texts below were read from secondary hosts; the original official court/advisory PDFs remain pending unless explicitly stated.

| ID | Instrument | Status | Source level | Scope / limitation | Link |
|---|---|---|---|---|---|
| AR-SRC-010 | دادنامه ۱۴۰۵۳۱۳۹۰۰۰۱۱۳۱۴۰۶، ۱۴۰۵/۰۵/۰۶؛ نامه ۱۳۴۲۵۲/۴۲۰ | ANNULLED | COURT_PRIMARY (full text reproduced; official PDF pending) | ابطال نامه مدیرکل درباره تکلیف ناظر به تطبیق نقشه مصوب با مباحث ملی؛ نظارت ناظر بر اجرا در حدود صلاحیت و انطباق با پروانه/نقشه/محاسبات باقی است. | [متن رأی](https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D9%86%D8%A7%D9%85%D9%87-%D8%B4%D9%85%D8%A7%D8%B1%D9%87-%DB%B1%DB%B3%DB%B4%DB%B2%DB%B5%DB%B2-%DB%B4%DB%B2%DB%B0-%D9%85%D9%88%D8%B1%D8%AE-%DB%B1%DB%B4%DB%B0%DB%B4-%DB%B8-%DB%B1%DB%B1-%D9%85%D8%AF%DB%8C%D8%B1%DA%A9%D9%84-%D8%AF%D9%81%D8%AA%D8%B1-%D9%85%D9%82%D8%B1-%D8%B1%D8%A7%D8%AA-%D9%85%D9%84-%DB%8C-140531390001131406) |
| AR-SRC-011 | دادنامه ۱۴۰۵۳۱۳۹۰۰۰۰۲۳۷۵۰۳، ۱۴۰۵/۰۲/۰۸ | ANNULLED | COURT_PRIMARY (official PDF pending) | فقط بندهای ب و ج ماده ۴ و تبصره دو مصوبه ۱۶۳۸۲/ش و ۱۷۳۲۹/ش؛ نه کل ماده/تعرفه. | [متن رأی](https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D8%A8%D9%86%D8%AF%D9%87%D8%A7%DB%8C-%D8%A8-%D9%88-%D8%AC-%D9%85%D8%A7%D8%AF%D9%87-%DB%B4-%D9%88-%D8%AA%D8%A8%D8%B5%D8%B1%D9%87-%D8%B0%DB%8C%D9%84-%D8%A2%D9%86-%D8%A7%D8%B2-%D9%85%D8%B5%D9%88%D8%A8%D8%A7%D8%AA-%D8%B4%D9%85%D8%A7%D8%B1%D9%87-%DB%B1%DB%B4%DB%B0%DB%B1-%DB%B1%DB%B6%DB%B3۸۲-%D8%B4-140531390000237503) |
| AR-SRC-012 | دادنامه ۱۴۰۵۳۱۳۹۰۰۰۰۵۴۷۱۳۶، ۱۴۰۵/۰۳/۰۵ | ANNULLED | COURT_PRIMARY (official PDF pending) | فقط بندهای ب و ج ماده ۴ و تبصره ذیل مصوبه ۱۷۳۲۹/ش درباره باغات مشمول دستورالعمل ماده ۱۴ قانون زمین شهری. | [متن رأی](https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D8%A8%D9%86%D8%AF%D9%87%D8%A7%DB%8C-%D8%A8-%D9%88-%D8%AC-%D9%85%D8%A7%D8%AF%D9%87-%DB%B4-%D9%88-%D8%AA%D8%A8%D8%B5%D8%B1%D9%87-%D8%B0%DB%8C%D9%84-%D8%A2%D9%86-%D8%A7%D8%B2-%D9%85%D8%B5%D9%88%D8%A8%D9%87-%D8%B4%D9%85%D8%A7%D8%B1%D9%87-%DB%B1%DB%B7%DB%B3%DB%B2%DB%B9-%DB%B1%DB%B4%DB%B0۱-%D8%B4-140531390000547136) |
| AR-SRC-013 | دادنامه ۱۴۰۵۳۱۳۹۰۰۰۰۸۷۹۳۹۲، ۱۴۰۵/۰۴/۰۹ | ANNULLED | COURT_PRIMARY (official PDF pending) | کل مصوبه دو مرحله‌ای کردن پروانه از تاریخ تصویب ابطال شد؛ شماره ۱۵۹۳۸/۱۵۳۹۸ و تاریخ ۰۲/۰۴ آبان ۱۴۰۱ در متن بازنشرشده ناسازگار است. | [متن رأی](https://hoghogh.ai/case-law/%D8%A7%D8%A8%D8%B7%D8%A7%D9%84-%D9%85%D8%B5%D9%88%D8%A8%D9%87-%D8%AC%D9%84%D8%B3%D9%87-%DB%B9%DB%B9-%D9%85%D9%88%D8%B1%D8%AE-%DB%B1%DB%B4%DB%B0%DB%B1-%DB%B1%DB%B1-%DB%B2-%D8%AF%D9%88%D8%B1%D9%87-%D8%B4%D8%B4%D9%85-%D8%B4%D9%88%D8%B1%D8%A7%DB%8C-%D8%A7%D8%B3%D9%84%D8%A7%D9%85%DB%8C-%D8%B4%D9%87%D8%B1-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-140531390000879392) |
| AR-SRC-014 | دادنامه وحدت رویه ۱۴۰۵۳۱۳۹۰۰۰۰۴۷۱۷۹۴، ۱۴۰۵/۰۲/۲۹ | EFFECTIVE | COURT_PRIMARY (official PDF pending) | دیوان عدالت اداری مرجع رسیدگی به آرای شوراهای انتظامی سازمان نظام مهندسی شناخته نشد؛ دامنه به آرای انتظامی محدود است. | [متن رأی](https://hoghogh.ai/case-law/%D8%A7%D8%B9%D9%84%D8%A7%D9%85-%D8%AA%D8%B9%D8%A7%D8%B1%D8%B6-%D8%AF%D8%B1-%D8%A2%D8%B1%D8%A7%DB%8C-%D8%B4%D8%B9%D8%A8-%D8%AF%DB%8C%D9%88%D8%A7%D9%86-%D8%B9%D8%AF%D8%A7%D9%84%D8%AA-%D8%A7%D8%AF%D8%A7%D8%B1%DB%8C-%D8%AF%D8%B1-%D8%B1%D8%A7%D8%A8%D8%B7%D9%87-%D8%A8%D8%A7-%D8%B5%D9%84%D8%A7%D8%AD%DB%8C%D8%AA-%DB%8C%D8%A7-%D8%B9%D8%AF%D9%85-140531390000471794) |
| AR-SRC-015 | نظریه ۷/۱۴۰۵/۵۵، ۱۴۰۵/۰۴/۲۴ | UNKNOWN | OFFICIAL_SECONDARY | حریم شهر در قانون حفظ کاربری با خارج از حریم مصوب شهر در ماده ۹۹ یکی نیست؛ اراضی زراعی/باغی در حریم نیازمند مجوز جهاد؛ احراز محدوده/حریم از وزارت کشور و زیرمجموعه‌ها. | [متن نظریه](https://hoghogh.ai/advisory-opinions/a-5f8d51ae) |
| AR-SRC-016 | نظریه ۷/۱۴۰۴/۷۲۲، ۱۴۰۵/۰۳/۲۷ | UNKNOWN | OFFICIAL_SECONDARY | تفکیک اجرای ماده ۹۹ از ماده ۱۰۰؛ عدم تبدیل جریمه ماده ۹۹ به تخریب و عدم وصول از طریق دعوای حقوقی. | [متن نظریه](https://lawlex.ir/opinions/opinion-7-1404-722) |
| AR-SRC-017 | نظریه ۷/۱۴۰۵/۲۳۱، ۱۴۰۵/۰۶/۱۵ | UNKNOWN | OFFICIAL_SECONDARY | کمیسیون ماده ۱۰۰ فقط تخلف ساختمانی را رسیدگی می‌کند، نه اصل تفکیک اراضی؛ ماده ۱۰۱ و مراجع مربوط جدا هستند. | [متن نظریه](https://hoghogh.ai/advisory-opinions/a-ebab6334) |
| AR-SRC-018 | نظریه ۷/۱۴۰۵/۲۶۱، ۱۴۰۵/۰۶/۲۲ | UNKNOWN | OFFICIAL_SECONDARY | اجرای رأی تخریب در حدود منطوق؛ عدم توسعه تخریب به بخش‌های فاقد تخلف؛ دشواری اجرا به‌تنهایی مجوز عدم اجرا نیست. | [متن نظریه](https://hoghogh.ai/advisory-opinions/a-cd5ad656) |
| AR-SRC-019 | نظریه ۷/۱۴۰۴/۷۲۷، ۱۴۰۵/۰۴/۱۰ | UNKNOWN | OFFICIAL_SECONDARY | در تخلفات متعدد، پرداخت جریمه بعضی موارد مانع درخواست تخریب برای موارد پرداخت‌نشده نیست. | [متن نظریه](https://lawlex.ir/opinions/opinion-7-1404-727) |
| AR-SRC-020 | نظریه ۷/۱۴۰۴/۸۱۷، ۱۴۰۵/۰۳/۳۱ | UNKNOWN | OFFICIAL_SECONDARY | پس از قطعیت و پرداخت جریمه کسری پارکینگ، تأمین بعدی پارکینگ به‌تنهایی حق استرداد ایجاد نمی‌کند. | [متن نظریه](https://lawlex.ir/opinions/opinion-7-1404-817) |
| AR-SRC-021 | مبحث ۲۴، ویرایش اول ۱۴۰۴ | NOTIFIED (effective date calculated) | OFFICIAL_SECONDARY | نامه ۱۴۰۴۶۱/۱۰۰/۲ مورخ ۱۴۰۴/۰۷/۲۷؛ شش ماه پس از ابلاغ به‌صورت محاسباتی ۱۴۰۵/۰۱/۲۷؛ نسخه رسمی وزارتخانه و SHA-256 دریافت نشد. | [PDF بازنشرشده](https://qsce.ir/uploads/%D9%85%D8%A8%D8%AD%D8%AB%20%D8%A8%DB%8C%D8%B3%D8%AA%20%D9%88%20%DA%86%D9%87%D8%A7%D8%B1%D9%85%20%D9%85%D9%82%D8%B1%D8%B1%D8%A7%D8%AA%20%D9%85%D9%84%DB%8C.pdf) |
| AR-SRC-022 | خبر ارتفاع طبقات مسکونی تا ۳۵۰ سانتی‌متر، ۱۴۰۵/۰۸/۱۷ | ANNOUNCED | PRESS_LEAD | اصل مصوبه ماده ۵، تعریف ارتفاع، دامنه و تاریخ اجرا دریافت نشده؛ هیچ قاعده طراحی فعال نمی‌شود. | [گزارش رسانه‌ای](https://s4.soumashop.ir/news/7004179/%D8%A7%D8%B1%D8%AA%D9%81%D8%A7%D8%B9-%D8%B7%D8%A8%D9%82%D8%A7%D8%AA-%D9%85%D8%B3%DA%A9%D9%88%D9%86%DB%8C-%D8%AF%D8%B1-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%A8%D9%87-%DB%B3-%DB%B5-%D9%85%D8%AA%D8%B1-%D8%A7%D9%81%D8%B2%D8%A7%DB%8C%D8%B4-%DB%8C%D8%A7%D9%81%D8%AA) |
| AR-SRC-023 | گزارش جلسه شانزدهم شورای عالی شهرسازی درباره مرحله نخست طرح جامع شیراز، ۱۴۰۵/۰۸/۲۶ | APPROVED (stage-one framework only) | OFFICIAL_SECONDARY | راهبردهای کلان و شروع تهیه طرح تفصیلی گزارش شده؛ مصوبه امضاشده، نقشه‌ها و ضوابط پلاک هنوز دریافت نشده‌اند. | [گزارش بازنشرشده از پایگاه خبری وزارت راه](https://funfarsi.ir/%D8%AA%D9%88%D8%B3%D8%B9%D9%87-%D8%B4%D9%87%D8%B1%DB%8C-%D8%B4%DB%8C%D8%B1%D8%A7%D8%B2-%D8%A8%D8%A7-%D8%B1%D9%88%DB%8C%DA%A9%D8%B1%D8%AF-%D8%AD%D9%81%D8%B8-%D9%85%DB%8C%D8%B1%D8%A7%D8%AB-%D9%88-%D8%AA/) |

### Interpretation controls
- The 2026-11-24 watch found no new official primary binary or signed original in the searched municipal, provincial, fire, heritage, utility, national-regulation, court, or council portals. This is a retrieval limitation, not proof that no new instrument exists.
- Do not treat the 350 cm report as an effective design rule until the Commission Article 5 resolution, notification, definitions, applicability maps and date of effect are obtained.
- Do not use the stage-one master-plan report as parcel zoning; detailed plan and official maps remain required.
- Do not generalize the three Shiraz judgments beyond the exact clauses and instruments they annul.
- No new rule was added to the executable rule list; no PASS rule was activated.

### Next acquisition actions
1. Request certified minutes, resolution number, amendment text, notification letter and map attachments from the Article 5 Fars Secretariat for the 350 cm amendment.
2. Request the signed 16th Supreme Council resolution and spatial-structure maps for the stage-one Shiraz master plan; separately obtain the later detailed-plan initiation letter.
3. Request the original Council resolution 15938/15398 and the current municipal permit workflow after judgment 879392.
4. Request official court/Gazette copies for judgments 237503, 547136, 879392, 1131406, 471794, 547350 and 1829587.
5. Retrieve the consolidated Article 100 text from the Majlis/Gazette and the official M24 binary from the Ministry/INBR; compute SHA-256 only after successful download.
6. Obtain the integrated historic-fabric protection/development regulations and all maps from the National Archives of the South and the Fars Cultural Heritage Directorate.
