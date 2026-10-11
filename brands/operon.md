# Operon — ficha de marca para video

Fuente: operonhub.com/reservas (relevado el 11/10/2026). Si la web cambia, la web manda.

## Colores

| Token | Hex | Uso |
|---|---|---|
| `--paper` | `#fbf9f4` | Fondo principal |
| `--cream` | `#f2efe6` | Fondo alternativo |
| `--sand` | `#e1dbcc` | Celdas, superficies apagadas |
| `--line` | `#d9d2c0` | Bordes y separadores |
| `--ink` | `#14130f` | Texto y fondo oscuro, botón principal |
| `--mute` | `#6b655b` | Texto secundario, itálicas |
| `--soft` | `#a39c90` | Texto terciario sobre oscuro |
| `--blue` | `#1f40c2` | Acento: una palabra del titular, barras de reserva |
| `--blue-soft` | `#e3e7f8` | Chips |
| `--sol` | `#f2c94c` | Acento sobre fondo oscuro, tachados, alertas |

Tres climas que se alternan para dar ritmo: papel, oscuro (`--ink` con acento `--sol`) y, como mucho una vez por
pieza, azul pleno. Nada de gradientes sobre texto. Los fondos llevan una grilla de puntos suave y dos manchas
desenfocadas (azul claro y amarillo) que se mueven muy lento.

## Tipografía

- **Space Grotesk 600** — titulares. Tracking -0.035em, interlineado ~0.98.
- **Geist 400/500** — cuerpo.
- **JetBrains Mono 500** — etiquetas en mayúsculas con tracking .2em y números de paso.
- La segunda mitad de un titular suele ir en itálica y en `--mute` o `--blue`: "Tus reservas entran *directo.*"

Las tres fuentes están en `toolkit/template/assets/fonts/`.

## Logo

Una "O" que es un globo con piolín, seguida de "peron" y, en mono chico, `RESERVAS`. El SVG está en
`toolkit/template/ejemplo-reel.html` (clase `.lockup`). Se dibuja trazando el círculo; no se deforma ni se recolorea
fuera de `--ink` o `--paper`.

## Voz

Rioplatense, de dueño de cabaña a dueño de cabaña: "vos", frases cortas, humor seco. Concreto antes que
aspiracional: "Confirmar a mano a las 23:40", "«Che, ¿el 14 está libre?»". Nunca jerga de startup.

## Reglas que no se negocian

1. **Ninguna cifra, precio, testimonio ni resultado que no esté publicado** en la web o en la documentación del
   producto. Si un número es un ejemplo, lleva la etiqueta "Ejemplo" o el supuesto escrito en pantalla.
2. Los datos de la demo son ficticios (Refugio Alto Cielo, Martina Roldán, Cabañas del Beagle) y se pueden usar.
3. Las capturas son del producto real. Si una pantalla se reconstruye, se dice.
4. Cierre siempre igual: logo, una frase, "Ver la demo →" y `operonhub.com/reservas`.
5. Sobre Booking y Airbnb: el 15 % es "típico" o "la media que reportan"; nunca "siempre" ni "te roban".

## Productos

- **Operon Reservas** — motor de reservas para cabañas y alojamientos chicos. Ángulos ya usados: doble reserva
  (miedo), comisión (plata), Tu zona este mes (anticipación), se vende solo (tiempo), panel en el bolsillo (control).
- **Operon Agencia** — automatizaciones, SaaS y software a medida para pymes (operonhub.com). Cierre: "Agendar una
  llamada →" o "Contanos tu proceso →" y `operonhub.com`; el logo va sin la palabra RESERVAS. Ángulos ya usados:
  caso Virex (agente de IA que agenda), showreel de webs en producción, caso Aberturas FAR (Lighthouse 99/100),
  caso Papelera Roma (5.949 precios, un clic) y automatizaciones (lead.in → crm.sync → wa.notify → stripe.paid).
  No usar Nutri Studio ni Costito.
- **Capturas de clientes**: Virex solo en modo demo. La app local de Virex puede estar conectada a la base real:
  no capturarla sin confirmar que muestra datos de ejemplo. Papelera Roma, solo desde `?preview=1` en localhost y
  sin mostrar su lista de precios.

## Frases aprobadas (de la web)

- Tus reservas entran directo. Sin comisión en el medio.
- No podés vender dos veces la misma noche.
- Seis pantallas. Ninguna planilla.
- El panel entra en el bolsillo.
- Va abajo de tu web. No la reemplaza.
- Booking te trae huéspedes. Y se lleva el 15%.
- Entrá y tocá todo. Después hablamos.
