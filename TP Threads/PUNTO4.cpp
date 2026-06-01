#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

/**
 * @brief Clase base para comprobar el race condition.
 * 
 */
class race_condition {
protected:
  int contador;
  const int NUM_HILOS;
  const int INCREMENTOS;

  virtual void incrementar() = 0;

public:
  race_condition(const int hilos, const int incrementos);
  void ejecutar();
  void resultados() const;
};

/**
 * @brief Constructor de la clase.
 * 
 * @param hilos Cantidad de hilos que generará.
 * @param incrementos Hasta que valor incrementará el contador.
 */
race_condition::race_condition(const int hilos, const int incrementos)
  : contador(0), NUM_HILOS(hilos), INCREMENTOS(incrementos) {}

/**
 * @brief Crea y ejecuta los hilos.
 * 
 */
void race_condition::ejecutar() {
  std::vector<std::thread> hilos;
  
  std::cout << "Iniciando " << NUM_HILOS << " hilos...\n";
  std::cout << "Cada hilo incrementa " << INCREMENTOS << " veces\n";
  
  // Crear y lanzar los hilos
  for (int i = 0; i < NUM_HILOS; ++i) {
    hilos.push_back(std::thread(&race_condition::incrementar, this));
  }
  
  // Esperar a que terminen todos los hilos
  for (auto& hilo : hilos) {
    hilo.join();
  }
}

/**
 * @brief Muestra los resultados finales.
 * 
 */
void race_condition::resultados() const {
  std::cout << "Valor esperado: " << (NUM_HILOS * INCREMENTOS) << "\n";
  std::cout << "Valor final del contador: " << contador << "\n";
  std::cout << "Diferencia: " << (NUM_HILOS * INCREMENTOS - contador) << "\n";
}

/**
 * @brief Clase que demostra los problemas de race conditions
 * sin sincronización de hilos.
 */
class sin_control : public race_condition {
private:
  void incrementar() override;

public:
  using race_condition::race_condition;
};

/**
 * @brief Incrementa el contador las veces indicadas al crear la calse sin sincronización.
 * 
 */
void sin_control::incrementar() {
  for (int i = 0; i < INCREMENTOS; ++i) {
    contador++;
  }
}

/**
 * @brief Clase que evita la race condition usando un mutex.
 */
class con_control : public race_condition {
private:
  std::mutex mtx;
  void incrementar() override;
  
public:
  using race_condition::race_condition;
};

/**
 * @brief Incrementa el contador las veces indicadas al crear la calse de forma sincronizada.
 * 
 */
void con_control::incrementar() {
  for (int i = 0; i < INCREMENTOS; ++i) {
    std::lock_guard<std::mutex> lock(mtx);
    contador++;
  }
}

int main() {
  std::cout << "--- Ejecutando sin sincronización ---\n";
  sin_control sc(5, 10000);
  sc.ejecutar();
  sc.resultados();

  std::cout << "\n--- Ejecutando con sincronización ---\n";
  con_control cc(5, 10000);
  cc.ejecutar();
  cc.resultados();

  return 0;
}
