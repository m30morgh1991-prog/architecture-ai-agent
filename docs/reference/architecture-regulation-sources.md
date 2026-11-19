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
