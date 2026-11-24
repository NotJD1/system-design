"""Pruebas del Ejercicio 3: las escriben ustedes, en pareja, una a la vez."""

import pytest

from recurrentes_ejercicio3 import AgendaDeCancha


def test_obtener_calendario():
    agenda = AgendaDeCancha("cancha1")

    calendario = agenda.calendario("2026-11-16")

    assert calendario is not None


def test_misma_fecha_devuelve_mismo_calendario():
    agenda = AgendaDeCancha("cancha1")

    calendario1 = agenda.calendario("2026-11-16")
    calendario2 = agenda.calendario("2026-11-16")

    assert calendario1 is calendario2


def test_fechas_diferentes_tienen_calendarios_diferentes():
    agenda = AgendaDeCancha("cancha1")

    calendario1 = agenda.calendario("2026-11-16")
    calendario2 = agenda.calendario("2026-11-23")

    assert calendario1 is not calendario2


def test_reservar_una_semana():
    agenda = AgendaDeCancha("cancha1")

    resultados = agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 9, 10, 1)

    assert resultados == [ ("2026-11-16", "reservada") ]

    assert agenda.calendario("2026-11-16").franja_de( "entreno-1" ).inicio == 9


def test_reservar_varias_semanas():
    agenda = AgendaDeCancha("cancha1")

    resultados = agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 3 )

    assert resultados == [ ("2026-11-16", "reservada"), ("2026-11-23", "reservada"), ("2026-11-30", "reservada") ]


def test_fecha_ocupada_se_saltea_y_continua():
    agenda = AgendaDeCancha("cancha1")

    agenda.calendario("2026-11-16").reservar( "otra-reserva", "pedro", 9, 10 )

    resultados = agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 3 )

    assert resultados == [ ("2026-11-16", "ocupada"), ("2026-11-23", "reservada"), ("2026-11-30", "reservada") ]

    assert agenda.calendario("2026-11-23").franja_de( "entreno-2" ).inicio == 9


def test_superar_limite_de_horas_no_reserva():
    agenda = AgendaDeCancha("cancha1")

    agenda.calendario("2026-11-16").reservar( "otra-reserva", "ana", 7, 8 )

    resultados = agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 11, 2 )

    assert resultados == [ ("2026-11-16", "limite"), ("2026-11-23", "reservada") ]

    assert agenda.calendario("2026-11-16").reservas() == [ ("otra-reserva", "ana", agenda.calendario("2026-11-16").franja_de("otra-reserva")) ]


def test_acepta_una_semana():
    agenda = AgendaDeCancha("cancha1")

    resultados = agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 1 )

    assert len(resultados) == 1


def test_acepta_doce_semanas():
    agenda = AgendaDeCancha("cancha1")

    resultados = agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 12 )

    assert len(resultados) == 12
    assert all(resultado == "reservada" for _, resultado in resultados)


def test_cero_semanas_lanza_error_sin_reservar():
    agenda = AgendaDeCancha("cancha1")

    with pytest.raises(ValueError):
        agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 0 )

    assert agenda.calendarios == {}


def test_mas_de_doce_semanas_lanza_error_sin_reservar():
    agenda = AgendaDeCancha("cancha1")

    with pytest.raises(ValueError):
        agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 13 )

    assert agenda.calendarios == {}


def test_identificadores_corresponden_a_la_semana():
    agenda = AgendaDeCancha("cancha1")

    agenda.calendario("2026-11-23").reservar( "ocupada", "pedro", 9, 10 )

    agenda.reservar_cada_semana( "entreno", "ana", "2026-11-16", 9, 10, 3 )

    assert agenda.calendario("2026-11-16").franja_de( "entreno-1" ).fecha == "2026-11-16"

    assert agenda.calendario("2026-11-30").franja_de( "entreno-3" ).fecha == "2026-11-30"
