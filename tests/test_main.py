from ast import Expression
from pyommlbuilder.main import (
    Run,
    Text,
    NormalText,
    RunPropertyNormalText,
    Fraction,
    FractionPropertyBarType,
)


def test_simple_expression():
    expression = Run([Text("x+3")])
    assert expression._render_to_omml() == "<m:r><m:t>x+3</m:t></m:r>"


def test_element_property():
    expression = Text("abc ", **{"xml:space": "preserve"})
    assert expression._render_to_omml() == '<m:t xml:space="preserve">abc </m:t>'


def test_run_property_normal_text():
    expression = RunPropertyNormalText()
    assert expression._render_to_omml() == "<m:rPr><m:nor /></m:rPr>"


def test_fraction():
    expression = Fraction([FractionPropertyBarType(), Run([Text(1)]), Run([Text(3)])])
    assert (
        expression._render_to_omml()
        == '<m:f><m:fPr><m:type m:val="skw" /></m:fPr><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>3</m:t></m:r></m:den></m:f>'
    )
