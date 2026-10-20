"""Ejercicio 3: balanceador de menos conexiones (least connections).

Corre las pruebas con:

    pytest test_menos_conexiones_ejercicio3.py

Las pruebas tambien usan tu BalanceadorRoundRobin del Ejercicio 2, para
comparar los dos algoritmos con el mismo trafico.
"""


class BalanceadorMenosConexiones:
    def __init__(self, servidores):
        self.servidores = servidores

    def enviar(self, duracion):
        # TODO: elige, entre los servidores sanos que todavia pueden
        # atender, el que tiene menos conexiones activas en este momento.
        # Si hay empate, gana el que aparece primero en la lista.
        # Enviale la solicitud y devuelve su nombre. Si ningun servidor
        # puede atenderla, devuelve None.

        servidores_sanos = []

        for intento in self.servidores:

            if intento.puede_atender():

                servidores_sanos.append(intento)

        if len(servidores_sanos) == 0:
            return None

        mejor_servidor = servidores_sanos[0]

        for conexiones in servidores_sanos:

            if conexiones.conexiones_activas() < mejor_servidor.conexiones_activas():

                mejor_servidor = conexiones

        mejor_servidor.atender(duracion)

        return mejor_servidor.nombre
