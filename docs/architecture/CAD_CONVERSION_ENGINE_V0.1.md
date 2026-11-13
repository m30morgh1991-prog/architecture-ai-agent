# CAD Conversion Engine v0.1 — Architecture and Safety Contract

## Purpose

Provide optional, replaceable local DWG/DXF conversion adapters. This is an orchestration layer around an installed CAD codec, not a newly reverse-engineered DWG codec and not a source of architectural truth.

## Engine selection policy

1. **AutoCAD Core Console is the preferred evaluation route when a supported, licensed full AutoCAD installation is already present on the workstation.** It uses the AutoCAD engine installed by the office and avoids bundling or separately licensing another DWG codec. It must be treated as a local capability, not a mandatory dependency.
2. **ODA SDK is the candidate independent commercial codec** for deployments without AutoCAD, but only after obtaining a suitable commercial license and validating the distribution model and total cost.
3. **ODA File Converter is evaluation-only for a non-member** and must not be used for commercial architecture-office workflows or shipped in a commercial product without written authorization or an appropriate commercial license.
4. **ACadSharp (MIT) is a research/read-path candidate**, not an approved lossless writer. Its DWG/DXF read/write claims require our own Golden corpus qualification.
5. **LibreDWG/libdxfrw are isolated research candidates** because their GPL licensing and current format/entity coverage require legal and technical qualification before any commercial integration.
6. ezdxf is an independent DXF parser/validator, not a DWG converter.

AutoCAD Core Console was introduced with AutoCAD 2013 and accepts an input drawing and script through /i and /s. Autodesk documents using it for command-line/script automation. A third-party MIT batch utility (acadbp) demonstrates bulk DWG/DXF conversion with Core Console and lists AutoCAD/AutoCAD LT 2013 or later as requirements. However, command availability and behavior must be verified for each supported AutoCAD product/version. A community report indicates that the similarly named executable bundled with DWG TrueView may not offer the same script-command behavior as a licensed AutoCAD installation; therefore DWG TrueView is NOT assumed to qualify.

Sources:
- Autodesk Core Console overview: https://www.autodesk.com/support/technical/article/caas/sfdcarticles/sfdcarticles/How-to-use-the-AutoCAD-Core-Console.html
- Autodesk Core Console article: https://www.autodesk.com/blogs/autocad/core-console-autocad-tuesday-tips-frank/
- Autodesk command scripts: https://help.autodesk.com/view/ACD/2026/ENU/?caas=caas%2Fdocumentation%2FACD%2F2014%2FENU%2Ffiles%2FGUID-95BB6824-0700-4019-9672-E6B502659E9E-htm.html
- Autodesk SAVEAS prompts: https://help.autodesk.com/cloudhelp/2025/ENG/AutoCAD-Core/files/GUID-E2CEA3F2-43CA-41D0-A2C6-BACF2229715A.htm
- MIT batch utility: https://github.com/k-awata/acadbp
- Independent community note on TrueView/Core Console differences: https://github.com/mozman/ezdxf/discussions/724

## Current implementation

- The Python ODA adapter invokes an installed external ODA File Converter executable.
- Exactly one source DWG is copied into a private temporary input directory; the original directory is never passed to the converter.
- Recursive processing is disabled and a single-file filter is supplied.
- The process has a bounded timeout and is invoked without a shell.
- Existing outputs are never overwritten.
- Source SHA-256 is checked before and after conversion, and the staged input hash must match the original snapshot.
- Non-zero exit, missing/empty/ambiguous output, timeout, missing executable, or source mutation is rejected.
- The initial adapter supports DWG → DXF only. DXF → DWG is deferred until an independent DWG reopen/verification path is available.
- AutoCAD Core Console has been researched but is NOT YET IMPLEMENTED or enabled as a conversion provider. A script-based SAVEAS sequence must not be assumed correct until tested against actual AutoCAD Core Console installations.

## Core Console implementation gate

Before implementing or enabling the provider, qualify the following on a Windows workstation with the user's permission and an installed, licensed AutoCAD version:

1. Resolve the exact accoreconsole.exe belonging to the selected AutoCAD product/version; do not infer that DWG TrueView is equivalent.
2. Record executable/product version, language, command output, exit code, timeout behavior, and generated artifacts.
3. Confirm a deterministic, noninteractive DWG → DXF script sequence and output version on AutoCAD 2020; then qualify any older version explicitly.
4. Verify whether the script changes or saves the source DWG. The original must remain immutable; use a private staged copy.
5. Run on both Golden DWGs and independently parse DXF with ezdxf.
6. Compare entity type/count, handles where meaningful, layers, blocks/attributes, dimensions, MTEXT/Unicode Persian text, styles/fonts, coordinates, units/INSUNITS, layouts/viewports, Xrefs, proxy/opaque data, and extents.
7. Test DXF → DWG only after the reverse route can be reopened independently and passes the same fidelity gate.
8. Keep all real Windows/Core Console/ODA tests marked NOT_RUN until the user confirms Windows replacement and software reinstallation.

Until these steps pass, Core Console is a preferred candidate, not a validated engine. No provider may promote conversion fidelity to PASS from process exit or file existence alone.

## Evidence boundary

execution_status=COMPLETED means only that the external converter returned success and produced a non-empty file while the source remained unchanged.

fidelity_status=UNKNOWN and requires_review=true are mandatory until independent validation passes. No adapter currently claims preservation of entity inventories, layers, blocks, xrefs, proxy objects, dimensions, text/font encodings, layouts, coordinate systems, units, or plot scale. Independent DXF parsing, semantic comparison, and where appropriate human review are required before use.

A converted DXF must not silently replace the original DWG. The original remains immutable and the converted file is a derived artifact with provenance.

## ODA license boundary

ODA states that ODA Viewer and ODA File Converter are example/community applications; non-members may use them for non-commercial applications only. The Community User Agreement likewise limits Community Applications and restricts commercial redistribution/use. Therefore this adapter is evaluation-only for a non-member and MUST NOT be enabled for commercial architecture-office workflows or shipped in a commercial product unless ODA provides separate written authorization or the deployment obtains an appropriate commercial license. This adapter does not grant redistribution rights.

Official sources:
- https://www.opendesign.com/faq/question/what-are-oda-viewer-and-oda-file-converter
- https://www.opendesign.com/files/2025-09/ODA%20Community%20User%20Agreement%2009-2025.pdf
- https://www.opendesign.com/pricing

## Deferred work

1. Implement Core Console discovery and a version-qualified adapter after the user's Windows environment is ready.
2. Independent DXF parse/audit and entity/layer/block/text/units/coordinates comparison.
3. Adapter for another legally compatible local codec, if required.
4. DXF → DWG only after independent reopen and fidelity evidence can be collected.
5. Real Windows installation and execution tests after the user's Windows replacement and CAD software setup.

## Explicit non-goals

- No DWG write-back to the source.
- No automatic repair/audit by default.
- No semantic promotion into PlanModel or ConstraintMap.
- No compliance verdict or visual equivalence claim.
- No mandatory cloud dependency.
