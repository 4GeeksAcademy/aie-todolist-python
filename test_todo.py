import todo


def test_add_list_remove_persist(tmp_path, capsys):
    f = str(tmp_path / "todos.csv")
    assert todo.main(["-f", f, "add", "Llamar", "al", "cliente, urgente"]) == 0
    assert todo.main(["-f", f, "add", "Revisar ruta"]) == 0
    assert todo.load_tasks(f) == ["Llamar al cliente, urgente", "Revisar ruta"]

    capsys.readouterr()
    todo.main(["-f", f, "list"])
    assert capsys.readouterr().out.splitlines() == [
        "1. Llamar al cliente, urgente",
        "2. Revisar ruta",
    ]

    assert todo.main(["-f", f, "remove", "1"]) == 0
    assert todo.load_tasks(f) == ["Revisar ruta"]


def test_load_missing_file(tmp_path):
    assert todo.load_tasks(tmp_path / "nada.csv") == []


def test_invalid_position(tmp_path):
    f = str(tmp_path / "todos.csv")
    assert todo.main(["-f", f, "remove", "1"]) == 1
    todo.main(["-f", f, "add", "x"])
    assert todo.main(["-f", f, "remove", "0"]) == 1


def test_empty_title():
    try:
        todo.add_task([], "   ")
    except ValueError:
        return
    raise AssertionError("esperaba ValueError")
