# Ramachandran Thiruvengadam: CV website (public edition)

Static pages for GitHub Pages: index, about, research, publications, cv (Downloads), admin.

- `cv_data.json`: public-edition data and fallback copy. Live content is read first from Supabase (`site_content`).
- `docx/`, `pdf/`: standard CV files (static; admin edits do not regenerate them).
- `img/`: portraits; `img/download/`: full-resolution photographs for the Downloads page.
- `admin.html`: passphrase sign-in (secret `ADMIN_PASSPHRASE` on the `cv-admin` edge function); edits, publishes, restores versions, shows the download log.
- Template filling and download alerts: edge function `cv-portal` (secrets `ANTHROPIC_API_KEY`, `NTFY_TOPIC`).

Never add the full edition (date of birth, mobile number, unsanctioned grants) to this repository.
