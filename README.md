# 🚀 E-Commerce Logistics & Analytics Pipeline

Pipeline ETL (Extract, Transform, Load) modular y robusto desarrollado en Python para la ingesta, limpieza, modelado relacional y exportación de datos de comercio electrónico provenientes de la **Fake Store API**.

---

## 💡 Enfoque y Arquitectura del Proyecto
Este repositorio implementa una solución de **Ingeniería de Datos modular**, diseñada para desacoplar las fuentes brutas de su consumo analítico. 
El pipeline automatiza la ingesta, el modelado relacional y la persistencia en una base de datos local, e incluye una capa de servicios (`query_db.py`) capaz de ejecutar consultas SQL avanzadas y exportar reportes ejecutivos estructurados (en formato Excel multipestaña) listos para ser consumidos de forma directa por herramientas de Business Intelligence como Looker Studio o Power BI.

---

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.x
* **Procesamiento de Datos:** Pandas
* **Base de Datos:** SQLite (Modelo Relacional Normalizado)
* **Automatización y Reportes:** Openpyxl (Generación de reportes multipestaña)
* **Control de Versiones:** Git & GitHub

## 📂 Estructura del Proyecto
```text
ecommerce-logistics-pipeline/
│
├── data/                  # Almacenamiento local y reportes (Ignorado en Git)
├── logs/                  # Registros de ejecución y trazabilidad
├── src/                   # Módulos principales del pipeline
│   ├── extract.py         # Extracción desde la Fake Store API
│   ├── transform.py       # Limpieza, normalización y modelado relacional
│   └── load.py            # Carga y persistencia en SQLite
│
├── .gitignore             # Archivos excluidos del control de versiones
├── main.py                # Orquestador central del ETL
├── query_db.py            # Capa de servicios, consultas SQL y exportación a Excel
├── README.md              # Documentación del proyecto
└── requirements.txt       # Dependencias del proyecto

```

## 🔄 Flujo del Pipeline (ETL)
Extracción (extract.py): Conexión segura a los endpoints de productos y carritos de la API pública.

Transformación (transform.py):

Limpieza de tipos de datos y estandarización de fechas.

Desglose y normalización de objetos anidados (ratings).

Modelado relacional (explode de carritos para generar la tabla de detalle relacional cart_items).

Carga (load.py): Persistencia automatizada de tres tablas normalizadas en SQLite (products, carts, cart_items).

Reportes y Explotación (query_db.py): Ejecución de consultas SQL avanzadas (JOINs, agrupaciones y métricas de negocio) y exportación automática a un reporte ejecutivo en Excel (ecommerce_report.xlsx) preparado para analítica visual.

## ⚙️ Instrucciones de Instalación y Ejecución
Clonar el repositorio:


git clone [https://github.com/tu-usuario/ecommerce-logistics-pipeline.git]
cd ecommerce-logistics-pipeline
Instalar las dependencias:


pip install -r requirements.txt
Ejecutar el pipeline ETL principal:

python main.py
Generar las consultas SQL y el reporte Excel para BI:

python query_db.py