from pyommlbuilder.main import Run, Text


def test_simple_expression():
    expression = Run([Text("x+3")])
    assert expression._render_to_omml() == "<m:r><m:t>x+3</m:t></m:r>"
