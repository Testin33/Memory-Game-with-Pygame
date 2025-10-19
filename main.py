from __future__ import annotations

import sys

try:
    from game.scene import GameScene
except ImportError as exc:
    print(
        "Error: no se pudo importar pygame.\n"
        "Instala dependencias con: pip install -r requirements.txt\n"
        "Si usas un entorno virtual, verifica que tu IDE use ese intérprete."
    )
    sys.exit()


def main() -> None:
    GameScene().run()


if __name__ == "__main__":
    main()


