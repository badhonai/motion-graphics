# Agent Instructions

You are working in the `motion-graphics` repository. Help create polished, intentional motion graphics and maintain this repository's structure.

## Repository layout

- `raw/`: Original input assets such as footage, images, audio, fonts, and source files.
- `reference/`: Inspiration, visual references, storyboards, moodboards, and creative direction.
- `exports/`: Rendered previews and final deliverables.
- `README.md`: Project overview and repository conventions.
- `agents.md`: These instructions.

Do not rename or repurpose these top-level locations.

## Before starting

1. Inspect the repository and read the relevant project files.
2. Review available assets in `raw/` and creative direction in `reference/`.
3. Identify the intended platform, aspect ratio, resolution, frame rate, duration, and output format. If the brief does not specify them, choose sensible defaults and state those assumptions.
4. Check the existing stack and conventions before introducing dependencies or restructuring files.

## Creative standards

- Build around a clear visual concept and hierarchy.
- Use deliberate typography, spacing, composition, color, and contrast.
- Make animation purposeful. Use easing, anticipation, follow-through, and consistent motion language where appropriate.
- Keep transitions coherent and avoid excessive effects, random gradients, generic templates, and other visual clutter.
- Ensure text remains readable at the target display size.
- Respect supplied brand assets and references. Do not invent logos or alter provided assets without a clear reason.
- Prefer reusable components, tokens, and animation helpers over duplicated one-off implementations.

## Implementation standards

- Choose tools based on the task. HTML, CSS, JavaScript, SVG, Canvas, and WebGL are suitable for browser-based motion graphics. Use an existing project framework when one is already established.
- Keep source code and editable project files outside `exports/`.
- Use clear filenames and organize project-specific work into descriptive subdirectories without changing the required top-level structure.
- Avoid unnecessary dependencies. Explain any significant new dependency.
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
- Do not commit secrets, credentials, private client data, or unrelated files.
- Avoid committing huge render files or caches. Use Git LFS or external storage when appropriate.
- Keep commits focused and use clear commit messages.
- Update `README.md` when project structure, setup, or usage changes.

## Delivery notes

When a task is complete, summarize what was created, where the source files and exports are located, how to run or render the work, and what verification was performed. Clearly identify anything that remains unverified.
