# Isolated acadrust DWG → DXF comparison pilot

This is an experiment, not a production converter and not a production dependency.

## Implementations compared

- **Stable release baseline:** crates.io `acadrust = 0.6.8`, MPL-2.0.
- **Current upstream source snapshot:** exact Git revision `52034a673ff59bf6936ebf01ec794b07a97df246`, also declares MPL-2.0. This is 581 commits ahead of the `v0.6.8` release tag even though the package version string remains 0.6.8.
- Both implementations are optional Cargo features and are tested separately. `default-features = false` disables acadrust's optional Rayon parallelism for a lower-concurrency baseline.
- The exact git revision is pinned; the workflow generates Cargo.lock and uploads it with the evidence artifact.

## Safety and method

- The probe writes directly from the parsed `CadDocument` to a temporary DXF file through `DxfWriter::write_to_file`; it does not build a full intermediate DXF byte/string buffer.
- DWG reads are strict (failsafe/recovery disabled) and capped at 512 MiB decompressed bytes, 1,000,000 mesh faces and 4,000,000 mesh face indices.
- Input is SHA-256 hashed before and after; the original file is never opened for writing.
- The output is always named and treated as a `.candidate.dxf`, independently reopened by acadrust, and independently inspected by ezdxf in CI.
- Existing candidate/report paths are never overwritten. Atomic create-if-absent hard-link publication prevents replacement in a race window.
- Reports include candidate byte size, candidate SHA-256, elapsed time and Linux peak RSS when available.
- The report never declares fidelity PASS. Even if structural counts match, the decision remains NEEDS_REVIEW pending deeper entity/property comparison and CAD-host verification.

## Run both implementations

From the repository root:

```sh
cargo generate-lockfile --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml

cargo test --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml --locked --no-default-features --features release
cargo test --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml --locked --no-default-features --features upstream-main

cargo run --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml --locked --no-default-features --features release -- \
  test-assets/golden-projects/bagheri7.dwg /tmp/bagheri7.release.candidate.dxf /tmp/bagheri7.release.report.json
python tools/acadrust_dwg2dxf_pilot/verify_ezdxf.py /tmp/bagheri7.release.candidate.dxf /tmp/bagheri7.release.report.json

cargo run --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml --locked --no-default-features --features upstream-main -- \
  test-assets/golden-projects/bagheri7.dwg /tmp/bagheri7.upstream.candidate.dxf /tmp/bagheri7.upstream.report.json
python tools/acadrust_dwg2dxf_pilot/verify_ezdxf.py /tmp/bagheri7.upstream.candidate.dxf /tmp/bagheri7.upstream.report.json
```

The output and report paths must not already exist. The converter creates a same-directory temporary file and atomically publishes a review-only candidate only after the DXF can be reopened by acadrust. A candidate is not a final deliverable.

## Evidence limits

The initial gate compares source/output entity and modelspace counts, table counts, drawing version, unit variables, parser diagnostics and architecture omissions. The independent ezdxf check validates that a second parser can reopen the DXF and compares core inventories. This is intentionally conservative but is not a complete fidelity proof. XData, proxy graphics, nested block semantics, dimension rendering, paper-space layout fidelity, OCS/WCS, fonts and AutoCAD/ODA interoperability still require deeper tests.

Windows/AutoCAD host tests remain NOT_RUN until the user confirms the Windows environment is ready.


## Targeted POLYLINE spline-fit regression

The pilot records every 2D POLYLINE smooth-surface value (DXF group code 75), including the default zero, from the source `CadDocument` across Model Space, layouts and block definitions. It then checks the same handles, owner handles and values after an independent `ezdxf` reopen. A second comparison checks source-side and independently reopened output values between the pinned release and upstream implementations. This helps distinguish DWG reader decoding differences from DXF writer serialization loss. Any missing handle, unapproved entity-type conversion, group-75 mismatch, or cross-engine disagreement fails the pilot. The pinned writer's documented POLYLINE-to-LWPOLYLINE normalization is accepted only when the source is a plain 2D POLYLINE with group 75 equal to zero, flags limited to the closed/continuous bits, and default vertex flags. This check establishes only the group-75 representation rule; it is not a full geometry-fidelity proof.


## Latest dual-engine Golden comparison — 2026-11-18

The exact-head workflow run on code head `04c5591a66f6a2a2ef36cbd7426136ef874c8323` completed Rust formatting and both feature-specific Rust unit-test suites successfully. The independent verifier now accepts only the pinned writer's exact documented plain-2D POLYLINE-to-LWPOLYLINE normalization (default group 75, allowed flags, default vertex flags).

Results:
- Upstream-main candidate: independent ezdxf verification passed for Bagheri7 and Afifiiiii; both reports remain NEEDS_REVIEW, not fidelity PASS.
- Release 0.6.8 candidate: independent ezdxf verification blocked on 12 Bagheri7 and 27 Afifiiiii group-code-75 mismatches (source value 6, output value 0).
- Cross-engine comparison reports exactly 12 and 27 output disagreements respectively.
- The former 13 Bagheri7 POLYLINE-to-LWPOLYLINE normalizations are now accepted only under the exact source flags predicate; no false entity-type mismatch remains.
- The pilot workflow remains failed intentionally because the release candidate loses non-default smooth-surface metadata. This is a real conversion fidelity failure, not a test harness or Rust compilation failure.

This pilot is not production-ready and must not be made green by weakening the source/output comparison. Native Windows/AutoCAD/ODA host validation remains NOT_RUN.
