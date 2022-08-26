from pyommlbuilder.functions import sin

def test_sin():
    expression = sin("θ")
    assert expression._render_to_omml() == '<m:func><m:fName><m:r><m:rPr><m:sty m:val="p" /></m:rPr><m:t>sin</m:t></m:r></m:fName><m:e><m:r><m:t>θ</m:t></m:r></m:e></m:func>'