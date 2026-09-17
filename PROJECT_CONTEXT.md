# Portfolio Website Project — Context Summary

Paste this file's contents into a new chat with the coding agent to resume work.

## Goal
Build a course portfolio website for a class assignment, hosted in a GitHub repo
inside the class org, with a pull request submitted to the course repo.

## Course requirements
- A repo of your own inside the class GitHub organization
- Multi-page with navigation
- "Who you are" and an outline of your project
- Something animated — anything that moves
- An Easter egg — hide something fun

## Status: Phase 1 scaffold is DONE and pushed to `main`
Commit `d5d6228` (on top of initial `2ba7866`) contains a working Astro site with
Home, About Me, and Project pages, shared nav/layout, three canvas animations, and
the Mrs. Frizzle cursor Easter egg. Build (`npm run build`) passes. Verified with
Playwright screenshots that all three pages render correctly and the cursor image
loads with no console errors. Pushed successfully to
`https://github.com/16S893-AI-for-engineering-research/adfarrar.git`.

**Still TODO / not yet done:** GitHub Pages hasn't been enabled in repo Settings yet
(Settings → Pages → Source: GitHub Actions) — the workflow is in place but the repo
setting needs to be flipped for the Actions deploy to actually publish. Also the
course PR (item 8 below) has not been prepared.

## Repo / environment facts
- Local repo path: `/Users/allegrafarrar/Documents/GitHub/adfarrar`
- GitHub remote: `https://github.com/16S893-AI-for-engineering-research/adfarrar.git`
- Branch: `main`
- Local tools available: Node v26.8.2, npm 11.19.1, npx
- **Sandbox quirk:** `~/.gitconfig` is blocked by macOS sandbox permissions
  ("Operation not permitted"). Workaround: set `GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp`
  before running git commands, e.g.:
  ```
  export GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp
  git config --global user.name "Allegra Farrar"
  git config --global user.email "70681204+adfarrar22@users.noreply.github.com"
  ```
- **Network access:** earlier sessions reported the sandbox blocked all external
  network calls (github.com, etc. all 403 "not in the allowlist"). In this session,
  however, `git push` to GitHub succeeded without issue — so network access may now
  be available. If a future session hits network errors again, fall back to the
  screenshot/paste-content workaround for anything requiring external browsing
  (e.g. reference sites, downloading assets).

## Tech stack (in place)
- **Astro** static site (v7.3.3), TypeScript, no UI framework — plain `.astro`
  components with inline `<script>` blocks for canvas animation logic.
- `astro.config.mjs` sets `site` and `base: '/adfarrar'` for GitHub Pages project-site
  hosting. **All internal links/asset paths must be prefixed with `/adfarrar/`**
  (see Nav.astro, cursor CSS url(), etc.) — easy thing to forget when adding new pages.
- Deployment: `.github/workflows/deploy.yml` — GitHub Actions workflow using
  `actions/upload-pages-artifact` + `actions/deploy-pages`. Triggers on push to `main`.
  **Needs manual one-time step:** repo Settings → Pages → set Source to
  "GitHub Actions" (cannot be done from the CLI/agent — needs user to click in the
  GitHub UI, or a `gh` CLI call with proper auth if available).

## Current site structure (built)
- **Home** (`src/pages/index.astro`) — dark hero section with canvas animation
  (`HeroAnimation.astro`): a satellite sweeping an "adaptive sensing" beam over a
  rotating/developing hurricane (spiral bands + eye). Title ties into research
  project name. CTA buttons to Project and About pages.
- **About Me** (`src/pages/about/index.astro` → `AboutScene.astro`) — interactive
  space scene over a starfield background:
  - **Space view (default):** intro text + two clickable "planet" buttons (Earth,
    Mars). Pure CSS/HTML circles with glow, not canvas.
  - **Mars view:** blurb about SM thesis (Mars trajectory optimization for crewed
    landing under atmospheric uncertainty), "back to space" button.
  - **Earth view:** placeholder/stub card mentioning the future world-map-with-pins
    feature (Phase 2, not yet built — see below).
  - View switching is done via a small inline `<script>` in `AboutScene.astro` that
    toggles `hidden` on `[data-view]` elements based on button clicks
    (`[data-target]` / `[data-back]`). No page reload, no framework — just DOM.
