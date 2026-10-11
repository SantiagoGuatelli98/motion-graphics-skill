# Fuentes

Lista original: "28 Things to Install into Claude for motion graphics" (Charlie Hills). Instalado el 2026-10-11.

## Packs copiados en `packs/`

| Pack | Repo | Commit | Licencia | Qué se copió |
|---|---|---|---|---|
| `gsap/` | greensock/gsap-skills | aed9cfd | MIT | `skills/*` |
| `remotion/` | remotion-dev/skills | 32b241b | sin archivo de licencia en el repo | `skills/*` |
| `threejs/` | CloudAI-X/threejs-skills | b1c6230 | sin archivo de licencia en el repo | `skills/*` |
| `launch-motion/` | charlie947/motion-graphics-skills | 229022e | MIT | `skills/*` y `prompts/` (sin `assets/` ni `downloads/*.zip`) |
| `elevenlabs/` | elevenlabs/skills | 1d08a4a | MIT | music, sound-effects, text-to-speech, speech-to-text, setup-api-key, voice-changer, voice-isolator, dubbing |
| `manimgx/` | academa-labs/manimgx | 7ea9ad5 | MIT | `skills/manimgx/SKILL.md` (agregado después de la lista original) |
| `anthropic/` | anthropics/skills | dbd4588 | ver cada skill | algorithmic-art, canvas-design, slack-gif-creator |

## Solo documentados (no copiados)

MCPs — `references/mcp-setup.md`: ahujasid/mcp-for-blender, Dakkshin/after-effects-mcp, 21st-dev/magic-mcp.

Librerías — `references/stack.md`: mrdoob/three.js, juliangarnier/anime, motiondivision/motion,
pmndrs/react-three-fiber, airbnb/lottie-web, greensock/GSAP, FFmpeg/FFmpeg, remotion-dev/remotion,
heygen-com/hyperframes, 3b1b/manim, motion-canvas/motion-canvas, midrender/revideo, shadcn-ui/ui,
DavidHDev/react-bits, magicuidesign/magicui, ibelick/motion-primitives, openai/whisper, Tonejs/Tone.js,
katspaugh/wavesurfer.js.

## Actualizar un pack

Clonar el repo con `git clone --depth 1`, revisar el diff de `skills/` y reemplazar la carpeta correspondiente.
Actualizar el commit en esta tabla.
