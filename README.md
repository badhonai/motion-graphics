# Motion Graphics Studio

A lightweight, **AI-neutral** workspace for creating a different, original motion film each time. Built from the reference research and production lessons in this project—not a collection of giant videos or a one-style animation template.

**Any coding assistant:** start with [`AGENTS.md`](AGENTS.md). No Claude subscription, proprietary agent runtime or voice API is required.

## Quick start

Node 20.19+ (22 LTS recommended), npm, Git, FFmpeg/ffprobe and Chrome's Linux system libraries are required. See [setup](docs/SETUP.md).

```bash
npm ci
npx remotion browser ensure
npm run doctor
npm test
npm run typecheck
npm run build:check
npm run new -- my-film
# Fill projects/my-film/brief.md, storyboard.md and assets.json first.
npm run studio -- my-film
npm run still -- my-film --frame=120
npm run render -- my-film
npm run qa -- my-film
```

Studio opens on port 3000; use `--port=3001` for another project. Generated source is in `projects/my-film/`. Local output is in ignored `renders/my-film/`. Never run a second npm install inside each project.

### Small engineering smoke test

```bash
npm run render -- starter --frames=0-11 --scale=0.25
npm run qa -- starter --frames=0-11
```

This tests the pipeline, **not** a finished creative film. Full production still needs visual/audio review and a new concept.

## Repository map

```text
AGENTS.md                 Canonical instructions for any AI
CLAUDE.md / GEMINI.md      Thin pointers, not competing workflows
.agents/skills/            Four curated direction/choreography/engineering/sound-QA skills
docs/                     Setup, workflow, taste, QA, security and production lessons
  research/               Distilled findings, immutable source pointers and notices
templates/starter/        Small frame-clock/font/integration fixture + planning documents
projects/<slug>/           Your separately scoped film source and brief
tools/                    Generator, preview/render/QA, checks and optional audio master
tests/                    Built-in Node tests
public/fonts/             One small licensed shared font (OFL retained)
.github/workflows/        Source checks and an optional manual render smoke
```

Excluded from Git: `local/`, `raw/`, `exports/`, `reference/`, `renders/`, supplied project media, caches, model weights, credentials and production archives. The previous films/research cache are preserved locally under `local/production-workspace/`; that folder is not part of the public checkout. Old Git history is preserved, not force-rewritten.

## The reusable creative workflow

**Brief → three concepts → art direction → scene/cue table → key states → motion → sound → correction loops → final encode/QA → honest delivery.**

- [Full workflow](docs/WORKFLOW.md)
- [Design principles](docs/DESIGN.md)
- [QA and review limits](docs/QA.md)
- [Research and sources](docs/research/README.md)
- [Tested production lessons](docs/DECISIONS.md)
- [Actual rebuild validation](docs/VALIDATION.md)
- [Assets, fonts and audio](docs/ASSETS.md)
- [Security/public-repo rules](docs/SECURITY.md)

Remotion is the clock. Framer Motion receives explicit frame-derived transforms/easing; this is an application pattern that must be tested, not an official integration. PNG capture, explicit `swangle`, matching Remotion versions and fresh/reverse seek tests are deliberate defaults from production experience.

## Scope / licenses

No creator media, client marks, narration, full upstream repositories or finished exports are bundled. Research links are references, not permission to copy. Eleven upstream MIT notices are retained for attribution; their media are not covered. Shared Inter is under its included SIL OFL. This repository does not make a new blanket license grant over third-party material or generated client work. Check Remotion's current license for your use case.
