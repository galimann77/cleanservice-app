import streamlit as st
from services.calculation import CalculationService

def show_express_calculator():
    st.title("⚡ Express-Kalkulation")
    st.caption("Schnelle Preisindikation in 30 Sekunden")
    
    col1, col2 = st.columns(2)
    area = col1.number_input("Fläche (m²)", min_value=10, max_value=50000, value=500)
    service = col2.selectbox("Reinigungsart", [
        "Büroreinigung", "Baureinigung (Grob)", "Baureinigung (Fein)",
        "Grundreinigung", "Glasreinigung", "Sanitärreinigung",
        "Pflaster-/Verkehrsflächenreinigung", "Steinreinigung/Naturstein"
    ])
    
    if st.button("🚀 Sofort-Kalkulation", type="primary"):
        # Direct instantiation as per prompt, ignoring cache for simplicity in this view or use cached helper
        # Prompt uses: calc = CalculationService()
        calc = CalculationService()
        result = calc.calc_express(area, service)
        
        st.divider()
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Minimum", f"{result['min']:,.2f} €")
        col_b.metric("Mittelwert", f"{result['center']:,.2f} €", delta="±15%")
        col_c.metric("Maximum", f"{result['max']:,.2f} €")
        
        st.info("⚡ Schnellschätzung - für genaue Kalkulation Raumbuch nutzen")
