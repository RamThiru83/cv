// Shared header, footer and data loader for every page.
(function () {
  const PAGES = [['index.html', 'Home'], ['about.html', 'About'], ['research.html', 'Research'], ['publications.html', 'Publications'], ['cv.html', 'Downloads']];
  const here = (location.pathname.split('/').pop() || 'index.html');
  const nav = PAGES.map(([h, t]) => `<a href="${h}"${h === here ? ' aria-current="page"' : ''}${h === 'cv.html' ? ' class="cta"' : ''}>${t}</a>`).join('');
  const hdr = document.getElementById('hdr');
  if (hdr) hdr.innerHTML = `<a class="skip" href="#main">Skip to content</a><div class="bar"><div class="wrap"><a class="mark" href="index.html">Ramachandran Thiruvengadam</a><button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M3 6h14M3 10h14M3 14h14"/></svg></button><nav class="nav" id="nav" aria-label="Primary">${nav}</nav></div></div>`;
  const b = document.querySelector('.burger');
  if (b) b.addEventListener('click', () => { const o = document.getElementById('nav').classList.toggle('open'); b.setAttribute('aria-expanded', o); });
  const ftr = document.getElementById('ftr');
  if (ftr) ftr.innerHTML = `<div class="wrap"><div class="fgrid"><div><div class="mark" style="margin-bottom:.5rem">Ramachandran Thiruvengadam</div><p data-t="footer_text" style="margin:0;max-width:24rem">Physician-scientist, Associate Professor, Maternal and Child Health Programme, BRIC-Translational Health Science and Technology Institute, Faridabad, India.</p></div><div><h4>Site</h4><a href="about.html">About</a><a href="research.html">Research</a><a href="publications.html">Publications</a><a href="cv.html">Downloads</a></div><div><h4>Profiles</h4><a id="f-orcid" href="https://orcid.org/0000-0002-9195-2730" rel="noopener">ORCID</a><a id="f-scholar" href="https://scholar.google.com/citations?user=2yFI5XoAAAAJ" rel="noopener">Google Scholar</a><a id="f-mail" href="about.html#contact">Contact</a></div></div><div class="legal"><span id="ver">Public edition.</span><span><a href="admin.html" style="display:inline;opacity:.6">Admin</a> &nbsp;·&nbsp; Views are the author's own.</span></div></div>`;

  const esc = (s) => String(s ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const SB = 'https://vpcfegnfzulpxcmoittm.supabase.co', KEY = 'sb_publishable_bEsBtP1gqRe9ovzKci91Uw_gTHt02ov';
  const DEFAULT_SITE = {
    hero_eyebrow: 'Physician-scientist \u00b7 Maternal and child health',
    hero_title: 'Better tools to protect mothers and babies.',
    hero_lede: 'Dr Ramachandran Thiruvengadam is an Associate Professor at BRIC-THSTI, Faridabad. His group develops prediction models, AI-enabled imaging and trials to reduce adverse pregnancy outcomes.',
    hero_tag: 'M.D., Ph.D. \u00b7 BRIC-THSTI',
    focus_title: 'Four lines of work, one aim',
    focus_sub: 'Reduce preterm birth, fetal growth restriction and other adverse outcomes with tools that work at public-health scale.',
    band_title: 'Need a CV for a funding call?',
    band_text: 'ICMR, DBT, BIRAC, NIH-style and ERC-style layouts as Word or PDF, or upload the funder\u2019s template.',
    research_title: 'Prediction, imaging and prevention',
    research_lede: 'Work that moves from cohorts and biomarkers to tools that clinicians and programmes can use.',
    about_title: 'Physician, researcher, teacher',
    about_lede: 'Trained in paediatrics and biochemistry, with a Ph.D. in maternal and child health.',
    pubs_title: 'Peer-reviewed articles',
    pubs_lede: 'Search by title, author or journal, and filter by year or authorship role.',
    dl_title: 'CV and photograph',
    dl_lede: 'A few quick questions come first, so each download reaches the right person and purpose.',
    footer_text: 'Physician-scientist, Associate Professor, Maternal and Child Health Programme, BRIC-Translational Health Science and Technology Institute, Faridabad, India.',
    themes: [
      ['Clinical prediction models', 'Developing and validating risk and dating models for pregnancy outcomes.', 'Developing and validating predictive and diagnostic tools for adverse pregnancy outcomes such as preterm birth and fetal growth restriction, using robustly designed cohort studies and pooled analyses.'],
      ['AI-enabled imaging', 'Point-of-care obstetric ultrasound tools, including gestational age estimation (GAUGE).', 'Point-of-care obstetric ultrasound tools, including the patented Garbh-Ini gestational age estimation system (GAUGE), built with IIT Madras and the Robert Bosch Centre for Data Science and AI.'],
      ['Multi-omics and biomarkers', 'Biomarker discovery for preterm birth within the GARBH-Ini cohort programme.', 'Biomarker discovery for preterm birth and other outcomes within the GARBH-Ini programme, working with multi-omics and data-science teams.'],
      ['Trials and epidemiology', 'Randomised trials, cohort studies and pooled analyses across Indian and global cohorts.', 'Randomised trials such as GRASPP, large cohort analyses of small vulnerable newborns and gestational weight gain, and the Multi-Omics for Mothers and Infants (MOMI) consortium.']
    ]
  };
  const getJson = (url, headers) => fetch(url, { headers, signal: AbortSignal.timeout(6000) }).then((r) => { if (!r.ok) throw new Error(r.status); return r.json(); });
  let cache;
  const data = () => cache || (cache = (async () => {
    let d = null;
    try { const rows = await getJson(SB + '/rest/v1/site_content?key=eq.cv_data&select=value', { apikey: KEY }); if (rows && rows[0] && rows[0].value) d = rows[0].value; } catch (_) {}
    if (!d) { try { d = await getJson('cv_data.json'); } catch (_) { return null; } }
    d.SITE = Object.assign({}, DEFAULT_SITE, d.SITE || {});
    const v = document.getElementById('ver'); if (v && d.DATA_VERSION) v.textContent = 'Public edition. Data as of ' + String(d.DATA_VERSION).split(' (')[0] + '.';
    const o = document.getElementById('f-orcid'); if (o && d.PERSON && d.PERSON.orcid) o.href = 'https://orcid.org/' + d.PERSON.orcid;
    const sc = document.getElementById('f-scholar'); if (sc && d.PERSON && d.PERSON.scholar) sc.href = d.PERSON.scholar;
    document.querySelectorAll('[data-t]').forEach((el) => { const t = d.SITE[el.dataset.t]; if (typeof t === 'string' && t) el.textContent = t; });
    return d;
  })());
  const boldMe = (au) => esc(au).replace(/(Thiruvengadam R)/g, '<b>$1</b>');
  const pubHtml = (p) => `<article class="pub"><div class="ti">${esc(p[1])}</div><div class="au">${boldMe(p[0])}</div><div class="jr"><i>${esc(p[2])}</i> ${esc(p[3])}${p[4] ? ';' + esc(p[4]) : ''}</div><div class="lk">${p[7] ? `<span class="chip n">${esc(p[7])}</span>` : ''}${p[6] ? `<a href="https://pubmed.ncbi.nlm.nih.gov/${esc(p[6])}/" rel="noopener">PubMed</a>` : ''}${p[5] ? `<a href="https://doi.org/${esc(p[5])}" rel="noopener">DOI</a>` : ''}</div></article>`;
  window.CV = { data, esc, boldMe, pubHtml, DEFAULT_SITE, SB, KEY };
})();
