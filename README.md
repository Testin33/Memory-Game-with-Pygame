# Memory Game (Pygame)

Juego de memoria en una sola pantalla: muestra un patrón aleatorio, lo oculta con un efecto de flip y el jugador debe reconstruirlo con clics antes de 40 s. Lógica pura separada del render para poder testear en CI.

## Ejecutar

1) Crear venv (opcional) e instalar dependencias:

```bash
pip install -r requirements.txt
```

2) Ejecutar el juego:

```bash
python main.py
```

## Controles

- Click izquierdo sobre las celdas para reproducir el patrón cuando el estado sea `PLAYING`.

## Estados

- `SHOWING`: el juego resalta el patrón, paso a paso.
- `PLAYING`: el jugador reproduce la secuencia.
- `WON`: secuencia correcta completa.
- `LOST`: error o tiempo agotado (40 s).

## Estructura del proyecto

```text
.
├─ main.py
├─ settings.py
├─ game/
│  ├─ __init__.py
│  ├─ core.py    # Lógica pura: patrón, verificación, temporizador, estados
│  └─ scene.py   # Render y loop de Pygame
├─ models/
│  ├─ __init__.py
│  └─ tile.py    # Clase Tile (coordenadas)
└─ tests/
   └─ test_core.py
```

## Tests

```bash
pytest -q
```

## Configuración

Constantes en `settings.py`: tamaño de ventana, grid, colores y tiempos (`SHOW_TIME_PER_STEP_MS`, `HIDE_FLIP_MS`, `TOTAL_TIME_SECONDS`).

A python mini project

