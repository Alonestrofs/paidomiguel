import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import (symbols, diff, integrate, series, parse_expr, sin, cos, tan, 
                  exp, log, sqrt, latex, solve, summation, Eq, Symbol, lambdify, 
                  limit, laplace_transform, inverse_laplace_transform, apart, together, simplify, expand, pretty, Add, Mul)
from sympy.parsing.sympy_parser import parse_expr
import streamlit.components.v1 as components

def render_katex(latex_str, height=80):
    """Renderiza uma string LaTeX usando KaTeX via HTML"""
    html = f"""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.0/dist/contrib/auto-render.min.js"
        onload="renderMathInElement(document.body, {{
            delimiters: [
                {{left: '$$', right: '$$', display: true}},
                {{left: '$', right: '$', display: false}}
            ]
        }});"></script>
    <div style="font-size: 20px;">{latex_str}</div>
    """
    components.html(html, height=height)

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
    padding: 20px 0;finalsimplificado:0
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
    """Calculadora avançada com passo a passo, separada em abas"""
    st.subheader("Cálculos Avançados - Passo a Passo")

    tabs = st.tabs([
        "Derivada", 
        "Integral", 
        "Limite", 
        "Série de Taylor", 
        "Transformação"
    ])

# Tab: Derivada
    with tabs[0]:
        func_str = st.text_input("Função para derivar:", placeholder="Ex: x^2 + sin(x)", key="deriv_func")
        order = st.number_input("Ordem da derivada:", min_value=1, value=1, step=1, key="deriv_order")
        if st.button("Calcular derivada", key="deriv_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^', '**'))
                    x = symbols('x')
                    steps = [f"Função original: f(x) = {latex(expr)}"]

                    if isinstance(expr, Add):
                        steps.append(r"Aplicar a regra da soma: (f+g)' = f' + g'")
                        for arg in expr.args:
                            d = diff(arg, x, order)
                            steps.append(rf"\frac{{d^{order}}}{{dx^{order}}}({latex(arg)}) = {latex(d)}")
                    elif isinstance(expr, Mul):
                        steps.append(r"Aplicar a regra do produto: (uv)' = u'v + uv'")
                        u, v = expr.args
                        du = diff(u, x, order)
                        dv = diff(v, x, order)
                        steps.append(rf"u = {latex(u)}, \ u' = {latex(du)}")
                        steps.append(rf"v = {latex(v)}, \ v' = {latex(dv)}")
                        deriv = du*v + u*dv
                        steps.append(rf"Resultado: u'v + uv' = {latex(deriv)}")
                    else:
                        deriv = diff(expr, x, order)
                        steps.append(rf"Derivando diretamente: $$f^{{({order})}}(x) = {latex(deriv)}$$")

                    steps.append(rf"Resultado final simplificado: $${latex(simplify(deriv))}$$")

                    # Renderizar todos os passos com KaTeX
                    for s in steps:
                        render_katex(s, height=60)

                except Exception as e:
                    st.error(f"Erro no cálculo: {str(e)}")

    # Tab: Integral
    with tabs[1]:
        func_str = st.text_input("Função para integrar:", placeholder="Ex: x^2 + sin(x)", key="int_func")
        int_type = st.radio("Tipo de integral:", ["Indefinida", "Definida"], key="int_type")
        if int_type == "Definida":
            a = st.text_input("Limite inferior (a):", value="0", key="int_a")
            b = st.text_input("Limite superior (b):", value="1", key="int_b")
        if st.button("Calcular integral", key="int_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^', '**'))
                    x = Symbol('x')
                    steps = [f"Função original: $f(x) = {latex(expr)}$"]
                    if isinstance(expr, Add):
                        steps.append("Aplicar a linearidade: $\\int(f+g)dx = \\int f dx + \\int g dx$")
                        parts = []
                        for arg in expr.args:
                            integ = integrate(arg, x)
                            parts.append(f"$\\int {latex(arg)} dx = {latex(integ)}$")
                        steps += parts
                        total = integrate(expr, x)
                        steps.append(f"Somando: ${latex(total)}$")
                        steps.append(f"Resultado final: ${latex(total)} + C$")
                    else:
                        intg = integrate(expr, x)
                        steps.append(f"Primitiva: ${latex(intg)}$")
                        steps.append(f"Resultado final: ${latex(intg)} + C$")
                    if int_type == "Definida":
                        a_expr = parse_expr(a.replace('^', '**'))
                        b_expr = parse_expr(b.replace('^', '**'))
                        Fa = intg.subs(x, a_expr)
                        Fb = intg.subs(x, b_expr)
                        result = Fb - Fa
                        steps.append(f"Avaliar: $F({latex(b_expr)}) - F({latex(a_expr)}) = {latex(Fb)} - {latex(Fa)} = {latex(result)}$")
                    for s in steps:
                        st.latex(s)
                except Exception as e:
                    st.error(f"Erro no cálculo: {str(e)}")

    # Tab: Limite
    with tabs[2]:
        func_str = st.text_input("Função para limite:", placeholder="Ex: sin(x)/x", key="lim_func")
        point = st.text_input("Ponto de aproximação:", value="0", key="lim_point")
        direction = st.selectbox("Direção:", ["ambos", "+", "-"], key="lim_dir")
        if st.button("Calcular limite", key="lim_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^', '**'))
                    x = Symbol('x')
                    point_expr = parse_expr(point.replace('^', '**'))
                    dir_map = {"ambos": None, "+": "+", "-": "-"}
                    result = limit(expr, x, point_expr, dir_map[direction])
                    steps = [
                        f"Função original: $f(x) = {latex(expr)}$",
                        f"Calcular: $\\lim_{{x \\to {latex(point_expr)}{direction}}} f(x)$",
                        f"Resultado: ${latex(result)}$"
                    ]
                    for s in steps:
                        st.latex(s)
                except Exception as e:
                    st.error(f"Erro no cálculo: {str(e)}")

    # Tab: Série de Taylor
    with tabs[3]:
        func_str = st.text_input("Função:", placeholder="Ex: exp(x)", key="taylor_func")
        x0 = st.text_input("Ponto (x0):", value="0", key="taylor_x0")
        n = st.number_input("Ordem (n):", min_value=1, value=4, step=1, key="taylor_n")
        if st.button("Calcular série", key="taylor_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^','**'))
                    x0_expr = parse_expr(x0.replace('^','**'))
                    result = series(expr, Symbol('x'), x0_expr, n).removeO()
                    steps = [
                        f"Função original: $f(x) = {latex(expr)}$",
                        f"Série de Taylor até ordem {n} em $x_0={latex(x0_expr)}$:",
                        f"${latex(result)}$"
                    ]
                    for s in steps:
                        st.latex(s)
                except Exception as e:
                    st.error(f"Erro no cálculo: {str(e)}")

    # Tab: Transformação
    with tabs[4]:
        func_str = st.text_input("Função:", placeholder="Ex: exp(-2*x)", key="transf_func")
        transf_type = st.selectbox("Tipo de transformação:", ["Laplace", "Inversa de Laplace"], key="transf_type")
        if st.button("Calcular transformação", key="transf_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^','**'))
                    s = Symbol('s')
                    x = Symbol('x')
                    if transf_type == "Laplace":
                        lap = laplace_transform(expr, x, s, noconds=True)
                        st.latex(f"Transformada de Laplace: $\\mathcal{{L}}[{latex(expr)}] = {latex(lap)}$")
                    else:
                        inv = inverse_laplace_transform(expr, s, x)
                        st.latex(f"Inversa: $\\mathcal{{L}}^{{-1}}[{latex(expr)}] = {latex(inv)}$")
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
