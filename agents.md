# Agent Instructions

You are working in the `motion-graphics` repository. Your job is to create polished, intentional motion graphics while preserving the user's identity, voice, brand, and project context.

## Read these files first

Before doing project work, read:

1. `README.md` for repository conventions.
2. `setup.md` for the media toolchain and verification requirements.
3. `taste.md` for reference analysis and creative direction.

Do not assume tools are installed just because they are documented. Inspect the current environment and verify them.

## Toolchain responsibilities

Use the tools according to these roles:

- **Remotion:** Main programmatic video composition and rendering with React.
- **HyperFrames:** HTML/GSAP-based motion-graphics compositions, animation systems, and previews.
- **FFmpeg / FFprobe:** Cutting, transcoding, audio processing, media inspection, and final encoding.
- **Whisper:** Speech transcription and caption generation.
- **yt-dlp:** Downloading reference media only when the user is permitted to download it and platform terms allow it.

Choose the appropriate renderer for each job. Do not force both Remotion and HyperFrames into every project. Keep the source project editable and make the rendering pipeline reproducible.

## Setup and verification

When asked to set up the environment:

1. Follow `setup.md` from the repository root.
2. Install Node packages locally in this repository and Python packages inside `.venv/` where possible.
3. Install FFmpeg using an appropriate system package manager or approved local binary. Do not pretend FFmpeg is installed in the repository if it is a system dependency.
4. Run the CLI checks and actual smoke tests described in `setup.md`.
5. Report each tool as Pass, Fail, or Blocked. Never say all five work unless all five have passed real smoke tests.

Do not overwrite existing project configuration or package manifests without inspecting them first. Do not run a project scaffolder that rejects an existing Git repository at the repository root.

## Before creating a video

1. Inspect the repository and read the relevant project files.
2. Review `raw/` for source assets and `reference/` for creative references.
3. Follow `taste.md`: analyze pacing, captions, colour, motion, and sound before designing.
4. Preserve the user's facts, wording, voice, brand, and project identity. Never invent personal or project claims.
5. Confirm the intended platform, aspect ratio, resolution, frame rate, duration, and output format. If unspecified, use sensible defaults and state them.
6. Create an original direction inspired by abstract reference principles, never a direct copy.

## Creative standards

- Build around a clear visual concept and hierarchy.
- Use deliberate typography, spacing, composition, colour, and contrast.
- Make animation purposeful. Use easing, anticipation, follow-through, and a consistent motion language.
- Keep transitions coherent. Avoid excessive effects, random gradients, generic templates, and visual clutter.
- Ensure text remains readable at the target display size.
- Respect supplied brand assets. Do not invent logos or alter provided assets without a clear reason.
- Prefer reusable components, design tokens, and animation helpers over duplicated one-off implementations.

## Implementation standards

- Choose Remotion or HyperFrames based on the project requirements; use both only when there is a clear integration reason.
- Use FFmpeg for media operations that are better handled outside the renderer.
- Keep source code and editable project files outside `exports/`.
- Use clear filenames and organize project-specific work into descriptive subdirectories without changing the required top-level structure.
- Avoid unnecessary dependencies. Explain significant new dependencies.
- Keep generated assets reproducible when practical.

## Rendering and quality assurance

Before delivering an export:

1. Run the project using its documented commands.
2. Check the composition at its target dimensions and aspect ratio.
3. Verify animation timing, easing, transitions, and loop behavior where applicable.
4. Check for clipping, overflow, font-loading issues, visual artifacts, and console errors.
5. Verify audio synchronization and levels when audio is present.
6. Render a preview, inspect it, fix issues, and render the final output.
7. Save deliverables in `exports/` with descriptive names.

Never claim that a render or test passed unless it was actually run and inspected.

## Git and asset handling

- Do not overwrite or delete original files in `raw/`.
- Do not commit secrets, credentials, private client data, virtual environments, dependency folders, caches, or unrelated files.
- Avoid committing huge reference downloads or rendered videos. Use Git LFS or external storage when appropriate.
- Keep commits focused and use clear commit messages.
- Update `README.md` when project structure, setup, or usage changes.

## Delivery notes

When a task is complete, summarize what was created, where the source files and exports are located, how to run or render the work, and what verification was performed. Clearly identify anything that remains unverified.
