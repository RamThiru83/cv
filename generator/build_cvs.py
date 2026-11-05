import sys, json, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import cvdata as D

OUT = sys.argv[1] if len(sys.argv) > 1 else 'files'
PUBLIC = os.environ.get('CV_PUBLIC') == '1'   # public site: no DOB, no unsanctioned/pending grants
DOB = '[to be entered by the applicant before submission]' if PUBLIC else D.PERSON['dob']
PROFILE = D.PROFILE
if PUBLIC:
    PROFILE = PROFILE.replace('I currently lead, as Principal Investigator, an ANRF MAHA MedTech Mission project on point-of-care AI ultrasound (PRAGATI) and two ICMR National Health Research Priority (NHRP) projects', 'I currently lead, as Principal Investigator, two ICMR National Health Research Priority (NHRP) projects')
os.makedirs(OUT, exist_ok=True)
P = D.PERSON
INK = RGBColor(0x1B, 0x2A, 0x3A)

def new_doc(title, margins=2.0, size=10):
    d = Document()
    for s in d.sections:
        s.page_width = Cm(21.0); s.page_height = Cm(29.7)
        s.left_margin = s.right_margin = Cm(margins); s.top_margin = Cm(1.8); s.bottom_margin = Cm(1.8)
    st = d.styles['Normal']; st.font.name = 'Arial'; st.font.size = Pt(size)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Arial')
    st.paragraph_format.space_after = Pt(3); st.paragraph_format.space_before = Pt(0)
    d.core_properties.title = title; d.core_properties.author = 'Ramachandran Thiruvengadam'
    return d

def border_bottom(p, color='1B2A3A', sz=6):
    pPr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr'); e = OxmlElement('w:bottom')
    e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(sz)); e.set(qn('w:space'), '1'); e.set(qn('w:color'), color)
    b.append(e); pPr.append(b)

def run(p, text, bold=False, italic=False, size=None, color=None):
    r = p.add_run(text); r.bold = bold; r.italic = italic
    if size: r.font.size = Pt(size)
    if color: r.font.color.rgb = color
    return r

def title_block(d, name, sub_lines, center=False):
    p = d.add_paragraph(); run(p, name, bold=True, size=16, color=INK)
    if center: p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for l in sub_lines:
        q = d.add_paragraph(); run(q, l, size=9)
        if center: q.alignment = WD_ALIGN_PARAGRAPH.CENTER
        q.paragraph_format.space_after = Pt(0)
    d.add_paragraph().paragraph_format.space_after = Pt(2)

def h1(d, text):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(9); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run(p, text, bold=True, size=11, color=INK); border_bottom(p); return p

def para(d, text, bold=False, italic=False, size=None, after=3):
    p = d.add_paragraph(); run(p, text, bold=bold, italic=italic, size=size); p.paragraph_format.space_after = Pt(after); return p

def bullets(d, items, size=None):
    for t in items:
        p = d.add_paragraph(style='List Bullet'); run(p, t, size=size); p.paragraph_format.space_after = Pt(2)

def shade(cell, fill='E6EBF0'):
    tcPr = cell._tc.get_or_add_tcPr(); sh = OxmlElement('w:shd')
    sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), fill); tcPr.append(sh)

def table(d, header, rows, widths, size=8.5):
    t = d.add_table(rows=1, cols=len(header)); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]; c.text = ''; run(c.paragraphs[0], h, bold=True, size=size); shade(c)
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            cells[i].text = ''; run(cells[i].paragraphs[0], str(v), size=size)
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Cm(w)
        for c in row.cells:
            for p in c.paragraphs: p.paragraph_format.space_after = Pt(1)
    d.add_paragraph().paragraph_format.space_after = Pt(2)
    return t

def kv(d, rows, widths=(4.5, 12.5), size=9):
    t = d.add_table(rows=0, cols=2); t.style = 'Table Grid'; t.autofit = False
    for k, v in rows:
        c = t.add_row().cells; c[0].text = ''; c[1].text = ''
        run(c[0].paragraphs[0], k, bold=True, size=size); shade(c[0]); run(c[1].paragraphs[0], v, size=size)
    for row in t.rows:
        for i, w in enumerate(widths): row.cells[i].width = Cm(w)
    d.add_paragraph().paragraph_format.space_after = Pt(2)

