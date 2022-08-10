from ast import Expression
import lxml
from pyommlbuilder.main import (
    ElementList,
    Run,
    Text,
    NormalText,
    RunPropertyNormalText,
    WrappedTextElement,
    AlignedEqual,
    Fraction,
    FractionPropertyBarType,
    Radical,
    SquareRoot,
)


def test_simple_expression():
    expression = Run(Text("x+3"))
    assert expression._render_to_omml() == "<m:r><m:t>x+3</m:t></m:r>"
    xml_element = expression._as_xml_element()
    assert isinstance(xml_element, lxml.etree._Element)
    assert xml_element.tag == "m:r"
    children = xml_element.getchildren()
    assert len(children) == 1
    first_child = children[0]
    assert first_child.tag == "m:t"
    assert first_child.text == "x+3"


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
    expression = Fraction([FractionPropertyBarType(), Run(Text(1)), Run(Text(3))])
    assert (
        expression._render_to_omml()
        == '<m:f><m:fPr><m:type m:val="skw" /></m:fPr><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>3</m:t></m:r></m:den></m:f>'
    )


def test_square_root():
    expression = SquareRoot(WrappedTextElement("x+5"))
    assert (
        expression._render_to_omml()
        == '<m:rad><m:radPr><m:degHide m:val="1" /></m:radPr><m:deg /><m:e><m:r><m:t>x+5</m:t></m:r></m:e></m:rad>'
    )


def test_radical():
    expression = Radical([WrappedTextElement("3"), WrappedTextElement("2x-4")])
    assert (
        expression._render_to_omml()
        == "<m:rad><m:deg><m:r><m:t>3</m:t></m:r></m:deg><m:e><m:r><m:t>2x-4</m:t></m:r></m:e></m:rad>"
    )
