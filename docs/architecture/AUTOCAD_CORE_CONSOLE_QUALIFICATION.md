# AutoCAD Core Console — Qualification Plan

## Decision

Prioritize AutoCAD Core Console as the first local conversion provider to qualify on workstations that already have a supported, licensed full AutoCAD installation. Do not bundle Autodesk binaries, download them automatically, assume DWG TrueView is equivalent, or treat executable discovery as conversion success.

## Evidence reviewed

- Autodesk describes Core Console as the command-line/script execution route for AutoCAD and documents its use for automation.
- Autodesk script documentation warns that script files are prompt sequences: each line/blank is significant and command prompts can change between releases.
- Autodesk SAVEAS documentation states that FILEDIA=0 exposes command prompts; DXF save then asks for decimal precision, binary/ASCII, object selection, preview, and version.
- The MIT-licensed acadbp project demonstrates batch DWG/DXF conversion via accoreconsole and lists AutoCAD/AutoCAD LT 2013+ as a requirement.
- A community report documents a practical distinction between AutoCAD's Core Console and the similarly named TrueView executable; TrueView behavior is not accepted as equivalent evidence.

## Why this route is attractive

- Reuses the office's installed AutoCAD engine, potentially avoiding an additional per-seat DWG SDK cost.
- Local/offline execution; source drawings need not leave the workstation.
- Uses Autodesk's own DWG implementation for files opened/saved by that AutoCAD version.
- Can serve as an optional local provider while ODA remains a separately licensed fallback for machines without AutoCAD.

## Risks and unresolved questions

- Core Console command/script behavior must be qualified by product and release. Do not assume a script validated on AutoCAD 2026 works on AutoCAD 2020 or older.
- The exact SAVEAS DXF prompt sequence and output-version tokens need a real console run. Do not ship a guessed prompt script.
- AutoCAD licensing and permitted unattended/headless use must follow Autodesk product terms; Core Console is not a way to bypass licensing.
- Third-party vertical products may need product-specific startup modules or flags.
- Core Console may emit warnings or report nonzero status despite creating an output, or exit zero with an incomplete output; both process and artifact checks are required.
- DWG TrueView is not a qualified substitute until a supported, repeatable command workflow is demonstrated and licensing is checked.

## Proposed adapter contract

Provider name: autocad_core_console

Inputs: staged source DWG, destination DXF path, requested DXF release, explicit language/product profile, timeout.

Safety requirements:
- Resolve accoreconsole.exe only from an explicitly selected AutoCAD installation or a deterministic, version-aware discovery list.
- Never invoke through a shell; pass arguments as an argv array.
- Copy exactly one source into a private temporary directory and hash the original and staged bytes.
- Generate a temporary script only from validated paths/options; quote paths and reject newline/control characters in paths.
- Run with a bounded timeout and terminate the process tree on timeout.
- Never overwrite an existing output; only copy an exact, non-empty expected DXF from the private output path.
- Verify source hash after the process and hash the output.
- Record executable path/version, command arguments (redacting sensitive paths where required), exit code, stdout/stderr, elapsed time, source/output hashes, and requested format in a conversion manifest.
- Set execution status separately from fidelity status; fidelity remains UNKNOWN/NEEDS_REVIEW until independent validation succeeds.

## Golden qualification matrix

| Case | Required evidence |
|---|---|
| AutoCAD 2020 full installation | Executable path/version and deterministic successful run |
| Older AutoCAD release, if supported | Separate exact-version run; no inferred compatibility |
| DWG input | Both bagheri7.dwg and afifiiiii.end.edit3.dwg |
| DXF version | Explicit target version recorded in manifest |
| Source integrity | SHA-256 unchanged; no writes to original path |
| DXF parse | Independent ezdxf read + audit result |
| Structure | Entity types/counts, layers, blocks, attributes, dimensions, layouts, xrefs, proxies |
| Text | Persian MTEXT/TEXT, Unicode/codepage, styles, SHX/TTF dependencies |
| Geometry | Coordinates, extents, lengths, areas, orientation and tolerance report |
| Units | INSUNITS, unit scale, inch/mm conversion and insertion scale |
| Visual | Independent CAD render/print comparison; not a substitute for structure checks |
| Failure modes | Missing executable, timeout, invalid script, no output, empty output, multiple outputs, output collision, source mutation |

## Release gate

Do not mark the provider available for conversion until every mandatory case for the declared AutoCAD version passes. Do not claim lossless conversion if unsupported objects, proxy entities, external references, font dependencies, or any semantic differences remain unexplained. A successful process is execution PASS only; fidelity requires its own evidence.

## Current status

- Research and architecture decision: COMPLETE.
- Provider implementation: NOT_STARTED.
- Script prompt sequence: NOT_VERIFIED.
- AutoCAD 2020 execution: NOT_RUN.
- Golden DWG Core Console tests: NOT_RUN.
- Older AutoCAD compatibility: NOT_RUN.
- User's Windows replacement and CAD reinstall: WAITING_FOR_USER.
- Commercial production authorization: MUST_FOLLOW_AUTODESK_LICENSE_TERMS.

## Sources

- https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-use-the-AutoCAD-Core-Console.html
- https://www.autodesk.com/blogs/autocad/core-console-autocad-tuesday-tips-frank/
- https://help.autodesk.com/view/ACD/2026/ENU/?caas=caas%2Fdocumentation%2FACD%2F2014%2FENU%2Ffiles%2FGUID-95BB6824-0700-4019-9672-E6B502659E9E-htm.html
- https://help.autodesk.com/cloudhelp/2025/ENG/AutoCAD-Core/files/GUID-E2CEA3F2-43CA-41D0-A2C6-BACF2229715A.htm
- https://github.com/k-awata/acadbp
- https://github.com/mozman/ezdxf/discussions/724