ROLE_TAG = {'first': 'First author', 'second': 'Second author', 'corresponding': 'Corresponding author', 'last': 'Last author',
            'co-author': 'Co-author', 'group member': 'Group/consortium member'}

def cite(d, p, tag=True, pmid=False, num=None, size=None):
    authors, title, jr, yr, vp, doi, pm, role = p
    para_ = d.add_paragraph(); para_.paragraph_format.space_after = Pt(3)
    if num is not None: run(para_, f'{num}. ', size=size)
    run(para_, f'{authors}. {title}. ', size=size); run(para_, jr, italic=True, size=size)
    run(para_, f'. {yr};{vp}. doi:{doi}', size=size)
    if pmid and pm: run(para_, f'. PMID: {pm}', size=size)
    if tag: run(para_, f'  [{ROLE_TAG[role]}]', italic=True, size=size, color=RGBColor(0x55, 0x60, 0x6B))
    return para_

def ongoing_rows(with_status=True):
    rows = []
    for g in D.GRANTS_ONGOING:
        if PUBLIC and g[5]: continue
        dur = g[3] + (f'. {g[5]}' if (with_status and g[5]) else '')
        rows.append([g[0], g[1], g[2], dur, g[4]])
    return rows

def footer_note(d, text):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(8)
    run(p, text, italic=True, size=8, color=RGBColor(0x55, 0x60, 0x6B))

NOTE_STD = 'Standard layout assembled from the master CV; check section order and limits against the call\'s own template. '
import datetime as _dt
ASOF = 'Data as of ' + str(_dt.date.today().day) + ' ' + _dt.date.today().strftime('%B %Y') + '.'

# ---------- 1. Full CV ----------
def full_cv():
    d = new_doc('Curriculum Vitae - Ramachandran Thiruvengadam')
    title_block(d, 'CURRICULUM VITAE', [P['name'], P['quals'], P['position'] + ', ' + P['institute']])
    h1(d, '1. Contact and identifiers')
    kv(d, [('Address', P['address']), ('E-mail', P['email']), ('ORCID', P['orcid']), ('Web of Science ID', P['wos']), ('Google Scholar', P['scholar']), ('Domain expertise', P['domain'])])
    h1(d, '2. Profile'); para(d, PROFILE)
    h1(d, '3. Academic qualifications'); table(d, ['Institution', 'Degree', 'Year'], D.EDUCATION, [10.5, 5.0, 1.5], 9)
    h1(d, '4. Specialised training and courses'); table(d, ['Course', 'Place and date', 'Conducted by'], D.TRAINING, [7.5, 5.0, 4.5])
    h1(d, '5. Professional experience'); table(d, ['Institution', 'Position', 'From', 'To'], D.POSITIONS, [6.0, 6.0, 2.5, 2.5])
    h1(d, '6. Research grants and sponsored projects')
    para(d, '6.1 Ongoing', bold=True); table(d, ['Project', 'Funding agency', 'Role', 'Duration / status', 'Amount'], ongoing_rows(), [5.6, 3.4, 1.8, 3.4, 2.8], 8)
    if not PUBLIC:
        para(d, '6.2 Recommended or provisionally funded, awaiting sanction', bold=True); table(d, ['Project', 'Funding agency', 'Role', 'Status', 'Outlay'], D.GRANTS_PENDING, [5.6, 3.2, 2.2, 3.2, 2.8], 8)
    para(d, '6.3 Completed', bold=True); table(d, ['Project', 'Funding agency', 'Role', 'Duration', 'Amount'], D.GRANTS_COMPLETED, [5.6, 3.4, 2.6, 2.0, 3.4], 8)
    h1(d, '7. Patents (filed in India)')
    table(d, ['Title', 'Application no.', 'Status', 'Role'], D.PATENTS, [5.0, 2.4, 2.8, 6.8], 8.5)
    h1(d, '8. Awards and honours'); table(d, ['Award', 'Date'], D.AWARDS, [14.0, 3.0], 9)
    h1(d, '9. Teaching and pedagogy'); bullets(d, D.TEACHING)
    h1(d, '10. Institution-building and leadership'); bullets(d, D.LEADERSHIP)
    h1(d, '11. Memberships, editorial and expert roles'); bullets(d, D.ROLES)
    h1(d, '12. Workshops organised'); bullets(d, D.WORKSHOPS)
    h1(d, '13. Book chapters and technical documents'); bullets(d, D.CHAPTERS)
    h1(d, '14. Bibliometric summary')
    kv(d, [('Articles in PubMed (past 10 years)', D.BIBLIO['pubmed_10y']), ('h-index', D.BIBLIO['h_index']), ('Citations', D.BIBLIO['citations'] + '; i10-index ' + D.BIBLIO['i10']), ('Patents', D.BIBLIO['patents']), ('Fellowships of academies', D.BIBLIO['academies'])])
    h1(d, f'15. Publications ({len(D.PUBS)}, peer-reviewed, reverse chronological, AMA style)')
    para(d, 'Papers with more than six authors list the first three authors followed by et al. The bracket gives the role of Dr Thiruvengadam.', italic=True, size=8.5)
    for i, p in enumerate(D.PUBS, 1): cite(d, p, num=i, pmid=True, size=9)
    footer_note(d, ASOF + ' Version: ' + D.DATA_VERSION + ('' if not PUBLIC else ' (public edition)'))
    d.save(f'{OUT}/Full_CV.docx')

