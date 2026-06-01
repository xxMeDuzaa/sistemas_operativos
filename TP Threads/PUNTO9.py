import threading
import time

# Barrera para forzar a que ambos hilos se esperen mutuamente antes de evaluar
barrera_intencion = threading.Barrier(2)
barrera_evaluacion = threading.Barrier(2)

intencion_hilo_A = False
intencion_hilo_B = False
simulacion_activa = True

def funcion_hilo_A():
    global intencion_hilo_A, intencion_hilo_B
    print("[Hilo A] Iniciado.\n")
    while simulacion_activa:
        intencion_hilo_A = True
        print("[Hilo A] Quiero usar el recurso...\n")

        # ESPERA 1: Forzamos a que ambos hayan declarado su intención
        try: barrera_intencion.wait(timeout=1)
        except threading.BrokenBarrierError: break

        # CONDICIÓN DE LIVELOCK
        if intencion_hilo_B:
            print("[Hilo A] ¡Oh! El Hilo B también lo quiere. Cedo el paso...\n")
            intencion_hilo_A = False

            # ESPERA 2: Esperamos a que ambos hayan decidido ceder antes de reintentar
            try: barrera_evaluacion.wait(timeout=1)
            except threading.BrokenBarrierError: break

            time.sleep(0.1)
            continue

        print("[Hilo A] *** ÉXITO ***")
        intencion_hilo_A = False
        break

def funcion_hilo_B():
    global intencion_hilo_A, intencion_hilo_B
    print("[Hilo B] Iniciado.\n")
    while simulacion_activa:
        intencion_hilo_B = True
        print("[Hilo B] Quiero usar el recurso...\n")

        # ESPERA 1: Forzamos a que ambos hayan declarado su intención
        try: barrera_intencion.wait(timeout=1)
        except threading.BrokenBarrierError: break

        # CONDICIÓN DE LIVELOCK
        if intencion_hilo_A:
            print("[Hilo B] ¡Oh! El Hilo A también lo quiere. Cedo el paso...\n")
            intencion_hilo_B = False

            # ESPERA 2: Esperamos a que ambos hayan decidido ceder antes de reintentar
            try: barrera_evaluacion.wait(timeout=1)
            except threading.BrokenBarrierError: break

            time.sleep(0.1)
            continue

        print("[Hilo B] *** ÉXITO ***")
        intencion_hilo_B = False
        break

if __name__ == "__main__":
    print("\n--- INICIANDO SIMULACIÓN DE LIVELOCK ---")
    print("Observa cómo ambos hilos cambian de estado continuamente, pero ninguno avanza.\n")

    hilo_a = threading.Thread(target=funcion_hilo_A)
    hilo_b = threading.Thread(target=funcion_hilo_B)

    hilo_a.start()
    hilo_b.start()

    time.sleep(4)
    print("\n--- DETENIENDO SIMULACIÓN FORZOSA ---")
    simulacion_activa = False
    barrera_intencion.abort()
    barrera_evaluacion.abort()

    hilo_a.join()
    hilo_b.join()
    print("Simulación terminada. Ninguno de los hilos logró imprimir el mensaje de *** ÉXITO ***.")
