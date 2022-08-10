# pyommlbuilder
A Python package that helps with building OMML tags for use in docx files.

Simple example:

    from pyommlbuilder.main import Math, Fraction, Numerator, Denominator, SquareRoot, SuperscriptObject
    import docx

    expression = Math([
        "x=",
        Fraction([
            Numerator(["-b±", SquareRoot([SuperscriptObject(["b", "2"]), "-4ac"])]), 
            Denominator("2a"),
        ]),
    ])


    xml_element = expression._as_xml_element()

    doc = docx.Document()
    p = doc.add_paragraph()
    p._element.append(xml_element)

    doc.save("quadratic.docx")