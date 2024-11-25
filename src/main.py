import streamlit as st
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime

# Conexión a la base de datos SQLite
conn = sqlite3.connect("ventas.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    precio REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS ventas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    producto_id INTEGER,
    fecha DATE,
    cantidad INTEGER,
    FOREIGN KEY (producto_id) REFERENCES productos(id)
)
""")
conn.commit()

# Funciones para el CRUD
def crear_producto(nombre, precio):
    cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
    conn.commit()

def leer_productos():
    cursor.execute("SELECT * FROM productos")
    return cursor.fetchall()

def crear_venta(producto_id, fecha, cantidad):
    cursor.execute("INSERT INTO ventas (producto_id, fecha, cantidad) VALUES (?, ?, ?)", (producto_id, fecha, cantidad))
    conn.commit()

def leer_ventas(producto_id):
    cursor.execute("SELECT fecha, cantidad FROM ventas WHERE producto_id = ?", (producto_id,))
    return cursor.fetchall()

# Función para predecir ventas usando regresión lineal
def predecir_ventas(ventas_historicas):
    # Convertir fechas a números
    fechas = [datetime.strptime(venta[0], '%Y-%m-%d').timestamp() for venta in ventas_historicas]
    cantidades = [venta[1] for venta in ventas_historicas]

    # Transformar datos en arrays numpy
    X = np.array(fechas).reshape(-1, 1)
    y = np.array(cantidades)

    # Entrenar el modelo de regresión lineal
    model = LinearRegression()
    model.fit(X, y)

    # Realizar predicciones para los próximos 7 días
    futuro = np.array([max(fechas) + 86400 * i for i in range(1, 8)]).reshape(-1, 1)
    predicciones = model.predict(futuro)

    # Devolver las fechas futuras y las predicciones
    fechas_futuras = [datetime.fromtimestamp(fecha).strftime('%Y-%m-%d') for fecha in futuro.flatten()]
    return fechas_futuras, predicciones

# Interfaz con Streamlit
st.title("Sistema de Proyección de Ventas")

# Crear producto
st.header("Agregar Producto")
nombre_producto = st.text_input("Nombre del Producto")
precio_producto = st.number_input("Precio del Producto", min_value=0.01, format="%.2f")
if st.button("Agregar Producto"):
    crear_producto(nombre_producto, precio_producto)
    st.success(f"Producto '{nombre_producto}' agregado exitosamente.")

# Leer productos
st.header("Productos Disponibles")
productos = leer_productos()
for producto in productos:
    st.write(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}")

# Agregar ventas
st.header("Registrar Venta")
producto_id = st.selectbox("Selecciona un Producto", [producto[0] for producto in productos])
fecha_venta = st.date_input("Fecha de la Venta", datetime.today())
cantidad_venta = st.number_input("Cantidad Vendida", min_value=1, step=1)
if st.button("Registrar Venta"):
    crear_venta(producto_id, fecha_venta, cantidad_venta)
    st.success(f"Venta de {cantidad_venta} unidades registrada para el producto con ID {producto_id}.")

# Mostrar ventas y proyecciones
st.header("Proyección de Ventas")
producto_seleccionado = st.selectbox("Selecciona un Producto para Proyección", [producto[1] for producto in productos])

if producto_seleccionado:
    producto_id = [producto[0] for producto in productos if producto[1] == producto_seleccionado][0]
    ventas_historicas = leer_ventas(producto_id)

    if ventas_historicas:
        st.write(f"Ventas históricas para {producto_seleccionado}:")
        ventas_df = pd.DataFrame(ventas_historicas, columns=["Fecha", "Cantidad Vendida"])
        st.dataframe(ventas_df)

        # Predecir las ventas para los próximos 7 días
        fechas_futuras, predicciones = predecir_ventas(ventas_historicas)

        # Mostrar las predicciones
        st.write(f"Proyección de ventas para los próximos 7 días de {producto_seleccionado}:")
        proyeccion_df = pd.DataFrame({"Fecha": fechas_futuras, "Proyección de Ventas": predicciones})
        st.dataframe(proyeccion_df)

        # Graficar las predicciones
        plt.figure(figsize=(10, 5))
        plt.plot(fechas_futuras, predicciones, marker='o', label="Proyección de Ventas", color="red")
        plt.title(f"Proyección de Ventas para {producto_seleccionado}")
        plt.xlabel("Fecha")
        plt.ylabel("Cantidad Vendida")
        plt.xticks(rotation=45)
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write("No hay ventas históricas para este producto.")
