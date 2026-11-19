"""Ejercicio 3: el orden del feed y los espacios mas reservados.

Mostrar el feed de lo mas nuevo a lo mas viejo es justo y es aburrido: un
entrenamiento de hace 5 minutos tapa el partido de tu propio equipo, que
ya tiene 40 confirmaciones. ReservaU pide un ranking simple, que se pueda
explicar en una oracion.

OrdenadorDeFeed se construye con dos diccionarios:
- interacciones: id de publicacion -> cuantas personas confirmaron
  asistencia o comentaron (0 si no aparece).
- equipos_de: estudiante -> lista de autores (equipos) en los que juega
  (lista vacia si no aparece).

Metodos:

- puntaje(publicacion, estudiante, ahora): (interacciones + 1) multiplicado
  por 3 si el autor es un equipo del estudiante (por 1 si no), dividido
  para (1 + horas), donde horas es (ahora - publicacion.momento) // 60
  (los momentos estan en minutos).

- ordenar(publicaciones, estudiante, ahora, cantidad): las `cantidad`
  publicaciones de mayor puntaje. En un empate de puntaje, primero la mas
  nueva (mayor momento), y si tambien empatan, la de id menor. Ademas,
  nunca tres seguidas del mismo autor: si la siguiente por puntaje seria
  la tercera seguida de ese autor, va la mejor de otro autor; si no queda
  ninguna de otro autor, va igual.

- espacios_mas_reservados(reservas, ahora, cantidad): reservas es una lista
  de tuplas (espacio, momento). Cuenta, por espacio, las reservas con
  momento en los ultimos 7 dias (ahora - 10080 < momento <= ahora), y
  devuelve una lista de tuplas (espacio, conteo) con los `cantidad` de
  mayor conteo; en un empate, primero el nombre menor. Los espacios sin
  reservas en esa ventana no aparecen.

Esta vez no hay codigo de partida. Corre las pruebas con:

    pytest test_ranking_ejercicio3.py
"""

from actividad import Publicacion

class OrdenadorDeFeed:
  def __init__(self, interacciones, equipos_de):
    self.interacciones = interacciones
    self.equipos_de = equipos_de

  def puntaje(self, publicacion, estudiante, ahora):

    interacciones = self.interacciones.get(publicacion.id, 0)

    equipos = self.equipos_de.get(estudiante, [])

    multiplicador = 1

    if publicacion.autor in equipos:
      multiplicador = 3

    horas = (ahora - publicacion.momento) // 60

    return (interacciones + 1) * multiplicador / (1 + horas)

  def ordenar(self, publicaciones, estudiante, ahora, cantidad):

    pendientes = []

    for publicacion in publicaciones:

      puntaje = self.puntaje(publicacion, estudiante, ahora)

      pendientes.append((puntaje, publicacion.momento, publicacion.id, publicacion))

    for i in range(1, len(pendientes)):

      actual = pendientes[i]
      j = i - 1

      while j >= 0:

        anterior = pendientes[j]

        if actual[0] > anterior[0]:
          pendientes[j + 1] = anterior

        elif actual[0] == anterior[0]:

          if actual[1] > anterior[1]:
            pendientes[j + 1] = anterior

          elif actual[1] == anterior[1] and actual[2] < anterior[2]:
            pendientes[j + 1] = anterior

          else:
            break

        else:
          break

        j -= 1

      pendientes[j + 1] = actual

    resultado = []

    while len(resultado) < cantidad and len(pendientes) > 0:

      posicion = 0

      if len(resultado) >= 2:

        autor_1 = resultado[-1].autor
        autor_2 = resultado[-2].autor

        if autor_1 == autor_2:

          for i in range(len(pendientes)):

            if pendientes[i][3].autor != autor_1:
              posicion = i
              break

      seleccionada = pendientes.pop(posicion)

      resultado.append(seleccionada[3])

    return resultado

  def espacios_mas_reservados(self, reservas, ahora, cantidad):

    conteos = {}

    for espacio, momento in reservas:

      if ahora - 10080 < momento <= ahora:

        if espacio not in conteos:
          conteos[espacio] = 0

        conteos[espacio] += 1

    resultado = []

    for espacio in conteos:

      resultado.append((espacio, conteos[espacio]))

    for i in range(1, len(resultado)):

      actual = resultado[i]
      j = i - 1

      while j >= 0:

        anterior = resultado[j]

        if actual[1] > anterior[1]:
          resultado[j + 1] = anterior

        elif actual[1] == anterior[1] and actual[0] < anterior[0]:
          resultado[j + 1] = anterior

        else:
          break

        j -= 1

      resultado[j + 1] = actual

    return resultado[:cantidad]
