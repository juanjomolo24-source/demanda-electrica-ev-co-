# ⚡ Predicción de Demanda Energética en Estaciones de Carga EV
### *Mediante Arquitectura Medallion en Databricks*

---

## 📌 Descripción del Proyecto
Este proyecto implementa una solución analítica en **Databricks** utilizando la **Arquitectura Medallion** ( Bronze, Silver y Gold) para procesar, limpiar e integrar datos que permitan predecir la demanda energética en estaciones de carga para vehículos eléctricos (EV). Se anexa un documento en word donde se encuentra el caso de negocio, ademas de los objetivos del presente trabajo, se carga por aparte en imagen la arquitectura del caso.
Ademas, Hemos decidido implementar un aplicativo interactivo donde se muestre la dashboard con algunas especifiaciones de los resultados obtenidos y de las proyecciones hasta el 2030. Se trabaja con con **streamlit** que permite que cualquier usuario pueda ingresar a ver los resultados sin restricciones.

🚀 **[Abrir Aplicación Interactiva en Vivo](https://idftgnjrz4vt8e5qyqe6zw.streamlit.app/)**

### 📊 ¿Qué encontrarás en el Dashboard?

El panel interactivo permite explorar la información consolidada procesada mediante las siguientes secciones y funcionalidades:

* **📈 Indicadores Clave (KPIs):** Resumen ejecutivo con las métricas principales de consumo acumulado (en kWh y MWh) y la flota estimada de vehículos eléctricos (EV).
* **🗺️ Análisis Geográfico y Territorial:** Filtros por municipio y año para analizar el comportamiento regional de la demanda energética.
* **🔮 Modelos de Predicción:** Visualización de tendencias de consumo energético futuro para apoyar la toma de decisiones en infraestructura de carga.
* **🎛️ Filtros Dinámicos:** Panel lateral (*sidebar*) para segmentar las lecturas por periodo de tiempo, región geográfica y tipo de métrica.

  <img width="756" height="172" alt="image" src="https://github.com/user-attachments/assets/1ee16878-8e85-49ce-b597-88a046044811" />

  En esta area econtrarás los Items al detalle y en cada una de las pestañas , se observa los detalles de los datos , estos son filtrados por año y lugar 

  <img width="504" height="59" alt="image" src="https://github.com/user-attachments/assets/17ae4777-1600-4a19-8d2a-be13752b4f42" />




## Job and Pipeline
Se ejecuta de manera mensual para la lectura de nuevos datos 
<img width="1568" height="729" alt="image" src="https://github.com/user-attachments/assets/0e3eb846-8c44-4baf-9a46-0d2b11067e8f" />

## Linage

<img width="1024" height="362" alt="image" src="https://github.com/user-attachments/assets/88e275ce-1578-4e85-9b41-45df717f0fa5" />

## Arquitectura
<img width="981" height="1600" alt="Arquitectura_Medallion" src="https://github.com/user-attachments/assets/7a018830-f4a4-48d9-b929-87d78d94b1b7" />

## Graficos 
1. Proyeccion de demanda eléctrica nacional por vehiculos eléctricos , crecimiento del parque de vehiculos eléctricos

<img width="658" height="256" alt="image" src="https://github.com/user-attachments/assets/61cd69e3-f8a3-4dbd-b3b2-2cf835b77a6a" />

2. Demanda eléctrica sectorizada por ciudades

<img width="444" height="270" alt="image" src="https://github.com/user-attachments/assets/5205207a-f4f7-4d12-b279-c4d0ee19cdfb" />

3. Evolucion demanda eléctrica por ciudades

<img width="532" height="261" alt="image" src="https://github.com/user-attachments/assets/10001d6d-f440-406e-94ce-445038132cac" />


## Representación grafica del módelo predictivo 

<img width="528" height="298" alt="image" src="https://github.com/user-attachments/assets/a2d3656a-ce59-4824-b428-cda6adf67308" />

En le mismo documento ( "Arquitectura Medallion Vehiculos Electricos Colombia.ipynb") se puede encontrar la infromación al detalle


---

## 👥 Integrantes

| N° | Nombre del Integrante |
|:--:|---|
| 1 | **Juan José Montoya Lopera** |
| 2 | **Lucela Montoya Quintero** |
| 3 | **Lizeth Catalina Pineda Arteaga** |
| 4 | **Luisa Fernanda Zapata Correa** |
