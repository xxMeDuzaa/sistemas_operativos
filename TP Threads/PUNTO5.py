#Código con deadlock intencional:

import threading
import time


recursoA = threading.Lock()
recursoB = threading.Lock()

def hilo1():

    print("Hilo 1 intentando bloquear RecursoA")
    recursoA.acquire()
    print("Hilo 1 bloqueó RecursoA")

    time.sleep(1)

    print("Hilo 1 intentando bloquear RecursoB")
    recursoB.acquire()
    print("Hilo 1 bloqueó RecursoB")

    recursoB.release()
    recursoA.release()


def hilo2():

    print("Hilo 2 intentando bloquear RecursoB")
    recursoB.acquire()
    print("Hilo 2 bloqueó RecursoB")

    time.sleep(1)

    print("Hilo 2 intentando bloquear RecursoA")
    recursoA.acquire()
    print("Hilo 2 bloqueó RecursoA")

    recursoA.release()
    recursoB.release()


t1 = threading.Thread(target=hilo1)
t2 = threading.Thread(target=hilo2)

t1.start()
t2.start()

t1.join()
t2.join()

print("Programa finalizado")