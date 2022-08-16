from sympy.abc import x, y
from sympy import StrPrinter

from pyommlbuilder.main import Run, Text

def test_simple_sympy_expression():
    expr = Run(Text(x+y))
    assert expr._render_to_omml() == "<m:r><m:t>x + y</m:t></m:r>"
