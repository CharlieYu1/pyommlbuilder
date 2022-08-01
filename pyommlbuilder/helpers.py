from unittest import expectedFailure
from pyommlbuilder.main import Run, Text, Element, ElementList, AlignedEqual, Math


def wrap_text_in_r_t(maybe_text) -> Element:
    if isinstance(maybe_text, str):
        return Run([Text(maybe_text)])
    if isinstance(maybe_text, Text):
        return Run([maybe_text])
    if isinstance(maybe_text, Run) and isinstance(maybe_text._elements[0], Text):
        return maybe_text
    raise Exception("Input must be either text or text-like")


def make_aligned_equation(left: ElementList, right: ElementList):
    if not isinstance(left, ElementList):
        left = ElementList([left])
    if not isinstance(right, ElementList):
        right = ElementList([right])
    return Math(left._elements + [AlignedEqual()] + right._elements)
