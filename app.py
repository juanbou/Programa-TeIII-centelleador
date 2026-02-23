import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- INTERFAZ DE STREAMLIT (Configuración inicial) ---
st.set_page_config(page_title="Calibración Centelleador", layout="wide")
st.title("🔬 Conversor Canal ➔ Energía")

# --- APARTADO DE AJUSTES EN LA BARRA LATERAL ---
st.sidebar.header("⚙️ Parámetros de Calibración")
st.sidebar.markdown("Edita los coeficientes del ajuste $E = ax^2 + bx + c$")

# Usamos los valores originales como 'value' (por defecto)
# El formato 'format="%.3e"' es útil para notación científica
# --- EN LA BARRA LATERAL ---
col_a, col_da = st.sidebar.columns(2)
with col_a:
    A = st.number_input("Coeficiente a (e-4)", value=6.023e-04, format="%.3e", step=1e-5, key="input_a")
with col_da:
    DA = st.number_input("Δa (e-5)", value=2.488e-5, format="%.3e", step=1e-6, key="input_da")

col_b, col_db = st.sidebar.columns(2)
with col_b:
    B = st.number_input("Coeficiente b (e0)", value=1.446, format="%.3f", step=0.01, key="input_b")
with col_db:
    DB = st.number_input("Δb (e-2)", value=1.815e-2, format="%.3e", step=1e-3, key="input_db")

col_c, col_dc = st.sidebar.columns(2)
with col_c:
    C = st.number_input("Coeficiente c (e0)", value=4.235, format="%.3f", step=0.1, key="input_c")
with col_dc:
    DC = st.number_input("Δc (e0)", value=2.095, format="%.3f", step=0.1, key="input_dc")
# --- LÓGICA DE CÁLCULO ---
def calculate_energy_and_error(x, dx, a, da, b, db, c, dc):
    energy = a*(x**2) + b*x + c
    error = (x**2 * da) + (x * db) + dc + abs(2*a*x + b) * dx
    return energy, error

# --- ENTRADAS DEL USUARIO ---
col1, col2 = st.columns(2)
with col1:
    # He añadido un key también aquí por seguridad
    x_input = st.number_input("Canal medido (x):", min_value=0.0, value=500.0, step=1.0, key="main_x")
with col2:
    dx_input = st.number_input("Error del canal (Δx):", min_value=0.0, value=2.0, step=0.1, key="main_dx")
# Cálculos pasando las variables obtenidas de los inputs
energy_val, error_val = calculate_energy_and_error(x_input, dx_input, A, DA, B, DB, C, DC)


# --- INTERFAZ DE STREAMLIT ---


st.sidebar.header("Parámetros de Calibración")
st.sidebar.latex(r"E = ax^2 + bx + c")
st.sidebar.info(f"a: {A} ± {DA}\nb: {B} ± {DB}\nc: {C} ± {DC}")


# Cálculos
energy_val, error_val = calculate_energy_and_error(
    x_input, dx_input, A, DA, B, DB, C, DC
)
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