from pathlib import Path
import importlib.util
import json
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from checks import Report, check_trace, check_log, check_inputs, digest, strip_comments
from build import dependency_errors
from generate_profile import render

PROFILE=json.loads((ROOT/'profiles/research-grants-2026-09.json').read_text(encoding='utf-8'))

def trace(language='english',mode='submission'):
    lines=['profile|'+PROFILE['id'],'language|'+language,'mode|'+mode,'font|Arial',
           'limits|17|8','boundary|main']
    for heading in PROFILE['headings']:
        if heading['number']=='4': lines.append('boundary|supplement')
        lines.append('heading|'+heading['id']+'|'+heading['number'])
    lines+=['ethics|no','pages|2|3','complete|yes']
    return '\n'.join(lines)

class CheckTests(unittest.TestCase):
    def report(self,text,release=True,lang='english'):
        r=Report();check_trace(text,PROFILE,lang,release,r);return r
    def test_completed_english(self): self.assertFalse(self.report(trace()).failed)
    def test_completed_german(self): self.assertFalse(self.report(trace('german'),lang='german').failed)
    def test_missing_heading(self):
        self.assertTrue(self.report(trace().replace('heading|objectives|2.2','')).failed)
    def test_duplicate_heading(self):
        row='heading|objectives|2.2'
        self.assertTrue(self.report(trace().replace(row,row+'\n'+row)).failed)
    def test_reordered_headings(self):
        text=trace().replace('heading|objectives|2.2','SWAP').replace('heading|data|2.4','heading|objectives|2.2').replace('SWAP','heading|data|2.4')
        self.assertTrue(self.report(text).failed)
    def test_wrong_language(self): self.assertTrue(self.report(trace('german')).failed)
    def test_wrong_boundary(self):
        self.assertTrue(self.report(trace().replace('boundary|supplement','boundary|main')).failed)
    def test_unfinished_trace(self): self.assertTrue(self.report(trace().replace('complete|yes','')).failed)
    def test_old_profile(self):
        self.assertTrue(self.report(trace().replace(PROFILE['id'],'research-grants-2025-09')).failed)
    def test_optional_services(self):
        self.assertFalse(self.report(trace().replace('ethics|no','heading|services|5.9\nethics|no')).failed)
    def test_unknown_heading(self):
        self.assertTrue(self.report(trace().replace('ethics|no','heading|made-up|5.9\nethics|no')).failed)
    def test_pending_ethics_release(self): self.assertTrue(self.report(trace().replace('ethics|no','ethics|pending')).failed)
    def test_duplicate_ethics(self): self.assertTrue(self.report(trace().replace('ethics|no','ethics|no\nethics|yes')).failed)
    def test_draft_prompts_warn(self):
        r=self.report(trace(mode='draft')+'\ntodo|unresolved',False)
        self.assertFalse(r.failed); self.assertTrue(any(x['status']=='warning' for x in r.items))
    def test_submission_prompts_fail(self): self.assertTrue(self.report(trace()+'\ntodo|unresolved').failed)
    def test_page_boundaries(self):
        self.assertFalse(self.report(trace().replace('pages|2|3','pages|17|8')).failed)
        for counts in ('18|8','17|9','0|1'):
            self.assertTrue(self.report(trace().replace('pages|2|3','pages|'+counts)).failed)
    def test_overridden_limits(self): self.assertTrue(self.report(trace().replace('limits|17|8','limits|99|99')).failed)
    def test_release_fallback_font(self): self.assertTrue(self.report(trace().replace('font|Arial','font|Liberation Sans')).failed)
    def test_draft_fallback_font(self): self.assertFalse(self.report(trace().replace('font|Arial','font|Liberation Sans'),False).failed)
    def test_unresolved_citation(self):
        r=Report();check_log("LaTeX Warning: Citation 'missing' on page 1 undefined",True,r);self.assertTrue(r.failed)
    def test_missing_glyph(self):
        r=Report();check_log('Missing character: There is no glyph',True,r);self.assertTrue(r.failed)
    def test_missing_dependencies_release(self):
        with patch('shutil.which',return_value=None):
            self.assertIn('pdftohtml',dependency_errors('xelatex',True))
            self.assertNotIn('pdftohtml',dependency_errors('xelatex',False))
    def test_profile_generation(self):
        self.assertEqual(render(PROFILE),(ROOT/'dfg-research-grants-2026-09.def').read_text(encoding='utf-8'))
    def test_comments(self):
        self.assertNotIn('TODO',strip_comments('Text % TODO'))
        self.assertIn(r'\%',strip_comments(r'Text \% preserved'))
    def test_source_freshness(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'main.tex';pdf=root/'main.pdf';manifest=root/'main.inputs.json'
            source.write_text('Actual text',encoding='utf-8');pdf.write_bytes(b'test fixture')
            manifest.write_text(json.dumps({'source':str(source),'pdf_sha256':digest(pdf),'inputs':[{'path':str(source),'sha256':digest(source)}]}))
            r=Report();check_inputs(manifest,source,pdf,True,r);self.assertFalse(r.failed)
            source.write_text('Changed text')
            r=Report();check_inputs(manifest,source,pdf,True,r);self.assertTrue(r.failed)
    def test_wrong_source_pdf_pair(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);source=root/'main.tex';pdf=root/'main.pdf';manifest=root/'main.inputs.json'
            source.write_text('text');pdf.write_bytes(b'pdf')
            manifest.write_text(json.dumps({'source':str(source),'pdf_sha256':digest(pdf),'inputs':[]}))
            r=Report();check_inputs(manifest,root/'other.tex',pdf,True,r);self.assertTrue(r.failed)

if __name__=='__main__': unittest.main()
