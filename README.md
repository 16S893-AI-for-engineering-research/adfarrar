# Allegra Farrar — Class Portfolio

Portfolio site for **16.S893 · AI Agents for Engineering Research** (MIT AeroAstro, Fall 2026).

**Live:** https://16s893-ai-for-engineering-research.github.io/adfarrar/

## Pages

| Page | What's there |
| --- | --- |
| **Home** | Project title + an abstract Earth with satellites in inclined orbits. Only some passes acquire a target — when one does, the ground target lights coral and the satellite opens a beam. That's the adaptive sensing thesis in one loop. |
| **About Me** | Bio + headshot, an interactive inner solar system, research interests, motivation, an animated research timeline, and where the work goes beyond the thesis. |
| **Project** | Outline of the PhD: the problem, four research questions, the onboard inference pipeline, the stakeholders it answers to, and the contribution. |
| **CV** | Inline PDF viewer plus a structured text version (education, research, publications, grants, awards, teaching). |
| **Dev Log** | Per-session log of what was delegated to the agent, what was verified, and what was rejected. Collapsible entries. |

## The interactive solar system

On the About page: Sun, Mercury, Venus, Earth and Mars on tilted elliptical orbits, the Moon orbiting Earth, and the Sun–Earth **L2** point marked on the anti-Sun line with a small hexagonal JWST. Four bodies are clickable and open a modal (no page navigation):

- **Earth** → world map with hoverable place pins
- **Mars** → SM thesis on Mars entry under atmospheric uncertainty
- **L2** → JWST internship
- **Moon** → a surprise

Keyboard accessible: focus the canvas, arrow keys to cycle bodies, Enter to open.

## Easter egg

Hover any link or button — the cursor becomes Mrs. Frizzle from *The Magic School Bus*. 🚌

## Editing content

Content is deliberately separated from layout:

| To change… | Edit |
| --- | --- |
| Map pins (places, blurbs, coordinates) | `src/data/pins.ts` |
| Research timeline entries | the `events` array in `src/components/Timeline.astro` |
| Dev log entries | the `entries` array in `src/pages/devlog/index.astro` |
| Colours, fonts, spacing | the `:root` block in `src/styles/global.css` |
| Bio / page copy | the relevant `src/pages/**/index.astro` |

Sections marked `[Placeholder]` are scaffolding — real structure, wording still to be written.

## Colour palette

Lifted from the `Ocean-darkmode` theme in the JPL SURP deck so the site and the talks read as one identity:

`#00AFFF` blue · `#52CADB` cyan · `#ACD6E1` pale · `#7CD0BC` mint · `#FA5A67` coral · `#F9D095` sand · `#031154` navy

## Tech

- [Astro](https://astro.build) — static output, no UI framework
- Canvas animations written by hand (`requestAnimationFrame`), no animation library
- World map from [Natural Earth](https://www.naturalearthdata.com/) 110m land vectors (public domain), reprojected to plate carrée and simplified with Ramer–Douglas–Peucker so lat/lon → pixel is plain arithmetic at runtime
- Deployed to GitHub Pages via `.github/workflows/deploy.yml`

## Local development

```sh
npm install
npm run dev       # http://localhost:4321/adfarrar/
npm run build     # → ./dist
npm run preview   # serve the production build
```

## Structure

```
src/
├── components/
│   ├── GlobeHero.astro   # home: Earth + satellites + targeted beams
│   ├── Orrery.astro      # about: clickable solar system + all four modals
│   ├── Timeline.astro    # about: animated research timeline
│   └── Nav.astro
├── data/
│   ├── pins.ts           # map pin content — edit here
│   └── world.ts          # generated world path + lat/lon projection
├── layouts/BaseLayout.astro
├── pages/
│   ├── index.astro       ├── about/    ├── project/
│   ├── cv/               └── devlog/
└── styles/global.css     # design system

public/
├── files/AFarrar_CV.pdf
└── images/               # headshot, dance photo, Frizzle cursor
```

Note: `personal_pictures/` and `supplemental-info/` are working source material and
are gitignored — web-sized copies of what the site uses live in `public/`.
