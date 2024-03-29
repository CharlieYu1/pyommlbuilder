from .main import (
    Run,
    Text,
    Element,
    ElementList,
    AlignedEqual,
    LineBreak,
    Math,
    RunPropertyNormalText,
)
import hashlib


def make_aligned_equation(
    left: ElementList, right: ElementList, line_break: bool = True
):
    if not isinstance(left, ElementList):
        left = ElementList(left)
    if not isinstance(right, ElementList):
        right = ElementList(right)
    return_value = Math(left._elements + [AlignedEqual()] + right._elements)
    if line_break:
        return_value.append(LineBreak())
    return return_value


def normal_text(text):
    return Run(RunPropertyNormalText(), Text(text))


def save_xml_element_as_docx(element: Element, filename: str):
    import docx

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(element._as_xml_element())
    doc.save(filename)


def hash_file(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
