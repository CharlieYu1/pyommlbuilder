# pyommlbuilder
A Python package that helps with building OMML tags for use in docx files.

For reference of OMML standards, please refer to P.3603-3723 of part 1 of ECMA-376, which defines the standards of Open Office XML, and can be downloaded [here](https://www.ecma-international.org/publications-and-standards/standards/ecma-376/).

Example of quadratic equation:

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


Example of an equation block:

    from pyommlbuilder.main import MathPara
    import docx

    line1 = make_aligned_equation("x+3", "8")
    line2 = make_aligned_equation("x", "8-3")
    line3 = make_aligned_equation("", "5")

    equation_block = MathPara(line1, line2, line3)

    xml_element = equation_block._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)
    
    doc.save("equation_block.docx")


