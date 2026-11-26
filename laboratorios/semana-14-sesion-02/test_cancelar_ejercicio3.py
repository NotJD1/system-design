"""Ejercicio 3: las pruebas de cancelar. Sin pruebas de partida: las
escribes tu, decidiendo de que tipo es cada una.

    pytest test_cancelar_ejercicio3.py --durations=0
"""
import pytest

from repositorio import RepositorioEnMemoria, RepositorioSQLite
from servicio import ServicioDeReservas


# UNITARIAS

@pytest.fixture
def repositorio_memoria():
    return RepositorioEnMemoria()


@pytest.fixture
def servicio(repositorio_memoria):
    return ServicioDeReservas(repositorio=repositorio_memoria)


def test_cancelar_elimina_reserva(servicio, repositorio_memoria):
    repositorio_memoria.guardar("r1", "pedro", "2026-11-26")

    servicio.cancelar("r1", 30)

    assert repositorio_memoria.buscar("r1") is None


def test_cancelar_suma_puntos(servicio, repositorio_memoria):
    repositorio_memoria.guardar("r1", "pedro", "2026-11-26")

    servicio.cancelar("r1", 30)

    assert repositorio_memoria.puntos_de("pedro") == 2


def test_cancelar_reserva_desconocida(servicio, repositorio_memoria):
    with pytest.raises(ValueError, match="reserva desconocida"):
        servicio.cancelar("inexistente", 30)

    assert repositorio_memoria.puntos_de("pedro") == 0


def test_cancelar_dos_veces_no_duplica_puntos(servicio, repositorio_memoria):
    repositorio_memoria.guardar("r1", "pedro", "2026-11-26")

    servicio.cancelar("r1", 30)

    with pytest.raises(ValueError, match="reserva desconocida"):
        servicio.cancelar("r1", 30)

    assert repositorio_memoria.puntos_de("pedro") == 2


# INTEGRACION

def test_cancelar_con_sqlite():
    repositorio = RepositorioSQLite(":memory:")
    servicio = ServicioDeReservas(repositorio=repositorio)

    try:
        repositorio.guardar("r1", "pedro", "2026-11-26")

        servicio.cancelar("r1", 30)

        assert repositorio.buscar("r1") is None
        assert repositorio.puntos_de("pedro") == 2

    finally:
        repositorio.cerrar()