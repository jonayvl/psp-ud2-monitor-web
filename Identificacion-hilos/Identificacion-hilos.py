
import threading
import requests
import time

servicios = {
    "web-python": "https://www.python.org/",
    "web-pypi": "https://pypi.org/",
    "web-github": "https://github.com/"
}


def comprobar_web(url):
    nombre = threading.current_thread().name
    print(f"[{nombre}] Iniciando {url}")

    inicio = time.perf_counter()

    try:
        respuesta = requests.get(url, timeout=6)
        tiempo = time.perf_counter() - inicio

        if respuesta.status_code >= 400:
            print(f"[{nombre}] ERROR HTTP ({respuesta.status_code}) - {tiempo:.2f} s")
        else:
            print(f"[{nombre}] ONLINE - {tiempo:.2f} s")

    except requests.Timeout:
        tiempo = time.perf_counter() - inicio
        print(f"[{nombre}] TIMEOUT - {tiempo:.2f} s")

    except requests.RequestException:
        tiempo = time.perf_counter() - inicio
        print(f"[{nombre}] ERROR DE CONEXIÓN - {tiempo:.2f} s")

    finally:
        print(f"[{nombre}] Finalizada comprobación de {url}")


inicio_total = time.perf_counter()
hilos = []

for nombre, url in servicios.items():
    hilo = threading.Thread(
        target=comprobar_web,
        args=(url,),
        name=nombre
    )
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    if hilo.is_alive():
        print(f"[ESTADO] {hilo.name} sigue activo")

for hilo in hilos:
    hilo.join()

tiempo_total = time.perf_counter() - inicio_total

print(f"\nTiempo total concurrente: {tiempo_total:.2f} s")
