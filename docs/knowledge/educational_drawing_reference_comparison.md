# Educational Drawing-Reading Reference Comparison

## Purpose

Compare the user-provided 1396 reference with newer candidate references found through web research, and decide which sources should be prioritized for the Architecture AI Agent plan-understanding core.

## Evidence boundary

This comparison distinguishes:
- **STUDIED**: the source PDF was actually provided and examined.
- **CATALOG-VERIFIED**: bibliographic identity, publication year, publisher, authors and subject classification were verified from available catalog/search evidence.
- **NOT YET STUDIED**: no full legal copy/content was available for direct chapter-by-chapter extraction.

No candidate book is treated as authoritative regulation merely because it is newer.

## 1. Primary reference — user-provided 1396 book

**Title:** اصول نقشه‌کشی و نقشه‌خوانی ساختمان 1 (سازه و معماری)  
**Author:** نوید سلیمانیپور  
**Year:** 1396  
**Publisher:** as recorded in the supplied source  
**ISBN:** 978-600-04-8122-3  
**Status:** STUDIED

### Value to the project

This is currently the strongest directly studied educational source for:
- architectural drawing language;
- plan/section relationships;
- conventional symbols;
- dimensions and annotations;
- level/elevation evidence;
- stairs and ramps;
- structural drawing vocabulary.

The extracted knowledge is already registered in:
- `docs/knowledge/uas1_plan_drawing_reading_reference.md`
- `docs/knowledge/architecture_understanding_core_layers.md`

## 2. Same-series newer edition — 1402

**Title:** اصول نقشه‌خوانی ساختمان (۱) (سازه و معماری) بر مبنای آخرین ویرایش آیین‌نامه‌ها و مقررات ملی ساختمان  
**Authors:** نوید سلیمانی‌پور، محمدهادی بهمن‌آبادی  
**Publisher:** نوید عمران  
**Year:** 1402  
**Status:** CATALOG-VERIFIED / NOT YET STUDIED

### Decision

**Priority: P0**

This is the first candidate to obtain legally and study in full because it is the closest newer edition of the same reference family. The project should not assume that every rule or drawing convention changed between 1396 and 1402 until the two editions are directly compared.

### Required comparison

When a legal copy becomes available, compare:
1. table of contents;
2. drawing symbols and conventions;
3. plan/section interpretation;
4. level/elevation notation;
5. stair and ramp treatment;
6. structural plan language;
7. references to current national regulations;
8. changed terminology or revised examples.

Only then promote a difference to a project rule.

## 3. Same-series Volume 2 — 1402

**Title:** اصول نقشه‌خوانی ساختمان (۲): تأسیسات مکانیکی و برقی  
**Authors:** نوید سلیمانی‌پور، شیوا قاسمیان‌لنگرودی  
**Publisher:** نوید عمران  
**Year:** 1402  
**Status:** CATALOG-VERIFIED / NOT YET STUDIED

### Decision

**Priority: P1**

This is highly relevant to the project's future cross-discipline understanding because it directly targets mechanical/electrical drawing interpretation.

It should feed the future chain:

Architectural Plan ↔ Structural Plan ↔ MEP Plan

but must not be treated as studied content until a legal full source is obtained.

## 4. نقشه‌خوانی در معماری — 1403

**Author:** لاله دهقان‌طرزجانی  
**Publisher:** رهاد  
**Year:** 1403  
**Subject classification:** architectural detailed drawings / architectural drawing and drafting  
**Status:** CATALOG-VERIFIED / NOT YET STUDIED

### Decision

**Priority: P1**

This is a strong candidate for the architectural-language lane because it is newer than the supplied source and specifically classified around architectural drawings.

However, the current evidence only verifies bibliographic identity and subject classification. No chapter-level claims should be imported into the semantic core until the book itself is legally studied.

## 5. نقشه‌خوانی و نقشه‌کشی معماری و سازه ساختمان‌ها — 1402

