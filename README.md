# pyommlbuilder
A Python package that helps with building OMML tags for use in docx files.

For reference of OMML standards, please refer to P.3603-3723 of part 1 of ECMA-376, which defines the standards of Open Office XML, and can be downloaded [here](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/).

Simple example:

    from pyommlbuilder.main import Math, Fraction, Numerator, Denominator, SquareRoot, SuperscriptObject
    import docx

    expression = Math(
        "x=",
        Fraction(
            Numerator("-b±", SquareRoot([SuperscriptObject(["b", "2"]), "-4ac"])), 
            Denominator("2a"),
        ),
    )


    xml_element = expression._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)

    doc.save("quadratic.docx")

