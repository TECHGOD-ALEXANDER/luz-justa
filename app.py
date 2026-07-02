
import streamlit as st
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

PRECIO_KWH=0.6134
CARGO_FIJO=2.27
MANTENIMIENTO=1.74
ALUMBRADO=33.04
INTERES=3.36
IGV_RATE=0.18
ELECTRIFICACION=6.92
INTERES_EXTRA=0.35

st.set_page_config(page_title="Luz Justa",page_icon="⚡",layout="centered")

st.markdown('''
<style>
.block-container{max-width:900px;}
.piso-header{background:linear-gradient(90deg,#2563EB,#3B82F6);color:white;padding:14px;border-radius:14px;font-size:22px;font-weight:bold;text-align:center;margin-bottom:10px;}
.total-box{background:#FEF3C7;border:2px solid #F59E0B;border-radius:14px;padding:12px;text-align:center;color:#B45309;font-size:28px;font-weight:bold;}
.techgod{text-align:center;color:#9CA3AF;margin-top:40px;font-style:italic;}
</style>
''', unsafe_allow_html=True)

def crear_pdf(piso,detalle):
    b=BytesIO()
    d=SimpleDocTemplate(b)
    data=[["Concepto","Monto (S/)"]]
    for k,v in detalle.items():
        data.append([k,f"{v:.2f}"])
    t=Table(data,colWidths=[260,120])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#2563EB")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.lightgrey),
    ]))
    d.build([t])
    pdf=b.getvalue()
    b.close()
    return pdf

st.title("⚡ Luz Justa")
st.caption("Ingresa únicamente los kWh consumidos por cada piso.")
st.divider()

pisos=[]
for i in range(4):
    pisos.append(st.number_input(f"🏠 Piso {i+1}",min_value=0.0,step=0.1,key=i))

if st.button("⚡ CALCULAR PAGOS",use_container_width=True):
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
        igv=subtotal*IGV_RATE
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

        a,b=st.columns([4,1])
        with a:
            with st.container(border=True):
                st.markdown(f'<div class="piso-header">🏠 Piso {i} • {kwh:.2f} kWh</div>',unsafe_allow_html=True)
                x,y=st.columns([3,1])
                for k,v in list(detalle.items())[:-1]:
                    x.write(k)
                    y.write(f"**S/ {v:.2f}**")
                st.markdown(f'<div class="total-box">💰 S/ {total:.2f}</div>',unsafe_allow_html=True)
        with b:
            st.download_button("📄 Descargar",crear_pdf(i,detalle),file_name=f"recibo_piso_{i}.pdf",mime="application/pdf",use_container_width=True)

st.markdown('<div class="techgod">Powered by - TECHGOD</div>',unsafe_allow_html=True)
