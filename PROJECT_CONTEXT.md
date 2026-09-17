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

## Repo / environment facts (already confirmed)
- Local repo path: `/Users/allegrafarrar/Documents/GitHub/adfarrar`
- GitHub remote: `https://github.com/16S893-AI-for-engineering-research/adfarrar.git`
- Branch: `main`, currently just has a `README.md` ("# adfarrar / Class Portfolio")
- Local tools available: Node v26.8.2, npm 11.19.1, npx, Ruby 2.6.10 (Jekyll possible
  but decided against it — see decision below)
- **Sandbox quirk:** `~/.gitconfig` is blocked by macOS sandbox permissions
  ("Operation not permitted"). Workaround: set `GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp`
  before running git commands, e.g.:
  ```
  export GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp
  git config --global user.name "Allegra Farrar"
  git config --global user.email "..."
  ```
- **No internet access** in this sandbox for the agent — network calls are locked to
  an allowlist and even github.com / raw.githubusercontent.com / arbitrary sites are
  blocked (confirmed via curl, got 403 "not in the allowlist"). So the agent **cannot
  browse reference websites** (e.g., flyingthenest.tv) directly.
  - Workaround for design references: user should take a **screenshot** and save it
    into the repo folder (or provide a path) so the agent can read it as an image file,
    or paste the visible text/HTML content directly into chat.

## Tech stack decision
- **Astro** (static site generator, compiles to static HTML/CSS/JS, deploys great on
  GitHub Pages) — chosen over Jekyll because the user wants richer, more realistic
  animations (canvas-based rain droplets, twinkling stars, satellite/hurricane hero
  animation) and classmates are also using Astro.
- Content should live in clean Markdown/MDX files with front-matter so the user can
  edit content without touching layout/animation code.
- Shared layout component for nav bar (edit once, updates everywhere).

## Site structure (planned)
- **Home** — dark theme landing page with animated hero graphic: a satellite doing
  "adaptive sensing" (sweeping beam) over a developing/rotating hurricane graphic.
  Page ties into research project title (see below).
- **About Me** — big animated interactive page (see phased plan below).
- **Project** — outline/description of research project. Possibly uses the starry
  night sky background.
- Possibly a Contact/Links page — not yet decided, TBD with user.
- Nav bar appears on all pages, with Easter egg cursor (see below).

## Research project info
- **Project title:** "Adaptive Sensing Design for Advanced Satellite Monitoring and
  Warning of Tropical Cyclones"
- User's background: space engineering, remote sensing, extreme weather (highly
  localized scenarios).
- User has an SM thesis on **Mars trajectory optimization for crewed landing dealing
  with atmospheric uncertainty** — this becomes content on the About Me page's Mars
  view (see below).
- User is currently doing a **PhD at MIT** (Cambridge, MA) — relevant for map pin.

## About Me page — phased interactive animation plan
Big creative concept, to be built in phases (user explicitly said: implement basic
version first, more advanced parts later).

**Phase 1 (build first):**
- Space view: user starts "hovering over Earth's atmosphere" in space; Earth and Mars
  both visible.
- Click Mars → zoom/transition to Mars view → shows blurb about SM thesis (Mars
  trajectory optimization for crewed landing, atmospheric uncertainty).
- Button/link to go back to space view.
- Click Earth → transitions toward Earth (leads into Phase 2 world map).

**Phase 2 (build later, defer for now):**
- Clicking Earth leads to a world map with clickable pin/dot markers.
- Clicking a pin pops up a blurb about the user related to that location.
- Confirmed list of pins (Puerto Rico explicitly deferred — do NOT implement yet):
  - Washington, DC
  - Pasadena, CA (JPL location)
  - Cambridge, MA (MIT — PhD)
  - A pin somewhere between Hyde Park, MA and Canton, MA (where user grew up)
  - (Deferred) Mayagüez, Puerto Rico
- User will supply the actual blurb content per pin later; code should be structured
  so pins are just data entries (easy to add more later without rewriting logic).

## Visual style / design direction
- **Dark mode**, mostly black, with a few color "pop" accents (specific accent colors
  not yet chosen — still needs user input, e.g. warm orange/red for storm energy vs.
  cyan/blue for space/atmosphere, or both).
- Multiple distinct **background animations** needed, reusable across pages:
  1. **Starry night sky** — dark background, small stars with slight flickering
     ("twinkle"), ideally realistic/sparkly not just flat CSS — likely canvas-based.
     Maybe include slow drifting "shooting stars" for extra life (agent's suggestion,
     not yet confirmed by user).
  2. **Rain on a window** — realistic-looking rain droplets falling against a dark
     background, like rain on a window pane (droplet formation, gravity/streaking,
     slight blur/refraction realism) — likely canvas-based for realism, not simple
     CSS lines.
  3. **Home hero graphic** — animated satellite performing "adaptive sensing" (sweep
     beam) over a rotating/developing hurricane (spiral cloud bands).
- User wants animations to look **realistic** — explicitly said "real water droplets
  against a black backdrop" and "realistic looking sparkly" (stars), not cartoonish
  or simplistic CSS effects.
- **Layout/font reference:** user likes the layout and font of
  https://www.flyingthenest.tv/ — agent could NOT access this site (no internet in
  sandbox). **Still need:** either a screenshot saved into the repo/provided path, or
  pasted text/description of the layout and font name, so agent can replicate.

## Easter egg
- On hover over embedded links (e.g., the nav bar menu items), the cursor icon should
  change to an icon of **Mrs. Frizzle** from The Magic School Bus.
- Agent cannot generate copyrighted character artwork. **Still need:** user to supply
  a small PNG/SVG image file (ideally transparent background) of Mrs. Frizzle, saved
  into the repo or with a path the agent can read. Until then, a placeholder
  "wacky teacher" CSS cursor could stand in.

## Open questions / things still needed from user (as of last message)
1. Accent color(s) for the dark theme's color "pops" — or should agent propose a palette?
2. Mrs. Frizzle cursor image file (path/location) — or proceed with placeholder for now?
3. Confirm final page list: Home, About Me, Project — anything else (Contact, Resume, Blog)?
4. Bio text (who you are) and project outline/summary text — even rough bullet points OK.
5. Course repo name/URL for the pull request, and what exactly the PR should contain
   (e.g., adding a line to a class roster/index file with name + repo link).
6. flyingthenest.tv reference — screenshot file (path) or pasted description/font name,
   since agent cannot browse the internet.
7. Confirm whether shooting stars / other embellishments beyond what user specified
   are wanted, or keep strictly to what was requested.

## Next steps once above info is provided
1. Scaffold Astro project in this repo (`npm create astro@latest` or manual setup).
2. Build shared layout + nav component with Easter egg cursor.
3. Build Home page with satellite/hurricane hero animation.
4. Build About Me page Phase 1 (space view → Mars view → back; Earth click stubbed
   or leads into Phase 2 placeholder).
5. Build Project page with content outline (starry sky background candidate).
6. Build starry sky and rain-on-window background components as reusable pieces.
7. Set up GitHub Pages deployment (GitHub Actions workflow for Astro) using the
   git workaround (`GIT_CONFIG_GLOBAL=/tmp/gitconfig_temp`) for any git operations.
8. Prepare and open the pull request to the course repo once its requirements are known.