# ---------- 2. Two-page CV ----------
def two_page():
    d = new_doc('Two-page CV - Ramachandran Thiruvengadam', margins=1.6, size=9)
    title_block(d, P['name'], [P['quals'], P['position'] + ', ' + P['institute'], P['email'] + '  |  ORCID ' + P['orcid']])
    h1(d, 'Summary')
    para(d, 'Physician-scientist in maternal and child health. Develops and validates predictive and diagnostic tools and interventions deployable at public-health scale to reduce preterm birth, fetal growth restriction and the great obstetrical syndromes. Investigator in the GARBH-Ini pregnancy cohort programme (DBT); coordinated the clinical component of the DBT Consortium for COVID-19 Research (2020-2023). PI of two ICMR NHRP projects; Co-PI of the ICMR GRASPP trial and MOMI-India Phase II. Four Indian patent applications (three awarded).', size=9)
    h1(d, 'Education'); table(d, ['Institution', 'Degree', 'Year'], [[e[0].split(',')[0] + (', ' + e[0].split(',')[1].strip() if ',' in e[0] else ''), e[1], e[2]] for e in D.EDUCATION], [10.5, 5.8, 1.5], 8.5)
    h1(d, 'Positions'); table(d, ['Institution', 'Position', 'From', 'To'], D.POSITIONS[:6], [6.4, 6.4, 2.5, 2.5], 8.5)
    h1(d, 'Current grants'); table(d, ['Project', 'Agency', 'Role', 'Amount'], [[g[0].split(':')[0].split(' (')[0][:110], g[1], g[2], g[4]] for g in D.GRANTS_ONGOING if not (PUBLIC and g[5])][:6], [7.3, 5.0, 2.2, 3.3], 8)
    h1(d, 'Patents'); bullets(d, [f'{p[0]} (Indian application {p[1]}; {p[2].lower()})' for p in D.PATENTS], size=8.5)
    h1(d, 'Selected publications')
    for i, ix in enumerate(D.KEY_PUB_IDX, 1): cite(d, D.PUBS[ix], num=i, size=8.5)
    h1(d, 'Service and recognition')
    bullets(d, [D.AWARDS[0][0] + ' (' + D.AWARDS[0][1] + ')', D.ROLES[1], D.ROLES[2], D.ROLES[3], [a for a in D.AWARDS if a[1]=='2020'][0][0] + ' (2020)', [a for a in D.AWARDS if a[1]=='2017'][0][0] + ' (2017)'], size=8.5)
    para(d, f'h-index {D.BIBLIO["h_index"]}; citations {D.BIBLIO["citations"]}.', size=8.5)
    d.save(f'{OUT}/Two_Page_CV.docx')

