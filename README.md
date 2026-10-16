# Práctica UD2 — Monitor Web Concurrente

**Módulo:** Programación de Servicios y Procesos  
**Curso:** 2.º DAM

## 1. Descripción

Esta práctica consiste en desarrollar una herramienta de monitorización web con Python que comprueba la disponibilidad de varios servicios mediante peticiones HTTP.

Se implementan una versión secuencial y otra concurrente para comparar sus tiempos de ejecución. También se utilizan hilos identificados por nombre, un monitor daemon y temporizadores para avisar de comprobaciones lentas.

## 2. Servicios comprobados

| Servicio | URL | Finalidad |
|---|---|---|
| Python | https://www.python.org/ | Comprobación normal |
| Documentación Python | https://docs.python.org/3/ | Comprobación normal |
| PyPI | https://pypi.org/ | Comprobación normal |
| GitHub | https://github.com/ | Comprobación normal |
| HTTPBin retraso | https://httpbin.org/delay/5 | Probar el aviso de lentitud |
| HTTPBin error | https://httpbin.org/status/503 | Probar la gestión de errores HTTP |

Las webs reales pueden fallar temporalmente. Por eso se utilizan también endpoints de prueba que permiten comprobar el comportamiento ante retrasos y errores HTTP.

## 3. Requisitos e instalación

Se necesita Python 3, conexión a Internet y la librería `requests`.

Para instalar las dependencias:

```bash
python -m pip install -r requirements.txt
```

En Windows también se puede utilizar:

```powershell
py -m pip install -r requirements.txt
```

## 4. Ejecución

Desde la carpeta raíz del repositorio, ejecutar:

```powershell
py monitor_web.py
```

El programa realiza las comprobaciones secuenciales y concurrentes, muestra el estado de los servicios y presenta una comparación de los tiempos obtenidos.

## 5. Funcionamiento técnico

### Versión secuencial

Las peticiones se realizan una después de otra. La siguiente comprobación comienza cuando termina la anterior. Se mide el tiempo total con `time.perf_counter()`.

### Versión concurrente

Se crea un hilo por servicio mediante `threading.Thread`. La URL y los datos necesarios se pasan mediante `args` o `kwargs`. Se inician todos los hilos con `start()` antes de esperar su finalización mediante `join()`.

### Identificación y estado de los hilos

Cada hilo tiene un nombre descriptivo y utiliza `threading.current_thread()` para identificar la comprobación que está ejecutando.

El método `is_alive()` permite consultar si un hilo sigue ejecutándose. El monitor lo utiliza para mostrar cuántas comprobaciones continúan activas.

### Monitor daemon

El monitor es un hilo auxiliar configurado con `daemon=True`. Su finalidad es informar periódicamente del estado de las comprobaciones. Al ser una tarea auxiliar, no debe impedir que el programa termine.

Una tarea crítica que deba completar su trabajo o guardar resultados no debería depender de un hilo daemon, porque puede interrumpirse cuando termina el resto del programa.

### Timer y timeout

`threading.Timer` programa un aviso si una comprobación supera el umbral de lentitud establecido. Si la petición termina antes, el temporizador se cancela.

El parámetro `timeout` de `requests.get()` limita la espera de la petición de red. El `Timer` avisa de que una comprobación está tardando demasiado, pero no cancela por sí mismo la petición.

### Gestión de errores

El programa distingue entre respuestas HTTP correctas, errores HTTP, timeout de red y errores de conexión. Cada comprobación gestiona sus propios errores para evitar que un servicio fallido impida comprobar los demás.

## 6. Comparación secuencial y concurrente

Después de ejecutar el programa, se deben registrar los tiempos obtenidos:

- **Tiempo secuencial:** [anotar el tiempo obtenido].
- **Tiempo concurrente:** [anotar el tiempo obtenido].
- **Diferencia:** [calcular la diferencia entre ambos tiempos].

Los resultados pueden variar según la conexión, la disponibilidad de los servidores y los tiempos de espera.

## 7. Análisis final obligatorio

### 1. ¿Qué diferencia de tiempo observaste entre la versión secuencial y la concurrente?

La versión secuencial tardó [tiempo medido] y la concurrente [tiempo medido]. La diferencia fue de [diferencia calculada]. Según estos resultados, [indicar cuál tardó menos]. Los tiempos deben corresponder a una ejecución real del programa.

### 2. ¿Por qué este problema puede considerarse I/O-bound?

Porque las peticiones HTTP pasan parte del tiempo esperando respuestas de la red. El tiempo de espera de entrada/salida tiene una influencia importante en la duración total.

### 3. ¿Por qué los hilos son adecuados para este caso?

Porque permiten iniciar varias comprobaciones independientes y solapar las esperas de red. Mientras un hilo espera una respuesta, otros pueden continuar con sus peticiones.

### 4. ¿Qué ocurriría si realizaras `join()` inmediatamente después de cada `start()`?

El programa esperaría a que terminase cada hilo antes de continuar con el siguiente. Esto reduciría la concurrencia efectiva y podría hacer que el tiempo total se acercase al de la versión secuencial.

### 5. ¿Los servicios terminan siempre en el mismo orden? Explica por qué.

No. El orden depende de los tiempos de respuesta de los servidores, de la red y de la planificación de los hilos. Por eso los resultados pueden aparecer en un orden diferente en cada ejecución.

### 6. ¿Qué utilidad tiene asignar un nombre a cada hilo?

Permite identificar qué hilo está realizando cada comprobación y facilita la lectura de los mensajes, la depuración y el seguimiento del programa.

### 7. ¿Qué información aporta `is_alive()` y qué diferencia tiene respecto a `join()`?

`is_alive()` indica si el hilo continúa ejecutándose en ese momento. `join()` espera a que el hilo termine. El primero consulta el estado; el segundo sincroniza la continuación del programa con su finalización.

### 8. ¿Por qué el monitor se ha configurado como daemon?

Porque es un hilo auxiliar de seguimiento y no debe impedir que el programa finalice. Una tarea crítica no debería configurarse como daemon si necesita garantizar que complete su trabajo.

### 9. ¿Qué diferencia existe entre el `Timer` de aviso y el `timeout` de `requests`?

El `Timer` ejecuta una función de aviso después de un intervalo determinado. El `timeout` limita la espera de la petición HTTP. El temporizador no sustituye al timeout ni cancela automáticamente la petición.

### 10. ¿Qué problema podría aparecer si varios hilos modificaran simultáneamente una misma estructura de resultados?

Podrían producirse condiciones de carrera si varios hilos leen y modifican los mismos datos al mismo tiempo. Esto podría ocasionar resultados inconsistentes, actualizaciones perdidas o estados difíciles de reproducir.

## 8. Conclusión

La práctica permite comparar una solución secuencial con otra concurrente y comprender la utilidad de los hilos en tareas de entrada/salida. También permite practicar la identificación y supervisión de hilos, los temporizadores, los tiempos de espera y la gestión individual de errores HTTP.

## 9. Recursos de consulta

- Requests: https://requests.readthedocs.io/
- Requests y timeouts: https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
- Excepciones de Requests: https://requests.readthedocs.io/en/latest/api/#exceptions
- HTTPBin: https://httpbin.org/
- Documentación oficial de Python: https://docs.python.org/3/