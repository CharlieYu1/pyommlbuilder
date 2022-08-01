from textwrap import wrap
from pyommlbuilder.main import Run, Text, Fraction
from pyommlbuilder.helpers import wrap_text_in_r_t, make_aligned_equation


def test_wrap_text_in_r_t():
    expression1 = "2x+y"
    expression2 = Text("2x+y")
    expression3 = Run([Text("2x+y")])
    correct_output = "<m:r><m:t>2x+y</m:t></m:r>"
    assert wrap_text_in_r_t(expression1)._render_to_omml() == correct_output
    assert wrap_text_in_r_t(expression2)._render_to_omml() == correct_output
    assert wrap_text_in_r_t(expression3)._render_to_omml() == correct_output


def test_make_aligned_equation():
    left = wrap_text_in_r_t("x+3")
    right = Fraction([wrap_text_in_r_t("2"), wrap_text_in_r_t("x-2")])
    assert left._render_to_omml() == "<m:r><m:t>x+3</m:t></m:r>"
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
        make_aligned_equation(left, right)._render_to_omml().replace(" ", "")
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
