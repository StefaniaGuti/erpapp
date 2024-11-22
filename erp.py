#%%writefile erp_streamlit.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from fpdf import FPDF

logo_path = "data:image/png;base64,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"  # Asegúrate de poner la ruta correcta

# Configuración inicial
st.set_page_config(page_title="Módulos del ERP", layout="wide",page_icon=logo_path)
# Ruta del archivo de imagen (logo)

# Mostrar el logo en la parte superior de la aplicación
st.image(logo_path, width=200)  # Puedes ajustar el tamaño cambiando el valor de 'width'

# Agregar un título o contenido a la aplicación
st.title("Sistema ERP")
st.write("Bienvenido al sistema ERP para la gestión de clientes, inventarios, facturación, reportes y análisis de ventas.")

st.sidebar.title("ERP_ITM")

# Variables de autenticación
USER = "Lira"
PASSWORD = "Lir@1120"

# Inicialización de variables globales
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "modulo_seleccionado" not in st.session_state:
    st.session_state["modulo_seleccionado"] = None

# Parámetros de ID
if "id_cliente" not in st.session_state:
    st.session_state["id_cliente"] = 1  # El primer ID de cliente

if "id_producto" not in st.session_state:
    st.session_state["id_producto"] = 1  # El primer ID de producto

if "id_factura" not in st.session_state:
    st.session_state["id_factura"] = 1  # El primer ID de factura

# Inicialización de DataFrames
if "clientes" not in st.session_state:
    st.session_state["clientes"] = pd.DataFrame(columns=["ID", "Nombre", "Correo", "Teléfono"])

if "productos" not in st.session_state:
    st.session_state["productos"] = pd.DataFrame(columns=["ID", "Producto", "Cantidad", "Precio Unitario"])

if "facturas" not in st.session_state:
    st.session_state["facturas"] = pd.DataFrame(columns=["Factura ID", "Cliente ID", "Cliente Nombre", "Productos", "Total", "IVA", "Fecha"])
    
# Función de autenticación
with st.sidebar:
    st.title("Módulos ERP")
if not st.session_state["auth"]:
    st.sidebar.subheader("Iniciar Sesión")
    usuario = st.sidebar.text_input("Usuario")
    contraseña = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Ingresar"):
        if usuario == USER and contraseña == PASSWORD:
            st.session_state["auth"] = True
            st.sidebar.success("Inicio de sesión exitoso.")
        else:
            st.sidebar.error("Usuario o contraseña incorrectos.")
else:
    st.sidebar.subheader(f"Bienvenido, {USER}")
    st.session_state["modulo_seleccionado"] = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Gestión de Clientes", "Gestión de Inventario", "Generar Factura", "Generar Reportes", "Análisis de Ventas"],
    )
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["auth"] = False
        st.session_state["modulo_seleccionado"] = None
        st.sidebar.success("Sesión cerrada correctamente.")


# Funciones auxiliares
def exportar_csv(df, nombre_archivo):
    """Permite exportar un DataFrame como archivo CSV."""
    st.download_button(
        label="Exportar Datos",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name=nombre_archivo,
        mime="text/csv",
    )

# Funciones de los módulos
def gestion_clientes():
    st.header("Gestión de Clientes")
    
    # Registro de nuevo cliente
    with st.form("Registro de Cliente"):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo Electrónico")
        telefono = st.text_input("Teléfono")
        submitted = st.form_submit_button("Registrar Cliente")
        
        if submitted:
            # Generación de ID para el nuevo cliente
            cliente_id = st.session_state["id_cliente"]
            nuevo_cliente = pd.DataFrame([{
                "ID": cliente_id, "Nombre": nombre, "Correo": correo, "Teléfono": telefono
            }])
            st.session_state["clientes"] = pd.concat([st.session_state["clientes"], nuevo_cliente], ignore_index=True)
            st.session_state["id_cliente"] += 1  # Incrementar el ID para el siguiente cliente
            st.success(f"Cliente {nombre} registrado correctamente con ID: {cliente_id}.")
    
    # Búsqueda de clientes
    st.subheader("Buscar Cliente")
    search_term = st.text_input("Buscar por nombre o ID")
    if search_term:
        clientes_filtrados = st.session_state["clientes"][st.session_state["clientes"]["Nombre"].str.contains(search_term, case=False)]
        st.dataframe(clientes_filtrados)
    else:
        st.dataframe(st.session_state["clientes"])

    # Edición de cliente
    cliente_a_editar = st.selectbox("Seleccionar cliente para editar", st.session_state["clientes"]["ID"])
    cliente_data = st.session_state["clientes"][st.session_state["clientes"]["ID"] == cliente_a_editar]
    if cliente_data.empty:
        st.warning("Cliente no encontrado.")
    else:
        with st.form("Editar Cliente"):
            nombre_edit = st.text_input("Nuevo Nombre", cliente_data["Nombre"].values[0])
            correo_edit = st.text_input("Nuevo Correo", cliente_data["Correo"].values[0])
            telefono_edit = st.text_input("Nuevo Teléfono", cliente_data["Teléfono"].values[0])
            submitted_edit = st.form_submit_button("Actualizar Cliente")
            
            if submitted_edit:
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Nombre"] = nombre_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Correo"] = correo_edit
                st.session_state["clientes"].loc[st.session_state["clientes"]["ID"] == cliente_a_editar, "Teléfono"] = telefono_edit
                st.success(f"Cliente con ID {cliente_a_editar} actualizado.")

    # Eliminación de cliente
    cliente_a_eliminar = st.selectbox("Seleccionar cliente para eliminar", st.session_state["clientes"]["ID"])
    if st.button("Eliminar Cliente"):
        st.session_state["clientes"] = st.session_state["clientes"][st.session_state["clientes"]["ID"] != cliente_a_eliminar]
        st.success("Cliente eliminado correctamente.")

