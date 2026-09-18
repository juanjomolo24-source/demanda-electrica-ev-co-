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

 Gráfico 1 – Proyección de Demanda Eléctrica Nacional (izquierda)

Muestra cuánta energía eléctrica (en MWh) se necesitaría a nivel nacional para cargar vehículos eléctricos, año por año, de 2020 a 2026. La demanda crece de forma moderada hasta 2024 (~29,534 MWh), pero luego se dispara con fuerza en 2025 y 2026, llegando a 177,670 MWh. Ese salto tan pronunciado al final indica una aceleración importante en la adopción de vehículos eléctricos.

 Gráfico 2 – Crecimiento del Parque de Vehículos Eléctricos (derecha)

Muestra el número total acumulado de vehículos eléctricos en circulación cada año, también de 2020 a 2026. Pasa de 1,302 vehículos en 2020 a 40,564 en 2026, con un crecimiento que se acelera claramente en los últimos dos años (2025-2026).

2. Demanda eléctrica sectorizada por ciudades

<img width="444" height="270" alt="image" src="https://github.com/user-attachments/assets/5205207a-f4f7-4d12-b279-c4d0ee19cdfb" />

Muestra la demanda eléctrica anual proyectada (en MWh) para 2026 en seis ciudades de Colombia, ordenadas de mayor a menor 

**Ciudades con mayor demanda:**
- **Bogotá** y **Medellín** concentran la mayor parte de la demanda proyectada, muy por encima del resto de ciudades.
- **Manizales** también destaca con 19,710 MWh, superando a ciudades como Cali, Barranquilla y Pereira.

**Ciudades con menor demanda:**
- **Cali** (6,412 MWh), **Barranquilla** (~6,256 MWh) y **Pereira** (6,132 MWh) presentan niveles de demanda similares entre sí y considerablemente menores que los de las dos principales ciudades.

**Conclusión general:**
La demanda eléctrica proyectada está fuertemente concentrada en las dos ciudades más grandes del país, lo que sugiere que la infraestructura de carga e inversión en red eléctrica debería priorizarse en estos centros urbanos

3. Evolucion demanda eléctrica por ciudades

<img width="532" height="261" alt="image" src="https://github.com/user-attachments/assets/10001d6d-f440-406e-94ce-445038132cac" />

Representa la evolución año a año de la demanda eléctrica (en MWh) para las seis ciudades analizadas, permitiendo comparar sus trayectorias de crecimiento entre 2020 y 2026.

**Ciudades con mayor crecimiento:**
- **Bogotá** (línea dorada) lidera claramente desde el inicio y mantiene el crecimiento más pronunciado, terminando cerca de 90,000 MWh en 2026, con una aceleración muy marcada a partir de 2024.
- **Medellín** (línea rosa/roja) parte muy bajo, similar al resto de ciudades, pero despega con fuerza desde 2024 y cierra 2026 alrededor de 50,000 MWh, ubicándose como la segunda ciudad con mayor demanda.

**Ciudades con crecimiento moderado:**
- **Cali** (línea magenta) muestra un crecimiento más gradual pero constante, alcanzando cerca de 20,000 MWh en 2026.

**Ciudades con crecimiento bajo:**
- **Barranquilla**, **Manizales** y **Pereira** se mantienen con valores muy bajos y cercanos entre sí durante casi todo el período, con un leve repunte hacia 2025-2026, pero sin despegar de forma significativa.

**Conclusión general:**
Con la representacion grafica podemos evidenciar una brecha creciente entre Bogotá y Medellín frente al resto de ciudades. Mientras las dos principales urbes muestran un crecimiento exponencial —especialmente después de 2024—, las demás ciudades presentan un incremento mucho más lento y sostenido, reforzando la idea de que la demanda eléctrica por vehículos eléctricos se está concentrando fuertemente en los grandes centros urbanos del país.


## Representación grafica del módelo predictivo 

<img width="528" height="298" alt="image" src="https://github.com/user-attachments/assets/a2d3656a-ce59-4824-b428-cda6adf67308" />

En le mismo documento ( "Arquitectura Medallion Vehiculos Electricos Colombia.ipynb") se puede encontrar la infromación al detalle

Este gráfico combina los **datos base históricos** (2020-2026) con una **proyección extendida** (2027-2030) generada por un modelo predictivo, mostrando cómo se espera que evolucione la demanda eléctrica nacional asociada a vehículos eléctricos.

**Datos base (2020-2026):**
- La demanda crece de forma casi imperceptible en la escala del gráfico (dado que está en millones de MWh), pasando de valores cercanos a 0 hasta aproximadamente 0.18 millones de MWh (177,670 MWh) en 2026.

**Proyección 2027-2030:**
Según la tabla de proyección extendida, se estima:

| Año | Vehículos EV | Demanda (MWh) |
|------|--------------|----------------|
| 2027 | 78,134 | 342,228.57 |
| 2028 | 150,502 | 659,200.67 |
| 2029 | 289,897 | 1,269,752.33 |
| 2030 | 558,401 | 2,445,796.95 |

**Tendencia observada:**
- La curva muestra un **crecimiento exponencial** cada vez más pronunciado: la demanda casi se **duplica año a año** entre 2027 y 2030.
- Para 2030, se proyecta una demanda eléctrica nacional cercana a **2.45 millones de MWh**, es decir, casi **14 veces más** que la demanda estimada en 2026.
- El total de vehículos eléctricos también seguiría esta tendencia exponencial, llegando a más de 558,000 unidades en 2030.

**Conclusión general:**
El modelo predictivo sugiere que, si se mantienen las tendencias actuales de adopción, el sistema eléctrico nacional deberá prepararse para un incremento muy significativo en la demanda en los próximos años, lo cual tiene implicaciones importantes en términos de planificación de infraestructura, capacidad de generación y expansión de redes de carga para vehículos eléctricos


---

## 👥 Integrantes

| N° | Nombre del Integrante |
|:--:|---|
| 1 | **Juan José Montoya Lopera** |
| 2 | **Luisa Fernanda Zapata Correa** |
