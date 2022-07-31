from ast import Expression
from pyommlbuilder.main import (
    ElementList,
    Run,
    Text,
    NormalText,
    RunPropertyNormalText,
    AlignedEqual,
    Fraction,
    FractionPropertyBarType,
)


def test_simple_expression():
    expression = Run([Text("x+3")])
    assert expression._render_to_omml() == "<m:r><m:t>x+3</m:t></m:r>"


def test_element_property():
    expression = Text("abc ", **{"xml:space": "preserve"})
    assert expression._render_to_omml() == '<m:t xml:space="preserve">abc </m:t>'


def test_element_list():
    expression = ElementList([Run([Text("x+3")]), Run([Text("12")])])
    assert (
        expression._render_to_omml()
        == "<m:r><m:t>x+3</m:t></m:r><m:r><m:t>12</m:t></m:r>"
    )


def test_run_property_normal_text():
    expression = RunPropertyNormalText()
    assert expression._render_to_omml() == "<m:rPr><m:nor /></m:rPr>"


def test_aligned_equal():
    expression = AlignedEqual()
    assert (
        expression._render_to_omml()
        == "<m:r><m:rPr><m:aln /></m:rPr><m:t>=</m:t></m:r>"
    )


def test_fraction():
    expression = Fraction([FractionPropertyBarType(), Run([Text(1)]), Run([Text(3)])])
    assert (
        expression._render_to_omml()
        == '<m:f><m:fPr><m:type m:val="skw" /></m:fPr><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>3</m:t></m:r></m:den></m:f>'
    )
