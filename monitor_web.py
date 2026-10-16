
import threading
import time
import requests


# ==========================================================
# CONFIGURACIÓN
# ==========================================================

SERVICIOS = {
    "Python": "https://www.python.org/",
    "PyPI": "https://pypi.org/",
    "GitHub": "https://github.com/",
    "Google": "https://www.google.com/",
    "HTTPBin OK": "https://httpbin.org/status/200",
    "HTTPBin Error": "https://httpbin.org/status/500",
}

TIMEOUT_RED = 8
LIMITE_LENTITUD = 2
INTERVALO_MONITOR = 1


# ==========================================================
# TEMPORIZADOR DE AVISO
# ==========================================================

def avisar_lentitud(nombre, url):
    """Avisa si una comprobación tarda demasiado."""
    print(
        f"[TIMER] AVISO: {nombre} lleva más de "
        f"{LIMITE_LENTITUD} segundos comprobándose."
    )


# ==========================================================
# COMPROBACIÓN DE UN SERVICIO
# ==========================================================

def comprobar_web(nombre, url):
    """
    Comprueba un servicio y devuelve:
    (disponible, codigo_http, tiempo, mensaje).
    """
    hilo_actual = threading.current_thread()
    inicio = time.perf_counter()

    print(f"[{hilo_actual.name}] Comprobando {nombre}: {url}")

    # El Timer avisa de lentitud, pero no cancela la petición.
    temporizador = threading.Timer(
        LIMITE_LENTITUD,
        avisar_lentitud,
        args=(nombre, url),
    )
    temporizador.start()

    try:
        respuesta = requests.get(url, timeout=TIMEOUT_RED)
        tiempo = time.perf_counter() - inicio
        codigo = respuesta.status_code

        if codigo < 400:
            mensaje = f"ONLINE - HTTP {codigo}"
            disponible = True
        else:
            mensaje = f"ERROR HTTP - HTTP {codigo}"
            disponible = False

        print(
            f"[{hilo_actual.name}] {nombre}: "
            f"{mensaje} ({tiempo:.2f} s)"
        )

        return disponible, codigo, tiempo, mensaje

    except requests.Timeout:
        tiempo = time.perf_counter() - inicio
        mensaje = f"TIMEOUT DE RED ({tiempo:.2f} s)"
        print(f"[{hilo_actual.name}] {nombre}: {mensaje}")
        return False, None, tiempo, mensaje

    except requests.RequestException as error:
        tiempo = time.perf_counter() - inicio
        mensaje = f"ERROR DE CONEXIÓN: {error}"
        print(
            f"[{hilo_actual.name}] {nombre}: "
            f"{mensaje} ({tiempo:.2f} s)"
        )
        return False, None, tiempo, mensaje

    finally:
        # Evita que el aviso se dispare si ya terminó la petición.
        temporizador.cancel()
        print(
            f"[{hilo_actual.name}] Finalizada comprobación de "
            f"{nombre}."
        )


# ==========================================================
# VERSIÓN SECUENCIAL
# ==========================================================

def version_secuencial():
    """Comprueba los servicios uno después de otro."""
    print("\n" + "=" * 55)
    print("VERSIÓN SECUENCIAL")
    print("=" * 55)

    resultados = {}
    inicio = time.perf_counter()

    for nombre, url in SERVICIOS.items():
        resultados[nombre] = comprobar_web(nombre, url)

    tiempo_total = time.perf_counter() - inicio

    return resultados, tiempo_total


# ==========================================================
# MONITOR DAEMON
# ==========================================================

def monitorizar(hilos, finalizar_monitor):
    """
    Informa periódicamente de cuántos hilos de comprobación
    siguen ejecutándose.
    """
    while not finalizar_monitor.wait(INTERVALO_MONITOR):
        activos = sum(1 for hilo in hilos if hilo.is_alive())

        if activos > 0:
            print(
                f"[MONITOR] Comprobaciones activas: {activos}"
            )


