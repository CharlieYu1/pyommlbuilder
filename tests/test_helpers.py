from textwrap import wrap
from pyommlbuilder.main import Run, Text, Fraction, wrap_text, MathPara, MathPara
from pyommlbuilder.helpers import make_aligned_equation, normal_text
from pyommlbuilder.functions import square


def test_wrap_text():
    expression1 = "2x+y"
    expression2 = Run(Text("2x+y"))
    correct_output = "<m:r><m:t>2x+y</m:t></m:r>"
    assert wrap_text(expression1)._render_to_omml() == correct_output
    assert wrap_text(expression2)._render_to_omml() == correct_output


def test_normal_test():
    expression1 = normal_text("This is normal text")
    correct_output = "<m:r><m:rPr><m:nor /></m:rPr><m:t>This is normal text</m:t></m:r>"
    assert wrap_text(expression1)._render_to_omml() == correct_output


def test_make_aligned_equation():
    left = "x+3"
    right = Fraction(2, "x-2")

    assert (
        right._render_to_omml()
        == """
            <m:f>
                <m:num><m:r><m:t>2</m:t></m:r></m:num>
                <m:den><m:r><m:t>x-2</m:t></m:r></m:den>
            </m:f>""".replace(
            " ", ""
        ).replace(
            "\n", ""
        )
    )

    assert (
        make_aligned_equation(left, right, line_break=False)
        ._render_to_omml()
        .replace(" ", "")
        == """
            <m:oMath>
                <m:r><m:t>x+3</m:t></m:r>
                <m:r><m:rPr><m:aln /></m:rPr><m:t>=</m:t></m:r>
                <m:f>
                    <m:num><m:r><m:t>2</m:t></m:r></m:num><m:den>
                    <m:r><m:t>x-2</m:t></m:r></m:den>
                </m:f>
            </m:oMath>""".replace(
            " ", ""
        ).replace(
            "\n", ""
        )
    )
    
def test_square_in_aligned_equation():
    equation_block = MathPara(
        make_aligned_equation(
            square(Text("a")), [
                square(Text("b")), "+", square(Text("c")), " ",
                normal_text("(Pyth's thm)")]
        ),
    )
    assert (
        equation_block
        ._render_to_omml()
        .replace(" ", "")
        == """
            <m:oMathPara>
                <m:oMath>
                    <m:sSup>
                        <m:e><m:r><m:t>a</m:t></m:r></m:e>
                        <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                    </m:sSup>
                    <m:r>
                        <m:rPr><m:aln /></m:rPr><m:t>=</m:t>
                    </m:r>
                    <m:sSup>
                        <m:e><m:r><m:t>b</m:t></m:r></m:e>
                        <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                    </m:sSup>
                    <m:r>
                        <m:t>+</m:t>
                    </m:r>
                    <m:sSup>
                        <m:e><m:r><m:t>c</m:t></m:r></m:e>
                        <m:sup><m:r><m:t>2</m:t></m:r></m:sup>
                    </m:sSup>
                    <m:r>
                        <m:t></m:t>
                    </m:r>
                    <m:r>
                        <m:rPr>
                            <m:nor />
                        </m:rPr>
                        <m:t>(Pyth's thm)</m:t>
                    </m:r>
                    <w:br />
                </m:oMath>
            </m:oMathPara>""".replace(
            " ", ""
        ).replace(
            "\n", ""
        )
    )


def test_make_aligned_equation_block():
    line1 = make_aligned_equation("x+3", 8)
    line2 = make_aligned_equation("x", "8-3")
    line3 = make_aligned_equation("", 5)

    equation_block = MathPara(line1, line2, line3)
    print(equation_block._render_to_omml())
    assert (
        equation_block._render_to_omml()
        == "<m:oMathPara><m:oMath><m:r><m:t>x+3</m:t></m:r><m:r><m:rPr><m:aln /></m:rPr><m:t>=</m:t></m:r><m:r><m:t>8</m:t></m:r><w:br /></m:oMath><m:oMath><m:r><m:t>x</m:t></m:r><m:r><m:rPr><m:aln /></m:rPr><m:t>=</m:t></m:r><m:r><m:t>8-3</m:t></m:r><w:br /></m:oMath><m:oMath><m:r><m:t></m:t></m:r><m:r><m:rPr><m:aln /></m:rPr><m:t>=</m:t></m:r><m:r><m:t>5</m:t></m:r><w:br /></m:oMath></m:oMathPara>"
    )
