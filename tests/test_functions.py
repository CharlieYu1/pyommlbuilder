from pyommlbuilder.functions import sin, square
from pyommlbuilder.main import Text


def test_sin():
    expression = sin("θ")
    assert (
        expression._render_to_omml()
        == '<m:func><m:fName><m:r><m:rPr><m:sty m:val="p" /></m:rPr><m:t>sin</m:t></m:r></m:fName><m:e><m:r><m:t>θ</m:t></m:r></m:e></m:func>'
    )


def test_square():
    expression = square(Text("x"))
    assert (
        expression._render_to_omml()
        == "<m:sSup><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>"
    )
