Guia de Uso
============

Este proyecto utiliza `uv` para la gestion de dependencias y ejecucion, lo que garantiza que funcione de la misma manera en cualquier sistema Linux.

Instalacion
-----------

Para configurar el entorno de desarrollo y descargar todas las dependencias necesarias:

.. code-block:: bash

   uv sync

Ejecucion
---------

Para lanzar la aplicacion con la interfaz grafica:

.. code-block:: bash

   uv run main.py

Para ejecutar la aplicacion en modo entrenamiento (si esta configurado):

.. code-block:: bash

   uv run main.py -t

Tests
-----

Para ejecutar la suite de pruebas unitarias:

.. code-block:: bash

   uv run pytest amazons/tests

Analisis de Codigo
------------------

Para realizar comprobaciones de estilo y tipos:

.. code-block:: bash

   uv run ruff check .
   uv run pyright
