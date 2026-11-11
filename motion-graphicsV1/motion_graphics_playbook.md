# Motion Graphics Playbook

How the Fluton video (32 s, 1920×1080, 60 fps, with soundtrack) was made, written so an AI agent with a code sandbox can repeat the method for any brand.

**How to use this file:** upload it to a new chat together with your logo, then say what the video is for. Example prompt:

> Follow the attached playbook. Make a high-energy 30-second motion graphic for [BRAND]. Logo attached. Website: [URL]. Deliver an MP4.

The agent needs a sandbox that can run Python, install packages and reach the internet (for fonts and the brand's website).

---

## 1. The method in one paragraph

The whole video is one HTML page with a single `<canvas>` and one pure function, `frame(t)`, that draws the exact picture for any time `t` in seconds. A headless browser calls `frame(t)` for every frame, grabs the canvas as a JPEG, and pipes the frames into ffmpeg to make the MP4. The soundtrack is synthesised in Python with numpy at a fixed tempo, and every visual event is placed on a beat of that tempo, which is why the cuts feel tight. No video editor, no stock footage, no AI video model.

## 2. Tools

| Job | Tool |
| --- | --- |
| Drawing | HTML canvas 2D, plain JavaScript, no libraries |
| Frame capture | Playwright with headless Chromium (`pip install playwright`, `playwright install chromium`, `playwright install-deps chromium`) |
| Encoding | ffmpeg from `pip install imageio-ffmpeg` (no system ffmpeg needed) |
| Audio | numpy + scipy (`scipy.signal` for filters, `scipy.io.wavfile` to write) |
| Logo prep | Pillow + `scipy.ndimage.label` |
| Fonts | TTF files downloaded from the Google Fonts CSS API |

Installed packages do not survive between messages in most sandboxes, so reinstall at the start of each session.

## 3. Workflow, in order

1. **Research the brand.** Search the web and read the brand's own site. Take the tagline, feature names and key phrases from it word for word. Pull hex colours from the site's CSS. Do not invent claims.
2. **Inspect the logo.** A white logo on transparent looks blank, so composite it on a dark background to see it.
3. **Split the logo into parts** so they can animate separately (section 6).
4. **Pick the tempo and write the beat sheet** (section 4) before any code.
5. **Write `index.html`** with the helper toolkit (section 5) and one function per scene.
6. **Review stills.** Render contact sheets of 9–18 frames per scene, look at them, fix, repeat (section 8). This is where most of the quality comes from.
7. **Render the video** in a background process while writing the audio.
8. **Synthesise the audio** (section 7).
9. **Mux** video and audio, then pull one frame per second from the final MP4 into a single sheet as a last check.
10. **Tell the user what was invented** (sample numbers, sample data) and what could not be checked (the agent cannot hear the audio or watch playback).

## 4. Timing: everything sits on the beat

- Tempo 128 BPM. One beat `B = 0.46875 s`. One bar = 4 beats = 1.875 s.
- 64 beats = exactly 30.0 s. Add a 2 s tail for a 32 s total.
- One scene = 2 bars = 8 beats = 3.75 s. Eight scenes fill 30 s.
- In code, write every time as `bt(n)` = beat `n`, never as raw seconds.

Beat sheet used for Fluton (reuse the structure, swap the content):

| Beats | Seconds | Scene | Purpose |
| --- | --- | --- | --- |
| 0–8 | 0–3.75 | Problem | Cold open, no kick drum. One word per beat, then three hard-cut single words, then the picture collapses to a line. |
| 8–16 | 3.75–7.5 | Logo slam | The drop. Flash, shockwaves, logo parts fly in, wordmark, tagline types on. |
| 16–24 | 7.5–11.25 | Feature 1 | A UI card demonstrates the feature; giant one-word headline lands on beat 4 of the scene. |
| 24–32 | 11.25–15 | Feature 2 | A small action story (threat, defence, result), then headline and a rolling counter. |
| 32–40 | 15–18.75 | Feature 3 | Diagram scene: nodes pop in on half-beats around the logo. |
| 40–48 | 18.75–22.5 | Big idea | Breakdown for 4 beats (no kick, riser), second drop at beat 44. |
| 48–56 | 22.5–26.25 | Montage + question | Four full-screen words, one per beat, on alternating colour fields; then a quiet question with a riser. |
| 56–64 | 26.25–30 | Lockup | Final drop. Logo, wordmark, tagline, URL pill. |
| 64–68 | 30–32 | Tail | Hold with slow zoom, fade to black over the last 0.6 s. |

Rules that keep the energy up:

- Something new must start at least every beat or two. A scene that holds still for more than about 1 second needs another event (a pulse ring, a counter, an exit move).
- Scene changes are hard cuts on the beat with a short white flash, not crossfades.
- Each scene ends with an exit move in its last half-beat (zoom through, collapse, shoot off-screen).
- Energy has shape: quiet intro, drop, a breakdown around two-thirds in, a second drop, a final drop.

## 5. Drawing toolkit (`index.html`)

**Core rule: `frame(t)` must be deterministic.** No `Math.random()`, no state carried between frames. Use a hash for randomness:

```js
const rnd = i => { const s = Math.sin(i*127.1+311.7)*43758.5453; return s - Math.floor(s); };
```

**Progress and easing.** Every animation is `ease(p(t, start, duration))`:

```js
const p = (t,a,d) => clamp((t-a)/d);          // 0..1
outExpo  : t => 1 - 2**(-10*t)                // default for entrances: fast then settle
inExpo   : t => 2**(10*t-10)                  // exits
outBack  : t => 1+2.70158*(t-1)**3+1.70158*(t-1)**2   // overshoot for pops
inOutCubic                                    // moves between two positions
```

Nothing moves linearly. Entrances take 0.3–0.45 s.

**Text helpers**

- `rise(word, …)`: word slides up out of a clipping mask. Used for word-by-word headlines.
- `punch(word, …)`: starts at 1.5× scale and snaps to 1×. Used for the big hit word.
- `letters(word, …)`: per-letter staggered rise (0.045 s apart). Used for the wordmark.
- `typed(str, q)`: type-on, with a blinking `▌` cursor, for mono taglines.
- `cipher(str, q, t)`: replaces a fraction `q` of characters with glyphs that change every 0.07 s. Used for "encrypting" text.
- Measure text and centre groups of words by computed width. Check nothing runs off the 1920 px frame.

**Effect helpers**

- `shock(x,y,u)`: expanding rings. `burst(x,y,u)`: radial streak lines. Both fire on impacts.
- `orb(x,y,r,colour,alpha)`: soft radial glow. Layer these instead of flat fills.
- Glow on shapes and text with `ctx.shadowColor` + `ctx.shadowBlur` (30–70).
- `backdrop(t, tint, warp, streak)`: dark gradient plus 150 drifting particles that become warp streaks during drops.

**Master `frame(t)` wrapper**, applied to every scene:

- Camera shake: a list of `[beat, amplitude, duration]` impacts, decaying.
- Beat pulse: zoom `1 + 0.011 * exp(-beatFraction*6)` while the kick is playing.
- Flashes: a list of `[beat, alpha, duration]` white overlays.
- Vignette on top of everything.
- Reset canvas state (transform, alpha, dash, shadow) at the start of each frame.

**Design system**

- Background near-black navy (`#04060C`). Two or three brand colours plus white. One alarm colour (red) used only for the "problem".
- Two fonts: a bold grotesque for headlines (Space Grotesk 700), a monospace for labels and data (JetBrains Mono 500/800). Mono labels are small, upper case, wide letter-spacing.
- Headlines are huge: 110–300 px for lines, 350–470 px for single montage words.
- Feature scenes share a header: outlined section number, short rule, mono label, small logo top-right.
- Check the font has the glyphs you use (block characters and `●` exist in JetBrains Mono but not Space Grotesk).

## 6. Logo handling

1. Load the PNG, threshold the alpha channel, label connected components with `scipy.ndimage.label`.
2. Group components into meaningful parts by centroid position (Fluton: roof chevron, inner chevron, ring).
3. Save each part as its own PNG on the **same full-size canvas**, so drawing all parts at the same position reassembles the logo exactly.
4. Animate parts in from different directions with `outBack`, 0.07 s apart; scale-and-spin the smallest part in last.

## 7. Audio synthesis (`audio.py`)

All sounds are generated with numpy at 44.1 kHz stereo and added into two buffers at beat times.

- **Kick:** sine with pitch falling from ~196 Hz to 46 Hz, 0.16 s decay, soft-clipped.
- **Hats:** high-passed noise (7.5 kHz), very short decay. Off-beat open hat plus quiet 16ths.
- **Clap / snare:** band-passed noise bursts; clap on beats 2 and 4.
- **Bass:** sine + low-passed saw on the three 16ths after each kick (rolling bass).
- **Arp:** three detuned saws through a low-pass, 0.11 s pluck, 16th notes from the chord, with a delayed copy panned opposite.
- **Chords:** F minor, F minor, D♭, E♭, one per bar. Stab on each bar start.
- **Riser:** band-passed noise with a rising centre frequency plus a rising sine, amplitude growing as `q^2.2`. Used before every drop.
- **Boom:** low sine sweep with long decay plus noise, on each drop and big hit.
- **Whoosh:** band-passed noise swell just before scene cuts.
- **Arrangement:** follows the beat sheet. No kick in the intro and breakdowns; 20–110 ms of silence right before each drop; snare roll into each drop.
- **Master:** a few short delays as reverb, high-pass at 28 Hz, gentle `tanh` saturation, normalise to 0.94 peak, fade the last 0.75 s.
- **Checks without ears:** print RMS per 4 beats to confirm the energy shape, and band energy to confirm it is not all sub-bass (boost arp and stabs if mids are below about −15 dB).

## 8. Render and review scripts

**Contact sheet (`shots.py`)**: open the page with `window.__render = true` (so it does not auto-play), `await window.ready` (fonts + images), call `frame(t)` for a list of times, read `canvas.toDataURL('image/jpeg')`, paste into a grid, and look at it. Also collect `pageerror` events.

**Full render (`render.py`)**:

```
for n in range(frames):
    data = page.evaluate("(frame(n/FPS), canvas.toDataURL('image/jpeg', 0.97))")
    ffmpeg.stdin.write(base64-decoded bytes)

ffmpeg -f image2pipe -framerate 60 -c:v mjpeg -i - \
       -c:v libx264 -preset medium -crf 15 -pix_fmt yuv420p -movflags +faststart video.mp4
```

- Launch Chromium with `--allow-file-access-from-files` so the canvas can be read after drawing local images.
- About 0.1–0.15 s per frame at 1080p; 32 s at 60 fps takes about 3 minutes. Run it as a background process.
- Mux: `ffmpeg -i video.mp4 -i audio.wav -c:v copy -c:a aac -b:a 256k -shortest out.mp4`.
- Final check: `ffmpeg -i out.mp4 -vf "fps=1,scale=384:216,tile=8x4" -frames:v 1 sheet.jpg`.

## 9. Mistakes made and fixed on the Fluton video

| Problem seen in stills | Fix |
| --- | --- |
| Wordmark letters appeared on top of the logo while it was still moving | Delay the letters until the move has finished |
| Attackers were only visible for a few frames (ease-in from far away) | Approach fast, hover and circle with labels, then lunge in 0.2 s |
| Headline ran off both edges of the frame | Measure width; reduce size until it fits inside ~1700 px |
| Diagram overlapped the section header | Move the diagram down and shrink its radius |
| A label read "undefined" | Label array was shorter than the index range |
| Hit effects turned into a messy rosette of circles | Remove the rings, keep short-lived fragments |
| Final lockup sat still for 2 seconds | Add a pulse ring from the logo on every beat |

## 10. Honesty checklist for the agent

- Take copy from the brand's own site; flag any number or sample data you invented.
- Say plainly that you reviewed still frames, not playback, and that you cannot hear the soundtrack.
- Offer a silent version in case the synthesised music does not suit.
- Do not use other companies' logos; use text initials for third-party names.

## 11. What to tell the agent for a new video

- Brand name, website, and logo file (transparent PNG or SVG).
- Length and shape (default 32 s, 16:9; say 9:16 for vertical).
- Mood (default: high energy, dark, electronic).
- Three or four key messages, or "take them from the website".
- Any real statistics to feature, with their source.
- Whether you want music, and any words or claims to avoid.

## 12. Files from the Fluton project

- `fluton/index.html`: the animation (toolkit + eight scenes + master wrapper).
- `fluton/audio.py`: the soundtrack synthesiser.
- `fluton/render.py`, `fluton/shots.py`: render and contact-sheet scripts.
- `fluton/assets/`: fonts and the split logo parts.

Uploading `index.html` and `audio.py` alongside this playbook gives the agent the exact code to adapt, which is faster and closer to the original than rebuilding from the description.
