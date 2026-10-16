import threading
import time

import requests

servicios = {
    "web-python": "https://www.python.org/",
    "web-pypi": "https://pypi.org/",
    "web-github": "https://github.com/",
}

Online = 0
ErrorHttp = 0
tiempoExpirado = 0
ErrorConexion = 0


def comprobar_web(url):
    global Online, ErrorHttp, tiempoExpirado, ErrorConexion

    nombre = threading.current_thread().name
    print(f"[{nombre}] Iniciando {url}")

    inicio = time.perf_counter()

    try:
        respuesta = requests.get(url, timeout=6)
        tiempo = time.perf_counter() - inicio
        codigo = respuesta.status_code
        if codigo >= 400:
            ErrorHttp += 1
            print(f"[{nombre}] ERROR HTTP ({codigo}) - {tiempo:.2f} s")
        else:
            Online += 1
            print(f"[{nombre}] ONLINE - {tiempo:.2f} s")
    except requests.Timeout:
        tiempo = time.perf_counter() - inicio
        tiempoExpirado += 1
        print(f"[{nombre}] TIMEOUT - {tiempo:.2f} s")
    except requests.RequestException:
        tiempo = time.perf_counter() - inicio
        ErrorConexion += 1
        print(f"[{nombre}] ERROR DE CONEXIÓN - {tiempo:.2f} s")


inicio_total = time.perf_counter()

hilos = []
for alias, url in servicios.items():
    hilo = threading.Thread(target=comprobar_web, args=(url,), name=alias)
    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    if hilo.is_alive():
        print(f"[estado] {hilo.name} sigue activo")

for hilo in hilos:
    hilo.join()

tiempo_concurrente = time.perf_counter() - inicio_total

print("\n===============================")
print("       RESUMEN CONCURRENTE")
print("===============================")
print(f"WEB Online: {Online}")
print(f"ERROR http: {ErrorHttp}")
print(f"Tiempo Expirado: {tiempoExpirado}")
print(f"Error Conexion: {ErrorConexion}")
print(f"Tiempo total concurrente: {tiempo_concurrente:.2f} s")