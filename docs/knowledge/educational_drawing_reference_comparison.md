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
