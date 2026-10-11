# Stack: las 21 librerías

Se instalan **por proyecto** (npm/pip), no dentro de esta skill. Usar siempre el gestor de paquetes del proyecto.

## Engines — lo que hace que las cosas se muevan

| Herramienta | Repo | Instalar | Usar cuando |
|---|---|---|---|
| three.js | mrdoob/three.js | `npm i three` | Escenas 3D, cámaras, luces, shaders |
| anime.js | juliangarnier/anime | `npm i animejs` | Motion liviano de texto, formas y SVG |
| Motion | motiondivision/motion | `npm i motion` | Motion con springs para sitios (React/JS) |
| react-three-fiber | pmndrs/react-three-fiber | `npm i three @react-three/fiber` | 3D declarativo dentro de React |
| lottie-web | airbnb/lottie-web | `npm i lottie-web` | Reproducir archivos de After Effects (JSON) |
| GSAP | greensock/GSAP | `npm i gsap` | Timing exacto al frame, timelines, scroll |

## Render — convierten código en MP4

| Herramienta | Repo | Instalar | Usar cuando |
|---|---|---|---|
| FFmpeg | FFmpeg/FFmpeg | Windows: `winget install Gyan.FFmpeg` · macOS: `brew install ffmpeg` | Cortar, unir, convertir, encodear cualquier video |
| Remotion | remotion-dev/remotion | `npx create-video@latest` | MP4 desde React. Licencia paga para empresas de 4+ personas |
| HyperFrames | heygen-com/hyperframes | `npx hyperframes init` | Una página HTML → MP4 |
| Manim | 3b1b/manim | `pip install manimgl` (o `pip install manim` para Community Edition) | Matemática, diagramas, fórmulas |
| ManimGX | academa-labs/manimgx | `uv tool install --python 3.14 manimgx` (requiere Python 3.13+) | Misma API que Manim CE sobre un motor Rust/GPU, mucho más rápido; trae `manimgx inspect` para revisar layout. Preferirlo a Manim clásico |
| Motion Canvas | motion-canvas/motion-canvas | `npm init @motion-canvas@latest` | Explainers con preview en vivo (TypeScript, generadores) |
| Revideo | midrender/revideo | `npm init @revideo@latest` | Fork de Motion Canvas para render en servidor / API |

## UI parts — piezas animadas para soltar

| Herramienta | Repo | Instalar | Usar cuando |
|---|---|---|---|
| shadcn/ui | shadcn-ui/ui | `npx shadcn@latest init` | Base sobre la que se enchufan los kits de abajo |
| React Bits | DavidHDev/react-bits | copiar desde reactbits.dev (CLI shadcn/jsrepo) | Texto animado, fondos, efectos |
| Magic UI | magicuidesign/magicui | `npx shadcn@latest add "https://magicui.design/r/<componente>.json"` | Partes animadas para landings |
| Motion Primitives | ibelick/motion-primitives | `npx motion-primitives@latest add <componente>` | Texto y UI con movimiento, drop-in |
| Magic MCP | 21st-dev/magic-mcp | ver `mcp-setup.md` | Generar UI desde una biblioteca de componentes |

Para proyectos HTML vanilla, portar el componente: extraer la estructura del JSX, replicar las clases y reemplazar
hooks por JS vanilla.

## Sound — voz, música y subtítulos

| Herramienta | Repo | Instalar | Usar cuando |
|---|---|---|---|
| Whisper | openai/whisper | `pip install -U openai-whisper` (requiere ffmpeg) | Voz en off → subtítulos con timestamps, local y gratis |
| Tone.js | Tonejs/Tone.js | `npm i tone` | Música y sonido sintetizado en código |
| wavesurfer.js | katspaugh/wavesurfer.js | `npm i wavesurfer.js` | Dibujar waveforms que se mueven |
| ElevenLabs skills | elevenlabs/skills | copiado en `packs/elevenlabs/` | Voz, música y SFX. Necesita cuenta y API key |

## Combinaciones probadas

- **Launch video**: HTML + GSAP (timeline pausado) → HyperFrames o captura por frames → ffmpeg.
- **Explainer con voz**: guion → ElevenLabs TTS → Whisper para timestamps → animación sincronizada → ffmpeg mux.
- **Title 3D**: Three.js con cámara animada por GSAP → captura por frames → ffmpeg.
- **Reel con waveform**: audio → wavesurfer.js para la forma → GSAP para el resto → export 1080x1920.
