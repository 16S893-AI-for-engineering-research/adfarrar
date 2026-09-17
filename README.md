# Allegra Farrar — Class Portfolio

A multi-page portfolio site built with [Astro](https://astro.build) for
16S893 (AI for Engineering Research). Covers who I am, my research project,
and a couple of animated backgrounds because static dark backgrounds are boring.

Live site: https://16S893-AI-for-engineering-research.github.io/adfarrar/

## Pages

- **Home** — landing page with a canvas hero animation: a satellite doing an
  "adaptive sensing" sweep over a rotating hurricane.
- **About Me** — an interactive space scene. Click Earth or Mars to travel
  there; the Mars view has a blurb about my SM thesis (Mars entry trajectory
  optimization under atmospheric uncertainty), and the Earth view is a stub
  for a future world-map-with-pins feature.
- **Project** — outline of my current PhD research: adaptive sensing design
  for satellite monitoring and warning of tropical cyclones. Background is a
  canvas rain-on-glass animation.

## Easter egg

Hover over any nav link (or button) across the site — the cursor turns into
Mrs. Frizzle from *The Magic School Bus*. 🚌

## Tech stack

- [Astro](https://astro.build) (static site, zero client JS by default)
- Vanilla canvas animations for the starfield, rain, and hero graphic — no
  animation library, just `requestAnimationFrame`
- Deployed to GitHub Pages via GitHub Actions (`.github/workflows/deploy.yml`)

## Local development

```sh
npm install
npm run dev       # http://localhost:4321/adfarrar/
npm run build     # outputs to ./dist
npm run preview   # serve the production build locally
```

## Project structure

```
src/
├── components/
│   ├── AboutScene.astro     # interactive space/Mars/Earth view logic
│   ├── HeroAnimation.astro  # satellite + hurricane canvas animation
│   ├── Nav.astro            # shared nav bar (Easter-egg cursor lives here)
│   ├── RainField.astro      # rain-on-window canvas background
│   └── Starfield.astro      # twinkling starfield + shooting stars
├── layouts/
│   └── BaseLayout.astro     # shared <head>, nav, footer
├── pages/
│   ├── index.astro          # Home
│   ├── about/index.astro    # About Me
│   └── project/index.astro  # Project
├── styles/
│   └── global.css           # theme variables, shared components, cursor CSS
└── assets/                  # source images (not directly served)

public/images/                # served static images (cursor PNG, etc.)
```