**Authors:** مجید شجاعی‌اردکانی، زهرا امانی  
**Publisher:** دانش بنیاد  
**Year:** 1402  
**Status:** CATALOG-VERIFIED / NOT YET STUDIED

### Decision

**Priority: P2**

Potentially useful because it explicitly spans both architecture and structure. It is a good candidate for cross-discipline vocabulary and drawing coordination, but it is lower priority than the newer same-series Volume 1 and Volume 2.

## 6. طراحی، ضوابط و نقشه‌خوانی — candidate

**Author:** امیرحسین جعفرپناه  
**Known edition evidence:** at least multiple printings; one catalog record verifies چاپ 3, 1400, 460 pages, ISBN 978-622-6293-81-5.  
**Status:** CATALOG-VERIFIED / NOT YET STUDIED

### Decision

**Priority: P2**

Useful as a possible design/rules/plan-reading cross-reference. Current evidence is not sufficient to treat it as a 1402 edition or to infer its latest content. The project must record the exact edition before using it as a source.

## Priority matrix

| Source | Year | Scope | Current evidence | Project priority |
|---|---:|---|---|---|
| User-provided اصول نقشه‌کشی و نقشه‌خوانی ساختمان 1 | 1396 | Architecture + structure | Full source studied | **P0 / active** |
| Same-series اصول نقشه‌خوانی ساختمان 1 | 1402 | Architecture + structure | Catalog verified | **P0 / obtain & study** |
| Same-series اصول نقشه‌خوانی ساختمان 2 | 1402 | MEP | Catalog verified | **P1** |
| نقشه‌خوانی در معماری | 1403 | Architecture | Catalog verified | **P1** |
| نقشه‌خوانی و نقشه‌کشی معماری و سازه ساختمان‌ها | 1402 | Architecture + structure | Catalog verified | **P2** |
| طراحی، ضوابط و نقشه‌خوانی | 1400+ printings | Design + rules + plan reading | Edition evidence partial | **P2** |

## What changes in the Architecture AI Agent now

### Keep

The 1396 source remains an active educational reference. It is not replaced.

### Add as a research target

The 1402 same-series Volume 1 becomes the **first acquisition target** for a legal copy.

### Expand the knowledge architecture

The reference hierarchy should become:

1. **Authoritative regulations / standards / approved project documents**
2. **Verified technical standards**
3. **Educational references**
4. **Observed drawing evidence**
5. **Model inference**

Educational references can explain or generate semantic candidates, but they cannot override higher-authority sources or observed evidence.

### New research lanes

- **Educational Reference Delta:** 1396 ↔ 1402 same-series Volume 1
- **MEP Drawing Language:** Volume 2
- **Architecture Drawing Language:** 1403 architecture-specific reference
- **Architecture ↔ Structure Coordination:** 1402 architecture/structure reference

## Fail-closed requirement

Until the newer books are actually studied:
- their bibliographic existence may be recorded as PASS;
- their content must remain SOURCE_REQUIRED / NOT_YET_STUDIED;
- no new semantic rule may be claimed as derived from them;
- conflicts must remain NEEDS_REVIEW or BLOCKED;
- no educational source may silently override regulations.

## Research conclusion

The most valuable next step is **not collecting many books blindly**. It is obtaining and studying the 1402 same-series Volume 1 first, then using the 1403 architecture-specific book and the 1402 MEP volume to fill identified gaps.

This keeps the knowledge base traceable and prevents source proliferation without measurable benefit to the Plan Understanding Core.


## 7. Jorjani vocational drafting references — new research findings

**Primary lead:** نقشه‌کشی عمومی ساختمان مهارت فنی درجه ۲, عبیدالله جرجانی, دانش و فن, catalogued year 1400, 816 pages. The catalog listing is currently marked out of stock. The listed topic groups include line types and geometric constructions, orthographic views/sections, drawing symbols, building plans, stairs, axes/grids, foundation plans, sections/dimensioning, elevations/schedules, roof slope plans, and site/location plans. Source: https://fekrenobook.ir/architecture/drafting/drafting-general-building-skill-technical-degree-2/

