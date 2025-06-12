import streamlit as st
import pandas as pd
import plotly.express as px

# Cargar archivo Excel
df = pd.read_excel("Resumen_Indicadores_Financieros.xlsx")

# Crear etiquetas con fecha completa para evitar interpolación numérica
df["Fecha_etiqueta"] = df["Año"].astype(int).apply(lambda x: f"31.12.{x}")

# Paleta de colores
colores = px.colors.qualitative.Plotly + px.colors.qualitative.D3 + px.colors.qualitative.Dark24

st.title("📊 Dashboard de Indicadores Financieros")
st.markdown("Visualización interactiva de los principales indicadores económicos por año.")

# Mostrar la tabla original
st.subheader("📋 Tabla de Indicadores")
st.dataframe(df)

st.markdown("---")
st.subheader("📈 Gráficos por Indicador")

for i, col in enumerate(df.columns):
    if col not in ["Año", "Fecha_etiqueta"] and pd.api.types.is_numeric_dtype(df[col]):
        color = colores[i % len(colores)]

        if col.strip().upper() == "EBITDA":
            fig = px.bar(
                df,
                x="Fecha_etiqueta",
                y=col,
                title=f"{col} por Año",
                color_discrete_sequence=[color],
                text=col
            )
            fig.update_traces(width=0.4, texttemplate='%{text:.2s}', textposition='outside')
        else:
            fig = px.line(
                df,
                x="Fecha_etiqueta",
                y=col,
                markers=True,
                title=f"Evolución de {col}",
                color_discrete_sequence=[color]
            )

        fig.update_layout(xaxis_title="Año", yaxis_title=col)
        st.plotly_chart(fig, use_container_width=True)

