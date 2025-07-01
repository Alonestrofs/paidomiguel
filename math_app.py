import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import (symbols, diff, integrate, series, parse_expr, sin, cos, tan, 
                  exp, log, sqrt, latex, solve, summation, Eq, Symbol, lambdify)
from sympy.parsing.sympy_parser import parse_expr

# Configuração da página
st.set_page_config(
    page_title="Calculadora Avançada Pro",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #45a049;
}
.math-result {
    padding: 20px;
    background-color: #f0f2f6;
    border-radius: 5px;
    margin-top: 20px;
    font-family: monospace;
}
.header {
    color: #4CAF50;
    text-align: center;
}
.plot-container {
    margin-top: 30px;
}
.tab-content {
    padding: 20px 0;
}
</style>
""", unsafe_allow_html=True)

def plot_function(expr, var, x_range=(-10, 10), points=1000):
    """Gera o gráfico de uma função matemática"""
    x_vals = np.linspace(x_range[0], x_range[1], points)
    f = lambdify(var, expr, 'numpy')
    y_vals = f(x_vals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label=f'${latex(expr)}$', color='blue')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.legend()
    ax.set_xlabel(f'${latex(var)}$')
    ax.set_ylabel(f'$f({latex(var)})$')
    ax.set_title(f'Gráfico de $f({latex(var)}) = {latex(expr)}$')
    
    st.pyplot(fig)

def basic_calculator():
    """Calculadora básica com operações aritméticas"""
    st.subheader("Calculadora Básica")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        num1 = st.number_input("Primeiro número:", value=0.0)
    
    with col2:
        operation = st.selectbox("Operação:", ["+", "-", "×", "÷", "^"])
    
    with col3:
        num2 = st.number_input("Segundo número:", value=0.0)
    
    if st.button("Calcular"):
        try:
            x, y = symbols('x y')
            expr = None
            if operation == "+":
                expr = x + y
                result = num1 + num2
            elif operation == "-":
                expr = x - y
                result = num1 - num2
            elif operation == "×":
                expr = x * y
                result = num1 * num2
            elif operation == "÷":
                expr = x / y
                result = num1 / num2 if num2 != 0 else None
            elif operation == "^":
                expr = x ** y
                result = num1 ** num2

            if result is None:
                st.error("Erro: divisão por zero")
            else:
                st.latex(f"{latex(expr.subs({x:num1, y:num2}))} = {latex(result)}")
        except Exception as e:
            st.error(f"Erro no cálculo: {str(e)}")

def polynomial_solver():
    """Resolvedor de equações polinomiais"""
    st.subheader("Resolvedor de Equações Polinomiais")
    
    equation = st.text_input(
        "Digite a equação polinomial (ex: x^2 - 4 = 0):",
        placeholder="x^2 - 4 = 0"
    )
    
    if st.button("Resolver Equação"):
        if not equation:
            st.error("Por favor, insira uma equação válida.")
        else:
            try:
                x = symbols('x')
                # Substitui ^ por ** para compatibilidade com sympy
                equation = equation.replace('^', '**')
                if '=' in equation:
                    lhs, rhs = equation.split('=')
                    expr = Eq(parse_expr(lhs), parse_expr(rhs))
                else:
                    expr = Eq(parse_expr(equation), 0)
                
                solutions = solve(expr, x)
                
                if not solutions:
                    st.info("A equação não tem soluções reais.")
                else:
                    st.markdown(f"""
                    <div class="math-result">
                        <b>Soluções da equação:</b><br><br>
                        {"<br>".join([f"${latex(x)} = {latex(sol)}$" for sol in solutions])}
                    </div>
                    """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Erro ao resolver a equação: {str(e)}")

def summation_calculator():
    """Calculadora de somatórios"""
    st.subheader("Calculadora de Somatórios")
    
    col_expr, col_var, col_limits = st.columns([2, 1, 2])
    
    with col_expr:
        sum_expr = st.text_input("Expressão do somatório:", placeholder="k^2")
    
    with col_var:
        sum_var = st.text_input("Variável do somatório:", value="k")
    
    with col_limits:
        lower = st.number_input("Limite inferior:", value=1, step=1)
        upper = st.number_input("Limite superior:", value=10, step=1)
    
    if st.button("Calcular Somatório"):
        if not sum_expr or not sum_var:
            st.error("Por favor, preencha todos os campos.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                sum_expr = sum_expr.replace('^', '**')
                var = symbols(sum_var)
                expr = parse_expr(sum_expr)
                result = summation(expr, (var, lower, upper))
                
                st.latex(
                    rf"\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)} = {latex(result)}"
                )
            except Exception as e:
                st.error(f"Erro no cálculo do somatório: {str(e)}")

def advanced_calculator():
    """Calculadora avançada com derivadas, integrais, séries, limites, integrais parciais e transformações"""
    st.subheader("Calculadora Avançada")
    
    func_str = st.text_input(
        "Digite sua função matemática:", 
        placeholder="Ex: x^2 + sin(x) - exp(x)",
        key="adv_func"
    )
    
    operation = st.selectbox(
        "Operação:",
        (
            "Derivada",
            "Integral Indefinida",
            "Integral Definida",
            "Integral Parcial",
            "Limite",
            "Série de Taylor",
            "Transformação"
        ),
        key="adv_operation"
    )
    
    x = symbols('x')
    y = symbols('y')
    
    if operation == "Derivada":
        order = st.number_input("Ordem da derivada:", min_value=1, value=1, step=1, key="deriv_order")
    elif operation == "Integral Definida":
        col_a, col_b = st.columns(2)
        with col_a:
            a = st.text_input("Limite inferior (a):", value="0", key="int_a")
        with col_b:
            b = st.text_input("Limite superior (b):", value="1", key="int_b")
    elif operation == "Série de Taylor":
        col_x0, col_n = st.columns(2)
        with col_x0:
            x0 = st.text_input("Ponto (x0):", value="0", key="taylor_x0")
        with col_n:
            n = st.number_input("Ordem (n):", min_value=1, value=4, step=1, key="taylor_n")
    
    if st.button("Calcular", key="adv_calc"):
        if not func_str:
            st.error("Por favor, insira uma função válida.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                func_str = func_str.replace('^', '**')
                expr = parse_expr(func_str)
                
                if operation == "Derivada":
                    result = diff(expr, x, order)
                    st.latex(
                        rf"\frac{{d^{order}}}{{dx^{order}}}\left({latex(expr)}\right) = {latex(result)}"
                    )
                
                elif operation == "Integral Indefinida":
                    result = integrate(expr, x)
                    st.latex(
                        rf"\int {latex(expr)}\,dx = {latex(result)} + C"
                    )
                
                elif operation == "Integral Definida":
                    a_expr = parse_expr(a.replace('^', '**'))
                    b_expr = parse_expr(b.replace('^', '**'))
                    result = integrate(expr, (x, a_expr, b_expr))
                    st.latex(
                        rf"\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} {latex(expr)}\,dx = {latex(result)}"
                    )
                
                elif operation == "Série de Taylor":
                    x0_expr = parse_expr(x0.replace('^', '**'))
                    result = series(expr, x, x0_expr, n).removeO()
                    st.latex(
                        rf"\text{{Série de Taylor de }} {latex(expr)} \text{{ em }} x={latex(x0_expr)} \text{{ até ordem }} {n}:"
                    )
                    st.latex(latex(result))
                
                # Opção para plotar a função
                if st.checkbox("Mostrar gráfico desta função"):
                    plot_function(expr, x)
            
            except Exception as e:
                st.error(f"Erro no cálculo: {str(e)}")

def graphing_calculator():
    """Calculadora gráfica"""
    st.subheader("Calculadora Gráfica")
    
    func_str = st.text_input(
        "Digite a função para plotar:",
        placeholder="Ex: sin(x)*exp(-x/10)",
        key="graph_func"
    )
    
    col_xmin, col_xmax, col_points = st.columns(3)
    
    with col_xmin:
        x_min = st.number_input("X mínimo:", value=-10.0, key="xmin")
    
    with col_xmax:
        x_max = st.number_input("X máximo:", value=10.0, key="xmax")
    
    with col_points:
        points = st.number_input("Pontos no gráfico:", min_value=100, value=1000, step=100, key="points")
    
    if st.button("Plotar Função", key="plot_func"):
        if not func_str:
            st.error("Por favor, insira uma função válida.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                func_str = func_str.replace('^', '**')
                x = symbols('x')
                expr = parse_expr(func_str)
                plot_function(expr, x, (x_min, x_max), points)
            except Exception as e:
                st.error(f"Erro ao plotar função: {str(e)}")

def main():
    st.markdown('<h1 class="header">🧮 CALCULADORA AVANÇADA PRO</h1>', unsafe_allow_html=True)
    
    # Menu de abas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Calculadora Básica", 
        "Equações Polinomiais", 
        "Somatórios", 
        "Cálculos Avançados", 
        "Calculadora Gráfica"
    ])
    
    with tab1:
        basic_calculator()
    
    with tab2:
        polynomial_solver()
    
    with tab3:
        summation_calculator()
    
    with tab4:
        advanced_calculator()
    
    with tab5:
        graphing_calculator()

if __name__ == "__main__":
    main()