A historical vocational teaching reference lists these related Jorjani titles:
- نقشه‌کشی ساختمان مهارت فنی درجه ۱ — اسکلت فلزی / اسکلت بتنی
- نقشه‌کشی ساختمان مهارت فنی درجه ۱ — اتوکد
- نقشه‌کشی عمومی ساختمان مهارت فنی درجه ۲ — جلد اول و جلد دوم

Source: https://g-naghshekeshi.blogfa.com/post/124

A separate catalog record identifies a related AutoCAD volume titled نقشه‌کشی معماری درجه ۱ جلد ۳ (اتوکد ۲ بعدی و ۳ بعدی), publisher دانش و فن, ISBN 9789642945146. The exact title/edition relationship to the historical course title is not confirmed. Source: https://oxinbook.com/book/%D9%86%D9%82%D8%B4%D9%87-%DA%A9%D8%B4%DB%8C-%D9%85%D8%B9%D9%85%D8%A7%D8%B1%DB%8C-%D8%AF%D8%B1%D8%AC%D9%871%D8%AC%D9%84%D8%AF3%28%D8%A7%D8%AA%D9%88%DA%A9%D8%AF2%D8%A8%D8%B9%D8%AF%DB%8C-%D9%883%D8%A8%D8%B9%D8%AF%DB%8C%29%D8%B9%D8%A8%DB%8C%D8%AF%D8%A7%D9%84%D9%84%D9%87-%D8%AC%D8%B1%D8%AC%D8%A7%D9%86%DB%8C

A historical bibliography also attributes a title about mechanical/electrical building-services drawings to Jorjani, Tehran, 1386, but the exact edition and full contents remain unverified. Source: https://mohandesi-omran.blogfa.com/post/480

### Decision

- **P0:** locate/obtain and study the 1400 catalogue-listed Grade 2 book first; its listed scope most directly supports foundational drawing-grammar and evaluation fixtures.
- **P1:** verify the Grade 1 steel/concrete title and the mechanical/electrical services title for cross-discipline drawing interpretation.
- **P2:** verify the AutoCAD volume identity/edition; it is contextual for future CAD output but does not change the MVP's current no-DWG-editing boundary.

A dedicated record is maintained in `docs/knowledge/jorjani_drafting_reference_candidates.md`. All Jorjani sources remain CATALOG-VERIFIED or BIBLIOGRAPHIC LEAD / NOT YET STUDIED; no chapter-level rule is promoted without studying the actual text.


## 8. Targeted web search checkpoint — 2026-10-09

Searches were run using the exact 1402 title, both authors, publisher, PDF/download terms, and ISBN associated with the 1396 edition. The results reconfirmed catalog listings for the 1402 book, but **no full PDF could be verified as the exact 1402 edition**. A digital-download listing for a 51-page item under a similar title was found, but it does not establish that the item is the full 1402 edition and must not be mislabeled as such. Relevant leads: https://elmnet.ir/keyword/%D8%B3%D8%A7%D8%AE%D8%AA%D9%85%D8%A7%D9%86-%D8%B3%D8%A7%D8%B2%DB%8C-%D9%86%D9%82%D8%B4%D9%87-%D9%87%D8%A7%DB%8C-%D8%AA%D9%81%D8%B5%DB%8C%D9%84%DB%8C and https://sarzaminpdf.net/product/principles-of-architecture/.

**Status remains:** 1402 Volume 1 = CATALOG-VERIFIED / SOURCE_REQUIRED / NOT YET STUDIED. Do not claim the 1402 PDF has been found unless title, authors, year/edition, volume, and completeness can be checked against the actual file.
