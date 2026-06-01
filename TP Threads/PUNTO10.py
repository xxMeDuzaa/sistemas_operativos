import threading
import time
import random
from multiprocessing import Value

# =====================================================================
# 1. MUTEX / LOCK & CRITICAL SECTION
# Protege una variable compartida para evitar condiciones de carrera.
# Es binario (abierto o cerrado). Si un hilo entra a la sección crítica, "cierra la puerta"
# y los demás esperan afuera en fila.
# =====================================================================

contador_compartido = 0
lock = threading.Lock()

def incrementar_con_lock():
    global contador_compartido
    for _ in range(100000):
        # El bloque 'with' adquiere y libera el lock automáticamente
        with lock:
            # ---------------------------------------------------------
            # ZONA DE SECCIÓN CRÍTICA (Critical Section)
            # Solo un hilo a la vez puede modificar 'contador_compartido'
            contador_compartido += 1
            # ---------------------------------------------------------

def ejecutar_ejemplo_lock():
    global contador_compartido
    contador_compartido = 0
    hilos = [threading.Thread(target=incrementar_con_lock) for _ in range(3)]

    for h in hilos: h.start()
    for h in hilos: h.join()

    print(f"[LOCK] Contador final (esperado 300000): {contador_compartido}")


# =====================================================================
# 2. SEMAPHORE
# Permite que un número limitado de hilos accedan a un recurso.
# Es un contador. En este caso, permite el paso a los dos primeros hilos;
# el tercero rebotará y esperará a que uno de los dos primeros libere su lugar.
# =====================================================================

# Inicializamos el semáforo con un valor de 2
semaforo = threading.Semaphore(2)

def acceder_recurso_limitado(id_hilo):
    print(f"-> Hilo {id_hilo} intentando acceder al recurso...")
    with semaforo:
        # ---------------------------------------------------------
        # ZONA DE SECCIÓN CRÍTICA (Critical Section)
        # Máximo 2 hilos van a estar ejecutando este bloque en simultáneo
        print(f"   [!] Hilo {id_hilo} DENTRO del recurso.")
        time.sleep(1)  # Simulamos una tarea
        print(f"   [✓] Hilo {id_hilo} SALIENDO del recurso.")
        # ---------------------------------------------------------

def ejecutar_ejemplo_semaforo():
    hilos = [threading.Thread(target=acceder_recurso_limitado, args=(i,)) for i in range(5)]
    for h in hilos: h.start()
    for h in hilos: h.join()


# =====================================================================
# 3. MONITOR / CONDITION
# Coordina la comunicación entre un Productor y un Consumidor.
# Envuelve al Lock clásico agregándole variables de condición (wait() y notify()).
# Es ideal cuando un hilo no solo necesita exclusividad, sino que además debe esperar a que
# ocurra un evento específico (ej. que el buffer deje de estar lleno).
# =====================================================================

buffer = []
CAPACIDAD_BUFFER = 3
condicion = threading.Condition()

def productor():
    for i in range(5):
        time.sleep(random.uniform(0.1, 0.5))  # Simula tiempo de producción
        with condicion:
            # Si el buffer está lleno, el productor espera
            while len(buffer) == CAPACIDAD_BUFFER:
                print("[Productor] Buffer lleno. Esperando...")
                condicion.wait()

            # ---------------------------------------------------------
            # ZONA DE SECCIÓN CRÍTICA (Critical Section)
            item = f"Item-{i}"
            buffer.append(item)
            print(f"[Productor] Produjo: {item}. Buffer actual: {len(buffer)}")
            # ---------------------------------------------------------

            # Notifica al consumidor que ya hay elementos disponibles
            condicion.notify()

def consumidor():
    for _ in range(5):
        time.sleep(random.uniform(0.2, 0.6))  # Simula tiempo de consumo
        with condicion:
            # Si el buffer está vacío, el consumidor espera
            while len(buffer) == 0:
                print("[Consumidor] Buffer vacío. Esperando...")
                condicion.wait()

            # ---------------------------------------------------------
            # ZONA DE SECCIÓN CRÍTICA (Critical Section)
            item = buffer.pop(0)
            print(f"[Consumidor] Consumió: {item}. Buffer actual: {len(buffer)}")
            # ---------------------------------------------------------

            # Notifica al productor que se liberó espacio
            condicion.notify()

def ejecutar_ejemplo_monitor():
    h_prod = threading.Thread(target=productor)
    h_cons = threading.Thread(target=consumidor)

    h_prod.start()
    h_cons.start()

    h_prod.join()
    h_cons.join()


# =====================================================================
# 4. ATOMIC OPERATIONS
# En lenguajes compilados son instrucciones directas de la CPU (como LOCK XADD en x86).
# En Python, para garantizar que una modificación de variable sea 100% indivisible y segura sin
# locks manuales en el código principal, recurrimos a las estructuras optimizadas de
# multiprocessing.Value.
# =====================================================================

def incrementar_atomico(contador_global):
    for _ in range(100000):
        # ---------------------------------------------------------
        # ZONA DE SECCIÓN CRÍTICA (Critical Section - Manejada internamente)
        # El método 'get_lock()' asegura la atomicidad de la operación
        with contador_global.get_lock():
            contador_global.value += 1
        # ---------------------------------------------------------

def ejecutar_ejemplo_atomico():
    # 'i' representa un entero firmado mapeado en memoria compartida atómica
    contador_global = Value('i', 0)

    hilos = [threading.Thread(target=incrementar_atomico, args=(contador_global,)) for _ in range(3)]

    for h in hilos: h.start()
    for h in hilos: h.join()

    print(f"[ATOMIC] Contador final (esperado 300000): {contador_global.value}")


# =====================================================================
# EJECUCIÓN PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    print("\n--- 1. EJEMPLO MUTEX / LOCK ---")
    ejecutar_ejemplo_lock()
    print("\n")

    print("--- 2. EJEMPLO SEMAPHORE (Máximo 2 hilos a la vez) ---")
    ejecutar_ejemplo_semaforo()
    print("\n")

    print("--- 3. EJEMPLO MONITOR / CONDITION (Productor-Consumidor) ---")
    ejecutar_ejemplo_monitor()
    print("\n")

    print("--- 4. EJEMPLO ATOMIC OPERATIONS ---")
    ejecutar_ejemplo_atomico()
