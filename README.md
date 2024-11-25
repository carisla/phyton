# Sistema de Proyección de Ventas

Este es un sistema simple de proyección de ventas que utiliza **SQLite** como base de datos y **Streamlit** como interfaz de usuario. El sistema permite registrar productos, realizar ventas y generar predicciones de ventas utilizando un modelo de **regresión lineal**.

## Funcionalidades

- **CRUD de Productos**: Puedes agregar productos con nombre y precio.
- **Registro de Ventas**: Puedes registrar ventas de productos especificando la cantidad vendida y la fecha.
- **Proyección de Ventas**: Utiliza un modelo de regresión lineal para predecir las ventas de un producto para los próximos 7 días.
  
## Tecnologías Utilizadas

- **Python**: Lenguaje de programación.
- **Streamlit**: Framework para crear aplicaciones web interactivas en Python.
- **SQLite**: Base de datos ligera para almacenar productos y ventas.
- **Scikit-Learn**: Biblioteca para crear el modelo de regresión lineal.
- **Matplotlib**: Para graficar las predicciones de ventas.

## Requisitos

Para ejecutar este proyecto, asegúrate de tener las siguientes librerías instaladas:

bash
pip install streamlit sqlite3 pandas numpy matplotlib scikit-learn
pip install streamlit sqlite3
