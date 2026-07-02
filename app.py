import streamlit as st
from io import BytesIO
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

PRECIO_KWH = 0.6134
CARGO_FIJO = 2.27
MANTENIMIENTO = 1.74
ALUMBRADO = 33.04
INTERES = 3.36
IGV = 0.18
ELECTRIFICACION = 6.92
INTERES_EXTRA = 0.35

st.set_page_config(page_title="Luz Justa", page_icon="⚡", layout="centered")

st.markdown("""
<style>
.block-container{max-width:760px;padding-top:1rem;}
.piso-header{
background:linear-gradient(90deg,#2563EB,#3B82F6);
color:white;padding:10px 14px;border-radius:12px;
font-weight:700;font-size:20px;text-align:center;margin-bottom:8px;}
.total-box{
background:#FEF3C7;border:1px solid #F59E0B;
border-radius:12px;padding:10px;text-align:center;
font-size:26px;font-weight:bold;color:#B45309;}
.footer{text-align:center;color:#9CA3AF;margin-top:30px;font-style:italic;}
.small{font-size:14px;}
</style>
""", unsafe_allow_html=True)


def pdf_bytes(piso, kwh, detalle):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf)
    styles = getSampleStyleSheet()
    items = [
        Paragraph("⚡ <b>LUZ JUSTA</b>", styles["Title"]),
        Paragraph(f"Recibo de Energía - Piso {piso}", styles["Heading2"]),
        Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Normal"]),
        Paragraph(f"Consumo registrado: {kwh:.2f} kWh", styles["Normal"]),
        Spacer(1,12)
    ]
    data=[["Concepto","Monto (S/)"]]
    for k,v in detalle.items():
        data.append([k,f"{v:.2f}"])
    t=Table(data,colWidths=[300,120])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,-1),(-1,-1),colors.HexColor("#FEF3C7")),
        ("FONTNAME",(0,-1),(-1,-1),"Helvetica-Bold")
    ]))
    items.append(t)
    items.append(Spacer(1,10))
    items.append(Paragraph("Powered by TECHGOD", styles["Normal"]))
    doc.build(items)
    out=buf.getvalue()
    buf.close()
    return out


st.title("⚡ Luz Justa")
st.caption("Ingresa únicamente los kWh consumidos por cada piso.")

pisos=[]
for i in range(4):
    pisos.append(st.number_input(f"🏠 Piso {i+1}", min_value=0.0, step=0.1, key=i))

if st.button("⚡ CALCULAR PAGOS", use_container_width=True):
    n=4
    fijo=CARGO_FIJO/n
    mant=MANTENIMIENTO/n
    alum=ALUMBRADO/n
    interes=INTERES/n
    rural=ELECTRIFICACION/n
    extra=INTERES_EXTRA/n

    for i,kwh in enumerate(pisos,1):
        if kwh<=0:
            continue

        consumo=kwh*PRECIO_KWH
        subtotal=consumo+fijo+mant+alum+interes
        igv=subtotal*IGV
        total=subtotal+igv+rural+extra

        detalle={
            "Costo de tu consumo":consumo,
            "Cargo fijo":fijo,
            "Mantenimiento":mant,
            "Alumbrado público":alum,
            "Interés compensatorio":interes,
            "IGV (18%)":igv,
            "Electrificación rural":rural,
            "Interés adicional":extra,
            "TOTAL A PAGAR":total
        }

        with st.container(border=True):
            st.markdown(
                f'<div class="piso-header">🏠 Piso {i} • {kwh:.2f} kWh</div>',
                unsafe_allow_html=True
            )

            for k,v in list(detalle.items())[:-1]:
                st.markdown(
                    f'<div class="small"><b>{k}</b> .......... S/ {v:.2f}</div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                f'<div class="total-box">💰 S/ {total:.2f}</div>',
                unsafe_allow_html=True
            )

            c1,c2,c3=st.columns([1,2,1])
            with c2:
                st.download_button(
                    "📄 Descargar PDF",
                    pdf_bytes(i,kwh,detalle),
                    file_name=f"recibo_piso_{i}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )

st.markdown('<div class="footer">Powered by - TECHGOD</div>', unsafe_allow_html=True)
