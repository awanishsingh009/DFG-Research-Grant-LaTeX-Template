"""Opt-in real compiler regressions: set DFG_RUN_TEX_TESTS=1."""
from pathlib import Path
import json
import os
import subprocess
import sys
import unittest
import uuid

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from checks import Report, check_trace, check_pdf, check_log
PROFILE=json.loads((ROOT/'profiles/research-grants-2026-09.json').read_text(encoding='utf-8'))

@unittest.skipUnless(os.environ.get('DFG_RUN_TEX_TESTS')=='1','Set DFG_RUN_TEX_TESTS=1 for real TeX tests.')
class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output=ROOT/'build'/'integration'/uuid.uuid4().hex
        cls.output.mkdir(parents=True)
    def compile(self,name,text,passes=1):
        source=self.output/(name+'.tex');source.write_text(text,encoding='utf-8')
        for _ in range(passes):
            p=subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error','-no-shell-escape',
                              '-output-directory='+str(self.output),str(source)],cwd=ROOT,capture_output=True,
                             text=True,encoding='utf-8',errors='replace',timeout=90)
            if p.returncode: break
        (self.output/(name+'.console.txt')).write_text(p.stdout,encoding='utf-8')
        return p,source
    def fixture(self,mutation=None):
        parts=[r'\documentclass[english,portable,manualbibliography]{dfgproposal}',
               r'\DFGSetProjectTitle{Synthetic regression fixture}',
               r'\DFGAddApplicant{pi1}{Test Author}{Test City}',
               r'\begin{document}\DFGStartMainMatter\DFGMakeProposalHeader\DFGMainPageLimitNotice']
        for h in PROFILE['headings']:
            if h['number']=='4': parts.append(r'\DFGStartSupplement')
            parts.append(r'\DFGHeading {'+h['id']+'}')
            if h['id']=='objectives':
                parts.append(r'\label{sec:objective}See section~\ref{sec:objective}.')
            if h['id']=='ethics-general': parts.append(r'\DFGEthicsStatement{no}')
            parts.append('Synthetic explanatory text for this regression fixture.')
        parts.append(r'\end{document}')
        text='\n'.join(parts)
        return mutation(text) if mutation else text
    def test_actual_references_and_whitespace(self):
        p,source=self.compile('references',self.fixture(),2)
        self.assertEqual(p.returncode,0,p.stdout[-1600:])
        aux=source.with_suffix('.aux').read_text(encoding='utf-8')
        self.assertIn(r'\newlabel{sec:objective}{{2.2}',aux)
        r=Report();check_trace(source.with_suffix('.dfg-audit').read_text(),PROFILE,'english',False,r)
        self.assertFalse(r.failed,r.items)
    def test_inactive_heading_cannot_pass(self):
        p,source=self.compile('inactive',self.fixture(lambda s:s.replace(r'\DFGHeading {objectives}',r'\iffalse\DFGHeading {objectives}\fi')))
        self.assertEqual(p.returncode,0,p.stdout[-1200:])
        r=Report();check_trace(source.with_suffix('.dfg-audit').read_text(),PROFILE,'english',False,r)
        self.assertTrue(r.failed)
    def test_six_point_paragraph_detected(self):
        text=self.fixture(lambda s:s.replace(r'\label{sec:objective}',
                          r'{\fontsize{6pt}{7pt}\selectfont This paragraph is deliberately too small for the required document body.}\par\label{sec:objective}'))
        p,source=self.compile('small',text,2);self.assertEqual(p.returncode,0,p.stdout[-1200:])
        r=Report();pages=check_trace(source.with_suffix('.dfg-audit').read_text(),PROFILE,'english',False,r)
        check_pdf(source.with_suffix('.pdf'),PROFILE,'english',False,pages,r)
        self.assertTrue(any(x['check']=='paragraph text sizes' and x['status']=='failed' for x in r.items),r.items)
    def test_submission_rejects_prompt(self):
        text=self.fixture().replace('portable,manualbibliography','manualbibliography,submission').replace('Synthetic explanatory text',r'\DFGTodo{Unfinished} Synthetic explanatory text',1)
        p,_=self.compile('prompt',text);self.assertNotEqual(p.returncode,0)
        if 'Arial is unavailable' in p.stdout: self.skipTest('Arial is unavailable for this submission-mode case.')
        self.assertIn('Unresolved writing prompt',p.stdout)
    def test_pdftex_submission_rejected(self):
        text=r'\documentclass[submission,manualbibliography]{dfgproposal}\begin{document}Text\end{document}'
        source=self.output/'pdftex.tex';source.write_text(text)
        p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(self.output),str(source)],cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertNotEqual(p.returncode,0);self.assertIn('drafting-only',p.stdout)
    def page_source(self,main,supplement,float_at_end=False):
        text=r'\documentclass[portable,manualbibliography]{dfgproposal}\begin{document}\DFGStartMainMatter'+'\n'
        text+=('Page text.'+r'\newpage'+'\n')*(main-1)+'Page text.\n'
        text+=r'\DFGStartSupplement'+'\n'
        text+=('Supplement text.'+r'\newpage'+'\n')*(supplement-1)+'Supplement text.\n'
        if float_at_end: text+=r'\begin{figure}[p]\centering\rule{30mm}{100mm}\caption{Queued final float.}\end{figure}'
        return text+r'\end{document}'
    def test_page_limits_and_final_float(self):
        for main,supplement,extra,expected in [(17,8,False,False),(18,8,False,True),(17,9,False,True),(1,8,True,True)]:
            name=f'pages-{main}-{supplement}-{int(extra)}'
            p,source=self.compile(name,self.page_source(main,supplement,extra))
            self.assertEqual(p.returncode,0,p.stdout[-1200:])
            report=Report()
            check_trace(source.with_suffix('.dfg-audit').read_text(),PROFILE,'english',False,report)
            page_check=next(x for x in report.items if x['check']=='shipped pages')
            self.assertEqual(page_check['status']=='failed',expected,page_check)
    def test_highlight_limit(self):
        text=r'\documentclass[portable]{dfgproposal}\DFGHighlightPublications{'+','.join('key'+str(i) for i in range(11))+r'}\begin{document}Test\end{document}'
        p,_=self.compile('highlights',text)
        self.assertNotEqual(p.returncode,0)
        self.assertIn('More than ten applicant works',p.stdout)
    def test_bibliography_scope_and_freshness(self):
        from build import build
        bib=self.output/'scope.bib'
        bib.write_text('@book{mainwork,author={Example Author},title={Main-only reference},year={2026},publisher={Example}}\n'
                       '@book{suppwork,author={Example Author},title={Supplement-only reference},year={2026},publisher={Example}}\n')
        text=self.fixture().replace(',manualbibliography','')
        text=text.replace(r'\begin{document}',r'\addbibresource{'+bib.relative_to(ROOT).as_posix()+r'}\begin{document}')
        text=text.replace(r'\DFGHeading {starting-point}',r'\DFGHeading {starting-point}\cite{mainwork}')
        text=text.replace(r'\DFGHeading {publications}',r'\DFGPrintReferences')
        text=text.replace(r'\DFGHeading {research-context}',r'\DFGHeading {research-context}\cite{suppwork}')
        source=self.output/'scope.tex';source.write_text(text,encoding='utf-8')
        pdf=build(source,'english',output=self.output/'compiled')
        from checks import run
        output=run(['pdftotext',str(pdf),'-'])
        self.assertIn('Main-only reference',output)
        self.assertNotIn('Supplement-only reference',output)
        manifest=json.loads(pdf.with_suffix('.inputs.json').read_text())
        self.assertIn(str(bib.resolve()),[x['path'] for x in manifest['inputs']])

if __name__=='__main__': unittest.main()
