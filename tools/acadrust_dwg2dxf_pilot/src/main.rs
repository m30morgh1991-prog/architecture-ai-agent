#[cfg(all(feature = "release", feature = "upstream-main"))]
compile_error!("Select exactly one acadrust implementation feature.");
#[cfg(not(any(feature = "release", feature = "upstream-main")))]
compile_error!("Select either the release or upstream-main acadrust feature.");

#[cfg(feature = "upstream-main")]
use acadrust_main as acadrust;
#[cfg(feature = "release")]
use acadrust_release as acadrust;

#[cfg(feature = "release")]
const ACADRUST_BUILD: &str = "crates.io:0.6.8";
#[cfg(feature = "upstream-main")]
const ACADRUST_BUILD: &str = "git:52034a673ff59bf6936ebf01ec794b07a97df246";

use acadrust::{CadDocument, DwgReadOptions, DwgReader, DxfReader, DxfWriter, EntityType, ReadStats};
use serde::Serialize;
use sha2::{Digest, Sha256};
use std::{
    error::Error,
    fs::{self, File, OpenOptions},
    io::{Read, Write},
    path::{Path, PathBuf},
    time::Instant,
};

const MAX_INPUT_BYTES: u64 = 512 * 1024 * 1024;
const MAX_DECOMPRESSED_BYTES: usize = 512 * 1024 * 1024;
const MAX_MESH_FACES: usize = 1_000_000;
const MAX_MESH_FACE_INDICES: usize = 4_000_000;

#[derive(Debug, Clone, Serialize, PartialEq, Eq)]
struct TableCounts {
    layers: usize,
    line_types: usize,
    text_styles: usize,
    dim_styles: usize,
    block_records: usize,
    app_ids: usize,
}

#[derive(Debug, Clone, Serialize)]
struct PolylineSmoothSurfaceRecord {
    handle: String,
    owner_handle: String,
    smooth_surface: i16,
}

#[derive(Debug, Clone, Serialize)]
struct ReadSummary {
    stream_completed: bool,
    source_version: String,
    source_records: usize,
    decoded_source_records: usize,
    skipped_source_records: usize,
    output_entities: usize,
    output_objects: usize,
    output_table_records: usize,
    recovered_errors: usize,
    diagnostic_codes: Vec<String>,
}

impl From<&ReadStats> for ReadSummary {
    fn from(stats: &ReadStats) -> Self {
        Self {
            stream_completed: stats.stream_completed,
            source_version: stats.source_version.clone(),
            source_records: stats.source_records,
            decoded_source_records: stats.decoded_source_records,
            skipped_source_records: stats.skipped_source_records,
            output_entities: stats.output_entities,
            output_objects: stats.output_objects,
            output_table_records: stats.output_table_records,
            recovered_errors: stats.recovered_errors,
            diagnostic_codes: stats.diagnostics.iter().map(|d| d.code.clone()).collect(),
        }
    }
}

#[derive(Debug, Serialize)]
struct Report {
    schema_version: u8,
    tool: String,
    tool_version: String,
    acadrust_version: String,
    decision: String,
    structural_checks_pass: bool,
    input_path: String,
    input_bytes: u64,
    input_sha256_before: String,
    input_sha256_after: String,
    input_unchanged: bool,
    source_version: String,
    output_version: String,
    source_entity_count: usize,
    output_entity_count: usize,
    source_modelspace_entity_count: usize,
    output_modelspace_entity_count: usize,
    source_tables: TableCounts,
    output_tables: TableCounts,
    source_insertion_units: i16,
    output_insertion_units: i16,
    source_measurement: i16,
    output_measurement: i16,
    source_polyline_smooth_surfaces: Vec<PolylineSmoothSurfaceRecord>,
    source_read: ReadSummary,
    output_read: ReadSummary,
    architecture_omissions: Vec<String>,
    candidate_path: String,
    candidate_bytes: u64,
    candidate_sha256: String,
    peak_rss_kib: Option<u64>,
    elapsed_ms: u128,
    reasons: Vec<String>,
}

