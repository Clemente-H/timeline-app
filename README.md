# Timeline de Eventos

Aplicación simple en Streamlit para crear y visualizar eventos en una línea de tiempo interactiva (2022-2027).

## 🚀 Instalación

```bash
pip install streamlit pandas plotly
```

## ▶️ Ejecutar

```bash
streamlit run app.py
```

## 📋 Características

- ✅ Timeline proporcional y preciso
- ✅ Agregar/editar/eliminar eventos
- ✅ Hover interactivo con detalles
- ✅ Exportar como PNG para PPT
- ✅ Persistencia automática en CSV

## 🎯 Uso

1. **Agregar eventos:** Usar el panel lateral
2. **Ver detalles:** Hover sobre los eventos en el timeline
3. **Editar:** Usar la tabla inferior
4. **Exportar:** Clic en el ícono de cámara del gráfico → "Download plot as PNG"

## 📁 Archivos

- `app.py` - Aplicación principal
- `eventos.csv` - Base de datos (se crea automático)

## 💡 Tips

- Los eventos se guardan automáticamente
- Usa PNG exportado para mejor calidad en presentaciones
- El hover muestra título + descripción completa