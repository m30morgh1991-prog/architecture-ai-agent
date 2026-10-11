from __future__ import annotations
import csv
import hashlib
import json
from pathlib import Path
from runtime.dwg_semantic_evidence import extract_dwg_evidence

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'test-assets/golden-understanding/golden_manifest.json'
OUT = ROOT / 'artifacts/golden-dwg-evidence'

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()

def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    OUT.mkdir(parents=True, exist_ok=True)
    summary, dimensions, texts, index = [], [], [], []
    for case in manifest['cases']:
        source = ROOT / case['source_path']
        if not source.is_file():
            raise FileNotFoundError(f"SOURCE_REQUIRED:{case['case_id']}:{source}")
        before = sha256_file(source)
        expected = case.get('source_sha256')
        if expected and before != expected:
            raise RuntimeError(f"SOURCE_SHA256_MISMATCH:{case['case_id']}")
        evidence = extract_dwg_evidence(source)
        after = sha256_file(source)
        if before != after:
            raise RuntimeError(f"GOLDEN_SOURCE_CHANGED_DURING_READ:{case['case_id']}")
        if evidence['source_profile']['sha256'] != before:
            raise RuntimeError(f"EXTRACTOR_HASH_MISMATCH:{case['case_id']}")
        evidence['export_metadata'] = {'case_id': case['case_id'], 'sha256_before': before, 'sha256_after': after, 'source_mutated': False, 'regulatory_compliance_assessed': False, 'semantic_authority': False, 'measurement_warning': 'Extracted annotations are evidence, not a compliance verdict; validate units, view association and applicable official rules.'}
        json_name = f"{case['case_id'].lower()}-evidence.json"
        (OUT / json_name).write_text(json.dumps(evidence, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')
        profile = evidence['source_profile']
        summary.append({'case_id':case['case_id'],'source_path':case['source_path'],'sha256':before,'drawing_version':profile.get('version','UNKNOWN'),'decode_version':profile.get('decode_version','UNKNOWN'),'units_metadata':profile.get('units','UNKNOWN'),'entity_total':sum(evidence['entity_counts'].values()),'dimension_entity_count':len(evidence.get('dimensions',[])),'text_entity_count':len(evidence.get('text',[])),'layer_count':len(evidence.get('layer_counts',{})),'block_name_count':len(evidence.get('block_counts',{})),'extmin':json.dumps(evidence.get('header',{}).get('extmin'),ensure_ascii=False),'extmax':json.dumps(evidence.get('header',{}).get('extmax'),ensure_ascii=False),'source_mutated':False,'compliance_verdict':'NOT_ASSESSED','evidence_json':json_name})
        for row in evidence.get('dimensions',[]):
            dimensions.append({'case_id':case['case_id'],'source_sha256':before,'handle':row.get('handle'),'dimension_type':row.get('type'),'dimension_text':row.get('text'),'actual_measurement':json.dumps(row.get('actual_measurement'),ensure_ascii=False),'defpoint':json.dumps(row.get('defpoint'),ensure_ascii=False),'defpoint2':json.dumps(row.get('defpoint2'),ensure_ascii=False),'defpoint3':json.dumps(row.get('defpoint3'),ensure_ascii=False),'interpretation_status':'NEEDS_REVIEW'})
        for row in evidence.get('text',[]):
            texts.append({'case_id':case['case_id'],'source_sha256':before,'handle':row.get('handle'),'entity_type':row.get('type'),'text':row.get('text'),'insert':json.dumps(row.get('insert'),ensure_ascii=False),'rotation':row.get('rotation')})
        index.append({'case_id':case['case_id'],'source_path':case['source_path'],'source_sha256':before,'evidence_json':json_name,'entity_counts':evidence['entity_counts'],'layer_counts':evidence['layer_counts'],'block_counts':evidence['block_counts']})
    def write_csv(name, rows):
        if not rows:
            (OUT/name).write_text('no_rows_extracted\n',encoding='utf-8'); return
        with (OUT/name).open('w',newline='',encoding='utf-8-sig') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0].keys())); writer.writeheader(); writer.writerows(rows)
    write_csv('summary.csv',summary); write_csv('dimensions.csv',dimensions); write_csv('text-labels.csv',texts)
    (OUT/'index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2,sort_keys=True),encoding='utf-8')
    print(json.dumps({'status':'EXTRACTION_COMPLETE_NOT_COMPLIANCE_APPROVAL','output_dir':'artifacts/golden-dwg-evidence','plans':summary,'dimension_rows':len(dimensions),'text_rows':len(texts),'golden_sources_mutated':False},ensure_ascii=False,indent=2))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())