# ---------- 3. DBT biodata ----------
def dbt():
    d = new_doc('DBT biodata - Ramachandran Thiruvengadam')
    title_block(d, 'BIODATA OF INVESTIGATOR', [NOTE_STD + ASOF])
    h1(d, '1. Personal details')
    kv(d, [('Name', P['name']), ('Date of birth', DOB), ('Designation', P['position']), ('Institution and address', P['institute_long'] + '. ' + P['address']), ('E-mail', P['email']), ('Domain expertise', P['domain'])])
    h1(d, '2. Educational qualifications'); table(d, ['Degree', 'Institution', 'Year'], [[e[1], e[0], e[2]] for e in D.EDUCATION], [4.0, 11.0, 2.0], 9)
    h1(d, '3. Professional experience'); table(d, ['Position', 'Institution', 'From', 'To'], [[p[1], p[0], p[2], p[3]] for p in D.POSITIONS], [5.5, 6.5, 2.5, 2.5], 8.5)
    h1(d, '4. Research projects')
    para(d, 'Ongoing (sanctioned or under implementation)', bold=True)
    table(d, ['Title', 'Funding agency', 'Role', 'Duration / status', 'Amount'], ongoing_rows(), [5.6, 3.4, 1.8, 3.4, 2.8], 8)
    if not PUBLIC:
        para(d, 'Awaiting sanction', bold=True)
        table(d, ['Title', 'Funding agency', 'Role', 'Status', 'Outlay'], D.GRANTS_PENDING, [5.6, 3.2, 2.2, 3.2, 2.8], 8)
    para(d, 'Completed', bold=True)
    table(d, ['Title', 'Funding agency', 'Role', 'Duration', 'Amount'], D.GRANTS_COMPLETED, [5.6, 3.4, 2.6, 2.0, 3.4], 8)
    h1(d, '5. Patents'); table(d, ['Title', 'Application no.', 'Status', 'Role in invention'], D.PATENTS, [5.0, 2.4, 2.8, 6.8], 8.5)
    h1(d, '6. Awards and honours'); table(d, ['Award', 'Date'], D.AWARDS, [14.0, 3.0], 9)
    h1(d, '7. Bibliometrics')
    kv(d, [('Publications listed', str(D.BIBLIO['papers_listed'])), ('PubMed (past 10 years)', D.BIBLIO['pubmed_10y']), ('h-index', D.BIBLIO['h_index']), ('Citations', D.BIBLIO['citations'])])
    h1(d, '8. Ten selected publications')
    for i, ix in enumerate(D.KEY_PUB_IDX, 1): cite(d, D.PUBS[ix], num=i, size=9)
    h1(d, '9. Declaration'); para(d, 'I certify that the particulars above are true and correct.')
    para(d, 'Place: Faridabad\t\t\t\t\t\tSignature:'); para(d, 'Date:')
    d.save(f'{OUT}/DBT_Biodata.docx')

