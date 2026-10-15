# Gestor de tareas pendientes (CLI)

Herramienta ligera de terminal para que los coordinadores operativos registren, consulten y eliminen tareas pendientes sin depender de mensajes de chat ni notas sueltas. Las tareas se guardan en un archivo local (`todos.csv`), así que no se pierden al cerrar la terminal.

Está hecha **solo con la librería estándar de Python** (`argparse`, `csv`, `pathlib`, `sys`). No hay dependencias que instalar.

## Requisitos

- Python 3.8 o superior.

## Estructura del proyecto

| Archivo | Descripción |
|---|---|
| `todo.py` | Aplicación completa: lógica, persistencia y CLI. |
| `test_todo.py` | Pruebas automáticas (compatibles con pytest). |
| `todos.csv` | Se crea automáticamente al agregar la primera tarea. |
| `project.md` | Brief funcional original. |

## Uso

Todos los comandos se ejecutan desde la carpeta del proyecto.

### Modo interactivo (recomendado)

```bash
python3 todo.py
```

Sin ningún comando se abre un menú que permite usar todas las funciones sin recordar la sintaxis (también con `python3 todo.py interactive`):

```
=== Gestor de tareas ===
1. Agregar tarea
2. Ver tareas
3. Eliminar tarea
4. Salir
```

Los cambios se guardan en `todos.csv` al instante. Los errores (opción no válida, posición no numérica o fuera de rango) muestran un mensaje y el menú sigue activo. Ctrl+C o Ctrl+D también salen. En "Eliminar" puedes pulsar Enter para cancelar.

### Modo comandos

### Agregar una tarea

```bash
python3 todo.py add Llamar al cliente de Valencia
# Tarea agregada: Llamar al cliente de Valencia
```

El título puede tener varias palabras sin comillas. Si incluye caracteres especiales de la shell (`;`, `&`, `*`), ponlo entre comillas.

### Mostrar las tareas pendientes

```bash
python3 todo.py list
# 1. Llamar al cliente de Valencia
# 2. Revisar ruta de reparto
```

Si no hay tareas, muestra `No hay tareas pendientes.`

### Eliminar una tarea por su posición

```bash
python3 todo.py remove 1
# Tarea eliminada: Llamar al cliente de Valencia
```

La posición empieza en 1 y es la que muestra `list`. Al eliminar una tarea, las siguientes suben de posición, así que conviene ejecutar `list` de nuevo antes de borrar otra.

### Usar otro archivo CSV

```bash
python3 todo.py -f turno_noche.csv add Confirmar camion 12
```

La opción `-f` / `--file` va **antes** del comando. Por defecto se usa `todos.csv` en el directorio actual.

### Ayuda

```bash
python3 todo.py --help
python3 todo.py add --help
```

## Cómo funciona

Cada ejecución sigue el mismo ciclo:

1. **Carga** las tareas desde el CSV (`load_tasks`).
2. **Aplica** el comando pedido sobre la lista en memoria.
3. **Guarda** el resultado en el CSV si hubo cambios (`add` y `remove`).

Como el estado vive en el archivo, cerrar y abrir la terminal no pierde nada.

### Formato de `todos.csv`

Un CSV con una sola columna, `titulo`:

```csv
titulo
Llamar al cliente de Valencia
"Revisar ruta, urgente"
```

El módulo `csv` entrecomilla automáticamente los títulos que contienen comas, así que no hay problema en usarlas.

## Funciones (`todo.py`)

| Función | Qué hace |
|---|---|
| `load_tasks(path)` | Lee el CSV y devuelve la lista de títulos. Si el archivo no existe devuelve `[]`; ignora filas sin título. |
| `save_tasks(tasks, path)` | Escribe la lista completa en el CSV (con cabecera `titulo`), sobrescribiendo el contenido anterior. |
| `add_task(tasks, title)` | Quita espacios sobrantes y añade el título al final de la lista. Lanza `ValueError` si el título queda vacío. |
| `remove_task(tasks, position)` | Elimina y devuelve la tarea en la posición indicada (base 1). Lanza `IndexError` si está fuera de rango. |
| `format_tasks(tasks)` | Devuelve el texto numerado para mostrar, o el mensaje de lista vacía. |
| `build_parser()` | Define la CLI con `argparse`: opción `-f` y subcomandos `add`, `list`, `remove`, `interactive`. |
| `interactive(path, input_fn)` | Bucle del menú interactivo: agregar, ver, eliminar y salir, guardando tras cada cambio. |
| `main(argv=None)` | Punto de entrada: sin comando abre el menú; con comando orquesta carga, acción y guardado. Devuelve el código de salida. |

## Manejo de errores

Los errores se escriben en `stderr` y el programa termina con código de salida `1`:

```bash
python3 todo.py remove 5
# Error: Posicion 5 invalida. Hay 2 tarea(s) pendiente(s).
echo $?   # 1
```

Casos cubiertos: título vacío, posición `0`, negativa o mayor que el número de tareas, y lista vacía al intentar eliminar. Si la posición no es un número entero, `argparse` muestra su propio mensaje de uso (código de salida 2).

## Pruebas

```bash
pip install pytest
python3 -m pytest -q
```

Las pruebas usan directorios temporales, por lo que no tocan tu `todos.csv` real. Cubren agregar, listar, eliminar, persistencia entre ejecuciones, archivo inexistente, posiciones inválidas y título vacío.

## Alcance de esta versión

- Incluido: agregar, listar y eliminar por posición, con persistencia en CSV.
- Fuera de alcance: **editar tareas**. El flujo esperado es eliminar y volver a crear.
