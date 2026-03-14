import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Dashboard Académico", layout="wide")

st.title("📊 Dashboard de Desempeño Estudiantil")
st.markdown("Análisis basado en factores socioeconómicos y académicos.")

conn = sqlite3.connect('escuela.db')

# --- SIDEBAR ---
st.sidebar.header("Filtros de Análisis")
nivel_educativo = st.sidebar.multiselect(
    "Nivel Educativo de Padres:",
    options=["High School", "Associate's Degree", "Bachelor's Degree", "Master's Degree", "Some College"],
    default=["High School", "Bachelor's Degree"]
)

# --- CONSULTA ---
query = f"""
SELECT
    c.student_id, c.hours_studied, c.attendance, c.exam_score,
    e.parent_education, e.family_income, e.access_to_resources,
    s.gender
FROM Calificaciones c
JOIN Entorno e ON c.student_id = e.student_id
JOIN Estudiantes s ON c.student_id = s.student_id
WHERE e.parent_education IN {tuple(nivel_educativo) if len(nivel_educativo) > 1 else "('" + nivel_educativo[0] + "')"}
"""
df = pd.read_sql(query, conn)

# --- MÉTRICAS ---
col1, col2, col3 = st.columns(3)
col1.metric("Promedio Examen", f"{df['exam_score'].mean():.2f}")
col2.metric("Horas de Estudio Prom.", f"{df['hours_studied'].mean():.1f}h")
col3.metric("Asistencia Promedio", f"{df['attendance'].mean():.1f}%")

st.divider()

# --- GRÁFICOS ---
fila1_col1, fila1_col2 = st.columns(2)

with fila1_col1:
    st.subheader("Relación Horas de Estudio vs Nota")
    fig1 = px.scatter(df, x="hours_studied", y="exam_score", color="gender", template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with fila1_col2:
    st.subheader("Distribución de Notas por Género")
    fig2 = px.box(df, x="gender", y="exam_score", color="gender")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Vista Detallada de la Base de Datos")
st.dataframe(df.head(20), use_container_width=True)

conn.close()
