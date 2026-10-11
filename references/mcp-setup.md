# MCPs de motion graphics

Ninguno de estos tres está conectado todavía: cada uno necesita una app externa o una API key, y agregarlos
modifica la configuración de Claude Code. Conectarlos solo cuando el usuario lo pida.

## Blender — ahujasid/mcp-for-blender

Claude maneja Blender en 3D (crear objetos, materiales, cámaras, render).

Requisitos: Blender instalado, `uv` (ya está en esta máquina).

```bash
claude mcp add blender uvx mcp-for-blender
```

Después instalar el addon en Blender (el repo trae `uvx mcp-for-blender setup`, que lo hace solo y deja un `.bak`
de cada config que toca). Reiniciar Claude por completo y abrir Blender: el addon levanta su servidor al iniciar.

## After Effects — Dakkshin/after-effects-mcp

Maneja After Effects (composiciones, capas, keyframes). Requiere After Effects (pago) y Node.

```bash
git clone https://github.com/Dakkshin/after-effects-mcp
```

Dentro del repo: `npm install`, `npm run build`, `npm run install-bridge` (copia el panel a la instalación de AE;
puede pedir permisos de administrador). Después registrar el server:

```json
{
  "mcpServers": {
    "AfterEffectsMCP": {
      "command": "node",
      "args": ["RUTA/A/after-effects-mcp/build/index.js"]
    }
  }
}
```

En AE: abrir el panel desde Window > `mcp-bridge-auto.jsx` y dejarlo abierto mientras se usa el MCP.

## 21st Magic — 21st-dev/magic-mcp

Busca y genera componentes UI desde la biblioteca de 21st.dev. Es un MCP HTTP y necesita API key
(gratis en 21st.dev/mcp). La key la carga el usuario, nunca se escribe en un archivo del repo.

```bash
npx @21st-dev/cli@latest init --client claude
```

La generación con IA (`generate`, `iterate_generation`) depende del plan; sin eso quedan `search` y `get_component`.