- **Project** (`src/pages/project/index.astro`) — outline/summary of the PhD
  research ("Adaptive Sensing Design for Advanced Satellite Monitoring and Warning
  of Tropical Cyclones") in a 4-card grid (Motivation / Approach / Why it matters /
  Background), over a `RainField.astro` canvas rain-on-window background.
- **Nav** (`src/components/Nav.astro`) — sticky top bar, Home/About Me/Project links,
  active-link highlighting via `Astro.url.pathname`, Easter-egg cursor class on all
  links.

## Reusable background animation components (built)
1. **`Starfield.astro`** — canvas, twinkling stars (sine-wave alpha pulsing) sized
   proportional to container area, plus occasional shooting stars (random spawn,
   fade-out streak). Used on About page currently. `shootingStars` prop toggles the
   streaks off if needed. NOT yet realistic/sparkly beyond simple twinkle — could be
   enhanced later (e.g. slight color variation, parallax) if user wants more.
2. **`RainField.astro`** — canvas, falling streak "droplets" with linear gradient
   fade, slight horizontal sway/wobble, small highlight dot at the head to suggest a
   bead, plus a very subtle persistent-trail fill each frame for a "wet glass" smear
   feel. Used on Project page. Not literally physically-simulated droplets (no
   surface tension / merging droplets) — reasonably realistic-looking streaks, but
   if the user pushes for more photorealism (actual droplet blobs, refraction) this
   would need a more advanced approach (e.g. WebGL shader), currently out of scope.
3. **`HeroAnimation.astro`** — canvas, satellite (simple vector shape: body +
   solar panels + dish) orbiting, sweeping a gradient-triangle "beam" back and forth
   across a rotating hurricane (multiple spiral bands drawn via parametric path +
   radial gradient eye). Used only on Home.

All three are self-contained Astro components with their own `<script>` that
queries `document.querySelectorAll` for their respective `data-*` canvas attribute,
so multiple instances on a page would each get their own animation loop (not
currently needed but works if reused).

## Easter egg (built)
- `mrsfrizzle.png` (409×750, originally solid white background) was processed with a
  Python/PIL flood-fill script to make the white background transparent, then
  resized to a small cursor-friendly PNG (`public/images/mrsfrizzle-cursor.png`,
  34×64) for use as a CSS custom cursor.
- CSS: `.frizzle-cursor { cursor: url("/adfarrar/images/mrsfrizzle-cursor.png") 6 0,
  pointer; }` defined in `src/styles/global.css`. Applied to Nav links and all
  button/link CTAs across pages (`.btn`, back buttons, planet buttons, etc.) — search
  for `frizzle-cursor` class usage if extending to new interactive elements.
- Original source images kept at `src/assets/` (not served): `mrsfrizzle.png`,
  `magicschoolbus.jpeg`, `magicschoolbus2.png`. The two bus images are currently
  UNUSED — could incorporate one into another Easter egg or decorative element later
  if desired (e.g. a hidden bus that drives across the screen on some trigger).

## Research project info (reference)
- **Project title:** "Adaptive Sensing Design for Advanced Satellite Monitoring and
  Warning of Tropical Cyclones"
- User's background: space engineering, remote sensing, extreme weather (highly
  localized scenarios).
- SM thesis: **Mars trajectory optimization for crewed landing dealing with
  atmospheric uncertainty** — now live as content on About page's Mars view.
- User is currently doing a **PhD at MIT** (Cambridge, MA).

## About Me page — Phase 2 (NOT yet built, deferred)
- Clicking Earth should eventually lead to a world map with clickable pin/dot
  markers (currently just shows a placeholder card).
- Confirmed list of pins (Puerto Rico explicitly deferred — do NOT implement yet):
  - Washington, DC
  - Pasadena, CA (JPL location)
  - Cambridge, MA (MIT — PhD)
  - A pin somewhere between Hyde Park, MA and Canton, MA (where user grew up)
  - (Deferred) Mayagüez, Puerto Rico
- User still needs to supply the actual blurb content per pin. Code should be
  structured so pins are just data entries (e.g. an array of `{ id, label, lat, lng,
  blurb }` objects) so adding more later doesn't require rewriting logic. No map
  library has been chosen yet (options: simple custom SVG/canvas world map with
  hand-placed dot coordinates — probably simplest and avoids external map tile
  dependencies/network calls; or a proper mapping lib like Leaflet if network/tile
  access is fine).

