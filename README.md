# Motion Graphics

A workspace for creating, organizing, and exporting motion graphics.

## Project structure

```text
motion-graphics/
├── raw/          # Original footage, images, audio, fonts, and source assets
├── reference/    # Visual references, moodboards, examples, and creative direction
├── exports/     # Rendered previews and final deliverables
├── agents.md    # Instructions and workflow for AI agents
└── README.md    # Project overview and usage notes
```

## Folder conventions

### `raw/`
Keep original assets here. Preserve source filenames where practical. Do not overwrite originals. Organize larger collections into descriptive subfolders.

### `reference/`
Store inspiration, screenshots, storyboards, style frames, brand guidelines, and other materials that guide the work. Include source links or short notes when useful.

### `exports/`
Store rendered outputs and review previews. Use descriptive filenames that include the project or composition name and, when useful, a version number. Keep editable project files with their relevant project source rather than mixing them with final exports.

## Working principles

- Keep source assets separate from generated and exported files.
- Prefer reusable components, clear naming, and maintainable project structure.
- Match the brief and references before adding decorative effects.
- Verify timing, typography, layout, audio, and render quality before calling an export final.
- Do not commit large generated renders unless they are explicitly required. Use Git LFS or external storage for large binary assets when appropriate.

See [agents.md](agents.md) for the agent workflow and operating rules.