# ---------- 4. BIRAC biodata ----------
def birac():
    d = new_doc('BIRAC biodata - Ramachandran Thiruvengadam')
    title_block(d, 'BIODATA OF PRINCIPAL INVESTIGATOR / KEY PERSONNEL', [NOTE_STD + ASOF])
    h1(d, 'A. Personal and professional details')
    kv(d, [('Name', P['name']), ('Date of birth', DOB), ('Designation and organisation', P['position'] + ', ' + P['institute_long']), ('Address', P['address']), ('E-mail', P['email']), ('Area of expertise', P['domain'])])
    h1(d, 'B. Qualifications'); table(d, ['Degree', 'Institution', 'Year'], [[e[1], e[0], e[2]] for e in D.EDUCATION], [4.0, 11.0, 2.0], 9)
    h1(d, 'C. Experience'); table(d, ['Position', 'Organisation', 'From', 'To'], [[p[1], p[0], p[2], p[3]] for p in D.POSITIONS[:7]], [5.5, 6.5, 2.5, 2.5], 8.5)
    h1(d, 'D. Funded projects (as PI / Co-PI)')
    rows = [[g[0], g[1], g[2], g[3] + (f'. {g[5]}' if g[5] else ''), g[4]] for g in D.GRANTS_ONGOING if not (PUBLIC and g[5])]
    table(d, ['Title', 'Funding agency', 'Role', 'Duration / status', 'Amount'], rows, [5.6, 3.4, 1.8, 3.4, 2.8], 8)
    table(d, ['Completed project', 'Funding agency', 'Role', 'Duration', 'Amount'], D.GRANTS_COMPLETED, [5.6, 3.4, 2.6, 2.0, 3.4], 8)
    h1(d, 'E. Intellectual property and translation')
    table(d, ['Title', 'Application no.', 'Status', 'Role in invention'], D.PATENTS, [5.0, 2.4, 2.8, 6.8], 8.5)
    para(d, 'Translational partners: IIT Madras and the Robert Bosch Centre for Data Science and AI (AI for Ultrasound, GAUGE)' + ('' if PUBLIC else '; CareMother (PRAGATI)') + '.', size=9)
    h1(d, 'F. Five relevant publications')
    for i, ix in enumerate(D.KEY_PUB_IDX[:5], 1): cite(d, D.PUBS[ix], num=i, size=9)
    h1(d, 'G. Awards'); bullets(d, [f'{a[0]} ({a[1]})' for a in D.AWARDS[:6]], size=9)
    d.save(f'{OUT}/BIRAC_Biodata.docx')

# ---------- 5. NIH-style biosketch ----------
NIH_CONTRIB = [
 ('Gestational age estimation and pregnancy dating.', 'Within the GARBH-Ini pregnancy cohort I contributed to the development and external validation of Indian population-specific models for estimating gestational age in the second and third trimesters (Garbhini-GA2), and to a comparison of first-trimester dating methods and their effect on preterm birth classification. This work underlies two Indian patent applications, including an ultrasound image-based gestational age estimation system (GAUGE).', [21, 51, 22]),
 ('Small vulnerable newborns and gestational weight gain.', 'I led the analysis of incidence and risk factors for small vulnerable newborns in the GARBH-Ini cohort and described gestational weight gain trajectories against global references, with related work on weight gain monitoring in low- and middle-income settings and on weight gain and adverse pregnancy outcomes across South Asia and sub-Saharan Africa.', [20, 46, 31, 17]),
 ('Biomarkers and multi-omics of preterm birth.', 'I contributed clinical phenotyping and epidemiology to multi-omics studies of spontaneous preterm birth in GARBH-Ini, covering genetic variants, post-GWAS integration of multi-omics data, vaginal microbiome signatures and placental proteomics.', [12, 28, 19, 18]),
 ('COVID-19 vaccine effectiveness and immunity.', 'As clinical coordinator of the DBT Consortium for COVID-19 Research I led the test-negative evaluation of ChAdOx1 nCoV-19 effectiveness during the Delta surge in India with a mechanistic immune-response study, and the clinical and experimental comparison of Omicron and Delta, and I contributed to longitudinal serology of infected individuals.', [44, 27, 50, 45]),
 ('AI-enabled obstetric ultrasound and clinical prediction models.', 'I contribute clinical expertise to AI methods for obstetric ultrasound sweeps and to clinical prediction models for pregnancy outcomes, including reviews of spontaneous preterm birth prediction and gestational diabetes prediction models.', [23, 34, 6, 15]),
]
def nih():
    d = new_doc('NIH-style biosketch - Ramachandran Thiruvengadam')
    title_block(d, 'BIOGRAPHICAL SKETCH', ['NIH-style layout, not the official NIH form. ' + ASOF])
    kv(d, [('Name', P['name']), ('Position title', P['position'] + ', BRIC-THSTI'), ('ORCID', P['orcid'])])
    h1(d, 'A. Personal statement')
    para(d, 'I am a physician-scientist (M.B.,B.S., DCH, M.D. Biochemistry, Ph.D.) working on the prediction, diagnosis and prevention of adverse pregnancy outcomes. I am an investigator in the GARBH-Ini pregnancy cohort programme and lead cohort analyses on small vulnerable newborns and gestational weight gain. I coordinated the clinical component of the DBT Consortium for COVID-19 Research and I design and co-lead trials and AI-enabled imaging projects, including the ICMR GRASPP randomised trial' + ('' if PUBLIC else ' and the PRAGATI point-of-care ultrasound project') + '. I teach epidemiology, clinical research and biostatistics to PhD and MSc students.')
    h1(d, 'B. Professional preparation'); table(d, ['Institution', 'Degree', 'Year'], D.EDUCATION, [10.5, 5.0, 1.5], 9)
    h1(d, 'C. Appointments and positions'); table(d, ['Institution', 'Position', 'From', 'To'], D.POSITIONS[:8], [6.0, 6.0, 2.5, 2.5], 8.5)
    h1(d, 'D. Honors'); bullets(d, [f'{a[0]} ({a[1]})' for a in D.AWARDS[:6]], size=9)
    h1(d, 'E. Contributions to science')
    for n, (head, txt, refs) in enumerate(NIH_CONTRIB, 1):
        p = para(d, f'{n}. {head} ', bold=True, after=1); run(p, txt)
        for ix in refs: cite(d, D.PUBS[ix], tag=False, pmid=True, size=8.5)
    h1(d, 'F. Synergistic activities'); bullets(d, [D.ROLES[1], D.ROLES[2], D.ROLES[3], D.TEACHING[1], D.TEACHING[4]], size=9)
    h1(d, 'G. Patents'); bullets(d, [f'{p[0]}. Indian application {p[1]} ({p[2].lower()}).' for p in D.PATENTS], size=9)
    d.save(f'{OUT}/NIH_Style_Biosketch.docx')

