import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN DE LA CALIBRACIÓN ---
# Introduce aquí los valores obtenidos de tu ajuste
A, DA = 6.023e-04, 2.488e-5  # a y Delta a
B, DB = 1.446, 1.815e-2          # b y Delta b
C, DC = 4.235, 2.095          # c y Delta c

def calculate_energy_and_error(x, dx):
    # E = ax^2 + bx + c
    energy = A*(x**2) + B*x + C
    
    # Según tu fórmula: Delta E = x^2*Da + x*Db + Dc + (2ax + b)*Dx
    # He añadido abs() para asegurar que el error siempre sume, 
    # incluso con coeficientes negativos.
    error = (x**2 * DA) + (x * DB) + DC + abs(2*A*x + B) * dx
    
    return energy, error

# --- INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Calibración Centelleador", layout="wide")
st.title("🔬 Conversor Canal ➔ Energía")

st.sidebar.header("Parámetros de Calibración")
st.sidebar.latex(r"E = ax^2 + bx + c")
st.sidebar.info(f"a: {A} ± {DA}\nb: {B} ± {DB}\nc: {C} ± {DC}")

# Entradas del usuario
col1, col2 = st.columns(2)
with col1:
    x_input = st.number_input("Canal medido (x):", min_value=0.0, value=500.0, step=1.0)
with col2:
    dx_input = st.number_input("Error del canal (Δx):", min_value=0.0, value=2.0, step=0.1)

# Cálculos
energy_val, error_val = calculate_energy_and_error(x_input, dx_input)

# Visualización de resultados
st.markdown("---")
st.metric(label="Energía Resultante (E)", value=f"{energy_val:.3f}", delta=f"± {error_val:.3f}")

# --- GRÁFICA ---
x_range = np.linspace(max(0, x_input - 200), x_input + 200, 500)
y_range = A*x_range**2 + B*x_range + C

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x_range, y_range, label="Curva de calibración", color='black', alpha=0.7)

# Punto con barras de error en ambos ejes
ax.errorbar(x_input, energy_val, 
            xerr=dx_input, yerr=error_val, 
            fmt='o', color='red', ecolor='red', capsize=5,
            label=f"Medida: {energy_val:.2f} ± {error_val:.2f}")

ax.set_xlabel("Canal (ADC)")
ax.set_ylabel("Energía (keV)")
ax.set_title("Punto de medida en la curva de calibración")
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend()

st.pyplot(fig)

# Explicación de la fórmula aplicada
with st.expander("Ver detalle del cálculo de error"):
    st.latex(r"\Delta E = x^2 \cdot \Delta a + x \cdot \Delta b + \Delta c + |2ax + b| \cdot \Delta x")
    st.write(f"Sustituyendo:")
    st.write(f"- Término $a$: {x_input**2 * DA:.4f}")
    st.write(f"- Término $b$: {x_input * DB:.4f}")
    st.write(f"- Término $c$: {DC:.4f}")
    st.write(f"- Término $x$: {abs(2*A*x_input + B) * dx_input:.4f}")