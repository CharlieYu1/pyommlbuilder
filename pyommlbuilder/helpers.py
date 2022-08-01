from .main import Run, Text, Element, ElementList, AlignedEqual, Math


def make_aligned_equation(left: ElementList, right: ElementList):
    if not isinstance(left, ElementList):
        left = ElementList([left])
    if not isinstance(right, ElementList):
        right = ElementList([right])
    return Math(left._elements + [AlignedEqual()] + right._elements)