# ---------- 6. ERC-style CV ----------
def erc():
    d = new_doc('ERC-style CV - Ramachandran Thiruvengadam')
    title_block(d, 'CURRICULUM VITAE (ERC-style layout)', [NOTE_STD + ASOF])
    h1(d, 'Personal information'); kv(d, [('Name', P['name']), ('ORCID', P['orcid']), ('Web of Science ID', P['wos']), ('E-mail', P['email'])])
    h1(d, 'Education'); table(d, ['Year', 'Degree and institution'], [[e[2], e[1] + ', ' + e[0]] for e in D.EDUCATION], [2.0, 15.0], 9)
    h1(d, 'Current position'); para(d, f'{D.POSITIONS[0][1]}, {D.POSITIONS[0][0]} ({D.POSITIONS[0][2]} to date).')
    h1(d, 'Previous positions'); table(d, ['Period', 'Position and institution'], [[f'{p[2]} - {p[3]}', f'{p[1]}, {p[0]}'] for p in D.POSITIONS[1:]], [4.0, 13.0], 9)
    h1(d, 'Fellowships and awards'); table(d, ['Award', 'Date'], D.AWARDS, [14.0, 3.0], 9)
    h1(d, 'Supervision of graduate students and postdoctoral fellows')
    p = para(d, 'To be confirmed: not recorded in the master CV.'); p.runs[0].font.highlight_color = 7
    h1(d, 'Teaching activities'); bullets(d, D.TEACHING, size=9)
    h1(d, 'Organisation of scientific meetings'); bullets(d, D.WORKSHOPS, size=9)
    h1(d, 'Institutional responsibilities'); bullets(d, D.LEADERSHIP, size=9)
    h1(d, 'Commissions of trust and editorial roles'); bullets(d, D.ROLES, size=9)
    h1(d, 'Funding ID: ongoing grants'); table(d, ['Project', 'Funding agency', 'Role', 'Duration / status', 'Amount'], ongoing_rows(), [5.6, 3.4, 1.8, 3.4, 2.8], 8)
    h1(d, 'Funding ID: completed grants'); table(d, ['Project', 'Funding agency', 'Role', 'Duration', 'Amount'], D.GRANTS_COMPLETED, [5.6, 3.4, 2.6, 2.0, 3.4], 8)
    h1(d, 'Ten selected research outputs')
    for i, ix in enumerate(D.KEY_PUB_IDX, 1): cite(d, D.PUBS[ix], num=i, pmid=True, size=9)
    h1(d, 'Patents'); table(d, ['Title', 'Application no.', 'Status'], [[p[0], p[1], p[2]] for p in D.PATENTS], [10.0, 3.0, 4.0], 9)
    h1(d, 'Bibliometrics'); para(d, f'h-index {D.BIBLIO["h_index"]}; citations {D.BIBLIO["citations"]}; {D.BIBLIO["papers_listed"]} peer-reviewed articles.')
    d.save(f'{OUT}/ERC_Style_CV.docx')

