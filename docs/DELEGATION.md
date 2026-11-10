# Optional split: orchestrator + visual specialist

Use this mode only when requested. In solo mode, the active assistant handles everything. No paid Claude/API service is automatically called by this repo.

## Ownership
| Work | Orchestrator | Visual specialist |
|---|---|---|
| Brief, facts, concept selection, script, duration | Owns | Uses prepared baseline |
| Exact asset selection, permissions, branding constraints | Owns | Imports supplied assets |
| Scene illustration, composition, visual motion, components | Reviews/requests fixes | Owns implementation |
| Voice decisions/generation permission, alignment, music, SFX | Owns | No audio work |
| Full rendering, encoded review, technical QA, master, packaging | Owns | No production render work |

The specialist can run typecheck and a lightweight bundle to catch coding errors. This is not permission to redo the story, install stacks, browse every reference, generate sound, run long render/review loops or merge a PR.

## GitHub loop
1. Orchestrator creates projects/<slug>/ with a frozen data/timeline contract, source-checked claims, small essential brand assets, wrapper/captions, scoped AGENTS.md and a compact handoff/prompt.
2. Push preparation to main without secrets or big media. Set workflowMode to visual-handoff for this project only.
3. User opens the repo in their own Claude coding/GitHub environment and pastes the project prompt. The specialist branches from current main and edits only allowed visual files.
4. Specialist returns a PR, branch or commit. A read-only GitHub/chat integration may not be able to commit: in that case it must return a unified patch and say so. No token sharing in chat is necessary.
5. User sends the link/ref back to the orchestrator. The orchestrator fetches the exact ref, reviews the allowed-path diff, checks copy/timing/assets/dependencies and runs source checks, renders and inspection.
6. Send at most a narrow defect list back: timestamp/frame, evidence, requested visual change, files allowed. Avoid asking for full rewrites when one contact/mask needs fixing.
7. Orchestrator finishes narration/music/master/QA/delivery and merges only after review. User approval still controls spending/publication.

## Usage budget
The compact handoff is the primary specialist context. Do not attach raw videos, giant source ZIPs, base64 images, all research repositories or a long history of old films. Give one implementation pass, then targeted patches. If the specialist reaches a usage limit, it should save partial work and list unfinished scenes rather than claim completion.
