#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <thread>

/**
 * @brief Clase que controla un productor y un consumidor.
 * 
 */
class prod_cons{
private:
  std::queue<int> buffer;
  const unsigned int MAX_BUFFER;
  std::mutex mtx;

  // Sincronizan a los hilos
  std::condition_variable cv_producer;
  std::condition_variable cv_consumer;

public:
  prod_cons(const int max);
  void productor();
  void consumidor();
};

/**
 * @brief Constructor de la clase prod_cons.
 * 
 * @param size Tamaño maximo de la cola de acceso.
 */
prod_cons::prod_cons(const int size)
  : MAX_BUFFER(size) {}

/**
 * @brief Genera un hilo consumidor.
 * 
 */
void prod_cons::productor() {
  for (int i = 1; i < 20; ++i) {
    // El lock sirve para que otros hilos no puedan acceder a las variables al mismo tiempo.
    std::unique_lock<std::mutex> lock(mtx);
    
    // Si el buffer esta lleno, espera a que se vacie.
    cv_producer.wait(lock, [this] { return buffer.size() < MAX_BUFFER; });
    
    buffer.push(i);
    std::cout << "Productor: agregó " << i << "\n";
    
    lock.unlock();

    // Despierta al consumidor.
    cv_consumer.notify_one();
  }
}

/**
 * @brief Genera un hilo productor.
 * 
 */
void prod_cons::consumidor() {
  for (int i = 1; i < 20; ++i) {
    std::unique_lock<std::mutex> lock(mtx);
    // Esperar si el buffer está vacío.
    cv_consumer.wait(lock, [this] { return !buffer.empty(); });
    
    int valor = buffer.front();
    buffer.pop();
    std::cout << "Consumidor: consumió " << valor << "\n";
    
    lock.unlock();

    // Despierta al productor.
    cv_producer.notify_one();
  }
}

auto main() -> int {
  prod_cons hilos(5);
  
  // Crear hilo productor
  std::thread productor(&prod_cons::productor, &hilos);
  
  // Crear hilo consumidor
  std::thread consumidor(&prod_cons::consumidor, &hilos);
  
  // Esperar a que ambos hilos terminen
  productor.join();
  consumidor.join();
  
  std::cout << "\nFin de la ejecución\n";
  
  return 0;
}