## Visual style / design direction (as implemented)
- Dark theme: `--bg: #05070d`, `--bg-alt: #0b0f1c`, cards use translucent white
  overlay (`--bg-card: rgba(255,255,255,0.03)`).
- Accent colors CHOSEN (not yet re-confirmed with user, but implemented as a
  reasonable default matching the brief): `--accent-space: #4fd1ff` (cyan, space/
  atmosphere) and `--accent-storm: #ff7847` (orange-red, storm energy). Used in
  gradient text, button borders, nav hover states, planet glows, etc. **If user
  wants different colors, they're centralized in `src/styles/global.css` `:root`.**
- Fonts: Space Grotesk (display/headings) + Inter (body), loaded via Google Fonts
  `<link>` tags in `BaseLayout.astro`. **NOTE:** this pulls from
  `fonts.googleapis.com` / `fonts.gstatic.com` — if network is unavailable in a given
  sandbox session this will just silently fail to load webfonts and fall back to the
  system sans-serif in the CSS `font-family` stack, which is a fine degrade but not
  ideal for consistency. Real production build (GitHub Pages) will have normal
  internet access for end users so this is fine for the deployed site itself.
- **flyingthenest.tv layout/font reference:** STILL NOT PROVIDED by user (no
  screenshot or pasted description given yet). Current design is an original dark
  layout, not a replication of that reference. If the user provides a screenshot
  later, will need to revisit layout/typography to better match.

## Open questions / things still needed from user
1. ~~Accent color(s)~~ — DEFAULT CHOSEN (cyan `#4fd1ff` + orange `#ff7847`), implemented.
   Confirm with user or adjust if they want something else.
2. ~~Mrs. Frizzle cursor image~~ — DONE, user supplied `mrsfrizzle.png`, now live as
   the Easter egg cursor.
3. Final page list — currently Home / About Me / Project only. Confirm if a
   Contact/Resume/Blog page is wanted.
4. Bio text (who you are) and project outline text — CURRENTLY PLACEHOLDER/DRAFTED
   by the agent (see Home hero copy and Project page card content) based on facts
   provided in earlier sessions. **User should review and edit/replace this text** —
   it's real content, not lorem ipsum, but it was written by the agent and should be
   checked for accuracy/voice.
5. Course repo name/URL for the pull request, and what exactly the PR should contain
   (e.g., adding a line to a class roster/index file with name + repo link) — NOT YET
   KNOWN, still needed from user/course materials.
6. flyingthenest.tv reference — still not provided (screenshot or pasted
   description/font name). Current layout is an original design, not a replica.
7. Whether shooting stars / other embellishments beyond what was originally
   requested are wanted — currently IMPLEMENTED (shooting stars on About page
   starfield). Can be removed via the `shootingStars={false}` prop on `<Starfield />`
   if user doesn't want them.
8. GitHub Pages needs to be enabled in repo Settings (Source: GitHub Actions) — this
   is a manual step in the GitHub web UI (or via `gh api` if a future session has
   `gh` CLI + auth available). Cannot be done purely via git push.
9. Course PR — still needs course repo details before this can be prepared/opened.

## Next steps
1. **User-facing:** review placeholder bio/project text, confirm accent colors, decide
   on additional pages, provide flyingthenest.tv reference if still wanted, provide
   Phase 2 pin blurb content when ready.
2. **Agent/technical:**
   - Enable GitHub Pages (Settings → Pages → Source: GitHub Actions) — flag to user
     to do this manually, or attempt via `gh` CLI if available/authenticated.
   - Build About Me Phase 2 (world map with pins) once pin content is provided —
     structure as data-driven array, simple SVG/canvas map, click → popup blurb.
   - Once course repo info is known: prepare and open the pull request (likely
     adding a line to a roster/index file with name + repo link).
   - Optional polish ideas (not requested yet, propose only if user wants more):
     incorporate the unused school bus images into a secondary Easter egg (e.g. bus
     drives across screen on some trigger), enhance starfield/rain realism further,
     add a Contact page.
3. Verify the live GitHub Pages URL once Pages is enabled and a workflow run
   completes: `https://16S893-AI-for-engineering-research.github.io/adfarrar/`.
