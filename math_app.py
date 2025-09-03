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
                {{left: '$', right: '$', display: true}},
                {{left: '

def render_katex_steps(steps_list, title=""):
    """Renderiza uma lista de passos matemáticos usando KaTeX"""
    if title:
        st.markdown(f"**{title}**")
    
    for step in steps_list:
        if step.startswith("$") and step.endswith("$"):
            render_katex(step, height=60)
        else:
            # Para texto normal, ainda usar KaTeX se contém fórmulas
            if "$" in step:
                render_katex(step, height=60)
            else:
                st.markdown(step)

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
.step-container {
    margin: 10px 0;
    padding: 15px;
    background-color: #ffffff;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.katex-result {
    background-color: #ffffff !important;
    color: #1f1f1f !important;
    border: 2px solid #4CAF50 !important;
    border-radius: 8px !important;
    padding: 15px !important;
    margin: 10px 0 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}
</style>
""", unsafe_allow_html=True)

def plot_function(expr, var, x_range=(-10, 10), points=1000):
    """Gera o gráfico de uma função matemática"""
    x_vals = np.linspace(x_range[0], x_range[1], points)
    f = lambdify(var, expr, 'numpy')
    y_vals = f(x_vals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label=f'${latex(expr)}$', color='blue', linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(fontsize=12)
    ax.set_xlabel(f'${latex(var)}$', fontsize=14)
    ax.set_ylabel(f'$f({latex(var)})$', fontsize=14)
    ax.set_title(f'Gráfico de $f({latex(var)}) = {latex(expr)}$', fontsize=16)
    
    st.pyplot(fig)

def basic_calculator():
    """Calculadora básica com operações aritméticas usando KaTeX"""
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
            steps = []
            result = None
            
            if operation == "+":
                result = num1 + num2
                steps = [
                    "**Adição:**",
                    f"$${num1} + {num2} = {result}$$"
                ]
            elif operation == "-":
                result = num1 - num2
                steps = [
                    "**Subtração:**",
                    f"$${num1} - {num2} = {result}$$"
                ]
            elif operation == "×":
                result = num1 * num2
                steps = [
                    "**Multiplicação:**",
                    f"$${num1} \\times {num2} = {result}$$"
                ]
            elif operation == "÷":
                if num2 != 0:
                    result = num1 / num2
                    steps = [
                        "**Divisão:**",
                        f"$$\\frac{{{num1}}}{{{num2}}} = {result}$$"
                    ]
                else:
                    st.error("❌ **Erro:** Divisão por zero não é definida!")
                    return
            elif operation == "^":
                result = num1 ** num2
                steps = [
                    "**Potenciação:**",
                    f"$${num1}^{{{num2}}} = {result}$$"
                ]

            # Renderizar os passos usando KaTeX
            render_katex_steps(steps)
            
        except Exception as e:
            st.error(f"❌ **Erro no cálculo:** {str(e)}")

def polynomial_solver():
    """Resolvedor de equações polinomiais com KaTeX"""
    st.subheader("Resolvedor de Equações Polinomiais")
    
    equation = st.text_input(
        "Digite a equação polinomial (ex: x^2 - 4 = 0):",
        placeholder="x^2 - 4 = 0"
    )
    
    if st.button("Resolver Equação"):
        if not equation:
            st.error("❌ Por favor, insira uma equação válida.")
        else:
            try:
                x = symbols('x')
                # Substitui ^ por ** para compatibilidade com sympy
                equation_clean = equation.replace('^', '**')
                
                steps = []
                steps.append("**Resolução da Equação Polinomial:**")
                steps.append(f"$$\\text{{Equação original: }} {equation}$$")
                
                if '=' in equation_clean:
                    lhs, rhs = equation_clean.split('=')
                    expr = Eq(parse_expr(lhs), parse_expr(rhs))
                    steps.append(f"$$\\text{{Forma padrão: }} {latex(parse_expr(lhs))} = {latex(parse_expr(rhs))}$$")
                else:
                    expr = Eq(parse_expr(equation_clean), 0)
                    steps.append(f"$$\\text{{Assumindo: }} {latex(parse_expr(equation_clean))} = 0$$")
                
                solutions = solve(expr, x)
                
                if not solutions:
                    steps.append("$$\\text{A equação não possui soluções reais.}$$")
                else:
                    steps.append("**Soluções encontradas:**")
                    for i, sol in enumerate(solutions, 1):
                        steps.append(f"$$x_{i} = {latex(sol)}$$")
                        # Verificação da solução
                        if '=' in equation_clean:
                            lhs_val = parse_expr(lhs).subs(x, sol)
                            rhs_val = parse_expr(rhs).subs(x, sol)
                            steps.append(f"$$\\text{{Verificação: }} {latex(lhs_val)} = {latex(rhs_val)}$$")
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro ao resolver a equação:** {str(e)}")

def summation_calculator():
    """Calculadora de somatórios com KaTeX"""
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
            st.error("❌ Por favor, preencha todos os campos.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                sum_expr_clean = sum_expr.replace('^', '**')
                var = symbols(sum_var)
                expr = parse_expr(sum_expr_clean)
                result = summation(expr, (var, lower, upper))
                
                steps = []
                steps.append("**Cálculo do Somatório:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)}$$")
                
                # Mostrar alguns termos do somatório para visualização
                if upper - lower <= 10:
                    terms = []
                    for i in range(int(lower), int(upper) + 1):
                        term_value = expr.subs(var, i)
                        terms.append(f"{latex(term_value)}")
                    
                    steps.append("**Expandindo os termos:**")
                    steps.append(f"$${' + '.join(terms)}$$")
                
                steps.append("**Resultado:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)} = {latex(result)}$$")
                
                # Valor numérico se possível
                try:
                    numeric_result = float(result)
                    steps.append(f"$$\\approx {numeric_result:.6f}$$")
                except:
                    pass
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro no cálculo do somatório:** {str(e)}")

def advanced_calculator():
    st.header("Cálculos Avançados com Passo a Passo")
    tabs = st.tabs(["Derivada", "Integral", "Limite", "Série de Taylor", "Transformada de Laplace"])

    with tabs[0]: # Derivada
        func_str = st.text_input("Função para derivar f(x):", "x**3 * cos(x)", key="deriv_func")
        order = st.number_input("Ordem da derivada:", 1, 10, 1, key="deriv_order")
        if st.button("Calcular Derivada", key="deriv_calc"):
            try:
                x = symbols('x')
                expr = parse_expr(func_str.replace('^', '**'))
                steps = [f"Vamos calcular a derivada de ordem {order} da função:"]
                steps.append(f"$$f(x) = {latex(expr)}$$")
                
                current_expr = expr
                for i in range(1, order + 1):
                    deriv = diff(current_expr, x)
                    if isinstance(current_expr, Add):
                        steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Soma: $(u+v)' = u' + v'$.")
                        # O Sympy faz isso automaticamente.
                    elif isinstance(current_expr, Mul) and len(current_expr.args) == 2:
                        u, v = current_expr.args
                        du, dv = diff(u, x), diff(v, x)
                        steps.append(f"**{i}ª Derivada:** Aplicando a Regra do Produto: $(u \\cdot v)' = u' \\cdot v + u \\cdot v'$.")
                        steps.append(f"Onde $u = {latex(u)}$ e $v = {latex(v)}$.")
                        steps.append(f"As derivadas são $u' = {latex(du)}$ e $v' = {latex(dv)}$.")
                        steps.append("Substituindo na fórmula:")
                        steps.append(f"$$f^{{({i})}}(x) = ({latex(du)}) \\cdot ({latex(v)}) + ({latex(u)}) \\cdot ({latex(dv)})$$")
                    elif isinstance(current_expr, Pow):
                        base, exp_val = current_expr.args
                        if x in base.free_symbols and x not in exp_val.free_symbols:
                            steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Potência: $(u^n)' = n \\cdot u^{{n-1}} \\cdot u'$.")
                        elif x in exp_val.free_symbols:
                             steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Exponencial e/ou Cadeia.")
                    
                    simplified = simplify(deriv)
                    if order > 1:
                        steps.append(f"O resultado da {i}ª derivada é:")
                        steps.append(f"$$\\frac{{d^{i}}}{{dx^{i}}} f(x) = {latex(simplified)}$$")
                    current_expr = deriv

                final_deriv = diff(expr, x, order)
                final_simplified = simplify(final_deriv)
                
                steps.append("**Resultado Final:**")
                d_symbol = f"f^{{({order})}}(x)" if order > 1 else "f'(x)"
                steps.append(f"$${d_symbol} = {latex(final_deriv)}$$")

                if final_deriv != final_simplified:
                    steps.append("Após simplificação, obtemos:")
                    steps.append(f"$${d_symbol} = {latex(final_simplified)}$$")
                
                render_katex_steps(steps, "Cálculo da Derivada")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")

    with tabs[1]: # Integral
        func_str = st.text_input("Função para integrar f(x):", "x**2 + sin(x)", key="int_func")
        int_type = st.radio("Tipo de integral:", ["Indefinida", "Definida"], key="int_type", horizontal=True)
        a, b = "0", "1"
        if int_type == "Definida":
            col_a, col_b = st.columns(2)
            a = col_a.text_input("Limite inferior (a):", "0", key="int_a")
            b = col_b.text_input("Limite superior (b):", "1", key="int_b")
        
        if st.button("Calcular Integral", key="int_calc"):
            try:
                x = Symbol('x')
                expr = parse_expr(func_str.replace('^', '**'))
                
                steps = [f"Vamos calcular a integral da função:"]
                steps.append(f"$$f(x) = {latex(expr)}$$")

                if isinstance(expr, Add):
                    steps.append("Aplicando a Regra da Soma para integrais: $\\int (u+v) dx = \\int u dx + \\int v dx$.")
                    term_integrals = [f"$\\int {latex(arg)} dx = {latex(integrate(arg, x))}$" for arg in expr.args]
                    steps.append("<br>".join(term_integrals))


                primitive = integrate(expr, x)
                steps.append("A primitiva (integral indefinida) da função é:")
                steps.append(f"$$F(x) = \\int {latex(expr)} \\, dx = {latex(primitive)}$$")

                if int_type == "Indefinida":
                    steps.append("**Resultado Final (Integral Indefinida):**")
                    steps.append(f"$$\\int {latex(expr)} \\, dx = {latex(primitive)} + C$$")
                else:
                    a_expr, b_expr = parse_expr(a), parse_expr(b)
                    Fa = primitive.subs(x, a_expr)
                    Fb = primitive.subs(x, b_expr)
                    result = Fb - Fa
                    
                    steps.append("Para a integral definida, aplicamos o Teorema Fundamental do Cálculo:")
                    steps.append(f"$$\\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \\, dx = F({latex(b_expr)}) - F({latex(a_expr)})$$")
                    steps.append("Calculando os valores nos limites:")
                    steps.append(f"$$F({latex(b_expr)}) = {latex(Fb)}$$")
                    steps.append(f"$$F({latex(a_expr)}) = {latex(Fa)}$$")
                    steps.append("**Resultado Final (Integral Definida):**")
                    steps.append(f"$$\\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \\, dx = {latex(Fb)} - ({latex(Fa)}) = {latex(result)}$$")
                    if result.is_number:
                         steps.append(f"$$\\approx {result.evalf(6)}$$")

                render_katex_steps(steps, "Cálculo da Integral")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")

    with tabs[2]: # Limite
        func_str = st.text_input("Função para limite f(x):", "sin(x)/x", key="lim_func")
        point = st.text_input("Ponto de aproximação x₀:", "0", key="lim_point")
        direction = st.selectbox("Direção:", ["bilateral", "pela direita (+)", "pela esquerda (-)"], key="lim_dir")
        
        if st.button("Calcular Limite", key="lim_calc"):
            try:
                x = Symbol('x')
                expr = parse_expr(func_str.replace('^', '**'))
                point_expr = parse_expr(point.replace('^', '**'))
                
                dir_map = {"bilateral": None, "pela direita (+)": "+", "pela esquerda (-)": "-"}
                dir_symbol_map = {"bilateral": "", "pela direita (+)": "^+", "pela esquerda (-)": "^-"}
                
                steps = [f"Vamos calcular o limite da função quando $x$ tende a ${latex(point_expr)}$:"]
                steps.append(f"$$f(x) = {latex(expr)}$$")
                steps.append(f"$$\\lim_{{x \\to {latex(point_expr)}{dir_symbol_map[direction]}}} {latex(expr)}$$")

                # Tentar substituição direta
                try:
                    num = limit(expr.as_numer_denom()[0], x, point_expr)
                    den = limit(expr.as_numer_denom()[1], x, point_expr)
                    
                    if (num == 0 and den == 0) or (abs(num) == zoo and abs(den) == zoo):
                        steps.append(f"A substituição direta resulta em uma forma indeterminada ($\\frac{{{latex(num)}}}{{{latex(den)}}}$).")
                        steps.append("O Sympy aplicará técnicas avançadas, como a Regra de L'Hôpital, para resolver o limite.")
                    else:
                        direct_sub = expr.subs(x, point_expr)
                        steps.append("Tentando a substituição direta:")
                        steps.append(f"$$f({latex(point_expr)}) = {latex(direct_sub)}$$")
                except Exception:
                    steps.append("A substituição direta não é trivial. Vamos calcular o limite diretamente.")

                result = limit(expr, x, point_expr, dir_map[direction])
                
                steps.append("**Resultado Final:**")
                steps.append(f"$$\\lim_{{x \\to {latex(point_expr)}{dir_symbol_map[direction]}}} {latex(expr)} = {latex(result)}$$")
                
                render_katex_steps(steps, "Cálculo do Limite")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")

    with tabs[3]: # Série de Taylor
        func_str = st.text_input("Função f(x):", "exp(x)", key="taylor_func")
        x0 = st.text_input("Ponto de expansão (x₀):", "0", key="taylor_x0")
        n = st.number_input("Ordem (n):", 1, 10, 4, key="taylor_n")
        
        if st.button("Calcular Série de Taylor", key="taylor_calc"):
            try:
                x = Symbol('x')
                expr = parse_expr(func_str.replace('^','**'))
                x0_expr = parse_expr(x0.replace('^','**'))
                
                steps = [f"Calculando a expansão em Série de Taylor para $f(x) = {latex(expr)}$ em torno de $x_0 = {latex(x0_expr)}$ até a ordem {n}."]
                steps.append("A fórmula da Série de Taylor é:")
                steps.append("$$f(x) \\approx \\sum_{k=0}^{n} \\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k$$")
                steps.append("Calculando as derivadas e seus valores em $x_0$:")
                
                taylor_terms = []
                for i in range(n + 1):
                    deriv = diff(expr, x, i)
                    deriv_val = deriv.subs(x, x0_expr)
                    steps.append(f"$$f^{{({i})}}(x) = {latex(deriv)} \\implies f^{{({i})}}({latex(x0_expr)}) = {latex(deriv_val)}$$")
                
                result = series(expr, x, x0_expr, n+1).removeO()
                steps.append(f"**Resultado da Série de Taylor (ordem {n}):**")
                steps.append(f"$$f(x) \\approx {latex(result)}$$")
                
                render_katex_steps(steps, "Cálculo da Série de Taylor")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")

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
                    
                    steps = []
                    
                    if transf_type == "Laplace":
                        steps.append("**Transformada de Laplace:**")
                        steps.append(f"$$f(x) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}[f(x)] = \\int_0^{\\infty} f(x) e^{-sx} dx$$")
                        
                        lap = laplace_transform(expr, x, s, noconds=True)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}[{latex(expr)}] = {latex(lap)}$$")
                        
                    else:  # Inversa de Laplace
                        steps.append("**Transformada Inversa de Laplace:**")
                        steps.append(f"$$F(s) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}^{-1}[F(s)] = f(x)$$")
                        
                        inv = inverse_laplace_transform(expr, s, x)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}^{{-1}}[{latex(expr)}] = {latex(inv)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

def graphing_calculator():
    """Calculadora gráfica com KaTeX"""
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
            st.error("❌ Por favor, insira uma função válida.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                func_str_clean = func_str.replace('^', '**')
                x = symbols('x')
                expr = parse_expr(func_str_clean)
                
                # Mostrar a função em notação matemática
                steps = []
                steps.append("**Função plotada:**")
                steps.append(f"$$f(x) = {latex(expr)}$$")
                steps.append(f"**Domínio:** $[{x_min}, {x_max}]$")
                
                render_katex_steps(steps)
                
                # Plotar o gráfico
                plot_function(expr, x, (x_min, x_max), points)
                
            except Exception as e:
                st.error(f"❌ **Erro ao plotar função:** {str(e)}")

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
    main(), right: '

def render_katex_steps(steps_list, title=""):
    """Renderiza uma lista de passos matemáticos usando KaTeX"""
    if title:
        st.markdown(f"**{title}**")
    
    for step in steps_list:
        if step.startswith("$") and step.endswith("$"):
            render_katex(step, height=60)
        else:
            # Para texto normal, ainda usar KaTeX se contém fórmulas
            if "$" in step:
                render_katex(step, height=60)
            else:
                st.markdown(step)

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
.step-container {
    margin: 10px 0;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #4CAF50;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

def plot_function(expr, var, x_range=(-10, 10), points=1000):
    """Gera o gráfico de uma função matemática"""
    x_vals = np.linspace(x_range[0], x_range[1], points)
    f = lambdify(var, expr, 'numpy')
    y_vals = f(x_vals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label=f'${latex(expr)}$', color='blue', linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(fontsize=12)
    ax.set_xlabel(f'${latex(var)}$', fontsize=14)
    ax.set_ylabel(f'$f({latex(var)})$', fontsize=14)
    ax.set_title(f'Gráfico de $f({latex(var)}) = {latex(expr)}$', fontsize=16)
    
    st.pyplot(fig)

def basic_calculator():
    """Calculadora básica com operações aritméticas usando KaTeX"""
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
            steps = []
            result = None
            
            if operation == "+":
                result = num1 + num2
                steps = [
                    "**Adição:**",
                    f"$${num1} + {num2} = {result}$$"
                ]
            elif operation == "-":
                result = num1 - num2
                steps = [
                    "**Subtração:**",
                    f"$${num1} - {num2} = {result}$$"
                ]
            elif operation == "×":
                result = num1 * num2
                steps = [
                    "**Multiplicação:**",
                    f"$${num1} \\times {num2} = {result}$$"
                ]
            elif operation == "÷":
                if num2 != 0:
                    result = num1 / num2
                    steps = [
                        "**Divisão:**",
                        f"$$\\frac{{{num1}}}{{{num2}}} = {result}$$"
                    ]
                else:
                    st.error("❌ **Erro:** Divisão por zero não é definida!")
                    return
            elif operation == "^":
                result = num1 ** num2
                steps = [
                    "**Potenciação:**",
                    f"$${num1}^{{{num2}}} = {result}$$"
                ]

            # Renderizar os passos usando KaTeX
            render_katex_steps(steps)
            
        except Exception as e:
            st.error(f"❌ **Erro no cálculo:** {str(e)}")

def polynomial_solver():
    """Resolvedor de equações polinomiais com KaTeX"""
    st.subheader("Resolvedor de Equações Polinomiais")
    
    equation = st.text_input(
        "Digite a equação polinomial (ex: x^2 - 4 = 0):",
        placeholder="x^2 - 4 = 0"
    )
    
    if st.button("Resolver Equação"):
        if not equation:
            st.error("❌ Por favor, insira uma equação válida.")
        else:
            try:
                x = symbols('x')
                # Substitui ^ por ** para compatibilidade com sympy
                equation_clean = equation.replace('^', '**')
                
                steps = []
                steps.append("**Resolução da Equação Polinomial:**")
                steps.append(f"$$\\text{{Equação original: }} {equation}$$")
                
                if '=' in equation_clean:
                    lhs, rhs = equation_clean.split('=')
                    expr = Eq(parse_expr(lhs), parse_expr(rhs))
                    steps.append(f"$$\\text{{Forma padrão: }} {latex(parse_expr(lhs))} = {latex(parse_expr(rhs))}$$")
                else:
                    expr = Eq(parse_expr(equation_clean), 0)
                    steps.append(f"$$\\text{{Assumindo: }} {latex(parse_expr(equation_clean))} = 0$$")
                
                solutions = solve(expr, x)
                
                if not solutions:
                    steps.append("$$\\text{A equação não possui soluções reais.}$$")
                else:
                    steps.append("**Soluções encontradas:**")
                    for i, sol in enumerate(solutions, 1):
                        steps.append(f"$$x_{i} = {latex(sol)}$$")
                        # Verificação da solução
                        if '=' in equation_clean:
                            lhs_val = parse_expr(lhs).subs(x, sol)
                            rhs_val = parse_expr(rhs).subs(x, sol)
                            steps.append(f"$$\\text{{Verificação: }} {latex(lhs_val)} = {latex(rhs_val)}$$")
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro ao resolver a equação:** {str(e)}")

def summation_calculator():
    """Calculadora de somatórios com KaTeX"""
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
            st.error("❌ Por favor, preencha todos os campos.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                sum_expr_clean = sum_expr.replace('^', '**')
                var = symbols(sum_var)
                expr = parse_expr(sum_expr_clean)
                result = summation(expr, (var, lower, upper))
                
                steps = []
                steps.append("**Cálculo do Somatório:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)}$$")
                
                # Mostrar alguns termos do somatório para visualização
                if upper - lower <= 10:
                    terms = []
                    for i in range(int(lower), int(upper) + 1):
                        term_value = expr.subs(var, i)
                        terms.append(f"{latex(term_value)}")
                    
                    steps.append("**Expandindo os termos:**")
                    steps.append(f"$${' + '.join(terms)}$$")
                
                steps.append("**Resultado:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)} = {latex(result)}$$")
                
                # Valor numérico se possível
                try:
                    numeric_result = float(result)
                    steps.append(f"$$\\approx {numeric_result:.6f}$$")
                except:
                    pass
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro no cálculo do somatório:** {str(e)}")

def advanced_calculator():
    """Calculadora avançada com passo a passo usando KaTeX"""
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
                    
                    steps = []
                    steps.append("**Cálculo da Derivada:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    if order == 1:
                        steps.append(f"$$\\text{{Calculando: }} \\frac{{df}}{{dx}}$$")
                    else:
                        steps.append(f"$$\\text{{Calculando: }} \\frac{{d^{order}f}}{{dx^{order}}}$$")

                    # Análise por tipo de função
                    if isinstance(expr, Add):
                        steps.append("**Aplicando a regra da soma:** $(f+g)' = f' + g'$")
                        for arg in expr.args:
                            d = diff(arg, x, order)
                            steps.append(f"$$\\frac{{d^{order}}}{{dx^{order}}}\\left({latex(arg)}\\right) = {latex(d)}$$")
                    elif isinstance(expr, Mul):
                        if len(expr.args) == 2:
                            steps.append("**Aplicando a regra do produto:** $(uv)' = u'v + uv'$")
                            u, v = expr.args
                            du = diff(u, x, 1)
                            dv = diff(v, x, 1)
                            steps.append(f"$$u = {latex(u)}, \\quad u' = {latex(du)}$$")
                            steps.append(f"$$v = {latex(v)}, \\quad v' = {latex(dv)}$$")
                            if order == 1:
                                result_product = du*v + u*dv
                                steps.append(f"$$f'(x) = u'v + uv' = {latex(result_product)}$$")
                    
                    # Resultado final
                    final_deriv = diff(expr, x, order)
                    simplified = simplify(final_deriv)
                    
                    steps.append("**Resultado:**")
                    if order == 1:
                        steps.append(f"$$f'(x) = {latex(final_deriv)}$$")
                    else:
                        steps.append(f"$$f^{{({order})}}(x) = {latex(final_deriv)}$$")
                    
                    if final_deriv != simplified:
                        steps.append("**Simplificado:**")
                        if order == 1:
                            steps.append(f"$$f'(x) = {latex(simplified)}$$")
                        else:
                            steps.append(f"$$f^{{({order})}}(x) = {latex(simplified)}$$")

                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

    # Tab: Integral
    with tabs[1]:
        func_str = st.text_input("Função para integrar:", placeholder="Ex: x^2 + sin(x)", key="int_func")
        int_type = st.radio("Tipo de integral:", ["Indefinida", "Definida"], key="int_type")
        
        if int_type == "Definida":
            col_a, col_b = st.columns(2)
            with col_a:
                a = st.text_input("Limite inferior (a):", value="0", key="int_a")
            with col_b:
                b = st.text_input("Limite superior (b):", value="1", key="int_b")
        
        if st.button("Calcular integral", key="int_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^', '**'))
                    x = Symbol('x')
                    
                    steps = []
                    steps.append("**Cálculo da Integral:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    if int_type == "Indefinida":
                        steps.append("$$\\text{Calculando: } \\int f(x) \\, dx$$")
                    else:
                        steps.append(f"$$\\text{{Calculando: }} \\int_{{{a}}}^{{{b}}} f(x) \\, dx$$")
                    
                    # Análise por partes se for soma
                    if isinstance(expr, Add):
                        steps.append("**Aplicando a linearidade:** $\\int(f+g)dx = \\int f dx + \\int g dx$")
                        for arg in expr.args:
                            integ = integrate(arg, x)
                            steps.append(f"$$\\int {latex(arg)} \\, dx = {latex(integ)}$$")
                    
                    # Calcular a primitiva
                    primitive = integrate(expr, x)
                    steps.append("**Primitiva:**")
                    steps.append(f"$$F(x) = {latex(primitive)}$$")
                    
                    if int_type == "Indefinida":
                        steps.append("**Resultado final:**")
                        steps.append(f"$$\\int {latex(expr)} \\, dx = {latex(primitive)} + C$$")
                    else:
                        # Integral definida
                        a_expr = parse_expr(a.replace('^', '**'))
                        b_expr = parse_expr(b.replace('^', '**'))
                        
                        Fa = primitive.subs(x, a_expr)
                        Fb = primitive.subs(x, b_expr)
                        result = Fb - Fa
                        
                        steps.append("**Aplicando o Teorema Fundamental do Cálculo:**")
                        steps.append(f"$$\\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \\, dx = F({latex(b_expr)}) - F({latex(a_expr)})$$")
                        steps.append(f"$$= {latex(Fb)} - {latex(Fa)}$$")
                        steps.append(f"$$= {latex(result)}$$")
                        
                        # Valor numérico se possível
                        try:
                            numeric_result = float(result)
                            steps.append(f"$$\\approx {numeric_result:.6f}$$")
                        except:
                            pass
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    
                    steps = []
                    steps.append("**Cálculo do Limite:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    dir_symbol = ""
                    if direction == "+":
                        dir_symbol = "^+"
                    elif direction == "-":
                        dir_symbol = "^-"
                    
                    steps.append(f"$$\\text{{Calculando: }} \\lim_{{x \\to {latex(point_expr)}{dir_symbol}}} f(x)$$")
                    
                    # Verificar se é uma forma indeterminada
                    try:
                        direct_sub = expr.subs(x, point_expr)
                        if direct_sub.is_finite and not direct_sub.has(zoo):
                            steps.append("**Substituição direta:**")
                            steps.append(f"$$f({latex(point_expr)}) = {latex(direct_sub)}$$")
                        else:
                            steps.append("**Forma indeterminada detectada - aplicando técnicas de limite**")
                    except:
                        steps.append("**Substituição direta não possível - aplicando técnicas de limite**")
                    
                    dir_map = {"ambos": None, "+": "+", "-": "-"}
                    result = limit(expr, x, point_expr, dir_map[direction])
                    
                    steps.append("**Resultado:**")
                    steps.append(f"$$\\lim_{{x \\to {latex(point_expr)}{dir_symbol}}} {latex(expr)} = {latex(result)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    x = Symbol('x')
                    
                    steps = []
                    steps.append("**Série de Taylor:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    steps.append(f"$$\\text{{Expansão em torno de }} x_0 = {latex(x0_expr)}$$")
                    
                    # Fórmula geral da série de Taylor
                    steps.append("**Fórmula geral:**")
                    steps.append("$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(x_0)}{n!}(x-x_0)^n$$")
                    
                    # Calcular alguns termos
                    steps.append("**Derivadas no ponto:**")
                    for i in range(min(n+1, 5)):
                        if i == 0:
                            deriv = expr
                            steps.append(f"$$f({latex(x0_expr)}) = {latex(deriv.subs(x, x0_expr))}$$")
                        else:
                            deriv = diff(expr, x, i)
                            steps.append(f"$$f^{{({i})}}({latex(x0_expr)}) = {latex(deriv.subs(x, x0_expr))}$$")
                    
                    # Série resultante
                    result = series(expr, x, x0_expr, n+1).removeO()
                    steps.append("**Série de Taylor até ordem " + str(n) + ":**")
                    steps.append(f"$$f(x) \\approx {latex(result)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    
                    steps = []
                    
                    if transf_type == "Laplace":
                        steps.append("**Transformada de Laplace:**")
                        steps.append(f"$$f(x) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}[f(x)] = \\int_0^{\\infty} f(x) e^{-sx} dx$$")
                        
                        lap = laplace_transform(expr, x, s, noconds=True)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}[{latex(expr)}] = {latex(lap)}$$")
                        
                    else:  # Inversa de Laplace
                        steps.append("**Transformada Inversa de Laplace:**")
                        steps.append(f"$$F(s) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}^{-1}[F(s)] = f(x)$$")
                        
                        inv = inverse_laplace_transform(expr, s, x)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}^{{-1}}[{latex(expr)}] = {latex(inv)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

def graphing_calculator():
    """Calculadora gráfica com KaTeX"""
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
            st.error("❌ Por favor, insira uma função válida.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                func_str_clean = func_str.replace('^', '**')
                x = symbols('x')
                expr = parse_expr(func_str_clean)
                
                # Mostrar a função em notação matemática
                steps = []
                steps.append("**Função plotada:**")
                steps.append(f"$$f(x) = {latex(expr)}$$")
                steps.append(f"**Domínio:** $[{x_min}, {x_max}]$")
                
                render_katex_steps(steps)
                
                # Plotar o gráfico
                plot_function(expr, x, (x_min, x_max), points)
                
            except Exception as e:
                st.error(f"❌ **Erro ao plotar função:** {str(e)}")

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
    main(), display: false}}
            ]
        }});"></script>
    <div style="
        font-size: 20px; 
        text-align: center; 
        padding: 15px; 
        background-color: white; 
        color: #1f1f1f; 
        border: 2px solid #4CAF50; 
        border-radius: 8px; 
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">{latex_str}</div>
    """
    components.html(html, height=height)

def render_katex_steps(steps_list, title=""):
    """Renderiza uma lista de passos matemáticos usando KaTeX"""
    if title:
        st.markdown(f"**{title}**")
    
    for step in steps_list:
        if step.startswith("$") and step.endswith("$"):
            render_katex(step, height=60)
        else:
            # Para texto normal, ainda usar KaTeX se contém fórmulas
            if "$" in step:
                render_katex(step, height=60)
            else:
                st.markdown(step)

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
.step-container {
    margin: 10px 0;
    padding: 15px;
    background-color: #f8f9fa;
    border-left: 4px solid #4CAF50;
    border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

def plot_function(expr, var, x_range=(-10, 10), points=1000):
    """Gera o gráfico de uma função matemática"""
    x_vals = np.linspace(x_range[0], x_range[1], points)
    f = lambdify(var, expr, 'numpy')
    y_vals = f(x_vals)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_vals, y_vals, label=f'${latex(expr)}$', color='blue', linewidth=2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.legend(fontsize=12)
    ax.set_xlabel(f'${latex(var)}$', fontsize=14)
    ax.set_ylabel(f'$f({latex(var)})$', fontsize=14)
    ax.set_title(f'Gráfico de $f({latex(var)}) = {latex(expr)}$', fontsize=16)
    
    st.pyplot(fig)

def basic_calculator():
    """Calculadora básica com operações aritméticas usando KaTeX"""
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
            steps = []
            result = None
            
            if operation == "+":
                result = num1 + num2
                steps = [
                    "**Adição:**",
                    f"$${num1} + {num2} = {result}$$"
                ]
            elif operation == "-":
                result = num1 - num2
                steps = [
                    "**Subtração:**",
                    f"$${num1} - {num2} = {result}$$"
                ]
            elif operation == "×":
                result = num1 * num2
                steps = [
                    "**Multiplicação:**",
                    f"$${num1} \\times {num2} = {result}$$"
                ]
            elif operation == "÷":
                if num2 != 0:
                    result = num1 / num2
                    steps = [
                        "**Divisão:**",
                        f"$$\\frac{{{num1}}}{{{num2}}} = {result}$$"
                    ]
                else:
                    st.error("❌ **Erro:** Divisão por zero não é definida!")
                    return
            elif operation == "^":
                result = num1 ** num2
                steps = [
                    "**Potenciação:**",
                    f"$${num1}^{{{num2}}} = {result}$$"
                ]

            # Renderizar os passos usando KaTeX
            render_katex_steps(steps)
            
        except Exception as e:
            st.error(f"❌ **Erro no cálculo:** {str(e)}")

def polynomial_solver():
    """Resolvedor de equações polinomiais com KaTeX"""
    st.subheader("Resolvedor de Equações Polinomiais")
    
    equation = st.text_input(
        "Digite a equação polinomial (ex: x^2 - 4 = 0):",
        placeholder="x^2 - 4 = 0"
    )
    
    if st.button("Resolver Equação"):
        if not equation:
            st.error("❌ Por favor, insira uma equação válida.")
        else:
            try:
                x = symbols('x')
                # Substitui ^ por ** para compatibilidade com sympy
                equation_clean = equation.replace('^', '**')
                
                steps = []
                steps.append("**Resolução da Equação Polinomial:**")
                steps.append(f"$$\\text{{Equação original: }} {equation}$$")
                
                if '=' in equation_clean:
                    lhs, rhs = equation_clean.split('=')
                    expr = Eq(parse_expr(lhs), parse_expr(rhs))
                    steps.append(f"$$\\text{{Forma padrão: }} {latex(parse_expr(lhs))} = {latex(parse_expr(rhs))}$$")
                else:
                    expr = Eq(parse_expr(equation_clean), 0)
                    steps.append(f"$$\\text{{Assumindo: }} {latex(parse_expr(equation_clean))} = 0$$")
                
                solutions = solve(expr, x)
                
                if not solutions:
                    steps.append("$$\\text{A equação não possui soluções reais.}$$")
                else:
                    steps.append("**Soluções encontradas:**")
                    for i, sol in enumerate(solutions, 1):
                        steps.append(f"$$x_{i} = {latex(sol)}$$")
                        # Verificação da solução
                        if '=' in equation_clean:
                            lhs_val = parse_expr(lhs).subs(x, sol)
                            rhs_val = parse_expr(rhs).subs(x, sol)
                            steps.append(f"$$\\text{{Verificação: }} {latex(lhs_val)} = {latex(rhs_val)}$$")
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro ao resolver a equação:** {str(e)}")

def summation_calculator():
    """Calculadora de somatórios com KaTeX"""
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
            st.error("❌ Por favor, preencha todos os campos.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                sum_expr_clean = sum_expr.replace('^', '**')
                var = symbols(sum_var)
                expr = parse_expr(sum_expr_clean)
                result = summation(expr, (var, lower, upper))
                
                steps = []
                steps.append("**Cálculo do Somatório:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)}$$")
                
                # Mostrar alguns termos do somatório para visualização
                if upper - lower <= 10:
                    terms = []
                    for i in range(int(lower), int(upper) + 1):
                        term_value = expr.subs(var, i)
                        terms.append(f"{latex(term_value)}")
                    
                    steps.append("**Expandindo os termos:**")
                    steps.append(f"$${' + '.join(terms)}$$")
                
                steps.append("**Resultado:**")
                steps.append(f"$$\\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)} = {latex(result)}$$")
                
                # Valor numérico se possível
                try:
                    numeric_result = float(result)
                    steps.append(f"$$\\approx {numeric_result:.6f}$$")
                except:
                    pass
                
                render_katex_steps(steps)
                
            except Exception as e:
                st.error(f"❌ **Erro no cálculo do somatório:** {str(e)}")

def advanced_calculator():
    """Calculadora avançada com passo a passo usando KaTeX"""
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
                    
                    steps = []
                    steps.append("**Cálculo da Derivada:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    if order == 1:
                        steps.append(f"$$\\text{{Calculando: }} \\frac{{df}}{{dx}}$$")
                    else:
                        steps.append(f"$$\\text{{Calculando: }} \\frac{{d^{order}f}}{{dx^{order}}}$$")

                    # Análise por tipo de função
                    if isinstance(expr, Add):
                        steps.append("**Aplicando a regra da soma:** $(f+g)' = f' + g'$")
                        for arg in expr.args:
                            d = diff(arg, x, order)
                            steps.append(f"$$\\frac{{d^{order}}}{{dx^{order}}}\\left({latex(arg)}\\right) = {latex(d)}$$")
                    elif isinstance(expr, Mul):
                        if len(expr.args) == 2:
                            steps.append("**Aplicando a regra do produto:** $(uv)' = u'v + uv'$")
                            u, v = expr.args
                            du = diff(u, x, 1)
                            dv = diff(v, x, 1)
                            steps.append(f"$$u = {latex(u)}, \\quad u' = {latex(du)}$$")
                            steps.append(f"$$v = {latex(v)}, \\quad v' = {latex(dv)}$$")
                            if order == 1:
                                result_product = du*v + u*dv
                                steps.append(f"$$f'(x) = u'v + uv' = {latex(result_product)}$$")
                    
                    # Resultado final
                    final_deriv = diff(expr, x, order)
                    simplified = simplify(final_deriv)
                    
                    steps.append("**Resultado:**")
                    if order == 1:
                        steps.append(f"$$f'(x) = {latex(final_deriv)}$$")
                    else:
                        steps.append(f"$$f^{{({order})}}(x) = {latex(final_deriv)}$$")
                    
                    if final_deriv != simplified:
                        steps.append("**Simplificado:**")
                        if order == 1:
                            steps.append(f"$$f'(x) = {latex(simplified)}$$")
                        else:
                            steps.append(f"$$f^{{({order})}}(x) = {latex(simplified)}$$")

                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

    # Tab: Integral
    with tabs[1]:
        func_str = st.text_input("Função para integrar:", placeholder="Ex: x^2 + sin(x)", key="int_func")
        int_type = st.radio("Tipo de integral:", ["Indefinida", "Definida"], key="int_type")
        
        if int_type == "Definida":
            col_a, col_b = st.columns(2)
            with col_a:
                a = st.text_input("Limite inferior (a):", value="0", key="int_a")
            with col_b:
                b = st.text_input("Limite superior (b):", value="1", key="int_b")
        
        if st.button("Calcular integral", key="int_calc"):
            if func_str:
                try:
                    expr = parse_expr(func_str.replace('^', '**'))
                    x = Symbol('x')
                    
                    steps = []
                    steps.append("**Cálculo da Integral:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    if int_type == "Indefinida":
                        steps.append("$$\\text{Calculando: } \\int f(x) \\, dx$$")
                    else:
                        steps.append(f"$$\\text{{Calculando: }} \\int_{{{a}}}^{{{b}}} f(x) \\, dx$$")
                    
                    # Análise por partes se for soma
                    if isinstance(expr, Add):
                        steps.append("**Aplicando a linearidade:** $\\int(f+g)dx = \\int f dx + \\int g dx$")
                        for arg in expr.args:
                            integ = integrate(arg, x)
                            steps.append(f"$$\\int {latex(arg)} \\, dx = {latex(integ)}$$")
                    
                    # Calcular a primitiva
                    primitive = integrate(expr, x)
                    steps.append("**Primitiva:**")
                    steps.append(f"$$F(x) = {latex(primitive)}$$")
                    
                    if int_type == "Indefinida":
                        steps.append("**Resultado final:**")
                        steps.append(f"$$\\int {latex(expr)} \\, dx = {latex(primitive)} + C$$")
                    else:
                        # Integral definida
                        a_expr = parse_expr(a.replace('^', '**'))
                        b_expr = parse_expr(b.replace('^', '**'))
                        
                        Fa = primitive.subs(x, a_expr)
                        Fb = primitive.subs(x, b_expr)
                        result = Fb - Fa
                        
                        steps.append("**Aplicando o Teorema Fundamental do Cálculo:**")
                        steps.append(f"$$\\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \\, dx = F({latex(b_expr)}) - F({latex(a_expr)})$$")
                        steps.append(f"$$= {latex(Fb)} - {latex(Fa)}$$")
                        steps.append(f"$$= {latex(result)}$$")
                        
                        # Valor numérico se possível
                        try:
                            numeric_result = float(result)
                            steps.append(f"$$\\approx {numeric_result:.6f}$$")
                        except:
                            pass
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    
                    steps = []
                    steps.append("**Cálculo do Limite:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    
                    dir_symbol = ""
                    if direction == "+":
                        dir_symbol = "^+"
                    elif direction == "-":
                        dir_symbol = "^-"
                    
                    steps.append(f"$$\\text{{Calculando: }} \\lim_{{x \\to {latex(point_expr)}{dir_symbol}}} f(x)$$")
                    
                    # Verificar se é uma forma indeterminada
                    try:
                        direct_sub = expr.subs(x, point_expr)
                        if direct_sub.is_finite and not direct_sub.has(zoo):
                            steps.append("**Substituição direta:**")
                            steps.append(f"$$f({latex(point_expr)}) = {latex(direct_sub)}$$")
                        else:
                            steps.append("**Forma indeterminada detectada - aplicando técnicas de limite**")
                    except:
                        steps.append("**Substituição direta não possível - aplicando técnicas de limite**")
                    
                    dir_map = {"ambos": None, "+": "+", "-": "-"}
                    result = limit(expr, x, point_expr, dir_map[direction])
                    
                    steps.append("**Resultado:**")
                    steps.append(f"$$\\lim_{{x \\to {latex(point_expr)}{dir_symbol}}} {latex(expr)} = {latex(result)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    x = Symbol('x')
                    
                    steps = []
                    steps.append("**Série de Taylor:**")
                    steps.append(f"$$f(x) = {latex(expr)}$$")
                    steps.append(f"$$\\text{{Expansão em torno de }} x_0 = {latex(x0_expr)}$$")
                    
                    # Fórmula geral da série de Taylor
                    steps.append("**Fórmula geral:**")
                    steps.append("$$f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(x_0)}{n!}(x-x_0)^n$$")
                    
                    # Calcular alguns termos
                    steps.append("**Derivadas no ponto:**")
                    for i in range(min(n+1, 5)):
                        if i == 0:
                            deriv = expr
                            steps.append(f"$$f({latex(x0_expr)}) = {latex(deriv.subs(x, x0_expr))}$$")
                        else:
                            deriv = diff(expr, x, i)
                            steps.append(f"$$f^{{({i})}}({latex(x0_expr)}) = {latex(deriv.subs(x, x0_expr))}$$")
                    
                    # Série resultante
                    result = series(expr, x, x0_expr, n+1).removeO()
                    steps.append("**Série de Taylor até ordem " + str(n) + ":**")
                    steps.append(f"$$f(x) \\approx {latex(result)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

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
                    
                    steps = []
                    
                    if transf_type == "Laplace":
                        steps.append("**Transformada de Laplace:**")
                        steps.append(f"$$f(x) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}[f(x)] = \\int_0^{\\infty} f(x) e^{-sx} dx$$")
                        
                        lap = laplace_transform(expr, x, s, noconds=True)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}[{latex(expr)}] = {latex(lap)}$$")
                        
                    else:  # Inversa de Laplace
                        steps.append("**Transformada Inversa de Laplace:**")
                        steps.append(f"$$F(s) = {latex(expr)}$$")
                        steps.append("$$\\mathcal{L}^{-1}[F(s)] = f(x)$$")
                        
                        inv = inverse_laplace_transform(expr, s, x)
                        steps.append("**Resultado:**")
                        steps.append(f"$$\\mathcal{{L}}^{{-1}}[{latex(expr)}] = {latex(inv)}$$")
                    
                    render_katex_steps(steps)

                except Exception as e:
                    st.error(f"❌ **Erro no cálculo:** {str(e)}")

def graphing_calculator():
    """Calculadora gráfica com KaTeX"""
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
            st.error("❌ Por favor, insira uma função válida.")
        else:
            try:
                # Substitui ^ por ** para compatibilidade com sympy
                func_str_clean = func_str.replace('^', '**')
                x = symbols('x')
                expr = parse_expr(func_str_clean)
                
                # Mostrar a função em notação matemática
                steps = []
                steps.append("**Função plotada:**")
                steps.append(f"$$f(x) = {latex(expr)}$$")
                steps.append(f"**Domínio:** $[{x_min}, {x_max}]$")
                
                render_katex_steps(steps)
                
                # Plotar o gráfico
                plot_function(expr, x, (x_min, x_max), points)
                
            except Exception as e:
                st.error(f"❌ **Erro ao plotar função:** {str(e)}")

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
