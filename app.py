import streamlit as st

# ==========================
# CONFIGURACIÓN
# ==========================

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

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.block-container{
    max-width:850px;
}

footer{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# CABECERA
# ==========================

st.title("⚡ Luz Justa")

st.caption(
    "Calcula cuánto debe pagar cada inquilino ingresando únicamente los kWh consumidos."
)

st.divider()

# ==========================
# ENTRADAS
# ==========================

pisos = []

for i in range(4):

    valor = st.number_input(
        f"🏠 Piso {i+1}",
        min_value=0.0,
        step=0.1,
        key=i
    )

    pisos.append(valor)

# ==========================
# BOTÓN
# ==========================

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

        with st.container(border=True):

            st.subheader(f"🏠 Piso {i} • {kwh:.2f} kWh")

            col1, col2 = st.columns([3, 1])

            with col1:

                st.write(f"**Costo de tu consumo:** S/ {consumo:.2f}")
                st.write(f"**Cargo fijo:** S/ {fijo:.2f}")
                st.write(f"**Mantenimiento:** S/ {mant:.2f}")
                st.write(f"**Alumbrado público:** S/ {alum:.2f}")
                st.write(f"**Interés compensatorio:** S/ {interes:.2f}")
                st.write(f"**IGV (18%):** S/ {igv:.2f}")
                st.write(f"**Electrificación rural:** S/ {rural:.2f}")
                st.write(f"**Interés adicional:** S/ {extra:.2f}")

            with col2:

                recibo = f"""
LUZ JUSTA

Piso {i}
Consumo: {kwh:.2f} kWh

Costo de tu consumo: S/ {consumo:.2f}
Cargo fijo: S/ {fijo:.2f}
Mantenimiento: S/ {mant:.2f}
Alumbrado público: S/ {alum:.2f}
Interés compensatorio: S/ {interes:.2f}
IGV (18%): S/ {igv:.2f}
Electrificación rural: S/ {rural:.2f}
Interés adicional: S/ {extra:.2f}

TOTAL: S/ {total:.2f}

Powered by TECHGOD
"""

                st.download_button(
                    "📄 Descargar",
                    recibo,
                    file_name=f"recibo_piso_{i}.txt",
                    use_container_width=True
                )

            st.metric(
                "💰 Total a pagar",
                f"S/ {total:.2f}"
            )

            st.write("")

st.divider()

st.caption("Powered by - TECHGOD")
