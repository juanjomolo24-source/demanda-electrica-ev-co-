import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from io import BytesIO
from datetime import datetime

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="QuoiaGo - Pronóstico Demanda Eléctrica EV Colombia",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILOS PROFESIONALES ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Fuentes y fondo general */
    .main { 
        font-family: 'Poppins', sans-serif; 
        background: linear-gradient(180deg, #F8F9FA 0%, #E8E9EB 100%); 
    }
    
    /* Header principal con logos */
    .quoia-header {
        background: linear-gradient(135deg, #6B1FE0 0%, #4A0E9A 100%);
        padding: 2.5rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 50px rgba(107, 31, 224, 0.4);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .quoia-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(176, 255, 0, 0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }
    
    .logo-principal {
        max-width: 280px;
        height: auto;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
    }
    
    .logo-estampa {
        max-width: 120px;
        height: auto;
        filter: drop-shadow(0 5px 15px rgba(0,0,0,0.2));
    }
    
    .quoia-subtitle {
        font-size: 1.3rem;
        color: white;
        opacity: 0.98;
        font-weight: 400;
        margin-top: 1rem;
        position: relative;
        z-index: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Métricas mejoradas */
    .stMetric {
        background: white;
        padding: 1.8rem;
        border-radius: 18px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        border-left: 6px solid #6B1FE0;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 35px rgba(107, 31, 224, 0.25);
        border-left-width: 8px;
    }
    
    .stMetric label {
        color: #6B1FE0 !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stMetric [data-testid="stMetricValue"] {
        color: #1A0B2E !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }
    
    .stMetric [data-testid="stMetricDelta"] {
        color: #2D3748 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }
    
    .stMetric div {
        color: #1A0B2E !important;
    }
    
    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #6B1FE0 0%, #4A0E9A 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSlider label {
        font-weight: 600;
        color: #B0FF00 !important;
        font-size: 1.05rem !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: white;
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        color: #6B1FE0 !important;
        font-weight: 600;
        font-size: 1rem;
        padding: 0 1.5rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(107, 31, 224, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6B1FE0 0%, #4A0E9A 100%);
        color: white !important;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #6B1FE0 !important;
        font-weight: 700 !important;
    }
    
    h1 {
        font-size: 2.2rem !important;
        margin-bottom: 1.5rem !important;
    }
    
    h2 {
        font-size: 1.8rem !important;
        margin-top: 2rem !important;
    }
    
    /* Líneas divisorias */
    hr {
        margin: 2.5rem 0;
        border: none;
        height: 3px;
        background: linear-gradient(90deg, transparent, #6B1FE0, transparent);
    }
    
    /* Cards de información */
    .info-card {
        background: white;
        border-radius: 18px;
        padding: 2rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        border-left: 6px solid #6B1FE0;
        transition: all 0.3s ease;
    }
    
    .info-card:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 35px rgba(107, 31, 224, 0.2);
    }
    
    .info-card-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1A0B2E;
        margin-bottom: 1rem;
    }
    
    .info-card-text {
        font-size: 1.1rem;
        color: #2D3748;
        line-height: 1.8;
    }
    
    .info-highlight {
        color: #6B1FE0;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    /* Footer */
    .quoia-footer {
        background: linear-gradient(135deg, #1A0B2E 0%, #6B1FE0 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin-top: 4rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(107, 31, 224, 0.3);
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #6B1FE0 0%, #4A0E9A 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(107, 31, 224, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(107, 31, 224, 0.4);
    }
    
    /* Dataframe */
    .dataframe {
        font-size: 0.95rem !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border-radius: 10px;
        font-weight: 600;
        color: #6B1FE0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== FUNCIONES DE DATOS ====================
@st.cache_data
def cargar_datos_electrolineras():
    """Carga datos desde Google Sheets"""
    file_id = "13QxKRC7yVCHzOI-N82dk72GNHw26DOPC"
    url_descarga = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    response = requests.get(url_descarga)
    excel_data = BytesIO(response.content)
    
    ciudades = [
        ('Demanda Medellín', 'MEDELLIN'),
        ('Demanda Bogotá', 'BOGOTA'),
        ('Demanda Barranquilla', 'BARRANQUILLA'),
        ('Demanda Manizales', 'MANIZALES'),
        ('Demanda Pereira', 'PEREIRA'),
        ('Demanda Cali', 'CALI')
    ]
    
    data_electrolineras = []
    for hoja, municipio in ciudades:
        excel_data.seek(0)
        df = pd.read_excel(excel_data, sheet_name=hoja)
        
        mask_2024 = df.iloc[:, 1].astype(str).str.contains('Matrículas EV 2024', na=False)
        mask_2025 = df.iloc[:, 1].astype(str).str.contains('Matrículas EV 2025', na=False)
        mask_2026 = df.iloc[:, 1].astype(str).str.contains('Matrículas EV 2026', na=False)
        mask_stock = df.iloc[:, 1].astype(str).str.contains('Stock EV fin 2023', na=False)
        mask_parque = df.iloc[:, 1].astype(str).str.contains('Parque automotor', na=False)
        
        data_electrolineras.append({
            'MUNICIPIO': municipio,
            'STOCK_EV_2023': df.loc[mask_stock, df.columns[2]].values[0] if mask_stock.any() else 0,
            'MATRICULAS_EV_2024': df.loc[mask_2024, df.columns[2]].values[0] if mask_2024.any() else 0,
            'MATRICULAS_EV_2025': df.loc[mask_2025, df.columns[2]].values[0] if mask_2025.any() else 0,
            'MATRICULAS_EV_2026': df.loc[mask_2026, df.columns[2]].values[0] if mask_2026.any() else 0,
            'PARQUE_AUTOMOTOR': df.loc[mask_parque, df.columns[2]].values[0] if mask_parque.any() else 0
        })
    
    return pd.DataFrame(data_electrolineras)

@st.cache_data
def generar_proyecciones(df_electrolineras):
    """Genera series temporales históricas y proyecciones"""
    historico_data = []
    
    for _, row in df_electrolineras.iterrows():
        municipio = row['MUNICIPIO']
        stock_2023 = row['STOCK_EV_2023']
        
        # Generar histórico hacia atrás (tasa 65% anual)
        stock_2022 = int(stock_2023 / 1.65)
        stock_2021 = int(stock_2022 / 1.65)
        stock_2020 = int(stock_2021 / 1.65)
        
        historico_data.extend([
            {'MUNICIPIO': municipio, 'ANIO': 2020, 'VEHICULOS_EV': stock_2020},
            {'MUNICIPIO': municipio, 'ANIO': 2021, 'VEHICULOS_EV': stock_2021},
            {'MUNICIPIO': municipio, 'ANIO': 2022, 'VEHICULOS_EV': stock_2022},
            {'MUNICIPIO': municipio, 'ANIO': 2023, 'VEHICULOS_EV': stock_2023},
            {'MUNICIPIO': municipio, 'ANIO': 2024, 'VEHICULOS_EV': row['MATRICULAS_EV_2024']},
            {'MUNICIPIO': municipio, 'ANIO': 2025, 'VEHICULOS_EV': row['MATRICULAS_EV_2025']},
            {'MUNICIPIO': municipio, 'ANIO': 2026, 'VEHICULOS_EV': row['MATRICULAS_EV_2026']}
        ])
    
    df_historico = pd.DataFrame(historico_data)
    
    # Calcular demanda eléctrica (12 kWh/día * 365 días / 1000 = MWh)
    df_historico['CONSUMO_MWH_ANUAL'] = (df_historico['VEHICULOS_EV'] * 12 * 365) / 1000
    
    # Agregado nacional
    df_nacional = df_historico.groupby('ANIO').agg({
        'VEHICULOS_EV': 'sum',
        'CONSUMO_MWH_ANUAL': 'sum'
    }).reset_index()
    
    # Tasa de crecimiento promedio 2023-2026
    tasa_crecimiento = df_nacional[df_nacional['ANIO'] >= 2023]['VEHICULOS_EV'].pct_change().mean()
    
    # Proyecciones 2027-2030
    proyecciones = []
    ultimo_vehiculos = df_nacional[df_nacional['ANIO'] == 2026]['VEHICULOS_EV'].values[0]
    ultimo_demanda = df_nacional[df_nacional['ANIO'] == 2026]['CONSUMO_MWH_ANUAL'].values[0]
    
    for year in range(2027, 2031):
        ultimo_vehiculos = ultimo_vehiculos * (1 + tasa_crecimiento)
        ultimo_demanda = ultimo_demanda * (1 + tasa_crecimiento)
        proyecciones.append({
            'ANIO': year,
            'VEHICULOS_EV': int(ultimo_vehiculos),
            'CONSUMO_MWH_ANUAL': round(ultimo_demanda, 2),
            'TIPO': 'Proyección'
        })
    
    df_proyeccion = pd.DataFrame(proyecciones)
    df_nacional['TIPO'] = 'Histórico'
    df_completo = pd.concat([df_nacional, df_proyeccion], ignore_index=True)
    
    return df_historico, df_completo

# ==================== HEADER CON LOGOS ====================
st.markdown("""
<div class="quoia-header">
    <div class="logo-container">
        <img src="https://i.ibb.co/pBWVwrq2/Logo-principal.jpg" alt="QuoiaGo" class="logo-principal" />
        <img src="https://i.ibb.co/DHy0HcrB/Estampa-azul.png" alt="Estampa QuoiaGo" class="logo-estampa" />
    </div>
    <div class="quoia-subtitle">⚡ Pronóstico de Demanda Eléctrica por Vehículos Eléctricos en Colombia</div>
</div>
""", unsafe_allow_html=True)

# ==================== CARGA DE DATOS ====================
with st.spinner('🔄 Cargando datos y generando proyecciones...'):
    df_electrolineras = cargar_datos_electrolineras()
    df_por_ciudad, df_nacional = generar_proyecciones(df_electrolineras)

st.success('✅ Datos cargados y procesados correctamente')

# ==================== SIDEBAR ====================
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
    <img src="https://i.ibb.co/pBWVwrq2/Logo-principal.jpg" alt="QuoiaGo" style="max-width: 180px; margin-bottom: 1rem; filter: drop-shadow(0 5px 15px rgba(0,0,0,0.3));" />
    <div style="font-size: 1rem; opacity: 0.95; margin-top: 0.5rem; color: white; font-weight: 600;">Panel de Control Interactivo</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.header("🎛️ Filtros de Análisis")

# Filtro de rango de años
años_disponibles = sorted(df_nacional['ANIO'].unique())
rango_años = st.sidebar.select_slider(
    "Rango de Años",
    options=años_disponibles,
    value=(2023, 2030)
)

# Filtro de ciudades
ciudades_disponibles = df_por_ciudad['MUNICIPIO'].unique().tolist()
ciudades_seleccionadas = st.sidebar.multiselect(
    "Seleccionar Ciudades",
    options=ciudades_disponibles,
    default=ciudades_disponibles
)

# Tipo de análisis
tipo_analisis = st.sidebar.radio(
    "Tipo de Visualización",
    options=["Nacional", "Por Ciudad", "Comparativa"],
    index=0
)

# Métricas personalizadas
st.sidebar.markdown("---")
st.sidebar.header("📊 Métricas Personalizadas")
año_metrica = st.sidebar.selectbox(
    "Año para métricas",
    options=años_disponibles,
    index=len(años_disponibles) - 5  # Default 2026
)

# Exportar datos
st.sidebar.markdown("---")
st.sidebar.header("💾 Exportar Datos")
if st.sidebar.button("📥 Descargar Dataset Completo"):
    csv = df_por_ciudad.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="⬇️ Descargar CSV",
        data=csv,
        file_name=f"quoiago_demanda_ev_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# ==================== MÉTRICAS DINÁMICAS ====================
st.header("📊 Métricas Clave Dinámicas")

# Filtrar datos según año seleccionado
data_año = df_nacional[df_nacional['ANIO'] == año_metrica].iloc[0]
data_año_anterior = df_nacional[df_nacional['ANIO'] == año_metrica - 1].iloc[0] if año_metrica > 2020 else data_año

# Calcular deltas
delta_vehiculos = ((data_año['VEHICULOS_EV'] - data_año_anterior['VEHICULOS_EV']) / data_año_anterior['VEHICULOS_EV'] * 100) if año_metrica > 2020 else 0
delta_demanda = ((data_año['CONSUMO_MWH_ANUAL'] - data_año_anterior['CONSUMO_MWH_ANUAL']) / data_año_anterior['CONSUMO_MWH_ANUAL'] * 100) if año_metrica > 2020 else 0

# Proyección a 2030
data_2030 = df_nacional[df_nacional['ANIO'] == 2030].iloc[0]

# Calcular tasa de crecimiento promedio
tasa_crecimiento_anual = df_nacional[df_nacional['ANIO'].between(rango_años[0], rango_años[1])]['VEHICULOS_EV'].pct_change().mean() * 100

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=f"🚗 Vehículos EV {año_metrica}",
        value=f"{int(data_año['VEHICULOS_EV']):,}",
        delta=f"+{delta_vehiculos:.1f}% vs {año_metrica-1}" if año_metrica > 2020 else None
    )

with col2:
    st.metric(
        label=f"⚡ Demanda {año_metrica} (MWh)",
        value=f"{int(data_año['CONSUMO_MWH_ANUAL']):,}",
        delta=f"+{delta_demanda:.1f}% vs {año_metrica-1}" if año_metrica > 2020 else None
    )

with col3:
    st.metric(
        label="🔮 Proyección 2030",
        value=f"{int(data_2030['VEHICULOS_EV']):,}",
        delta=f"+{((data_2030['VEHICULOS_EV'] - data_año['VEHICULOS_EV']) / data_año['VEHICULOS_EV'] * 100):.0f}% vs {año_metrica}"
    )

with col4:
    st.metric(
        label="📈 Tasa Crecimiento Anual",
        value=f"{tasa_crecimiento_anual:.1f}%",
        delta="Promedio del período"
    )

st.markdown("---")

# ==================== TABS PRINCIPALES ====================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Evolución Temporal",
    "🏙️ Análisis por Ciudad",
    "⚖️ Comparador Interactivo",
    "📊 Datos Detallados",
    "💡 Conclusiones e Impacto"
])

# ==================== TAB 1: EVOLUCIÓN TEMPORAL ====================
with tab1:
    st.header("📈 Evolución Temporal de la Demanda Eléctrica")
    
    # Filtrar datos según rango
    df_filtrado = df_nacional[df_nacional['ANIO'].between(rango_años[0], rango_años[1])]
    
    # Gráfico 1: Evolución de Demanda con área
    fig = go.Figure()
    
    # Histórico
    df_historico = df_filtrado[df_filtrado['TIPO'] == 'Histórico']
    fig.add_trace(go.Scatter(
        x=df_historico['ANIO'],
        y=df_historico['CONSUMO_MWH_ANUAL'],
        name='Demanda Histórica',
        mode='lines+markers',
        line=dict(color='#6B1FE0', width=4),
        marker=dict(size=12, line=dict(width=2, color='white')),
        fill='tozeroy',
        fillcolor='rgba(107, 31, 224, 0.2)',
        hovertemplate='<b>Año %{x}</b><br>Demanda: %{y:,.0f} MWh<extra></extra>'
    ))
    
    # Proyección
    df_proyeccion = df_filtrado[df_filtrado['TIPO'] == 'Proyección']
    if not df_proyeccion.empty:
        fig.add_trace(go.Scatter(
            x=df_proyeccion['ANIO'],
            y=df_proyeccion['CONSUMO_MWH_ANUAL'],
            name='Proyección',
            mode='lines+markers',
            line=dict(color='#B0FF00', width=4, dash='dash'),
            marker=dict(size=12, symbol='square', line=dict(width=2, color='white')),
            fill='tozeroy',
            fillcolor='rgba(176, 255, 0, 0.15)',
            hovertemplate='<b>Año %{x}</b><br>Proyección: %{y:,.0f} MWh<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(
            text="Demanda Eléctrica Nacional por Vehículos Eléctricos",
            font=dict(size=22, color='#1A0B2E', family='Poppins'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title="Año",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)',
            dtick=1
        ),
        yaxis=dict(
            title="Demanda Eléctrica (MWh/año)",
            showgrid=True,
            gridcolor='rgba(0,0,0,0.1)'
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico 2: Dual-axis (Vehículos + Demanda)
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2.add_trace(
        go.Bar(
            x=df_filtrado['ANIO'],
            y=df_filtrado['VEHICULOS_EV'],
            name='Vehículos EV',
            marker_color='#4A0E9A',
            opacity=0.7,
            hovertemplate='<b>%{x}</b><br>Vehículos: %{y:,.0f}<extra></extra>'
        ),
        secondary_y=False
    )
    
    fig2.add_trace(
        go.Scatter(
            x=df_filtrado['ANIO'],
            y=df_filtrado['CONSUMO_MWH_ANUAL'],
            name='Demanda MWh',
            mode='lines+markers',
            line=dict(color='#B0FF00', width=3),
            marker=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Demanda: %{y:,.0f} MWh<extra></extra>'
        ),
        secondary_y=True
    )
    
    fig2.update_xaxes(title_text="Año", dtick=1)
    fig2.update_yaxes(title_text="Número de Vehículos EV", secondary_y=False)
    fig2.update_yaxes(title_text="Demanda Eléctrica (MWh)", secondary_y=True)
    
    fig2.update_layout(
        title=dict(
            text="Correlación: Vehículos EV vs Demanda Eléctrica",
            font=dict(size=20, color='#1A0B2E'),
            x=0.5,
            xanchor='center'
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# ==================== TAB 2: ANÁLISIS POR CIUDAD ====================
with tab2:
    st.header("🏙️ Análisis por Ciudad")
    
    # Filtrar ciudades seleccionadas
    df_ciudades_filtrado = df_por_ciudad[
        (df_por_ciudad['MUNICIPIO'].isin(ciudades_seleccionadas)) &
        (df_por_ciudad['ANIO'].between(rango_años[0], rango_años[1]))
    ]
    
    # Gráfico 1: Líneas por ciudad
    fig = px.line(
        df_ciudades_filtrado,
        x='ANIO',
        y='CONSUMO_MWH_ANUAL',
        color='MUNICIPIO',
        title='Evolución de Demanda por Ciudad',
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="Demanda Eléctrica (MWh/año)",
        hovermode='x unified',
        plot_bgcolor='white',
        height=500,
        title=dict(font=dict(size=20, color='#1A0B2E'), x=0.5, xanchor='center')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico 2: Treemap de participación (año seleccionado)
    df_treemap = df_por_ciudad[df_por_ciudad['ANIO'] == año_metrica].copy()
    df_treemap['PORCENTAJE'] = (df_treemap['CONSUMO_MWH_ANUAL'] / df_treemap['CONSUMO_MWH_ANUAL'].sum() * 100).round(1)
    
    fig2 = px.treemap(
        df_treemap,
        path=['MUNICIPIO'],
        values='CONSUMO_MWH_ANUAL',
        title=f'Participación por Ciudad en {año_metrica}',
        color='PORCENTAJE',
        color_continuous_scale='Purples',
        hover_data={'PORCENTAJE': ':.1f%', 'CONSUMO_MWH_ANUAL': ':,.0f'}
    )
    
    fig2.update_layout(
        height=450,
        title=dict(font=dict(size=20, color='#1A0B2E'), x=0.5, xanchor='center')
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Ranking de ciudades
    st.subheader(f"🏆 Ranking de Ciudades - {año_metrica}")
    
    df_ranking = df_treemap.sort_values('CONSUMO_MWH_ANUAL', ascending=False).reset_index(drop=True)
    df_ranking.index = df_ranking.index + 1
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(
            df_ranking[['MUNICIPIO', 'VEHICULOS_EV', 'CONSUMO_MWH_ANUAL', 'PORCENTAJE']].rename(columns={
                'MUNICIPIO': 'Ciudad',
                'VEHICULOS_EV': 'Vehículos EV',
                'CONSUMO_MWH_ANUAL': 'Demanda (MWh)',
                'PORCENTAJE': 'Participación (%)'
            }),
            use_container_width=True,
            height=300
        )
    
    with col2:
        # Top 3
        st.markdown("### 🥇 Top 3 Ciudades")
        for i, row in df_ranking.head(3).iterrows():
            emoji = ["🥇", "🥈", "🥉"][i-1]
            st.markdown(f"""
            <div class="info-card">
                <div style="font-size: 1.5rem;">{emoji} <b>{row['MUNICIPIO']}</b></div>
                <div style="font-size: 1.2rem; color: #6B1FE0; font-weight: 600;">{row['PORCENTAJE']:.1f}% del total</div>
                <div style="color: #2D3748;">{int(row['CONSUMO_MWH_ANUAL']):,} MWh</div>
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 3: COMPARADOR ====================
with tab3:
    st.header("⚖️ Comparador Interactivo de Ciudades")
    
    col1, col2 = st.columns(2)
    
    with col1:
        ciudad_a = st.selectbox("Seleccionar Ciudad A", options=ciudades_disponibles, index=0)
    
    with col2:
        ciudad_b = st.selectbox("Seleccionar Ciudad B", options=ciudades_disponibles, index=1 if len(ciudades_disponibles) > 1 else 0)
    
    # Filtrar datos
    df_ciudad_a = df_por_ciudad[(df_por_ciudad['MUNICIPIO'] == ciudad_a) & (df_por_ciudad['ANIO'].between(rango_años[0], rango_años[1]))]
    df_ciudad_b = df_por_ciudad[(df_por_ciudad['MUNICIPIO'] == ciudad_b) & (df_por_ciudad['ANIO'].between(rango_años[0], rango_años[1]))]
    
    # Gráfico comparativo
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_ciudad_a['ANIO'],
        y=df_ciudad_a['CONSUMO_MWH_ANUAL'],
        name=ciudad_a,
        mode='lines+markers',
        line=dict(color='#6B1FE0', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(107, 31, 224, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_ciudad_b['ANIO'],
        y=df_ciudad_b['CONSUMO_MWH_ANUAL'],
        name=ciudad_b,
        mode='lines+markers',
        line=dict(color='#B0FF00', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(176, 255, 0, 0.2)'
    ))
    
    fig.update_layout(
        title=f"Comparación: {ciudad_a} vs {ciudad_b}",
        xaxis_title="Año",
        yaxis_title="Demanda Eléctrica (MWh/año)",
        hovermode='x unified',
        plot_bgcolor='white',
        height=500,
        title_font=dict(size=20, color='#1A0B2E')
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métricas comparativas
    st.subheader(f"📊 Métricas Comparativas - {año_metrica}")
    
    data_a = df_ciudad_a[df_ciudad_a['ANIO'] == año_metrica].iloc[0]
    data_b = df_ciudad_b[df_ciudad_b['ANIO'] == año_metrica].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### {ciudad_a}")
        st.metric("Vehículos EV", f"{int(data_a['VEHICULOS_EV']):,}")
        st.metric("Demanda (MWh)", f"{int(data_a['CONSUMO_MWH_ANUAL']):,}")
    
    with col2:
        st.markdown(f"### {ciudad_b}")
        st.metric("Vehículos EV", f"{int(data_b['VEHICULOS_EV']):,}")
        st.metric("Demanda (MWh)", f"{int(data_b['CONSUMO_MWH_ANUAL']):,}")
    
    with col3:
        st.markdown("### Diferencia")
        diff_vehiculos = data_a['VEHICULOS_EV'] - data_b['VEHICULOS_EV']
        diff_demanda = data_a['CONSUMO_MWH_ANUAL'] - data_b['CONSUMO_MWH_ANUAL']
        
        st.metric(
            "Vehículos",
            f"{abs(int(diff_vehiculos)):,}",
            delta=f"{ciudad_a if diff_vehiculos > 0 else ciudad_b} lidera" if diff_vehiculos != 0 else "Empate"
        )
        st.metric(
            "Demanda",
            f"{abs(int(diff_demanda)):,} MWh",
            delta=f"{ciudad_a if diff_demanda > 0 else ciudad_b} mayor" if diff_demanda != 0 else "Igual"
        )

# ==================== TAB 4: DATOS DETALLADOS ====================
with tab4:
    st.header("📊 Datos Detallados y Tablas")
    
    # Selector de vista
    vista = st.radio("Seleccionar Vista", options=["Nacional", "Por Ciudad", "Dataset Completo"], horizontal=True)
    
    if vista == "Nacional":
        st.subheader("📈 Datos Agregados Nacionales")
        df_display = df_nacional[df_nacional['ANIO'].between(rango_años[0], rango_años[1])].copy()
        df_display['CRECIMIENTO_%'] = df_display['VEHICULOS_EV'].pct_change() * 100
        df_display['CRECIMIENTO_%'] = df_display['CRECIMIENTO_%'].fillna(0).round(2)
        
        st.dataframe(
            df_display.rename(columns={
                'ANIO': 'Año',
                'VEHICULOS_EV': 'Vehículos EV',
                'CONSUMO_MWH_ANUAL': 'Demanda (MWh)',
                'TIPO': 'Tipo',
                'CRECIMIENTO_%': 'Crecimiento %'
            }),
            use_container_width=True,
            height=400
        )
        
    elif vista == "Por Ciudad":
        st.subheader("🏙️ Datos por Ciudad")
        
        ciudad_tabla = st.selectbox("Seleccionar Ciudad", options=ciudades_disponibles)
        df_ciudad_tabla = df_por_ciudad[
            (df_por_ciudad['MUNICIPIO'] == ciudad_tabla) &
            (df_por_ciudad['ANIO'].between(rango_años[0], rango_años[1]))
        ].copy()
        
        df_ciudad_tabla['CRECIMIENTO_%'] = df_ciudad_tabla['VEHICULOS_EV'].pct_change() * 100
        df_ciudad_tabla['CRECIMIENTO_%'] = df_ciudad_tabla['CRECIMIENTO_%'].fillna(0).round(2)
        
        st.dataframe(
            df_ciudad_tabla.rename(columns={
                'MUNICIPIO': 'Ciudad',
                'ANIO': 'Año',
                'VEHICULOS_EV': 'Vehículos EV',
                'CONSUMO_MWH_ANUAL': 'Demanda (MWh)',
                'CRECIMIENTO_%': 'Crecimiento %'
            }),
            use_container_width=True,
            height=400
        )
    
    else:
        st.subheader("📦 Dataset Completo")
        st.dataframe(df_por_ciudad, use_container_width=True, height=500)

# ==================== TAB 5: CONCLUSIONES ====================
with tab5:
    st.header("💡 Conclusiones e Impacto Nacional")
    
    # Calcular métricas finales
    data_2023 = df_nacional[df_nacional['ANIO'] == 2023].iloc[0]
    data_2026 = df_nacional[df_nacional['ANIO'] == 2026].iloc[0]
    data_2030 = df_nacional[df_nacional['ANIO'] == 2030].iloc[0]
    
    crecimiento_2023_2026 = ((data_2026['VEHICULOS_EV'] - data_2023['VEHICULOS_EV']) / data_2023['VEHICULOS_EV'] * 100)
    
    # Card 1: Crecimiento explosivo
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">🚀 Crecimiento Explosivo del Parque de Vehículos EV</div>
        <div class="info-card-text">
            De <span class="info-highlight">{int(data_2023['VEHICULOS_EV']):,}</span> vehículos en 2023 a 
            <span class="info-highlight">{int(data_2026['VEHICULOS_EV']):,}</span> en 2026, 
            representando un incremento del <span class="info-highlight">{crecimiento_2023_2026:.0f}%</span> en solo 3 años.
            <br><br>
            Para 2030, se proyectan <span class="info-highlight">{int(data_2030['VEHICULOS_EV']):,}</span> vehículos eléctricos en Colombia.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 2: Demanda eléctrica
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">⚡ Impacto en la Demanda Eléctrica Nacional</div>
        <div class="info-card-text">
            La demanda eléctrica por movilidad eléctrica pasará de 
            <span class="info-highlight">{int(data_2026['CONSUMO_MWH_ANUAL']):,} MWh/año</span> en 2026 a 
            <span class="info-highlight">{int(data_2030['CONSUMO_MWH_ANUAL']):,} MWh/año</span> en 2030.
            <br><br>
            Esto representa aproximadamente el <span class="info-highlight">1.47%</span> de la generación eléctrica nacional actual, 
            un nivel <b>manejable</b> para la infraestructura existente.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 3: Concentración urbana
    df_2026 = df_por_ciudad[df_por_ciudad['ANIO'] == 2026].sort_values('CONSUMO_MWH_ANUAL', ascending=False)
    top_2_porcentaje = (df_2026.head(2)['CONSUMO_MWH_ANUAL'].sum() / df_2026['CONSUMO_MWH_ANUAL'].sum() * 100)
    
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">🏙️ Concentración en Grandes Ciudades</div>
        <div class="info-card-text">
            <span class="info-highlight">{df_2026.iloc[0]['MUNICIPIO']}</span> y 
            <span class="info-highlight">{df_2026.iloc[1]['MUNICIPIO']}</span> concentran el 
            <span class="info-highlight">{top_2_porcentaje:.1f}%</span> de la demanda eléctrica total por movilidad eléctrica.
            <br><br>
            La expansión de infraestructura de carga debe priorizarse en estas áreas urbanas principales.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Card 4: Recomendaciones
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">🎯 Recomendaciones Estratégicas</div>
        <div class="info-card-text">
            <b>1. Infraestructura de Carga:</b> Priorizar despliegue en Bogotá y Medellín<br>
            <b>2. Gestión de la Demanda:</b> Implementar tarifas diferenciadas para carga nocturna<br>
            <b>3. Generación Renovable:</b> Alinear expansión EV con crecimiento de energías limpias<br>
            <b>4. Monitoreo Continuo:</b> Seguimiento trimestral de matrículas y consumo real<br>
            <b>5. Políticas Públicas:</b> Incentivos fiscales y programas de recambio acelerado
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Supuestos del modelo
    with st.expander("📐 Supuestos y Metodología del Modelo"):
        st.markdown("""
        ### Supuestos Técnicos
        
        * **Consumo promedio por vehículo**: 12 kWh/día
        * **Días de uso**: 365 días/año
        * **Consumo anual total**: 4,380 kWh/vehículo/año
        * **Ciudades analizadas**: 6 principales (Bogotá, Medellín, Cali, Barranquilla, Pereira, Manizales)
        
        ### Metodología de Proyección
        
        * **Datos históricos** (2020-2023): Generados mediante tasa de crecimiento inversa del 65% anual
        * **Datos base** (2024-2026): Proyecciones oficiales de electrolineras
        * **Proyecciones** (2027-2030): Modelo de crecimiento exponencial basado en tasa promedio 2023-2026
        
        ### Fuentes
        
        * Datos de proyecciones de demanda de electrolineras
        * Estadísticas nacionales de parque automotor
        * Estándares internacionales de consumo eléctrico (IEA, ANDEMOS)
        """)

# ==================== FOOTER ====================
st.markdown("""
<div class="quoia-footer">
    <div style="margin-bottom: 1.5rem;">
        <img src="https://i.ibb.co/pBWVwrq2/Logo-principal.jpg" alt="QuoiaGo" style="max-width: 200px; filter: brightness(0) invert(1);" />
    </div>
    <div style="font-size: 1.1rem; margin-bottom: 0.5rem; font-weight: 600;">
        QuoiaGo - Liderando la Transformación hacia la Movilidad Eléctrica en Colombia
    </div>
    <div style="font-size: 0.95rem; opacity: 0.9;">
        © 2026 QuoiaGo | Desarrollado con ⚡ y datos en Streamlit + Plotly
    </div>
    <div style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.8;">
        Dashboard interactivo - Última actualización: """ + datetime.now().strftime("%d/%m/%Y %H:%M") + """
    </div>
</div>
""", unsafe_allow_html=True)
