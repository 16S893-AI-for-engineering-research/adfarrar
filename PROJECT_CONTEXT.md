# Project context — portfolio site

Working notes for resuming work on this repo. The [README](README.md) covers the
site itself; this file tracks state, decisions, and what's still open.

## Status

Site is rebuilt and live-ready: five pages, real content structure, new palette.
Assignment 1 requirements are all met (own repo in the class org, multi-page nav,
who-I-am + project outline, animation, Easter egg).

## Environment

- Local path: `/Users/allegrafarrar/Documents/GitHub/adfarrar`
- Remote: `https://github.com/16S893-AI-for-engineering-research/adfarrar.git`, branch `main`
- **Sandbox quirk:** `~/.gitconfig` is blocked by macOS sandbox permissions. Set
  `GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp` before git commands:
  ```sh
  export GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp
  git config --global user.name "Allegra Farrar"
  git config --global user.email "70681204+adfarrar22@users.noreply.github.com"
  ```
- Network access works (pushes succeed, external fetches succeed). Earlier sessions
  reported it blocked; that is no longer the case.
- Playwright is installed/uninstalled as needed for screenshot verification. Install
  with `npm i -D playwright && npx playwright install chromium`, then remove when done.

## Design decisions

- **Palette** comes from the `Ocean-darkmode` theme inside
  `supplemental-info/JPLSURPSeminarV2_Aug2026.pptx` (read from `ppt/theme/theme1.xml`
  after unzipping). Blue `#00AFFF`, cyan `#52CADB`, pale `#ACD6E1`, mint `#7CD0BC`,
  coral `#FA5A67`, sand `#F9D095`, navy `#031154`. Centralised in `:root` in
  `src/styles/global.css`.
- **Fonts:** Space Grotesk (display) + JetBrains Mono (labels/eyebrows/data).
- **Layout influences** (both reviewed in full, HTML+CSS fetched):
  - Ben McCloskey's site — bordered 3-up "entry-grid" route cards on Home, dev-log
    badge system, eyebrow/kicker labels.
  - Bjarni Kristinsson's site — About page order (photo + bio → timeline → scope),
    `.reveal` scroll animation, card hover lift, `.grad-text` sheen.
- **Scrollytelling** is deliberately loose: `.reveal` fires at 8% visibility with a
  -8% bottom root margin, so the next section is already visible while reading the
  current one (explicit request: "scrolly telly can flow").
- **Base path:** `astro.config.mjs` sets `base: '/adfarrar'`. All internal links use
  `import.meta.env.BASE_URL` — do not hardcode `/adfarrar/` in new pages, except the
  cursor `url()` in CSS which cannot read env vars.

## Rejected in review (v1 → v2)

The first build was scrapped for looking like a generic dark template. Specifically
removed: the hurricane-spiral hero graphic, the shooting stars (disorienting), the
rain-on-window background, and the abstract Earth/Mars circles that overlapped the
About page text. `Starfield.astro`, `RainField.astro`, `HeroAnimation.astro`, and
`AboutScene.astro` were deleted outright rather than left unused.

## Content still to write

Everything marked `[Placeholder]` in the source. Structure is up so the layout can
be judged; wording is Allegra's to write.

- **About:** research-interests wording, both motivation cards (Katrina / *When the
  Levees Broke*, and the Mars-methodology link), all seven timeline descriptions,
  all four "beyond the thesis" cards.
- **Orrery modals:** the JWST/L2 internship copy, the dance section copy and photo
  caption. Mars modal is written from the CV and is close to final.
- **Map pins** (`src/data/pins.ts`): six pins in place (Hyde Park/Canton, DC,
  Cambridge, Pasadena, Mayagüez, Luanda) with placeholder blurbs.
- **Project page** is scaffolded from the SURP deck and is fairly complete, but the
  language should be reviewed.

## Open items

1. **GitHub Pages** must be enabled once in the repo UI: Settings → Pages → Source →
   **GitHub Actions**. Cannot be done from the CLI without `gh` auth (`gh` is not
   installed in this sandbox).
2. **Class PR** — the class repo is `16S893-AI-for-engineering-research/class-repo`
   (clonable, though not listed in the org's public repo index). The file to edit is
   `content/students.json`, a flat `{"Name": "url"}` map. Add:
   `"Allegra Farrar": "https://16s893-ai-for-engineering-research.github.io/adfarrar/"`
   Per the orientation slides, the PR must be read before it is opened.
3. Unused assets: `src/assets/magicschoolbus.jpeg`, `magicschoolbus2.png` — could
   become a second Easter egg (a bus driving across the screen) if wanted.
   `public/images/me-presenting*.jpg`, `me-aeroafro.png`, `me-astronaut.jpg` are
   web-sized and available for a photo strip on About if desired.
4. Not verified: cross-browser rendering beyond Chromium; the inline PDF `<object>`
   viewer on the CV page is untested in Firefox and Safari (it has a download
   fallback).

## Verification habits used here

- `npm run build` after every page change.
- Playwright screenshots at 1440×950 and 390×844, scrolling the full page to trigger
  reveals, plus a console/pageerror check on all five routes.
- A DOM overflow probe (`getBoundingClientRect().right > clientWidth`) caught the
  five-item nav bar pushing the mobile viewport to 422px; fixed by stacking the nav
  under 620px and clipping `html` overflow-x.
- The Natural Earth world path was rendered to PNG and inspected before being wired
  into the Earth modal.
