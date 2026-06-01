import threading
import time

lock = threading.Lock()

# Contadores de acceso
accesos_rapidos = 0
accesos_lentos = 0

# Variable para detener ejecución
ejecutando = True

def hilo_rapido(nombre):
    global accesos_rapidos

    while ejecutando:

        lock.acquire()

        # Usa el recurso
        accesos_rapidos += 1

        print(nombre, "accedió al recurso")

        # Mantiene el recurso poco tiempo
        time.sleep(0.01)

        lock.release()

        # Vuelve a competir casi inmediatamente
        time.sleep(0.01)


def hilo_lento():
    global accesos_lentos

    while ejecutando:

        adquirido = lock.acquire(timeout=0.02)

        if adquirido:

            accesos_lentos += 1

            print("Hilo lento accedió al recurso")

            time.sleep(0.05)

            lock.release()

        else:
            print("Hilo lento quedó esperando")


hilos = []

# Varios hilos rápidos
for i in range(3):
    t = threading.Thread(target=hilo_rapido, args=(f"Hilo rápido {i+1}",))
    hilos.append(t)

# Un hilo lento
t_lento = threading.Thread(target=hilo_lento)
hilos.append(t_lento)

# Iniciar hilos
for h in hilos:
    h.start()

# Ejecutar durante unos segundos
time.sleep(5)

# Detener ejecución
ejecutando = False

# Esperar finalización
for h in hilos:
    h.join()

print("\nRESULTADOS")
print("Accesos hilos rápidos:", accesos_rapidos)
print("Accesos hilo lento:", accesos_lentos)