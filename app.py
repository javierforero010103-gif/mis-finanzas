# =========================================================
# APP: MIS FINANZAS
# Creado por Alexander Polanco
# =========================================================

import streamlit as st
import pandas as pd
import json
import os
import ast
import operator as op
from datetime import datetime
import plotly.express as px

# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="MIS FINANZAS",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_FILE = "mis_finanzas_db.json"

# =========================================================
# ESTILOS UI/UX PREMIUM
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #0F172A;
    color: white;
}

h1, h2, h3 {
    color: #F8FAFC;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #10B981;
    margin-bottom: 0;
}

.subtitle {
    color: #CBD5E1;
    margin-bottom: 20px;
}

.card {
    background: #1E293B;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #334155;
    margin-bottom: 20px;
}

.big-button button {
    width: 100%;
    height: 90px;
    font-size: 40px;
    border-radius: 18px;
    background-color: #10B981;
    color: white;
    border: none;
}

.big-button button:hover {
    background-color: #059669;
}

.stButton button {
    border-radius: 12px;
    font-weight: 600;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: #94A3B8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# FUNCIONES BASE
# =========================================================

def crear_db():
    """
    Crea el archivo JSON inicial si no existe.
    """

    if not os.path.exists(DB_FILE):

        data = {
            "pin": "1234",
            "historial": [],
            "historico_meses": {},
            "billeteras": {
                "Efectivo": 0,
                "Ahorro": 0,
                "Tarjetas": 0,
                "Colchón": 0
            },
            "categorias": [
                {"nombre": "Comida", "icono": "🍔"},
                {"nombre": "Transporte", "icono": "🚗"},
                {"nombre": "Salud", "icono": "🏥"},
                {"nombre": "Entretenimiento", "icono": "🎮"}
            ],
            "presupuestos": {},
            "recurrentes": []
        }

        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def cargar_db():
    """
    Carga los datos desde JSON.
    """

    crear_db()

    with open(DB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_db(data):
    """
    Guarda la base de datos.
    """

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================================================
# CALCULADORA SEGURA
# =========================================================

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg
}

def evaluar(expr):
    """
    Permite operaciones tipo:
    2000+500
    10000-2500
    """

    try:
        return eval_node(ast.parse(expr, mode='eval').body)
    except:
        raise ValueError("Expresión inválida")


def eval_node(node):

    if isinstance(node, ast.Num):
        return node.n

    elif isinstance(node, ast.BinOp):

        return OPERATORS[type(node.op)](
            eval_node(node.left),
            eval_node(node.right)
        )

    elif isinstance(node, ast.UnaryOp):

        return OPERATORS[type(node.op)](
            eval_node(node.operand)
        )

    else:
        raise TypeError(node)

# =========================================================
# SESSION STATE
# =========================================================

if "db" not in st.session_state:
    st.session_state.db = cargar_db()

if "login" not in st.session_state:
    st.session_state.login = False

db = st.session_state.db

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.login:

    st.markdown("<h1 class='main-title'>🔒 MIS FINANZAS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Acceso seguro mediante PIN</p>", unsafe_allow_html=True)

    pin = st.text_input("PIN", type="password")

    if st.button("Ingresar"):

        if pin == db["pin"]:
            st.session_state.login = True
            st.rerun()
        else:
            st.error("PIN incorrecto")

    st.stop()

# =========================================================
# HEADER
# =========================================================

st.markdown("<h1 class='main-title'>💰 MIS FINANZAS</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Gestión moderna de finanzas personales</p>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ MENÚ")

    pagina = st.radio(
        "Navegación",
        [
            "⚡ Entrada rápida",
            "📊 Organización",
            "📈 Análisis",
            "🗂️ Histórico",
            "⚙️ Configuración"
        ]
    )

    st.divider()

    st.subheader("💼 Billeteras")

    for wallet, saldo in db["billeteras"].items():

        st.metric(wallet, f"${saldo:,.0f}")

# =========================================================
# ENTRADA RÁPIDA
# =========================================================

if pagina == "⚡ Entrada rápida":

    st.subheader("⚡ Registrar gasto")

    st.markdown('<div class="big-button">', unsafe_allow_html=True)

    if st.button("＋"):
        st.toast("Formulario listo")

    st.markdown('</div>', unsafe_allow_html=True)

    with st.form("gasto_form"):

        descripcion = st.text_input("Descripción")

        monto_texto = st.text_input(
            "Monto",
            placeholder="Ejemplo: 2000+500"
        )

        categorias = [
            f"{c['icono']} {c['nombre']}"
            for c in db["categorias"]
        ]

        categoria = st.selectbox("Categoría", categorias)

        billetera = st.selectbox(
            "Billetera",
            list(db["billeteras"].keys())
        )

        guardar = st.form_submit_button("Guardar gasto")

        if guardar:

            try:

                monto = evaluar(monto_texto)

                gasto = {
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "descripcion": descripcion,
                    "monto": float(monto),
                    "categoria": categoria,
                    "billetera": billetera
                }

                db["historial"].append(gasto)

                db["billeteras"][billetera] -= float(monto)

                guardar_db(db)

                st.success("Gasto guardado correctamente")

            except Exception as e:

                st.error(f"Error: {e}")

    # =====================================================
    # RECURRENTES
    # =====================================================

    st.subheader("🔁 Gastos recurrentes")

    with st.expander("Añadir recurrente"):

        with st.form("recurrente_form"):

            r_desc = st.text_input("Descripción recurrente")
            r_monto = st.number_input("Monto recurrente", min_value=0.0)

            r_categoria = st.selectbox(
                "Categoría recurrente",
                categorias
            )

            r_wallet = st.selectbox(
                "Billetera recurrente",
                list(db["billeteras"].keys())
            )

            guardar_recurrente = st.form_submit_button("Guardar recurrente")

            if guardar_recurrente:

                db["recurrentes"].append({
                    "descripcion": r_desc,
                    "monto": r_monto,
                    "categoria": r_categoria,
                    "billetera": r_wallet
                })

                guardar_db(db)

                st.success("Recurrente guardado")

    for i, rec in enumerate(db["recurrentes"]):

        col1, col2 = st.columns([4,1])

        with col1:
            st.write(f"**{rec['descripcion']}** - ${rec['monto']:,.0f}")

        with col2:

            if st.button("Aplicar", key=f"rec_{i}"):

                db["historial"].append({
                    "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "descripcion": rec["descripcion"],
                    "monto": rec["monto"],
                    "categoria": rec["categoria"],
                    "billetera": rec["billetera"]
                })

                db["billeteras"][rec["billetera"]] -= rec["monto"]

                guardar_db(db)

                st.success("Recurrente aplicado")

# =========================================================
# ORGANIZACIÓN
# =========================================================

elif pagina == "📊 Organización":

    st.subheader("📊 Organización y control")

    # =====================================================
    # BILLETERAS
    # =====================================================

    st.markdown("## 💼 Gestión de billeteras")

    with st.form("wallet_form"):

        cols = st.columns(len(db["billeteras"]))

        nuevos_saldos = {}

        for i, (wallet, saldo) in enumerate(db["billeteras"].items()):

            with cols[i]:

                nuevos_saldos[wallet] = st.number_input(
                    wallet,
                    value=float(saldo)
                )

        save_wallets = st.form_submit_button("Guardar saldos")

        if save_wallets:

            db["billeteras"] = nuevos_saldos

            guardar_db(db)

            st.success("Billeteras actualizadas")

    # =====================================================
    # CATEGORÍAS
    # =====================================================

    st.markdown("## 🏷️ Categorías")

    with st.form("cat_form"):

        nombre_cat = st.text_input("Nombre")
        icono_cat = st.text_input("Ícono")

        guardar_cat = st.form_submit_button("Guardar categoría")

        if guardar_cat:

            db["categorias"].append({
                "nombre": nombre_cat,
                "icono": icono_cat
            })

            guardar_db(db)

            st.success("Categoría agregada")

    # =====================================================
    # PRESUPUESTOS
    # =====================================================

    st.markdown("## 🎯 Presupuestos")

    for cat in db["categorias"]:

        nombre = cat["nombre"]

        if nombre not in db["presupuestos"]:
            db["presupuestos"][nombre] = 0

        presupuesto = st.number_input(
            f"Presupuesto {nombre}",
            value=float(db["presupuestos"][nombre]),
            key=f"pres_{nombre}"
        )

        db["presupuestos"][nombre] = presupuesto

        total = sum(
            x["monto"]
            for x in db["historial"]
            if nombre in x["categoria"]
        )

        progreso = 0

        if presupuesto > 0:
            progreso = min(total / presupuesto, 1.0)

        st.progress(progreso)

        st.caption(
            f"${total:,.0f} / ${presupuesto:,.0f}"
        )

    guardar_db(db)

    # =====================================================
    # TABLA
    # =====================================================

    st.markdown("## 🧾 Tabla de gastos")

    vista = st.radio(
        "Vista",
        ["Mensual", "Quincenal"],
        horizontal=True
    )

    if db["historial"]:

        df = pd.DataFrame(db["historial"])

        st.data_editor(
            df,
            use_container_width=True,
            num_rows="dynamic"
        )

    else:
        st.info("No hay registros todavía")

# =========================================================
# ANÁLISIS
# =========================================================

elif pagina == "📈 Análisis":

    st.subheader("📈 Análisis financiero")

    if db["historial"]:

        df = pd.DataFrame(db["historial"])

        # =====================================================
        # GRÁFICO
        # =====================================================

        fig = px.pie(
            df,
            names="categoria",
            values="monto",
            title="Distribución de gastos"
        )

        st.plotly_chart(fig, use_container_width=True)

        # =====================================================
        # EXPORTAR
        # =====================================================

        st.markdown("## 📤 Exportar datos")

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Descargar CSV",
            csv,
            file_name="mis_finanzas.csv",
            mime="text/csv"
        )

        excel_name = "mis_finanzas.xlsx"

        with pd.ExcelWriter(excel_name, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)

        with open(excel_name, "rb") as f:

            st.download_button(
                "Descargar Excel",
                f,
                file_name="mis_finanzas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    else:
        st.info("No hay información para analizar")

# =========================================================
# HISTÓRICO
# =========================================================

elif pagina == "🗂️ Histórico":

    st.subheader("🗂️ Meses archivados")

    if db["historico_meses"]:

        mes = st.selectbox(
            "Selecciona un mes",
            list(db["historico_meses"].keys())
        )

        datos = db["historico_meses"][mes]

        df = pd.DataFrame(datos)

        st.dataframe(df, use_container_width=True)

    else:
        st.info("No hay cierres guardados")

# =========================================================
# CONFIGURACIÓN
# =========================================================

elif pagina == "⚙️ Configuración":

    st.subheader("⚙️ Configuración")

    # =====================================================
    # CAMBIAR PIN
    # =====================================================

    st.markdown("## 🔐 Cambiar PIN")

    with st.form("pin_form"):

        nuevo_pin = st.text_input("Nuevo PIN", type="password")

        save_pin = st.form_submit_button("Guardar PIN")

        if save_pin:

            db["pin"] = nuevo_pin

            guardar_db(db)

            st.success("PIN actualizado")

    # =====================================================
    # CIERRE DE MES
    # =====================================================

    st.markdown("## 📦 Cierre de Mes")

    st.warning(
        "Esta acción archivará el historial y reiniciará el mes."
    )

    if st.button("Ejecutar cierre de mes"):

        try:

            nombre_mes = datetime.now().strftime("%Y-%m")

            db["historico_meses"][nombre_mes] = db["historial"]

            db["historial"] = []

            guardar_db(db)

            st.success("Cierre realizado correctamente")

        except Exception as e:

            st.error(f"Error: {e}")

    # =====================================================
    # BORRAR DATOS
    # =====================================================

    st.markdown("## 🗑️ Borrar todos los datos")

    confirmar = st.checkbox(
        "Confirmo que deseo eliminar toda la información"
    )

    if confirmar:

        if st.button("Borrar datos"):

            try:

                os.remove(DB_FILE)

                st.success("Datos eliminados")

                st.session_state.clear()

                st.rerun()

            except Exception as e:

                st.error(f"Error: {e}")

# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        Creado por Alexander Polanco
    </div>
    """,
    unsafe_allow_html=True
)