import docx
from pyommlbuilder.main import (
    MathPara,
    Math,
    Run,
    Text,
    Fraction,
    Numerator,
    Denominator,
    WrappedTextElement,
    SquareRoot,
    SuperscriptObject,
)
from pyommlbuilder.helpers import hash_file


def test_simple_expresson():
    expression = Math(Run(Text("x+3=10")))
    xml_element = expression._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)
    doc_blob = doc._part.blob
    assert len(doc_blob) == 1606
    assert b"w:r" in doc_blob
    assert b"x+3" in doc_blob


def test_quadratic_equation():
    expression = Math(
        [
            WrappedTextElement("x="),
            Fraction(
                [
                    Numerator(
                        [
                            WrappedTextElement("-b±"),
                            SquareRoot(
                                [
                                    SuperscriptObject(
                                        [
                                            WrappedTextElement("x"),
                                            WrappedTextElement("2"),
                                        ]
                                    ),
                                    WrappedTextElement("-4ac"),
                                ]
                            ),
                        ]
                    ),
                    Denominator(WrappedTextElement("2a")),
                ]
            ),
        ]
    )

    xml_element = expression._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)
    doc_blob = doc._part.blob
    print(doc_blob)
    assert len(doc_blob) == 1883
    assert b"degHide" in doc_blob
    assert b"m:num" in doc_blob
    assert b"4ac" in doc_blob
    assert b"\xc2\xb1" in doc_blob
