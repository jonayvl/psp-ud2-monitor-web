# psp-ud2-monitor-web

## ¿Por qué el monitor puede ser un hilo daemon y una tarea crítica no?

El monitor web puede ejecutarse como un hilo *daemon* porque su función es comprobar el estado de diferentes páginas web y mostrar información sobre su disponibilidad. Si el programa principal termina, no es imprescindible que estas comprobaciones continúen ejecutándose, por lo que el hilo puede finalizar automáticamente.

En cambio, una tarea crítica no debería ejecutarse como un hilo *daemon* si necesita completar su trabajo antes de que termine el programa. Por ejemplo, una tarea que debe guardar datos importantes en un fichero o en una base de datos podría interrumpirse si el hilo principal finaliza. Esto podría provocar que la operación quedase incompleta o que se perdieran datos.
