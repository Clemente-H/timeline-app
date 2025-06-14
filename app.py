import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date
import os

# Configuración de la página
st.set_page_config(
    page_title="Timeline de Eventos",
    page_icon="📅",
    layout="wide"
)

# Archivo CSV para persistencia
CSV_FILE = "eventos.csv"

def cargar_eventos():
    """Carga eventos desde CSV o crea DataFrame vacío"""
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            df['fecha'] = pd.to_datetime(df['fecha'])
            return df
        except:
            return pd.DataFrame(columns=['fecha', 'titulo', 'descripcion'])
    else:
        return pd.DataFrame(columns=['fecha', 'titulo', 'descripcion'])

def guardar_eventos(df):
    """Guarda eventos en CSV"""
    df.to_csv(CSV_FILE, index=False)

def crear_timeline(df):
    """Crea la visualización de timeline con Plotly"""
    fig = go.Figure()
    
    # Fechas límite
    fecha_inicio = datetime(2022, 1, 1)
    fecha_fin = datetime(2027, 12, 31)
    
    # Línea base de timeline más gruesa
    fig.add_trace(go.Scatter(
        x=[fecha_inicio, fecha_fin],
        y=[1, 1],
        mode='lines',
        line=dict(color='#2E4057', width=6),
        showlegend=False,
        hoverinfo='skip',
        name=""
    ))
    
    # Marcadores de años centrados con períodos
    for year in range(2022, 2028):
        fecha_inicio_year = datetime(year, 1, 1)
        fecha_fin_year = datetime(year, 12, 31)
        fecha_centro_year = datetime(year, 7, 1)  # Centro del año
        
        # Línea vertical de inicio de año
        fig.add_trace(go.Scatter(
            x=[fecha_inicio_year, fecha_inicio_year],
            y=[0.7, 1.3],
            mode='lines',
            line=dict(color='#2E4057', width=3),
            showlegend=False,
            hoverinfo='skip',
            name=""
        ))
        
        # Línea horizontal del período del año
        fig.add_trace(go.Scatter(
            x=[fecha_inicio_year, fecha_fin_year],
            y=[0.6, 0.6],
            mode='lines',
            line=dict(color='#2E4057', width=2),
            showlegend=False,
            hoverinfo='skip',
            name=""
        ))
        
        # Etiquetas de años en el centro
        fig.add_annotation(
            x=fecha_centro_year,
            y=0.5,
            text=f"<b>{year}</b>",
            showarrow=False,
            font=dict(size=14, color='#2E4057')
        )
        
        # Marcadores de meses
        for month in range(1, 13):
            if month != 1:  # Skip enero (ya está el año)
                fecha_month = datetime(year, month, 1)
                fig.add_trace(go.Scatter(
                    x=[fecha_month, fecha_month],
                    y=[0.9, 1.1],
                    mode='lines',
                    line=dict(color='#BDC3C7', width=1),
                    showlegend=False,
                    hoverinfo='skip',
                    name=""
                ))
                
                # Número del mes en gris claro
                fig.add_annotation(
                    x=fecha_month,
                    y=0.8,
                    text=str(month),
                    showarrow=False,
                    font=dict(size=8, color='#BDC3C7')
                )
    
    # Línea vertical final (cierre de 2027)
    fecha_final = datetime(2027, 12, 31)
    fig.add_trace(go.Scatter(
        x=[fecha_final, fecha_final],
        y=[0.7, 1.3],
        mode='lines',
        line=dict(color='#2E4057', width=3),
        showlegend=False,
        hoverinfo='skip',
        name=""
    ))
    
    # Eventos con cuatro alturas - recálculo dinámico
    if not df.empty:
        # Ordenar eventos por fecha para distribuir alturas
        df_sorted = df.sort_values('fecha').reset_index(drop=True)
        alturas = [1.5, 1.8, 2.1, 2.4]  # Cuatro alturas diferentes
        
        # Algoritmo para evitar colapso: eventos cercanos van a alturas diferentes
        alturas_asignadas = []
        for i, evento in df_sorted.iterrows():
            # Para eventos cercanos (menos de 60 días), usar altura diferente
            altura_usada = i % 4
            
            # Verificar si hay eventos muy cercanos y ajustar
            if i > 0:
                fecha_actual = evento['fecha']
                fecha_anterior = df_sorted.iloc[i-1]['fecha']
                dias_diferencia = (fecha_actual - fecha_anterior).days
                
                # Si están muy cerca (menos de 45 días), forzar altura diferente
                if dias_diferencia < 45:
                    altura_anterior = alturas_asignadas[-1]
                    altura_idx_anterior = alturas.index(altura_anterior)
                    altura_usada = (altura_idx_anterior + 1) % 4
            
            alturas_asignadas.append(alturas[altura_usada])
        
        # 4 tonos de azul
        colores = ['#0B2F3A', '#1B4F72', '#2E86C1', '#5DADE2']  # Muy oscuro, oscuro, medio, claro
        
        for i, (idx, evento) in enumerate(df_sorted.iterrows()):
            altura_evento = alturas_asignadas[i]
            altura_idx = alturas.index(altura_evento)
            color_evento = colores[altura_idx]
            
            # Punto del evento más grande
            fig.add_trace(go.Scatter(
                x=[evento['fecha']],
                y=[1],
                mode='markers',
                marker=dict(
                    size=15,
                    color=color_evento,
                    symbol='diamond',
                    line=dict(width=2, color='white')
                ),
                showlegend=False,
                customdata=[evento['descripcion']],
                hovertemplate=(
                    "<b>%{text}</b><br>" +
                    "Fecha: %{x|%d/%m/%Y}<br>" +
                    "Descripción: %{customdata}<br>" +
                    "<extra></extra>"
                ),
                text=evento['titulo'],
                name=""
            ))
            
            # Línea vertical hacia el título más fina
            fig.add_trace(go.Scatter(
                x=[evento['fecha'], evento['fecha']],
                y=[1, altura_evento - 0.1],
                mode='lines',
                line=dict(color=color_evento, width=1.5),
                showlegend=False,
                hoverinfo='skip',
                name=""
            ))
            
            # Título del evento con mejor diseño
            titulo_texto = evento['titulo']
            if len(titulo_texto) > 20:
                # Partir título largo en dos líneas
                palabras = titulo_texto.split()
                mitad = len(palabras) // 2
                linea1 = ' '.join(palabras[:mitad])
                linea2 = ' '.join(palabras[mitad:])
                titulo_final = f"{linea1}<br>{linea2}"
            else:
                titulo_final = titulo_texto
            
            fig.add_annotation(
                x=evento['fecha'],
                y=altura_evento,
                text=f"<b>{titulo_final}</b>",
                showarrow=False,
                font=dict(size=9, color='white'),
                bgcolor=color_evento,
                bordercolor=color_evento,
                borderwidth=1,
                borderpad=4
            )
    
    # Configuración del layout
    fig.update_layout(
        title={
            'text': 'Timeline de Eventos 2022-2027',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2E4057'}
        },
        xaxis=dict(
            title="",
            range=[fecha_inicio, fecha_fin],
            showgrid=True,
            gridwidth=1,
            gridcolor='#ECF0F1',
            tickformat='%Y',
            dtick="M12"
        ),
        yaxis=dict(
            title="",
            range=[0.3, 3.0],
            showticklabels=False,
            showgrid=False,
            zeroline=False
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=500,
        margin=dict(l=50, r=50, t=100, b=80)
    )
    
    return fig

# Interfaz principal
st.title("📅 Timeline de Eventos")
st.markdown("Crea y visualiza eventos en una línea de tiempo interactiva")

# Cargar datos
if 'df_eventos' not in st.session_state:
    st.session_state.df_eventos = cargar_eventos()

# Sidebar para agregar eventos
with st.sidebar:
    st.header("➕ Agregar Evento")
    
    with st.form("form_evento"):
        fecha_evento = st.date_input(
            "Fecha",
            min_value=date(2022, 1, 1),
            max_value=date(2027, 12, 31),
            value=date(2024, 1, 1)
        )
        
        titulo_evento = st.text_input(
            "Título",
            placeholder="Ej: Inicio Construcción Tramo 1"
        )
        
        descripcion_evento = st.text_area(
            "Descripción (opcional)",
            placeholder="Detalles adicionales del evento..."
        )
        
        submit_button = st.form_submit_button("Agregar Evento")
        
        if submit_button and titulo_evento:
            nuevo_evento = pd.DataFrame({
                'fecha': [pd.to_datetime(fecha_evento)],
                'titulo': [titulo_evento],
                'descripcion': [descripcion_evento if descripcion_evento else ""]
            })
            
            st.session_state.df_eventos = pd.concat([
                st.session_state.df_eventos, 
                nuevo_evento
            ], ignore_index=True)
            
            guardar_eventos(st.session_state.df_eventos)
            st.success("¡Evento agregado!")
            st.rerun()

# Timeline principal
st.subheader("Timeline")
fig = crear_timeline(st.session_state.df_eventos)
st.plotly_chart(fig, use_container_width=True)

# Información de interactividad
st.info("💡 **Tip:** Haz hover sobre los eventos para ver detalles completos")

# Gestión de eventos
if not st.session_state.df_eventos.empty:
    st.subheader("📋 Eventos Registrados")
    
    # Mostrar tabla editable
    df_display = st.session_state.df_eventos.copy()
    df_display['fecha'] = df_display['fecha'].dt.strftime('%d/%m/%Y')
    
    edited_df = st.data_editor(
        df_display,
        use_container_width=True,
        num_rows="dynamic",
        column_config={
            "fecha": st.column_config.TextColumn("Fecha"),
            "titulo": st.column_config.TextColumn("Título"),
            "descripcion": st.column_config.TextColumn("Descripción")
        }
    )
    
    # Botón para aplicar cambios
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("💾 Guardar Cambios"):
            try:
                edited_df['fecha'] = pd.to_datetime(edited_df['fecha'], format='%d/%m/%Y')
                st.session_state.df_eventos = edited_df
                guardar_eventos(st.session_state.df_eventos)
                st.success("¡Cambios guardados!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
    
    with col2:
        if st.button("🗑️ Limpiar Todo"):
            st.session_state.df_eventos = pd.DataFrame(columns=['fecha', 'titulo', 'descripcion'])
            guardar_eventos(st.session_state.df_eventos)
            st.success("¡Eventos eliminados!")
            st.rerun()
    
    with col3:
        # Botón de descarga
        if st.download_button(
            label="📥 Descargar CSV",
            data=st.session_state.df_eventos.to_csv(index=False),
            file_name=f"eventos_timeline_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        ):
            st.success("¡CSV descargado!")

# Exportar imagen
st.subheader("📷 Exportar Timeline")
st.markdown("""
**Para exportar como imagen:**
1. Haz clic en el ícono de cámara en la esquina superior derecha del gráfico
2. Selecciona 'Download plot as PNG'
3. La imagen se descargará automáticamente

**Tip:** Para mejor calidad en PPT, usa el PNG descargado directamente.
""")

# Footer
st.markdown("---")
st.markdown("💡 Los eventos se guardan automáticamente en `eventos.csv`")