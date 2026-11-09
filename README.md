# Motion Graphics

A workspace for creating original, high-quality motion graphics with AI coding agents.

## Toolchain

- **Remotion:** Build and render programmatic videos with React.
- **HyperFrames:** Create HTML/GSAP-based motion-graphics compositions.
- **FFmpeg / FFprobe:** Cut, process, inspect, and export media.
- **OpenAI Whisper:** Transcribe speech and generate captions.
- **yt-dlp:** Download permitted reference media for analysis.

See [setup.md](setup.md) for installation and smoke tests. See [taste.md](taste.md) for reference analysis and creative standards. AI agents must follow [agents.md](agents.md).

## Project structure

```text
motion-graphics/
├── raw/          # Original footage, images, audio, fonts, and source assets
├── reference/    # Inspiration, examples, storyboards, and visual references
├── exports/      # Rendered previews and final deliverables
├── agents.md     # Instructions and workflow for AI agents
├── setup.md      # Toolchain installation and verification
├── taste.md      # Creative taste and reference-study rules
└── README.md     # Project overview and usage notes
```

## Folder conventions

### `raw/`
Keep original assets here. Preserve source filenames where practical. Do not overwrite originals. Organize larger collections into descriptive subfolders.

### `reference/`
Store inspiration, screenshots, storyboards, style frames, brand guidelines, and reference-analysis notes. Include source links or short notes when useful. Do not claim to have studied references that are not present or accessible.

### `exports/`
Store rendered previews and final deliverables. Use descriptive filenames that include the project or composition name and, when useful, a version number. Keep editable project files with their relevant project source rather than mixing them with final exports.

## Working principles

- Keep source assets separate from generated and exported files.
- Preserve the user's information, voice, brand, and project identity.
- Take inspiration from references without copying distinctive creative work.
- Prefer reusable components, clear naming, and maintainable project structure.
- Verify timing, typography, layout, audio, and render quality before calling an export final.
- Do not commit large generated renders, downloaded reference media, dependency folders, or caches unless explicitly required. Use Git LFS or external storage for large binary assets when appropriate.