fn sha256_file(path: &Path) -> Result<String, Box<dyn Error>> {
    let mut file = File::open(path)?;
    let mut hasher = Sha256::new();
    let mut buffer = [0u8; 1024 * 1024];
    loop {
        let read = file.read(&mut buffer)?;
        if read == 0 {
            break;
        }
        hasher.update(&buffer[..read]);
    }
    Ok(format!("{:x}", hasher.finalize()))
}

fn absolute_output(path: &Path) -> Result<PathBuf, Box<dyn Error>> {
    let name = path.file_name().ok_or("OUTPUT_PATH_MUST_HAVE_FILENAME")?;
    let parent = path
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    Ok(fs::canonicalize(parent)?.join(name))
}

fn temporary_sibling(path: &Path, label: &str) -> Result<PathBuf, Box<dyn Error>> {
    let name = path
        .file_name()
        .ok_or("OUTPUT_PATH_MUST_HAVE_FILENAME")?
        .to_string_lossy();
    let parent = path.parent().ok_or("OUTPUT_PARENT_MISSING")?;
    Ok(parent.join(format!(".{name}.{}.{}.tmp", std::process::id(), label)))
}

fn table_counts(document: &CadDocument) -> TableCounts {
    TableCounts {
        layers: document.layers.iter().count(),
        line_types: document.line_types.iter().count(),
        text_styles: document.text_styles.iter().count(),
        dim_styles: document.dim_styles.iter().count(),
        block_records: document.block_records.iter().count(),
        app_ids: document.app_ids.iter().count(),
    }
}

fn polyline_smooth_surface_records(document: &CadDocument) -> Vec<PolylineSmoothSurfaceRecord> {
    document
        .entities()
        .filter_map(|entity| match entity {
            EntityType::Polyline2D(polyline) if polyline.smooth_surface as i16 != 0 => {
                Some(PolylineSmoothSurfaceRecord {
                    handle: format!("{:X}", polyline.common.handle),
                    owner_handle: format!("{:X}", polyline.common.owner_handle),
                    smooth_surface: polyline.smooth_surface as i16,
                })
            }
            _ => None,
        })
        .collect()
}

fn reserve_new_file(path: &Path) -> Result<(), Box<dyn Error>> {
    OpenOptions::new().write(true).create_new(true).open(path)?;
    Ok(())
}

fn peak_rss_kib() -> Option<u64> {
    let status = fs::read_to_string("/proc/self/status").ok()?;
    let line = status.lines().find(|line| line.starts_with("VmHWM:"))?;
    line.split_whitespace().nth(1)?.parse().ok()
}

fn write_report_atomically(path: &Path, report: &Report) -> Result<(), Box<dyn Error>> {
    let temporary = temporary_sibling(path, "report")?;
    reserve_new_file(&temporary)?;
    let result = (|| -> Result<(), Box<dyn Error>> {
        let mut file = OpenOptions::new()
            .write(true)
            .truncate(true)
            .open(&temporary)?;
        serde_json::to_writer_pretty(&mut file, report)?;
        file.write_all(b"\n")?;
        file.sync_all()?;
        // Hard-link creation is atomic and fails if the destination exists;
        // unlike rename(), it cannot replace a file created in a race window.
        fs::hard_link(&temporary, path)?;
        let _ = fs::remove_file(&temporary);
        Ok(())
    })();
    if result.is_err() {
        let _ = fs::remove_file(&temporary);
    }
    result
}

