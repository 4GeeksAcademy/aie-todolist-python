#!/usr/bin/env python3
"""Gestor de tareas pendientes para terminal. Solo libreria estandar."""
import argparse
import csv
import sys
from pathlib import Path

TODOS_FILE = Path("todos.csv")
FIELDNAMES = ["titulo"]


def load_tasks(path=TODOS_FILE):
    """Carga las tareas desde el CSV. Si el archivo no existe, devuelve []."""
    path = Path(path)
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [row["titulo"] for row in csv.DictReader(f) if row.get("titulo")]


def save_tasks(tasks, path=TODOS_FILE):
    """Guarda la lista de tareas en el CSV."""
    with Path(path).open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for title in tasks:
            writer.writerow({"titulo": title})


def add_task(tasks, title):
    title = title.strip()
    if not title:
        raise ValueError("El titulo de la tarea no puede estar vacio.")
    tasks.append(title)
    return title


def remove_task(tasks, position):
    """Elimina la tarea en la posicion (base 1) y la devuelve."""
    if not 1 <= position <= len(tasks):
        raise IndexError(
            f"Posicion {position} invalida. Hay {len(tasks)} tarea(s) pendiente(s)."
        )
    return tasks.pop(position - 1)


def format_tasks(tasks):
    if not tasks:
        return "No hay tareas pendientes."
    return "\n".join(f"{i}. {t}" for i, t in enumerate(tasks, start=1))


def build_parser():
    parser = argparse.ArgumentParser(description="Gestor de tareas pendientes.")
    parser.add_argument(
        "-f", "--file", default=str(TODOS_FILE), help="archivo CSV (def.: todos.csv)"
    )
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="agregar una tarea")
    p_add.add_argument("titulo", nargs="+", help="titulo de la tarea")

    sub.add_parser("list", help="mostrar tareas pendientes")
    sub.add_parser("interactive", help="menu interactivo (por defecto sin comando)")

    p_rm = sub.add_parser("remove", help="eliminar una tarea por su posicion")
    p_rm.add_argument("posicion", type=int, help="posicion numerica (desde 1)")
    return parser


SEPARATOR_WIDTH = 30
CHOICE_TITLES = {
    "1": "Agregar tarea",
    "2": "Ver tareas",
    "3": "Eliminar tarea",
    "4": "Salir",
}


def separator(title):
    """Linea delimitadora con el titulo centrado, con salto de linea antes y despues."""
    return f"\n{f' {title} '.center(SEPARATOR_WIDTH, '-')}\n"

MENU = """
=== Gestor de tareas ===
1. Agregar tarea
2. Ver tareas
3. Eliminar tarea
4. Salir"""


def interactive(path=TODOS_FILE, input_fn=input):
    """Menu interactivo: permite usar todas las funciones sin recordar comandos."""
    tasks = load_tasks(path)
    while True:
        print(MENU)
        try:
            choice = input_fn("Elige una opcion (1-4): ").strip()
            print(separator(CHOICE_TITLES.get(choice, "Opcion no valida")))
            if choice == "1":
                title = add_task(tasks, input_fn("Titulo de la tarea: "))
                save_tasks(tasks, path)
                print(f"Tarea agregada: {title}")
            elif choice == "2":
                print(format_tasks(tasks))
            elif choice == "3":
                if not tasks:
                    print(format_tasks(tasks))
                    continue
                print(format_tasks(tasks))
                raw = input_fn("Posicion a eliminar (Enter para cancelar): ").strip()
                if not raw:
                    continue
                removed = remove_task(tasks, int(raw))
                save_tasks(tasks, path)
                print(f"Tarea eliminada: {removed}")
            elif choice == "4":
                print("Hasta luego.")
                return 0
            else:
                print("Opcion no valida. Elige un numero del 1 al 4.")
        except ValueError as e:
            msg = str(e)
            if msg.startswith("invalid literal"):
                msg = "La posicion debe ser un numero entero."
            print(f"Error: {msg}")
        except IndexError as e:
            print(f"Error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nHasta luego.")
            return 0
        finally:
            print("-" * SEPARATOR_WIDTH)


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.command in (None, "interactive"):
        return interactive(args.file)
    tasks = load_tasks(args.file)
    try:
        if args.command == "add":
            title = add_task(tasks, " ".join(args.titulo))
            save_tasks(tasks, args.file)
            print(f"Tarea agregada: {title}")
        elif args.command == "list":
            print(format_tasks(tasks))
        elif args.command == "remove":
            removed = remove_task(tasks, args.posicion)
            save_tasks(tasks, args.file)
            print(f"Tarea eliminada: {removed}")
    except (ValueError, IndexError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
