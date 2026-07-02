import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# =====================
# CONFIGURACIÓN BASE
# =====================

PRECIO_KWH = 0.6134
CARGO_FIJO = 2.27
MANTENIMIENTO = 1.74
ALUMBRADO = 33.04
INTERES = 3.36
IGV = 0.18
ELECTRIFICACION = 6.92
INTERES_EXTRA = 0.35

# =====================
# CONFIGURACIÓN STREAMLIT
# =====================

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

.block-container{
    max-width:900px;
    padding-top:2rem;
}

.card{
    background:#111827;
    border-radius:20px;
    padding:18px;
    border:1px solid #374151;
    margin-bottom:20px;
}

.total-box{
    background:#FEF3C7;
    padding:15px;
    border-radius:14px;
    text-align:center;
    color:#B45309;
    font-size:28px;
    font-weight:bold;
    margin-top:15px;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:60px;
}

</style>
""", unsafe_allow_html=True)

# =====================
# PDF
# =====================

def generar_pdf(piso, detalle):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    estilos = getSampleStyleSheet()

    elementos = []

    elementos.append(
        Paragraph("⚡ <b>LUZ JUSTA</b>", estilos["Title"])
    )

    elementos.append(
        Paragraph(f"Recibo Piso {piso}", estilos["Normal"])
    )

    elementos.append(Spacer(1,20))

    data = [["Concepto","Monto (S/)"]]

    for k,v in detalle.items():
        data.append([k,f"{v:.2f}"])

    tabla = Table(data, colWidths=[280,120])

    tabla.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.lightgrey),
        ("BACKGROUND",(0,1),(-1,-2),colors.whitesmoke),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#DCFCE7")),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold"),
    ]))

    elementos.append(tabla)

    doc.build(elementos)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf


# =====================
# INTERFAZ
# =====================

st.title("⚡ Luz Justa")

st.caption(
    "Ingresa únicamente los kWh consumidos por cada piso."
)

st.divider()

pisos = []

for i in range(4):

    valor = st.number_input(
        f"🏠 Piso {i+1}",
        min_value=0.0,
        step=0.1,
        key=i
    )

    pisos.append(valor)

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

        detalle = {
            "Costo de tu consumo": consumo,
            "Cargo fijo": fijo,
            "Mantenimiento": mant,
            "Alumbrado público": alum,
            "Interés compensatorio": interes,
            "IGV (18%)": igv,
            "Electrificación rural": rural,
            "Interés adicional": extra,
            "TOTAL A PAGAR": total
        }

        col1, col2 = st.columns([4,1])

        with col1:

            st.markdown(
                f"""
                <div class="card">

                    <div style="
                        background:#2563EB;
                        color:white;
                        padding:14px;
                        border-radius:14px;
                        font-size:22px;
                        font-weight:bold;
                        margin-bottom:20px;
                    ">
                        🏠 Piso {i} • {kwh:.2f} kWh
                    </div>

                """,
                unsafe_allow_html=True
            )

            for k, v in list(detalle.items())[:-1]:

                st.write(f"**{k}:** S/ {v:.2f}")

            st.markdown(
                f"""
                <div class="total-box">
                    💰 Total: S/ {total:.2f}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            pdf = generar_pdf(i, detalle)

            st.download_button(
                "📄 Descargar",
                pdf,
                file_name=f"recibo_piso_{i}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

st.markdown(
    """
    <div class="footer">
        Powered by - TECHGOD
    </div>
    """,
    unsafe_allow_html=True
)
