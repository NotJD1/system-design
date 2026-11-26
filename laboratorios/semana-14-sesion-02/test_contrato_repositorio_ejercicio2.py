"""Ejercicio 2: las pruebas de contrato del repositorio.

El servicio se prueba rapido con RepositorioEnMemoria, un doble de prueba.
Eso solo vale si el doble se comporta igual que RepositorioSQLite. Estas
pruebas corren dos veces cada una, una con cada repositorio (la fixture
`repositorio` tiene dos parametros): si una pasa con uno y falla con el
otro, el doble miente.

    pytest test_contrato_repositorio_ejercicio2.py -v
"""

import sqlite3

import pytest

from dominio import semana_de
from repositorio import RepositorioEnMemoria, RepositorioSQLite


@pytest.fixture(params=["memoria", "sqlite"])
def repositorio(request, tmp_path):
    if request.param == "memoria":
        repo = RepositorioEnMemoria()
    else:
        repo = RepositorioSQLite(str(tmp_path / "reservau.db"))
    yield repo
    repo.cerrar()


def test_guardar_y_buscar(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    assert repositorio.buscar("r1") == ("ana", "2026-11-17")


def test_buscar_inexistente(repositorio):
    assert repositorio.buscar("r_inexistente") is None


def test_contar_en_semana(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    repositorio.guardar("r2", "ana", "2026-11-18")
    repositorio.guardar("r3", "ana", "2026-11-24")
    repositorio.guardar("r4", "beto", "2026-11-17")

    assert repositorio.contar_en_semana("ana", semana_de("2026-11-17")) == 2
    assert repositorio.contar_en_semana("ana", semana_de("2026-11-24")) == 1
    assert repositorio.contar_en_semana("beto", semana_de("2026-11-17")) == 1


def test_guardar_id_duplicado(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")

    with pytest.raises(sqlite3.IntegrityError):
        repositorio.guardar("r1", "beto", "2026-11-18")


def test_puntos_de(repositorio):
    repositorio.guardar("r1", "ana", "2026-11-17")
    repositorio.guardar("r2", "ana", "2026-11-18")

    assert repositorio.puntos_de("ana") == 0
    assert repositorio.puntos_de("beto") == 0