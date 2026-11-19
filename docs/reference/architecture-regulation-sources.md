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
