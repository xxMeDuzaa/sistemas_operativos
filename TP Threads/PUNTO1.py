import threading
import time


def imprimir_numeros():

    for i in range(1, 11):

        print(f"Números: {i}")
        time.sleep(0.5)
       


def imprimir_letras():

    for letra in "ABCDEFGHIJ":

        print(f"Letras: {letra}")
        time.sleep(0.5)
     


hilo_numeros = threading.Thread(target=imprimir_numeros)

hilo_letras = threading.Thread(target=imprimir_letras)

hilo_numeros.start()

hilo_letras.start()

hilo_numeros.join()

hilo_letras.join()

print("Finalizó la ejecución de ambos hilos.")