def gestion_inventario():

    st.header("Gestión de Inventario")
    
    # Registro de producto
    with st.form("Registro de Producto"):
        producto = st.text_input("Producto")
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
        precio_unitario = st.number_input("Precio Unitario", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Registrar Producto")
        
        if submitted:
            # Generación de ID para el nuevo producto
            producto_id = st.session_state["id_producto"]
            nuevo_producto = pd.DataFrame([{
                "ID": producto_id, "Producto": producto, "Cantidad": cantidad, "Precio Unitario": precio_unitario
            }])
            st.session_state["productos"] = pd.concat([st.session_state["productos"], nuevo_producto], ignore_index=True)
            st.session_state["id_producto"] += 1  # Incrementar el ID para el siguiente producto
            st.success(f"Producto {producto} registrado correctamente con ID: {producto_id}.")
    
    # Búsqueda de productos
    st.subheader("Buscar Producto")
    search_term = st.text_input("Buscar producto por nombre")
    if search_term:
        inventario_filtrado = st.session_state["productos"][st.session_state["productos"]["Producto"].str.contains(search_term, case=False)]
        st.dataframe(inventario_filtrado)
    else:
        st.dataframe(st.session_state["productos"])

    # Eliminación de producto
    producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", st.session_state["productos"]["Producto"])
    if st.button("Eliminar Producto"):
        st.session_state["productos"] = st.session_state["productos"][st.session_state["productos"]["Producto"] != producto_a_eliminar]
        st.success("Producto eliminado correctamente.")

def gestion_facturas():
    st.header("Generar Factura")
    st.write("Selecciona un cliente y productos para crear una factura.")
    
    if st.session_state["clientes"].empty:
        st.warning("No hay clientes registrados. Por favor, registra clientes antes de crear una factura.")
        return
    
    if st.session_state["productos"].empty:
        st.warning("No hay productos en el inventario. Por favor, registra productos antes de crear una factura.")
        return
    
    cliente_id = st.selectbox("Seleccionar Cliente", st.session_state["clientes"]["ID"])
    cliente_nombre = st.session_state["clientes"].loc[
        st.session_state["clientes"]["ID"] == cliente_id, "Nombre"
    ].values[0]
    
    # Selección de productos
    productos_seleccionados = st.multiselect(
        "Selecciona productos", 
        st.session_state["productos"]["Producto"].values
    )
    
    if not productos_seleccionados:
        st.info("Selecciona al menos un producto para generar una factura.")
        return
    
    productos_detalle = []
    total = 0
    
    for producto in productos_seleccionados:
        producto_info = st.session_state["productos"].loc[
            st.session_state["productos"]["Producto"] == producto
        ]
        precio_unitario = producto_info["Precio Unitario"].values[0]
        stock_disponible = producto_info["Cantidad"].values[0]
        
        # Selección de cantidad
        cantidad = st.number_input(
            f"Cantidad de {producto} (Disponible: {stock_disponible})", 
            min_value=1, 
            max_value=stock_disponible, 
            step=1
        )
        
        subtotal = precio_unitario * cantidad
        total += subtotal
        productos_detalle.append({
            "Producto": producto,
            "Cantidad": cantidad,
            "Precio Unitario": precio_unitario,
            "Subtotal": subtotal
        })
    
    # Calcular IVA y total final
    iva = total * 0.16
    total_con_iva = total + iva
    
    # Mostrar resumen
    st.subheader("Resumen de Factura")
    st.table(pd.DataFrame(productos_detalle))
    st.write(f"Subtotal: ${total:,.2f}")
    st.write(f"IVA (16%): ${iva:,.2f}")
    st.write(f"Total: ${total_con_iva:,.2f}")
    
    # Confirmación y registro de factura
    if st.button("Confirmar y Generar Factura"):
        factura_id = st.session_state["id_factura"]
        fecha = pd.to_datetime("today").strftime("%Y-%m-%d")
        
        # Registrar factura
        factura = pd.DataFrame([{
            "Factura ID": factura_id, 
            "Cliente ID": cliente_id, 
            "Cliente Nombre": cliente_nombre,
            "Productos": productos_detalle, 
            "Total": total, 
            "IVA": iva, 
            "Fecha": fecha
        }])
        st.session_state["facturas"] = pd.concat([st.session_state["facturas"], factura], ignore_index=True)
        st.session_state["id_factura"] += 1  # Incrementar el ID para la siguiente factura
        
        # Reducir inventario
        for detalle in productos_detalle:
            producto = detalle["Producto"]
            cantidad = detalle["Cantidad"]
            st.session_state["productos"].loc[
                st.session_state["productos"]["Producto"] == producto, "Cantidad"
            ] -= cantidad
        
        st.success(f"Factura {factura_id} generada correctamente.")
        st.write(f"Total con IVA: ${total_con_iva:,.2f}")
        
        # Exportar factura
        exportar_csv(st.session_state["facturas"], f"factura_{factura_id}.csv")

def gestion_reportes():
 

    st.header("Generar Reportes")

    # Generación de reportes contables
    st.write("Aquí pueden ir los reportes contables.")
    st.write("Funciones específicas para reportes como ingresos, gastos y balances se agregarán aquí.")
    
    # Simulando el reporte básico
    st.text_area("Resumen", "Reporte generado: ingresos, gastos, balance general, etc.")
    
    # Exportar el reporte a CSV
    exportar_csv(st.session_state["facturas"], "reportes_contables.csv")

import plotly.express as px

def analisis_ventas():
    st.header("Análisis de Ventas")
    
    # Verificar si hay datos en las facturas
    if st.session_state["facturas"].empty:
        st.warning("No hay datos de facturas para analizar.")
        return

    # Crear una lista para desglosar productos en facturas
    productos_desglosados = []
    for _, fila in st.session_state["facturas"].iterrows():
        for producto in fila["Productos"]:
            productos_desglosados.append({
                "Producto": producto["Producto"],
                "Cantidad": producto["Cantidad"],
                "Subtotal": producto["Subtotal"],
                "Fecha": fila["Fecha"]
            })

    # Crear un DataFrame con los datos desglosados
    df_productos = pd.DataFrame(productos_desglosados)

    # Verificar si hay datos en el DataFrame desglosado
    if df_productos.empty:
        st.warning("No hay datos suficientes para generar análisis.")
        return

    # Análisis de ventas por producto
    st.subheader("Ventas por Producto")
    ventas_por_producto = df_productos.groupby("Producto").sum().reset_index()
    fig1 = px.bar(
        ventas_por_producto, 
        x="Producto", 
        y="Subtotal", 
        title="Ingresos por Producto", 
        labels={"Subtotal": "Ingresos ($)"},
        text="Subtotal"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Análisis de cantidades vendidas por producto
    st.subheader("Cantidad Vendida por Producto")
    fig2 = px.pie(
        ventas_por_producto, 
        names="Producto", 
        values="Cantidad", 
        title="Distribución de Cantidades Vendidas"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Análisis temporal de ventas
    st.subheader("Ingresos Totales por Fecha")
    df_productos["Fecha"] = pd.to_datetime(df_productos["Fecha"])
    ingresos_por_fecha = df_productos.groupby("Fecha").sum().reset_index()
    fig3 = px.line(
        ingresos_por_fecha, 
        x="Fecha", 
        y="Subtotal", 
        title="Evolución de Ingresos en el Tiempo",
        labels={"Subtotal": "Ingresos ($)", "Fecha": "Fecha"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.success("Gráficos interactivos generados correctamente.")

# Navegación entre módulos
if st.session_state["auth"]:
    if st.session_state["modulo_seleccionado"] == "Gestión de Clientes":
        gestion_clientes()
    elif st.session_state["modulo_seleccionado"] == "Gestión de Inventario":
        gestion_inventario()
    elif st.session_state["modulo_seleccionado"] == "Generar Factura":
        gestion_facturas()
    elif st.session_state["modulo_seleccionado"] == "Generar Reportes":
        gestion_reportes()
    elif st.session_state["modulo_seleccionado"] == "Análisis de Ventas":
        analisis_ventas()
else:
    st.warning("Por favor, inicia sesión para continuar.")
