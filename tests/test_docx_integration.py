import docx
from pyommlbuilder.main import MathPara, Math, Run, Text
from pyommlbuilder.helpers import hash_file


def test_simple_expresson():
    expression = MathPara(Math(Run(Text("x+3"))))
    xml_element = expression._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)
    doc_blob = doc._part.blob
    assert len(doc_blob) == 1630
    assert b"w:r" in doc_blob
    assert b"x+3" in doc_blob
