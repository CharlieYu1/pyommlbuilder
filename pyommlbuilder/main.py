from typing import List, Union, Any


class Element(object):
    omml_tag = "m:e"

    def __init__(self, elements, **kwargs):
        self._elements = elements
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
        return f"<{cls.omml_tag}{xml_attributes}>{''.join(rendered_elements)}</{cls.omml_tag}>"


class Run(Element):
    omml_tag = "m:r"


class Text(Element):
    omml_tag = "m:t"

    def __init__(self, text: str, **kwargs):
        self.text = text
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

    def __init__(self, **kwargs):
        self._elements = None
        self.attributes = kwargs


class RunProperty(Element):
    omml_tag = "m:rPr"


class RunPropertyNormalText(RunProperty, EmptyElement):
    def __init__(self, **kwargs):
        self._elements = [NormalText()]
        self.attributes = kwargs


class LineBreak(EmptyElement):
    omml_tag = "w:br"


class Math(Element):
    omml_tag = "m:omath"


class MathPara(Element):
    omml_tag = "m:oMathPara"


class FractionProperty(Element):
    omml_tag = "m:fPr"


class Numerator(Element):
    omml_tag = "m:num"


class Denominator(Element):
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
