# CV site: where everything lives and how it stays in sync

Updated 5 Nov 2026 (publications now 66: 63 from PubMed plus 3 verified from Google Scholar; CV downloads are also emailed to the requester; monthly automatic CV rebuild added).

| Place | What it holds | Master? |
|---|---|---|
| Computer: ~/Sites/cv-site | The website files, exactly as on GitHub | Master for site files |
| Computer: ~/Sites/cv-backend | Supabase source: edge functions cv-portal and cv-admin, schema.sql | Master for backend code |
| GitHub: RamThiru83/cv (main) | Published copy of ~/Sites/cv-site, served at https://ramthiru83.github.io/cv/ | Copy |
| Supabase vpcfegnfzulpxcmoittm | Edge functions (deployed copy of cv-backend), tables, secrets | Master for live text edited in /admin.html, and the download log |
| Claude Project "Ram CV pack" | Copy of the site files and backend source | Copy |

## Rules
1. Site files (html, css, js, docx, pdf, images): change them in ~/Sites/cv-site; Claude then uploads and commits the changed files to GitHub through Chrome and checks the live copy against the manifest below.
2. Wording on the pages: edit in /admin.html and press Publish. It is stored in Supabase and shown at once; GitHub is not involved. cv_data.json on GitHub is only the fallback if Supabase is unreachable, and matches the Supabase content as of 5 Nov 2026.
3. Backend code: change in ~/Sites/cv-backend, then redeploy to Supabase (ask Claude). Secrets (ANTHROPIC_API_KEY, ADMIN_PASSPHRASE) exist only in Supabase and are never stored in any folder or in GitHub. NTFY_TOPIC is no longer used.
4. Standard Word and PDF files (docx/, pdf/) are static: edits in admin do not regenerate them. They are built by ~/Sites/cv-backend/generator (cvdata.py, build_cvs.py, fill_icmr.py). Formats kept: ICMR short resume, DBT, BIRAC, Full CV, Two-page CV, Publication list, Short bio. NIH-style and ERC-style were retired on 5 Nov 2026.
5. Publication list source: PubMed search "Ramachandran Thiruvengadam" (63 results on 5 Nov 2026), plus Google Scholar papers that were checked on Crossref or the publisher page (3 added on 5 Nov 2026: BMC Pregnancy Childbirth 2026, J Anat Soc India 2026, F1000Research 2024), and Google Scholar for citation counts (3,956; h-index 22; i10 31). Preprints, conference abstracts and items where he is not an author are left out.
6. Automatic updates. Weekly (Claude scheduled task): fetches PubMed, Crossref and Google Scholar, adds verified new papers to the live site content in Supabase, and reports anything it could not verify. Monthly (GitHub Action .github/workflows/monthly-cv.yml, 1st of each month 03:17 UTC): rebuilds the six standard Word and PDF CVs from the live Supabase content with generator/ and commits them; the ICMR short resume is not rebuilt automatically. If the page-count check fails the job stops and nothing is overwritten.
7. Emailing CVs: cv-portal sends each requested CV to the visitor through Gmail SMTP. It needs two Supabase secrets, SMTP_USER and SMTP_PASS (a Google app password). Until they are set the page says email is not switched on and the download still works.

## Site file manifest (first 16 characters of SHA-256)
c6bb59af2a0541a0  .github/workflows/monthly-cv.yml
24cd8b37eca60554  README.md
b2c6090c17713773  Ramachandran_Thiruvengadam_photo_1.jpg
6258632812d83efa  Ramachandran_Thiruvengadam_photo_2.jpg
47b7688a5ad37ea4  about.html
a6233cc51af9b08f  admin.html
206077f25446039a  cv.html
9140b2a1fdf3121a  cv_data.json
988942dd455f9899  docx/BIRAC_Biodata.docx
4fdd1be0a17c5b4e  docx/DBT_Biodata.docx
3fc7363c7d461a1f  docx/Full_CV.docx
45923a5ed43f8f96  docx/ICMR_Short_Resume.docx
94079b2b211bd5ac  docx/Publication_List.docx
2ee935006b3bc5fe  docx/Short_Bio.docx
b33707def687f40f  docx/Two_Page_CV.docx
86ca492d19cee01a  generator/README.md
c68e61495a9e813a  generator/build_cvs.py
bd85a5bd092c81f5  generator/cvdata.py
fb6c2ffd21e287fc  index.html
90f313291af98d32  pdf/BIRAC_Biodata.pdf
9d74a03311634816  pdf/DBT_Biodata.pdf
4d88997888a84969  pdf/Full_CV.pdf
75fdaa5bbac4cac5  pdf/ICMR_Short_Resume.pdf
35d895fbfdf64799  pdf/Publication_List.pdf
16bb9b84e48389f5  pdf/Short_Bio.pdf
0fca72c36b6f56db  pdf/Two_Page_CV.pdf
a887040619972d94  portrait-2.jpg
ea96f4f62930c165  portrait.jpg
802ea2199f32bed7  publications.html
374516e37b83eafb  research.html
74bae0d78c4a1f6e  site.css
b61bd62fb5f437c9  site.js
