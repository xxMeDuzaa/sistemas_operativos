import threading

import time


def descargar_archivo():

    for progreso in range(10, 101, 10):

        print(f"Descargando archivo... {progreso}%")

        time.sleep(1)

    print("Descarga finalizada.")


def interfaz_activa():

    for i in range(10):

        print("Interfaz activa... el usuario puede seguir usando la aplicación.")

        time.sleep(0.5)


hilo_descarga = threading.Thread(target=descargar_archivo)

hilo_interfaz = threading.Thread(target=interfaz_activa)

hilo_descarga.start()

hilo_interfaz.start()

hilo_descarga.join()

hilo_interfaz.join()

print("Programa finalizado.")