fn convert(input: &Path, candidate: &Path, report_path: &Path) -> Result<Report, Box<dyn Error>> {
    let started = Instant::now();
    let input = fs::canonicalize(input)?;
    let candidate = absolute_output(candidate)?;
    let report_path = absolute_output(report_path)?;

    if !input.is_file() {
        return Err("INPUT_MUST_BE_A_FILE".into());
    }
    if input
        .extension()
        .and_then(|v| v.to_str())
        .map(|v| v.eq_ignore_ascii_case("dwg"))
        != Some(true)
    {
        return Err("INPUT_EXTENSION_MUST_BE_DWG".into());
    }
    if candidate
        .extension()
        .and_then(|v| v.to_str())
        .map(|v| v.eq_ignore_ascii_case("dxf"))
        != Some(true)
    {
        return Err("CANDIDATE_EXTENSION_MUST_BE_DXF".into());
    }
    if candidate == input || report_path == input || candidate == report_path {
        return Err("INPUT_CANDIDATE_REPORT_PATHS_MUST_BE_DISTINCT".into());
    }
    if candidate.exists() || report_path.exists() {
        return Err("REFUSE_TO_OVERWRITE_EXISTING_OUTPUT".into());
    }

    let input_bytes = fs::metadata(&input)?.len();
    if input_bytes == 0 || input_bytes > MAX_INPUT_BYTES {
        return Err("INPUT_SIZE_OUTSIDE_PILOT_LIMIT".into());
    }

    let input_sha256_before = sha256_file(&input)?;
    let candidate_tmp = temporary_sibling(&candidate, "dxf")?;
    reserve_new_file(&candidate_tmp)?;

    let conversion_result = (|| -> Result<Report, Box<dyn Error>> {
        let options = DwgReadOptions::default()
            .with_max_decompressed_bytes(MAX_DECOMPRESSED_BYTES)
            .with_mesh_limits(MAX_MESH_FACES, MAX_MESH_FACE_INDICES);
        let mut reader = DwgReader::from_file_with_options(&input, options)?;
        let source_outcome = reader.read_with_stats()?;
        let source_document = source_outcome.document;
        let source_stats = source_outcome.stats;
        let source_tables = table_counts(&source_document);
        // Capture non-default POLYLINE group 75 values from every layout and block.
        // These are the source-side evidence needed to distinguish reader loss
        // from DXF writer loss in the independent ezdxf comparison.
        let source_polyline_smooth_surfaces =
            polyline_smooth_surface_records(&source_document);
        let source_entity_count = source_document.entities().count();
        let source_modelspace_entity_count =
            source_document.entities_in_block("*Model_Space").count();
        let source_version = format!("{:?}", source_document.version);
        let source_insertion_units = source_document.header.insertion_units;
        let source_measurement = source_document.header.measurement;
        let omissions = DxfWriter::new(&source_document)
            .omitted_architecture_records()
            .iter()
            .map(|o| format!("{}: {}", o.name, o.reason))
            .collect::<Vec<_>>();

        // Direct document-to-file streaming: no intermediate DXF String/Vec.
        DxfWriter::new(&source_document).write_to_file(&candidate_tmp)?;

        // Reopen the exact candidate with a second read pass in acadrust.
        let output_outcome = DxfReader::from_file(&candidate_tmp)?.read_with_stats()?;
        let output_document = output_outcome.document;
        let output_stats = output_outcome.stats;
        let output_tables = table_counts(&output_document);
        let output_entity_count = output_document.entities().count();
        let output_modelspace_entity_count =
            output_document.entities_in_block("*Model_Space").count();
        let output_version = format!("{:?}", output_document.version);
        let output_insertion_units = output_document.header.insertion_units;
        let output_measurement = output_document.header.measurement;

        let input_sha256_after = sha256_file(&input)?;
        let input_unchanged = input_sha256_before == input_sha256_after;
        let candidate_bytes = fs::metadata(&candidate_tmp)?.len();
        let candidate_sha256 = sha256_file(&candidate_tmp)?;
        let peak_rss_kib = peak_rss_kib();

        let mut reasons = Vec::new();
        if source_entity_count != output_entity_count {
            reasons.push("TOTAL_ENTITY_COUNT_MISMATCH".to_string());
        }
        if source_modelspace_entity_count != output_modelspace_entity_count {
            reasons.push("MODELSPACE_ENTITY_COUNT_MISMATCH".to_string());
        }
        if source_tables != output_tables {
            reasons.push("TABLE_INVENTORY_MISMATCH".to_string());
        }
        if source_version != output_version {
            reasons.push("DRAWING_VERSION_MISMATCH".to_string());
        }
        if source_insertion_units != output_insertion_units {
            reasons.push("INSUNITS_MISMATCH".to_string());
        }
        if source_measurement != output_measurement {
            reasons.push("MEASUREMENT_MISMATCH".to_string());
        }
        if !source_stats.stream_completed || !output_stats.stream_completed {
            reasons.push("READ_STREAM_INCOMPLETE".to_string());
        }
        if source_stats.skipped_source_records != 0 || output_stats.skipped_source_records != 0 {
            reasons.push("SOURCE_RECORDS_SKIPPED".to_string());
        }
        if source_stats.recovered_errors != 0 || output_stats.recovered_errors != 0 {
            reasons.push("RECOVERED_PARSE_ERRORS".to_string());
        }
        if !source_stats.diagnostics.is_empty() || !output_stats.diagnostics.is_empty() {
            reasons.push("PARSER_DIAGNOSTICS_PRESENT".to_string());
        }
        if !omissions.is_empty() {
            reasons.push("ARCHITECTURE_RECORDS_OMITTED".to_string());
        }
        if !input_unchanged {
            reasons.push("SOURCE_INPUT_HASH_CHANGED".to_string());
        }

        let structural_checks_pass = reasons.is_empty();
        // Even a structural match is NOT a fidelity PASS; independent
        // ezdxf checks and deeper entity/property comparison remain required.
        let decision = if structural_checks_pass {
            "NEEDS_REVIEW"
        } else {
            "BLOCKED"
        }
        .to_string();
        reasons
            .push("INDEPENDENT_ENTITY_PROPERTY_AND_CAD_HOST_FIDELITY_REVIEW_REQUIRED".to_string());

        Ok(Report {
            schema_version: 1,
            tool: "acadrust-dwg2dxf-pilot".to_string(),
            tool_version: env!("CARGO_PKG_VERSION").to_string(),
            acadrust_version: ACADRUST_BUILD.to_string(),
            decision,
            structural_checks_pass,
            input_path: input.display().to_string(),
            input_bytes,
            input_sha256_before,
            input_sha256_after,
            input_unchanged,
            source_version,
            output_version,
            source_entity_count,
            output_entity_count,
            source_modelspace_entity_count,
            output_modelspace_entity_count,
            source_tables,
            output_tables,
            source_insertion_units,
            output_insertion_units,
            source_measurement,
            output_measurement,
            source_polyline_smooth_surfaces,
            source_read: ReadSummary::from(&source_stats),
            output_read: ReadSummary::from(&output_stats),
            architecture_omissions: omissions,
            candidate_path: candidate.display().to_string(),
            candidate_bytes,
            candidate_sha256,
            peak_rss_kib,
            elapsed_ms: started.elapsed().as_millis(),
            reasons,
        })
    })();

    match conversion_result {
        Ok(report) => {
            // Candidate path is explicit and never represents a production
            // output. Rename is atomic because temp and candidate share a dir.
            // Create-if-absent atomic promotion of the candidate artifact.
            // The candidate remains a review-only file, never a final output.
            fs::hard_link(&candidate_tmp, &candidate)?;
            let _ = fs::remove_file(&candidate_tmp);
            if let Err(error) = write_report_atomically(&report_path, &report) {
                let _ = fs::remove_file(&candidate);
                return Err(error);
            }
            Ok(report)
        }
        Err(error) => {
            let _ = fs::remove_file(&candidate_tmp);
            Err(error)
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let args = std::env::args().skip(1).collect::<Vec<_>>();
    if args.len() != 3 {
        eprintln!("Usage: acadrust-dwg2dxf-pilot INPUT.dwg OUTPUT.candidate.dxf REPORT.json");
        std::process::exit(2);
    }
    let report = convert(
        Path::new(&args[0]),
        Path::new(&args[1]),
        Path::new(&args[2]),
    )?;
    println!(
        "decision={} source_entities={} output_entities={} input_unchanged={}",
        report.decision,
        report.source_entity_count,
        report.output_entity_count,
        report.input_unchanged
    );
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::acadrust::{CadDocument, DwgWriter, EntityType, Line};
    use super::convert;
    use std::{
        fs,
        path::{Path, PathBuf},
        time::{SystemTime, UNIX_EPOCH},
    };

    fn test_dir(label: &str) -> PathBuf {
        let nonce = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let path = std::env::temp_dir().join(format!(
            "acadrust-pilot-{label}-{}-{nonce}",
            std::process::id()
        ));
        fs::create_dir_all(&path).unwrap();
        path
    }

    fn synthetic_dwg(path: &Path) {
        let mut document = CadDocument::new();
        document
            .add_entity(EntityType::Line(Line::from_coords(
                0.0, 0.0, 0.0, 100.0, 50.0, 0.0,
            )))
            .unwrap();
        DwgWriter::write_to_file(path, &document).unwrap();
    }

    #[test]
    fn synthetic_dwg_converts_to_candidate_and_never_claims_pass() {
        let dir = test_dir("synthetic");
        let input = dir.join("input.dwg");
        let candidate = dir.join("candidate.dxf");
        let report_path = dir.join("report.json");
        synthetic_dwg(&input);

        let report = convert(&input, &candidate, &report_path).unwrap();

        assert!(candidate.is_file());
        assert!(report_path.is_file());
        assert!(report.input_unchanged);
        assert_eq!(report.source_entity_count, report.output_entity_count);
        assert_eq!(
            report.source_modelspace_entity_count,
            report.output_modelspace_entity_count
        );
        assert_ne!(report.decision, "PASS");
        let _ = fs::remove_dir_all(dir);
    }

    #[test]
    fn malformed_dwg_is_rejected_without_candidate_output() {
        let dir = test_dir("malformed");
        let input = dir.join("broken.dwg");
        let candidate = dir.join("candidate.dxf");
        let report_path = dir.join("report.json");
        fs::write(&input, b"not a DWG file").unwrap();

        assert!(convert(&input, &candidate, &report_path).is_err());
        assert!(!candidate.exists());
        assert!(!report_path.exists());
        let _ = fs::remove_dir_all(dir);
    }

    #[test]
    fn existing_candidate_is_never_overwritten() {
        let dir = test_dir("no-overwrite");
        let input = dir.join("input.dwg");
        let candidate = dir.join("candidate.dxf");
        let report_path = dir.join("report.json");
        synthetic_dwg(&input);
        fs::write(&candidate, b"keep-me").unwrap();

        assert!(convert(&input, &candidate, &report_path).is_err());
        assert_eq!(fs::read(&candidate).unwrap(), b"keep-me");
        assert!(!report_path.exists());
        let _ = fs::remove_dir_all(dir);
    }

    #[test]
    fn existing_report_is_never_overwritten() {
        let dir = test_dir("report-no-overwrite");
        let input = dir.join("input.dwg");
        let candidate = dir.join("candidate.dxf");
        let report_path = dir.join("report.json");
        synthetic_dwg(&input);
        fs::write(&report_path, b"keep-report").unwrap();

        assert!(convert(&input, &candidate, &report_path).is_err());
        assert!(!candidate.exists());
        assert_eq!(fs::read(&report_path).unwrap(), b"keep-report");
        let _ = fs::remove_dir_all(dir);
    }
}
