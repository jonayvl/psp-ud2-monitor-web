
import threading
import requests
import time

servicios = {
    "Python": "https://www.python.org",
    "PyPI": "https://pypi.org",
    "GitHub": "https://github.com",
    "Web lenta": "https://httpbin.org/delay/5",
    "Web error": "https://httpbin.org/status/503"
}

Online = 0
ErrorHttp = 0
tiempoExpirado = 0
ErrorConexion = 0


def avisar_lentitud(url):
    print(f"\n[AVISO] {url} está tardando demasiado.")


def comprobar_web(nombre, url):
    global Online, ErrorHttp, tiempoExpirado, ErrorConexion

    hilo = threading.current_thread().name

    print(f"[{hilo}] Comprobando {nombre}: {url}")

    temporizador = threading.Timer(
        3,
        avisar_lentitud,
        args=[url]
    )
    temporizador.start()

    inicio = time.perf_counter()

    try:
        respuesta = requests.get(url, timeout=6)
        duracion = time.perf_counter() - inicio

        if respuesta.status_code < 400:
            Online += 1
            print(
                f"[OK] {nombre} está disponible "
                f"({duracion:.2f} segundos)."
            )
        else:
            ErrorHttp += 1
            print(
                f"[ERROR HTTP] {nombre}: "
                f"código {respuesta.status_code}."
            )

    except requests.Timeout:
        tiempoExpirado += 1
        print(f"[TIMEOUT] {nombre} ha superado el tiempo máximo de espera.")

    except requests.RequestException as error:
        ErrorConexion += 1
        print(f"[ERROR DE CONEXIÓN] {nombre}: {error}")

    finally:
        temporizador.cancel()


hilos = []

inicio_total = time.perf_counter()

for nombre, url in servicios.items():
    hilo = threading.Thread(
        target=comprobar_web,
        args=(nombre, url),
        name=nombre,
        daemon=True
    )

    hilos.append(hilo)
    hilo.start()

for hilo in hilos:
    hilo.join()

fin_total = time.perf_counter()

print("\n--- RESUMEN ---")
print(f"Servicios disponibles: {Online}")
print(f"Errores HTTP: {ErrorHttp}")
print(f"Timeouts: {tiempoExpirado}")
print(f"Errores de conexión: {ErrorConexion}")
print(f"Tiempo total: {fin_total - inicio_total:.2f} segundos")
