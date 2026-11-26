"""Ejercicio 1: la misma cobertura, en la base de la piramide. Empieza
vacio: se escribe en vivo.

Por cada prueba de punta a punta de test_suite_heredada.py que se pueda
bajar de nivel, una prueba unitaria del servicio (con RepositorioEnMemoria)
o una de integracion (con RepositorioSQLite o con la API), y una sola
prueba de punta a punta que recorra el camino completo.

    pytest test_rapidas_ejercicio1.py --durations=0
"""

import pytest
from repositorio import RepositorioEnMemoria, RepositorioSQLite
from servicio import ServicioDeReservas
from api import ApiDeReservas
from entorno_e2e import NavegadorSimulado

# fixture = todos los componentes para que el ambiente de testing funcione

#Unitarias

@pytest.fixture
def servicio():
    return ServicioDeReservas(repositorio=RepositorioEnMemoria())

def test_cuarta_reserva_se_rechaza(servicio):

    servicio.reservar('r1', 'pedro', '2026-11-26')
    servicio.reservar('r2', 'pedro', '2026-11-27')
    servicio.reservar('r3', 'pedro', '2026-11-28')

    with pytest.raises(ValueError, match='cupo semanal agotado'):
        servicio.reservar('r4', 'pedro', '2026-11-29')

def test_cuarta_reserva_diferente_semana_aceptada(servicio):

    servicio.reservar('r1', 'pedro', '2026-11-26')
    servicio.reservar('r2', 'pedro', '2026-11-27')
    servicio.reservar('r3', 'pedro', '2026-11-28')
    assert servicio.reservar('r4','pedro', '2026-11-30') is None

#integración
def test_api_cancelar_desconocido_404():

    servicio_sql = RepositorioSQLite(':memory:')
    api = ApiDeReservas(servicio=servicio_sql)

    respuesta = api.manejar({

        'metodo' : "delete",
        'ruta' : '/reservas/reserva-inexistente',
        'cuerpo' : {

            'minutos_de_anticipacion' : 90

        }
    })

    assert respuesta['estado']==404

#E2E

def test_reservar_cacnelar_ver_puntos():
    navegador = NavegadorSimulado()

    navegador.iniciar_sesion('pedro')

    assert navegador.reservar('r1', '2026-11-26')['estado'] == 201
    assert navegador.cancelar('r1', 30)['estado'] == 200
    assert navegador.ver_puntos() == 2