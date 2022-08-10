from typing import List, Union, Sequence, Any
from lxml import etree as ET


class Element(object):
    omml_tag = "m:e"

    def __init__(self, elements, **kwargs):
        if isinstance(elements, list):
            self._elements = elements
        else:
            self._elements = [elements]
        self.attributes = kwargs

    def __eq__(self, other: "Element"):
        return (self._elements == other._elements) and (
            self.attributes == other.attributes
        )

    def append(self, element: "Element"):
        self._elements.append(element)

    def _render_to_omml(self):
        cls = self.__class__
        xml_attributes = "".join(
            [
                " " + key + "=" + '"' + self.attributes[key] + '"'
                for key in self.attributes
            ]
        )

        if not self._elements:
            return f"<{cls.omml_tag}{xml_attributes} />"
        rendered_elements = [element._render_to_omml() for element in self._elements]
        if not cls.omml_tag:
            return f"{''.join(rendered_elements)}"
        return f"<{cls.omml_tag}{xml_attributes}>{''.join(rendered_elements)}</{cls.omml_tag}>"

    def _as_xml_element(self):
        parser = ET.XMLParser(recover=True)
        return ET.fromstring(self._render_to_omml(), parser)


class ElementList(Element):
    omml_tag = None  # a list of elements that does not belong to a parent element

    def _as_xml_element(self):
        raise Exception("cannot convert an ElementList to a XML element")


class Run(Element):
    omml_tag = "m:r"


class Text(Element):
    omml_tag = "m:t"

    def __init__(self, text: str, **kwargs):
        self.text = str(text)
        self.attributes = kwargs

    def _render_to_omml(self):
        cls = self.__class__
        xml_attributes = "".join(
            [
                " " + key + "=" + '"' + self.attributes[key] + '"'
                for key in self.attributes
            ]
        )
        return f"<{cls.omml_tag}{xml_attributes}>{self.text}</{cls.omml_tag}>"


class EmptyElement(Element):
    def __init__(self, **kwargs):
        self._elements = None
        self.attributes = kwargs


class NormalText(EmptyElement):
    omml_tag = "m:nor"


class Align(EmptyElement):
    omml_tag = "m:aln"


class RunProperty(Element):
    omml_tag = "m:rPr"


class RunPropertyNormalText(RunProperty, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [NormalText()]
        self.attributes = kwargs


class RunPropertyAlign(RunProperty, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [Align()]
        self.attributes = kwargs


class AlignedEqual(Run, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [RunPropertyAlign(), Text("=")]
        self.attributes = kwargs


class LineBreak(EmptyElement):
    omml_tag = "w:br"


class Math(Element):
    omml_tag = "m:oMath"


class MathPara(Element):
    omml_tag = "m:oMathPara"


class WrappedTextElement(Element):
    omml_tag = None

    def __init__(self, elements, **kwargs):
        def wrap_text_in_r_t(maybe_text) -> Element:
            if isinstance(maybe_text, str):
                return Run(Text(maybe_text))
            if isinstance(maybe_text, Text):
                return Run(maybe_text)
            if isinstance(maybe_text, Run) and isinstance(
                maybe_text._elements[0], Text
            ):
                return maybe_text
            raise Exception("Input must be either text or text-like")

        if not isinstance(elements, list):
            elements = [wrap_text_in_r_t(elements)]
        super().__init__(elements, **kwargs)


class FractionProperty(Element):
    omml_tag = "m:fPr"


class BarType(EmptyElement):
    omml_tag = "m:type"

    def __init__(self, **kwargs):
        self._elements = None
        self.attributes = kwargs
        self.attributes["m:val"] = "skw"


class FractionPropertyBarType(FractionProperty, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [BarType()]
        self.attributes = kwargs


class Numerator(WrappedTextElement):
    omml_tag = "m:num"


class Denominator(WrappedTextElement):
    omml_tag = "m:den"


class Fraction(Element):
    omml_tag = "m:f"

    def __init__(self, elements, **kwargs):
        super().__init__(elements, **kwargs)
        if not isinstance(self._elements[-2], Numerator):
            self._elements[-2] = Numerator(self._elements[-2])
        if not isinstance(self._elements[-1], Denominator):
            self._elements[-1] = Denominator(self._elements[-1])
        assert (len(self._elements) == 2) or (
            len(self._elements) == 3 and isinstance(self._elements[0], FractionProperty)
        )


class RadicalProperty(Element):
    omml_tag = "m:radPr"


class DegreeHide(EmptyElement):
    omml_tag = "m:degHide"

    def __init__(self, **kwargs):
        self._elements = None
        self.attributes = kwargs
        self.attributes["m:val"] = "1"


class RadicalPropertyDegreeHide(RadicalProperty, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [DegreeHide()]
        self.attributes = kwargs


class RadicalDegree(Element):
    omml_tag = "m:deg"


class Radicand(Element):
    omml_tag = "m:e"


class Radical(Element):
    omml_tag = "m:rad"

    def __init__(self, elements, **kwargs):
        super().__init__(elements, **kwargs)
        if not isinstance(self._elements[-2], RadicalDegree):
            self._elements[-2] = RadicalDegree(self._elements[-2])
        if not isinstance(self._elements[-1], Radicand):
            self._elements[-1] = Radicand(self._elements[-1])
        assert (len(self._elements) == 2) or (
            len(self._elements) == 3 and isinstance(self._elements[0], RadicalProperty)
        )


class SquareRoot(Radical):
    def __init__(self, radicand, **kwargs):
        super().__init__([RadicalPropertyDegreeHide(), [], [radicand]], **kwargs)