# ---------- 7. Short bio ----------
def short_bio():
    d = new_doc('Short bio - Ramachandran Thiruvengadam', size=11)
    title_block(d, 'Short bio', [P['name']])
    h1(d, 'About 100 words'); para(d, D.SHORT_BIO_100, size=11)
    h1(d, 'About 200 words')
    para(d, 'Dr Ramachandran Thiruvengadam is a physician-scientist and Associate Professor in the Maternal and Child Health Programme at the BRIC-Translational Health Science and Technology Institute (THSTI), Department of Biotechnology, Government of India. He trained in paediatrics and biochemistry (DCH, M.D. at AIIMS New Delhi) and holds a Ph.D. in maternal and child health. His work develops and validates predictive and diagnostic tools and interventions to reduce adverse pregnancy outcomes such as preterm birth and fetal growth restriction. He is an investigator in the GARBH-Ini pregnancy cohort programme, where he works with multi-omics and data-science teams on biomarkers and AI-driven decision tools, and he has four Indian patent applications. During 2020-2023 he coordinated the clinical component of the DBT Consortium for COVID-19 Research. He is Principal Investigator of two ICMR National Health Research Priority projects' + ('' if PUBLIC else ' and of the ANRF PRAGATI point-of-care AI ultrasound project') + ', and Co-Principal Investigator of the ICMR GRASPP randomised trial and MOMI-India Phase II. He teaches epidemiology, clinical research and biostatistics, and serves as Academic Editor of PLOS Global Public Health and Associate Editor of Frontiers in Pediatrics.', size=11)
    d.save(f'{OUT}/Short_Bio.docx')

# ---------- 8. Publication list ----------
def publist():
    d = new_doc('Publication list - Ramachandran Thiruvengadam', size=9.5)
    title_block(d, 'PUBLICATIONS', [P['name'] + f'  |  {len(D.PUBS)} peer-reviewed articles, 2017-2026  |  ORCID ' + P['orcid'], ASOF])
    para(d, 'AMA style, reverse chronological. Papers with more than six authors list the first three followed by et al. The bracket gives the role of Dr Thiruvengadam.', italic=True, size=8.5)
    yr = None
    for i, p in enumerate(D.PUBS, 1):
        if p[3] != yr: yr = p[3]; h1(d, yr)
        cite(d, p, num=i, pmid=True, size=9)
    d.save(f'{OUT}/Publication_List.docx')

for f in (full_cv, two_page, dbt, birac, short_bio, publist): f()  # NIH-style and ERC-style layouts retired 5 Nov 2026 (per user): ICMR, DBT, BIRAC and generic CVs only
_keys = ['PERSON','BIBLIO','PROFILE','SHORT_BIO_100','EDUCATION','POSITIONS','GRANTS_ONGOING','GRANTS_PENDING','GRANTS_COMPLETED','PATENTS','AWARDS','TEACHING','LEADERSHIP','ROLES','WORKSHOPS','PUBS','DATA_VERSION']
_out = {k: getattr(D, k) for k in _keys}
if PUBLIC:
    import copy
    _out = copy.deepcopy(_out)
    _out['PERSON'].pop('dob', None)
    _out['PROFILE'] = PROFILE
    _out['GRANTS_PENDING'] = []
    _out['GRANTS_ONGOING'] = [g for g in _out['GRANTS_ONGOING'] if not g[5]]
json.dump(_out, open(f'{OUT}/cv_data.json', 'w'), ensure_ascii=False)