# ==========================================================
# VERSIÓN CONCURRENTE
# ==========================================================

def version_concurrente():
    """Inicia todas las comprobaciones antes de esperar."""
    print("\n" + "=" * 55)
    print("VERSIÓN CONCURRENTE")
    print("=" * 55)

    resultados = {}
    hilos = []
    finalizar_monitor = threading.Event()

    inicio = time.perf_counter()

    def tarea(nombre, url):
        resultados[nombre] = comprobar_web(nombre, url)

    # Crear todos los hilos antes de iniciarlos.
    for nombre, url in SERVICIOS.items():
        hilo = threading.Thread(
            target=tarea,
            args=(nombre, url),
            name=f"web-{nombre}",
        )
        hilos.append(hilo)

    # El monitor es daemon porque no debe impedir que
    # el programa termine si el hilo principal finaliza.
    monitor = threading.Thread(
        target=monitorizar,
        args=(hilos, finalizar_monitor),
        name="monitor",
        daemon=True,
    )
    monitor.start()

    try:
        # Iniciar todas las comprobaciones antes de usar join().
        for hilo in hilos:
            hilo.start()

        # Esperar a que terminen todas las comprobaciones.
        for hilo in hilos:
            hilo.join()

    finally:
        finalizar_monitor.set()
        monitor.join()

    tiempo_total = time.perf_counter() - inicio

    return resultados, tiempo_total


# ==========================================================
# COMPARACIÓN DE RESULTADOS
# ==========================================================

def mostrar_resumen(resultados_seq, tiempo_seq,
                    resultados_conc, tiempo_conc):
    """Muestra los resultados y compara ambas versiones."""
    total = len(SERVICIOS)

    disponibles_seq = sum(
        1 for resultado in resultados_seq.values()
        if resultado[0]
    )
    disponibles_conc = sum(
        1 for resultado in resultados_conc.values()
        if resultado[0]
    )

    errores_seq = total - disponibles_seq
    errores_conc = total - disponibles_conc

    print("\n" + "=" * 55)
    print("RESUMEN DEL MONITOR WEB")
    print("=" * 55)

    print(f"Servicios comprobados: {total}")
    print(f"Disponibles (secuencial): {disponibles_seq}")
    print(f"Con error (secuencial): {errores_seq}")
    print(f"Disponibles (concurrente): {disponibles_conc}")
    print(f"Con error (concurrente): {errores_conc}")

    print(f"\nTiempo secuencial: {tiempo_seq:.2f} s")
    print(f"Tiempo concurrente: {tiempo_conc:.2f} s")

    if tiempo_conc > 0:
        relacion = tiempo_seq / tiempo_conc
        print(f"Relación de velocidad: {relacion:.2f}x")

    if tiempo_conc < tiempo_seq:
        mejora = (1 - tiempo_conc / tiempo_seq) * 100
        print(f"Reducción del tiempo: {mejora:.2f} %")
        print("La versión concurrente ha tardado menos.")
    elif tiempo_conc > tiempo_seq:
        print("La versión secuencial ha tardado menos.")
    else:
        print("Ambas versiones han tardado lo mismo.")

    print("\nANÁLISIS")
    print(
        "Las peticiones HTTP son una tarea I/O-bound: "
        "pasan parte del tiempo esperando respuestas de red."
    )
    print(
        "La concurrencia permite solapar esas esperas, por lo "
        "que puede reducir el tiempo total de comprobación."
    )
    print(
        "El resultado depende de la red, los servidores y "
        "los tiempos de espera."
    )


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():
    resultados_seq, tiempo_seq = version_secuencial()

    resultados_conc, tiempo_conc = version_concurrente()

    mostrar_resumen(
        resultados_seq,
        tiempo_seq,
        resultados_conc,
        tiempo_conc,
    )


if __name__ == "__main__":
    main()
