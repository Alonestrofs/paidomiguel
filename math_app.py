import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import (symbols, diff, integrate, series, parse_expr, sin, cos, tan,
                   exp, log, sqrt, latex, solve, summation, Eq, Symbol, lambdify,
                   limit, laplace_transform, inverse_laplace_transform, simplify, 
                   Add, Mul, Pow, zoo, oo)

# Configuração da página e Estilos CSS
st.set_page_config(
    page_title="Calculadora Avançada Pro",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Estilos gerais */
.stApp {
    background-color: #f0f2f6;
}
/* Botões */
div.stButton > button {
    width: 100%;
    background-color: #4CAF50;
    color: white;
    padding: 12px 18px;
    margin: 8px 0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #45a049;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
/* Título principal */
.header {
    color: #4CAF50;
    text-align: center;
    padding: 10px;
    font-size: 3em;
    font-weight: bold;
}
/* Container para passos de texto */
.step-container {
    margin: 10px 0;
    padding: 15px;
    background-color: #ffffff;
    border-left: 5px solid #4CAF50;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    font-size: 1.1em;
}
/* Container para fórmulas LaTeX */
.latex-container {
    margin: 15px 0;
    padding: 25px;
    background-color: #ffffff;
    border: 2px solid #4CAF50;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;
}
/* Estilo das abas */
.stTabs [data-baseweb="tab-list"] {
	gap: 24px;
}
.stTabs [data-baseweb="tab"] {
	height: 50px;
    white-space: pre-wrap;
	background-color: #F0F0F0;
	border-radius: 8px 8px 0px 0px;
	gap: 1px;
	padding-top: 10px;
	padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
  	background-color: #4CAF50;
	color: white;
	font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# --- Funções de Renderização ---

def render_latex_step(latex_expr):
    """Renderiza uma expressão LaTeX usando o método nativo do Streamlit."""
    st.markdown('<div class="latex-container">', unsafe_allow_html=True)
    st.latex(latex_expr)
    st.markdown('</div>', unsafe_allow_html=True)

def render_steps(steps_list, title=""):
    """Renderiza uma lista de passos matemáticos."""
    if title:
        st.markdown(f"### {title}")

    for step in steps_list:
        if isinstance(step, tuple) and step[0] == 'latex':
            # Se for uma tupla marcada como latex
            render_latex_step(step[1])
        elif step.startswith("$$") and step.endswith("$$"):
            # Se for uma string delimitada por $$
            latex_content = step.strip("$")
            render_latex_step(latex_content)
        else:
            # Texto explicativo normal
            st.markdown(f'<div class="step-container">{step}</div>', unsafe_allow_html=True)


# --- Funções da Calculadora ---

def plot_function(expr, var, x_range=(-10, 10), points=1000):
    """Gera o gráfico de uma função matemática."""
    try:
        x_vals = np.linspace(x_range[0], x_range[1], points)
        f = lambdify(var, expr, 'numpy')
        y_vals = f(x_vals)

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_vals, y_vals, label=f'${latex(expr)}$', color='#4CAF50', linewidth=2.5)
        ax.axhline(0, color='black', linewidth=0.7)
        ax.axvline(0, color='black', linewidth=0.7)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
        ax.legend(fontsize=14)
        ax.set_xlabel(f'${latex(var)}$', fontsize=14)
        ax.set_ylabel(f'$f({latex(var)})$', fontsize=14)
        ax.set_title(f'Gráfico de $f({latex(var)}) = {latex(expr)}$', fontsize=16)
        ax.set_facecolor('#f0f2f6')
        fig.patch.set_facecolor('#f0f2f6')

        st.pyplot(fig)
    except Exception as e:
        st.error(f"❌ **Erro ao gerar gráfico:** {e}")

def basic_calculator():
    st.header("Calculadora Básica")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1: num1 = st.number_input("Primeiro número:", value=0.0, format="%.4f")
    with col2: operation = st.selectbox("Operação:", ["+", "-", "×", "÷", "^"])
    with col3: num2 = st.number_input("Segundo número:", value=0.0, format="%.4f")

    if st.button("Calcular", key="basic_calc"):
        try:
            op_map = {"+": "+", "-": "-", "×": "\times", "÷": "/", "^": "^"}
            result_map = {
                "+": lambda a, b: a + b,
                "×": lambda a, b: a * b,
                "-": lambda a, b: a - b,
                "÷": lambda a, b: a / b if b != 0 else None,
                "^": lambda a, b: a ** b,
            }
            result = result_map[operation](num1, num2)
            if result is None:
                st.error("❌ **Erro:** Divisão por zero")
            else:
                steps = []
                steps.append("Cálculo da operação:")
                if operation == "÷":
                    latex_expr = f"\frac{{{num1}}}{{{num2}}} = {result}"
                else:
                    latex_expr = f"{num1} {op_map[operation]} {num2} = {result}"
                steps.append(f"$${latex_expr}$$")
                render_steps(steps)
        except Exception as e:
            st.error(f"❌ **Erro no cálculo:** {e}")


def polynomial_solver():
    st.header("Resolvedor de Equações Polinomiais")
    equation = st.text_input("Digite a equação (ex: x^2 - 5*x + 6 = 0):", "x^2 - 4 = 0")
    if st.button("Resolver Equação", key="poly_solve"):
        if not equation:
            st.warning("Por favor, insira uma equação.")
            return
        try:
            x = symbols('x')
            eq_clean = equation.replace('^', '**')
            steps = []
            if '=' in eq_clean:
                lhs, rhs = eq_clean.split('=')
                expr = Eq(parse_expr(lhs), parse_expr(rhs))
                steps.append("A equação fornecida é:")
                steps.append(f"$${latex(expr)}$$")
            else:
                expr = Eq(parse_expr(eq_clean), 0)
                steps.append("Assumindo que a expressão é igual a zero:")
                steps.append(f"$${latex(expr)}$$")

            solutions = solve(expr, x)
            if not solutions:
                steps.append("A equação não possui soluções no conjunto dos números reais.")
            else:
                sol_latex = [latex(s) for s in solutions]
                steps.append(f"As soluções para a variável $x$ são:")
                st.success(f"**Soluções encontradas:** {', '.join([f'x = {s}' for s in sol_latex])}")
                for i, sol in enumerate(solutions):
                    steps.append(f"$$x_{i+1} = {latex(sol)}$$")
            render_steps(steps, title="Passo a Passo da Resolução")
        except Exception as e:
            st.error(f"❌ **Erro ao resolver:** {e}")

def summation_calculator():
    st.header("Calculadora de Somatórios")
    col1, col2, col3, col4 = st.columns(4)
    sum_expr = col1.text_input("Expressão:", "k^2")
    sum_var = col2.text_input("Variável:", "k")
    lower = col3.number_input("Início (n):", value=1, step=1)
    upper = col4.number_input("Fim (m):", value=10, step=1)

    if st.button("Calcular Somatório", key="sum_calc"):
        try:
            var = symbols(sum_var)
            expr = parse_expr(sum_expr.replace('^', '**'))
            result = summation(expr, (var, lower, upper))

            steps = []
            steps.append(f"Calculando o somatório da expressão ${latex(expr)}$ de ${latex(var)}={lower}$ até ${latex(var)}={upper}$.")
            steps.append(f"$$\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)}$$")

            if upper - lower < 15:
                steps.append("Expandindo os termos da soma:")
                for i in range(int(lower), int(upper) + 1):
                    term_val = expr.subs(var, i)
                    steps.append(f"$$\text{{Para }} {latex(var)}={i}: {latex(term_val)}$$")

            steps.append("O resultado do somatório é:")
            steps.append(f"$$\sum_{{{latex(var)}={int(lower)}}}^{{{int(upper)}}} {latex(expr)} = {latex(result)}$$")
            render_steps(steps, "Cálculo do Somatório")
        except Exception as e:
            st.error(f"❌ **Erro no cálculo:** {e}")

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
                steps = []
                steps.append(f"Vamos calcular a derivada de ordem {order} da função:")
                steps.append(f"$$f(x) = {latex(expr)}$$")

                current_expr = expr
                for i in range(1, order + 1):
                    deriv = diff(current_expr, x)
                    if isinstance(current_expr, Add):
                        steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Soma: $(u+v)' = u' + v'$.")
                    elif isinstance(current_expr, Mul) and len(current_expr.args) == 2:
                        u, v = current_expr.args
                        du, dv = diff(u, x), diff(v, x)
                        steps.append(f"**{i}ª Derivada:** Aplicando a Regra do Produto: $(u \cdot v)' = u' \cdot v + u \cdot v'$.")
                        steps.append(f"Onde $u = {latex(u)}$ e $v = {latex(v)}$.")
                        steps.append(f"As derivadas são $u' = {latex(du)}$ e $v' = {latex(dv)}$.")
                        steps.append("Substituindo na fórmula:")
                        steps.append(f"$$f^{{({i})}}(x) = ({latex(du)}) \cdot ({latex(v)}) + ({latex(u)}) \cdot ({latex(dv)})$$")
                    elif isinstance(current_expr, Pow):
                        base, exp_val = current_expr.args
                        if x in base.free_symbols and x not in exp_val.free_symbols:
                            steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Potência: $(u^n)' = n \cdot u^{{n-1}} \cdot u'$.")
                        elif x in exp_val.free_symbols:
                             steps.append(f"**{i}ª Derivada:** Aplicando a Regra da Exponencial e/ou Cadeia.")

                    simplified = simplify(deriv)
                    if order > 1 and i < order:
                        steps.append(f"O resultado da {i}ª derivada é:")
                        steps.append(f"$$\frac{{d^{i}}}{{dx^{i}}} f(x) = {latex(simplified)}$$")
                    current_expr = deriv

                final_deriv = diff(expr, x, order)
                final_simplified = simplify(final_deriv)

                steps.append("**Resultado Final:**")
                if order == 1:
                    steps.append(f"$$f'(x) = {latex(final_simplified)}$$")
                else:
                    steps.append(f"$$f^{{({order})}}(x) = {latex(final_simplified)}$$")

                render_steps(steps, "Cálculo da Derivada")

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

                steps = []
                steps.append("Vamos calcular a integral da função:")
                steps.append(f"$$f(x) = {latex(expr)}$$")

                if isinstance(expr, Add):
                    steps.append("Aplicando a Regra da Soma para integrais: $\int (u+v) dx = \int u dx + \int v dx$.")
                    for arg in expr.args:
                        arg_integral = integrate(arg, x)
                        steps.append(f"$$\int {latex(arg)} \, dx = {latex(arg_integral)}$$")

                primitive = integrate(expr, x)
                steps.append("A primitiva (integral indefinida) da função é:")
                steps.append(f"$$F(x) = \int {latex(expr)} \, dx = {latex(primitive)}$$")

                if int_type == "Indefinida":
                    steps.append("**Resultado Final (Integral Indefinida):**")
                    steps.append(f"$$\int {latex(expr)} \, dx = {latex(primitive)} + C$$")
                else:
                    a_expr, b_expr = parse_expr(a), parse_expr(b)
                    Fa = primitive.subs(x, a_expr)
                    Fb = primitive.subs(x, b_expr)
                    result = Fb - Fa

                    steps.append("Para a integral definida, aplicamos o Teorema Fundamental do Cálculo:")
                    steps.append(f"$$\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \, dx = F({latex(b_expr)}) - F({latex(a_expr)})$$")
                    steps.append("Calculando os valores nos limites:")
                    steps.append(f"$$F({latex(b_expr)}) = {latex(Fb)}$$")
                    steps.append(f"$$F({latex(a_expr)}) = {latex(Fa)}$$")
                    steps.append("**Resultado Final (Integral Definida):**")
                    steps.append(f"$$\int_{{{latex(a_expr)}}}^{{{latex(b_expr)}}} f(x) \, dx = {latex(result)}$$")
                    if result.is_number:
                         steps.append(f"$$\approx {result.evalf(6)}$$")

                render_steps(steps, "Cálculo da Integral")

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

                steps = []
                steps.append(f"Vamos calcular o limite da função quando $x$ tende a ${latex(point_expr)}$:")
                steps.append(f"$$f(x) = {latex(expr)}$$")
                steps.append(f"$$\lim_{{x \to {latex(point_expr)}{dir_symbol_map[direction]}}} {latex(expr)}$$")

                # Tentar substituição direta
                try:
                    num = limit(expr.as_numer_denom()[0], x, point_expr)
                    den = limit(expr.as_numer_denom()[1], x, point_expr)

                    is_indeterminate = False
                    if (num == 0 and den == 0):
                        is_indeterminate = True
                    elif num.has(zoo, oo, -oo) or den.has(zoo, oo, -oo):
                        is_indeterminate = True

                    if is_indeterminate:
                        steps.append("A substituição direta resulta em uma forma indeterminada.")
                        steps.append("O SymPy aplicará técnicas avançadas, como a Regra de L'Hôpital, para resolver o limite.")
                    else:
                        direct_sub = expr.subs(x, point_expr)
                        steps.append("Tentando a substituição direta:")
                        steps.append(f"$$f({latex(point_expr)}) = {latex(direct_sub)}$$")
                except Exception:
                    steps.append("A substituição direta não é trivial. Vamos calcular o limite diretamente.")

                result = limit(expr, x, point_expr, dir_map[direction])

                steps.append("**Resultado Final:**")
                steps.append(f"$$\lim_{{x \to {latex(point_expr)}{dir_symbol_map[direction]}}} {latex(expr)} = {latex(result)}$$")

                render_steps(steps, "Cálculo do Limite")

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

                steps = []
                steps.append(f"Calculando a expansão em Série de Taylor para $f(x) = {latex(expr)}$ em torno de $x_0 = {latex(x0_expr)}$ até a ordem {n}.")
                steps.append("A fórmula da Série de Taylor é:")
                steps.append("$$f(x) \approx \sum_{k=0}^{n} \frac{f^{(k)}(x_0)}{k!}(x-x_0)^k$$")
                steps.append("Calculando as derivadas e seus valores em $x_0$:")

                for i in range(n + 1):
                    deriv = diff(expr, x, i)
                    deriv_val = deriv.subs(x, x0_expr)
                    steps.append(f"$$f^{{({i})}}(x) = {latex(deriv)} \implies f^{{({i})}}({latex(x0_expr)}) = {latex(deriv_val)}$$")

                result = series(expr, x, x0_expr, n+1).removeO()
                steps.append(f"**Resultado da Série de Taylor (ordem {n}):**")
                steps.append(f"$$f(x) \approx {latex(result)}$$")

                render_steps(steps, "Cálculo da Série de Taylor")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")

    with tabs[4]: # Transformada de Laplace
        func_str = st.text_input("Função f(t):", "t*exp(-a*t)", key="transf_func")
        transf_type = st.radio("Tipo:", ["Direta", "Inversa"], key="transf_type", horizontal=True)

        if st.button("Calcular Transformada", key="transf_calc"):
            try:
                t, s, a = symbols('t s a')
                expr = parse_expr(func_str.replace('^','**'))
                steps = []

                if transf_type == "Direta":
                    steps.append(f"Calculando a Transformada de Laplace de $f(t) = {latex(expr)}$:")
                    steps.append("$$\mathcal{{L}}\{{f(t)\}} = F(s) = \int_0^{\infty} f(t) e^{{-st}} dt$$")
                    result = laplace_transform(expr, t, s, noconds=True)
                    steps.append("**Resultado:**")
                    steps.append(f"$$F(s) = {latex(result)}$$")
                else:
                    steps.append(f"Calculando a Transformada Inversa de Laplace de $F(s) = {latex(expr)}$:")
                    steps.append("$$\mathcal{{L}}^{{-1}}\{{F(s)\}} = f(t)$$")
                    result = inverse_laplace_transform(expr, s, t)
                    steps.append("**Resultado:**")
                    steps.append(f"$$f(t) = {latex(result)}$$")

                render_steps(steps, f"Cálculo da Transformada {transf_type} de Laplace")

            except Exception as e:
                st.error(f"❌ **Erro no cálculo:** {e}")


def graphing_calculator():
    st.header("Calculadora Gráfica")
    func_str = st.text_input("Função f(x) para plotar:", "sin(x) * exp(-x/10)", key="graph_func")

    col1, col2, col3 = st.columns(3)
    x_min = col1.number_input("X mínimo:", value=-10.0)
    x_max = col2.number_input("X máximo:", value=10.0)
    points = col3.number_input("Pontos no gráfico:", 100, 5000, 1000)

    if st.button("Plotar Função", key="plot_func"):
        if not func_str:
            st.warning("Por favor, insira uma função.")
            return
        try:
            x = symbols('x')
            expr = parse_expr(func_str.replace('^', '**'))
            st.markdown("---")
            st.write("**Função a ser plotada:**")
            st.latex(f"f(x) = {latex(expr)}")
            plot_function(expr, x, (x_min, x_max), int(points))
        except Exception as e:
            st.error(f"❌ **Erro ao plotar:** {e}")

def main():
    st.markdown('<h1 class="header">🧮 Calculadora Avançada Pro</h1>', unsafe_allow_html=True)
    st.markdown("---")

    tool_options = [
        "Calculadora Básica",
        "Resolvedor de Equações",
        "Calculadora de Somatórios",
        "Cálculos Avançados (Cálculo)",
        "Calculadora Gráfica"
    ]

    st.sidebar.title("Ferramentas")
    selection = st.sidebar.radio("Escolha uma ferramenta:", tool_options)

    st.sidebar.markdown("---")
    st.sidebar.info("Esta aplicação utiliza as bibliotecas SymPy e Streamlit para fornecer uma calculadora simbólica interativa.")

    if selection == tool_options[0]:
        basic_calculator()
    elif selection == tool_options[1]:
        polynomial_solver()
    elif selection == tool_options[2]:
        summation_calculator()
    elif selection == tool_options[3]:
        advanced_calculator()
    elif selection == tool_options[4]:
        graphing_calculator()

if __name__ == "__main__":
    main()
