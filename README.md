# motion-graphics — skill de Claude Code

Skill para hacer motion graphics en código (reels, launch films, gráficos animados) con Claude Code.
Incluye el flujo con el que se hicieron los videos de Operon Reservas, la ficha de marca de Operon y packs de
skills de terceros como referencia.

## Instalar

1. Cloná este repo dentro de la carpeta de skills de Claude Code, con el nombre `motion-graphics`:

   macOS / Linux
   ```bash
   git clone https://github.com/SantiagoGuatelli98/motion-graphics-skill.git ~/.claude/skills/motion-graphics
   ```

   Windows (PowerShell)
   ```powershell
   git clone https://github.com/SantiagoGuatelli98/motion-graphics-skill.git "$env:USERPROFILE\.claude\skills\motion-graphics"
   ```

2. Abrí Claude Code de nuevo. La skill aparece como `/motion-graphics`.

## Requisitos

- Node 22 o más nuevo
- Google Chrome o Microsoft Edge
- ffmpeg (`winget install Gyan.FFmpeg` en Windows, `brew install ffmpeg` en macOS)
- Python 3 con numpy y scipy (`pip install numpy scipy`) — solo para la música

## Usar

Pedile a Claude algo como:

> /motion-graphics haceme un reel de 15 segundos de Operon Reservas sobre el calendario iCal

Claude lee la ficha de marca (`brands/operon.md`), copia el template, escribe el video, revisa frames, genera la
música y exporta el MP4.

## Qué hay adentro

- `SKILL.md` — instrucciones para Claude: flujo probado y tabla de decisión
- `toolkit/` — exportador frame a frame, sintetizador de música y un template con un reel de ejemplo
- `brands/operon.md` — paleta, tipografías, logo, tono y reglas de Operon
- `packs/` — skills de terceros (GSAP, Remotion, Three.js, ElevenLabs, y otros); licencias en `references/SOURCES.md`
- `references/` — librerías, MCPs y fuentes

## Actualizar

```bash
git -C ~/.claude/skills/motion-graphics pull
```
