"""
plots a title graphic with matplotlib
"""
from geometor.render import *
from rich import inspect

def run():

    titler = Titler('test')

    t1 = sp.sqrt(2)
    
    text2 = r"\begin{align*}"
    text2 += f"{sp.latex(t1)} &= {t1.evalf():.4f}"
    text2 += "\\\\"
    text2 += r"x^2 - x - 1 &= 0"
    text2 += r"\end{align*}"

    text2 = r"test \textcolor{red}{test}"
    text2 = r"test \bf{test} test"
    #  text2 = r"""
#  $
#  \color{yellow} A
#  \begingroup\color{magenta}=\endgroup
#  \textcolor{blue}{B}
#  \mathbin{\color{red}-}
#  \textcolor{green}{C}
#  \begingroup\color{cyan}+\endgroup
#  D
#  $
#  """

    print(text2)
    titler.plot_title(text2, ".","title.png")
    plt.show()

if __name__ == '__main__':
    run()
