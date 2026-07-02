import streamlit as st

# =====================
# CONFIGURACIÓN
# =====================

PRECIO_KWH = 0.6134
CARGO_FIJO = 2.27
MANTENIMIENTO = 1.74
ALUMBRADO = 33.04
INTERES = 3.36
IGV = 0.18
ELECTRIFICACION = 6.92
INTERES_EXTRA = 0.35

st.set_page_config(
    page_title="Luz Justa",
    page_icon="⚡",
    layout="centered"
)

# =====================
# ESTILOS
# =====================

st.markdown("""
<style>

.block-container {
    max-width: 850px;
}

.card {
    background: #0F172A;
    border: 1px solid #1E293B;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 20px;
}

.piso-header {
    background: #2563EB;
    color: white;
    padding: 12px;
    border-radius: 12px;
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 15px;
}

.total-box {
    background: #FEF3C7;
    color: #B45309;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    font-size: 28px;
    font-weight: bold;
    margin-top: 15px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 60px;
}

</style>
""", unsafe_allow_html=True)

# =====================
# TÍTULO
# =====================

st.title("⚡ Luz Justa")
st.caption("Ingresa únicamente los kWh consumidos por cada piso.")

st.divider()

# =====================
# ENTRADAS
# =====================

pisos = []

for i in range(4):
    valor = st.number_input(
        f"🏠 Piso {i+1}",
        min_value=0.0,
        step=0.1,
        key=i
    )
    pisos.append(valor)

# =====================
# CÁLCULO
# =====================

if st.button("⚡ CALCULAR PAGOS", use_container_width=True):

    n = 4

    fijo = CARGO_FIJO / n
    mant = MANTENIMIENTO / n
    alum = ALUMBRADO / n
    interes = INTERES / n
    rural = ELECTRIFICACION / n
    extra = INTERES_EXTRA / n

    st.divider()

    for i, kwh in enumerate(pisos, start=1):

        if kwh <= 0:
            continue

        consumo = kwh * PRECIO_KWH
        subtotal = consumo + fijo + mant + alum + interes
        igv = subtotal * IGV
        total = subtotal + igv + rural + extra

        st.markdown(
            f"""
            <div class="card">

                <div class="piso-header">
                    🏠 Piso {i} • {kwh:.2f} kWh
                </div>

                <b>Costo de tu consumo:</b> S/ {consumo:.2f}<br><br>

                <b>Cargo fijo:</b> S/ {fijo:.2f}<br><br>

                <b>Mantenimiento:</b> S/ {mant:.2f}<br><br>

                <b>Alumbrado público:</b> S/ {alum:.2f}<br><br>

                <b>Interés compensatorio:</b> S/ {interes:.2f}<br><br>

                <b>IGV (18%):</b> S/ {igv:.2f}<br><br>

                <b>Electrificación rural:</b> S/ {rural:.2f}<br><br>

                <b>Interés adicional:</b> S/ {extra:.2f}

                <div class="total-box">
                    💰 Total: S/ {total:.2f}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.download_button(
            label=f"📄 Descargar recibo Piso {i}",
            data=f'''
LUZ JUSTA

Piso {i}
Consumo: {kwh:.2f} kWh

Costo de tu consumo: S/ {consumo:.2f}
Cargo fijo: S/ {fijo:.2f}
Mantenimiento: S/ {mant:.2f}
Alumbrado público: S/ {alum:.2f}
Interés compensatorio: S/ {interes:.2f}
IGV: S/ {igv:.2f}
Electrificación rural: S/ {rural:.2f}
Interés adicional: S/ {extra:.2f}

TOTAL: S/ {total:.2f}

Powered by TECHGOD
''',
            file_name=f"recibo_piso_{i}.txt",
            use_container_width=True
        )

        st.write("")

st.markdown(
    """
    <div class="footer">
        Powered by - TECHGOD
    </div>
    """,
    unsafe_allow_html=True
)
