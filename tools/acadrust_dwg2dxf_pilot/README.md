# Isolated acadrust DWG → DXF pilot

This is an experiment, not a production converter and not a production dependency.

## Why isolated

- Exact upstream crate pin: `acadrust = 0.6.8` (MPL-2.0).
- `default-features = false` disables acadrust's optional Rayon parallelism for a lower-concurrency baseline.
- The probe writes directly from the parsed `CadDocument` to a temporary DXF file through `DxfWriter::write_to_file`; it does not build a full intermediate DXF byte/string buffer.
- DWG reads are strict (failsafe/recovery disabled) and capped at 512 MiB decompressed bytes, 1,000,000 mesh faces and 4,000,000 mesh face indices.
- Input is SHA-256 hashed before and after; the original file is never opened for writing.
- The output is always named and treated as a `.candidate.dxf`, independently reopened by acadrust, and independently inspected by ezdxf in CI.
- The report never declares fidelity PASS. Even if structural counts match, the decision remains NEEDS_REVIEW pending deeper entity/property comparison and CAD-host verification.

## Run

From the repository root:

```sh
cargo generate-lockfile --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml
cargo test --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml --locked
cargo run --manifest-path tools/acadrust_dwg2dxf_pilot/Cargo.toml -- \
  test-assets/golden-projects/bagheri7.dwg \
  /tmp/bagheri7.candidate.dxf \
  /tmp/bagheri7.report.json
python tools/acadrust_dwg2dxf_pilot/verify_ezdxf.py \
  /tmp/bagheri7.candidate.dxf /tmp/bagheri7.report.json
```

The output path and report path must not already exist. The converter writes a same-directory temporary file and atomically renames it to the candidate path only after the DXF can be reopened by acadrust. A candidate is not a final deliverable.

## Evidence limits

The initial gate compares source/output entity and modelspace counts, table counts, drawing version, unit variables, parser diagnostics and architecture omissions. This is intentionally conservative but is not a complete fidelity proof. The independent ezdxf check validates that a second parser can reopen the DXF and compares core inventories. XData, proxy graphics, nested block semantics, dimension rendering, paper-space layout fidelity, OCS/WCS, fonts and AutoCAD/ODA interoperability still require deeper tests.

Windows/AutoCAD host tests remain NOT_RUN until the user confirms the Windows environment is ready.
