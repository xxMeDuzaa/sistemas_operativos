#Código corregido evitando deadlock (mismo orden de bloqueo):

import threading
import time


recursoA = threading.Lock()
recursoB = threading.Lock()

def trabajar(nombre):

    print(nombre, "intentando bloquear RecursoA")

    with recursoA:

        print(nombre, "bloqueó RecursoA")

        time.sleep(1)

        print(nombre, "intentando bloquear RecursoB")

        with recursoB:

            print(nombre, "bloqueó RecursoB")
            print(nombre, "trabajando...")


t1 = threading.Thread(target=trabajar, args=("Hilo 1",))
t2 = threading.Thread(target=trabajar, args=("Hilo 2",))

t1.start()
t2.start()

t1.join()
t2.join()

print("Programa finalizado sin deadlock")