CBV_Data_Analytics
===============
[![Language: Python 3](https://img.shields.io/badge/python-3.8%20|%203.9%20|%203.10%20|%203.11-red)](https://www.python.org/)
[![Pip 3](https://img.shields.io/pypi/v/pip.svg)](https://pypi.org/project/pip/)


Este proyecto tiene por objectivo extraer los datos de incidentes de `resumen.cbv.cl` para posterior analisis.

Requerimientos
-----------------
* **[Python 3](https://www.python.org/):** A programming language that lets you work more quickly and integrate your systems more effectively.
* **[Pip 3](https://pypi.org/project/pip/):** Pip is the package installer for Python.

Uso
-----------------
1. Descargar e ingresar al proyecto:
    ```shell
    git clone https://github.com/Pr0gmaT1k/CBV_Data_Analytics
    cd CBV_Data_Analytics
    ```  

2. Instalar las [dependencias](https://github.com/Pr0gmaT1k/CBV_Data_Analytics/blob/main/requirements.txt):
    ```shell
    pip3 install -r requirements.txt
    ```    

3. Extraer los datos y conviertirlos a un `JSON` local `result.json`:
    ```shell
    python3 ./load_data.py
    ```
4. Compilar los datos y generar informes mensuales, anuales y historicos por cada compañia y todo el CBV.:
    ```shell
    python3 ./generate_chart.py
    ```

Bibliotecas externas:
-----------------
* **[alive_progress](https://github.com/rsalmei/alive-progress/tree/main):** A new kind of Progress Bar, with real-time throughput, ETA, and very cool animations!
* **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/):** Quick turnaround projects like screen-scraping.
* **[matplotlib](https://github.com/matplotlib/matplotlib):** Comprehensive library for creating static, animated, and interactive visualizations in Python.
* **[requests](https://github.com/psf/requests):** A simple, yet elegant, HTTP library.

Licencia GNU V3:
-----------------
CBV_Data_Analytics
Copyright (C) 2023  Cuerpo de Bomberos de Valparaíso

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
