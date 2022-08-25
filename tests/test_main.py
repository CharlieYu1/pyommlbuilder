from ast import Expression
import lxml
from pyommlbuilder.main import (
    ElementList,
    Run,
    Text,
    RunPropertyNormalText,
    AlignedEqual,
    Numerator,
    Denominator,
    Fraction,
    FractionPropertyBarType,
    Radical,
    SquareRoot,
    SuperscriptObject,
    SubscriptObject,
    Math,
    Function,
    RunPropertyPlainStyle,
    FunctionName,
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
    expression = ElementList("x+3", 12)
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
    expression = Fraction(FractionPropertyBarType(), 1, 3)
    assert (
        expression._render_to_omml()
        == '<m:f><m:fPr><m:type m:val="skw" /></m:fPr><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>3</m:t></m:r></m:den></m:f>'
    )


def test_square_root():
    expression = SquareRoot("x+5")
    assert (
        expression._render_to_omml()
        == '<m:rad><m:radPr><m:degHide m:val="1" /></m:radPr><m:deg /><m:e><m:r><m:t>x+5</m:t></m:r></m:e></m:rad>'
    )


def test_radical():
    expression = Radical(3, "2x-4")
    assert (
        expression._render_to_omml()
        == "<m:rad><m:deg><m:r><m:t>3</m:t></m:r></m:deg><m:e><m:r><m:t>2x-4</m:t></m:r></m:e></m:rad>"
    )


def test_superscript():
    expression = SuperscriptObject("x", "2")
    assert (
        expression._render_to_omml()
        == "<m:sSup><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>"
    )


def test_radical_and_superscript():
    expression = SuperscriptObject(["(", Radical(3, "2x-4"), "+7)"], 2)
    assert (
        expression._render_to_omml()
        == "<m:sSup><m:e><m:r><m:t>(</m:t></m:r><m:rad><m:deg><m:r><m:t>3</m:t></m:r></m:deg><m:e><m:r><m:t>2x-4</m:t></m:r></m:e></m:rad><m:r><m:t>+7)</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup>"
    )


def test_subscript():
    expression = SubscriptObject("x", 2)
    assert (
        expression._render_to_omml()
        == "<m:sSub><m:e><m:r><m:t>x</m:t></m:r></m:e><m:sub><m:r><m:t>2</m:t></m:r></m:sub></m:sSub>"
    )


def test_quadratic_equation():
    expression = Math(
        "x=",
        Fraction(
            Numerator(
                "-b±",
                SquareRoot(
                    [
                        SuperscriptObject(
                            "b",
                            2,
                        ),
                        "-4ac",
                    ],
                ),
            ),
            Denominator("2a"),
        ),
    )

    assert (
        expression._render_to_omml()
        == '<m:oMath><m:r><m:t>x=</m:t></m:r><m:f><m:num><m:r><m:t>-b±</m:t></m:r><m:rad><m:radPr><m:degHide m:val="1" /></m:radPr><m:deg /><m:e><m:sSup><m:e><m:r><m:t>b</m:t></m:r></m:e><m:sup><m:r><m:t>2</m:t></m:r></m:sup></m:sSup><m:r><m:t>-4ac</m:t></m:r></m:e></m:rad></m:num><m:den><m:r><m:t>2a</m:t></m:r></m:den></m:f></m:oMath>'
    )


def test_run_property_plain_style():
    expression = RunPropertyPlainStyle()
    assert expression._render_to_omml() == '<m:rPr><m:sty m:val="p" /></m:rPr>'


def test_function():
    expression = Function(Run(RunPropertyPlainStyle(), Text("sin")), "30°")
    assert (
        expression._render_to_omml()
        == '<m:func><m:fName><m:r><m:rPr><m:sty m:val="p" /></m:rPr><m:t>sin</m:t></m:r></m:fName><m:e><m:r><m:t>30°</m:t></m:r></m:e></m:func>'
    )
