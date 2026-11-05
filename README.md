# Ramachandran Thiruvengadam: CV website (public edition)

Static website served by GitHub Pages at https://ramthiru83.github.io/cv/

## Pages
index.html (Home), about.html, research.html, publications.html, cv.html (Downloads: CV formats, template fill, photographs), admin.html (owner sign-in, editing).

## Shared files
site.css and site.js: styling, header, footer and the content loader.
cv_data.json: public-edition data. It is the fallback; live content is read first from the Supabase table site_content.
portrait.jpg, portrait-2.jpg: web images. Ramachandran_Thiruvengadam_photo_1.jpg and _photo_2.jpg: full-resolution photographs for download.

## Folders
docx/ and pdf/: the standard CV files (BIRAC, DBT, ERC-style, Full CV, ICMR short resume, NIH-style biosketch, publication list, short bio, two-page CV). They are fixed copies; admin edits do not regenerate them.

## Backend (Supabase project, not in this repository)
cv-portal edge function: download log and template filling.
cv-admin edge function: admin sign-in and content saving.

## Rule
Public edition only. Never add the full edition (date of birth, mobile number, unsanctioned grants) to this repository.
