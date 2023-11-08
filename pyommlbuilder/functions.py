from .main import Function, Run, RunPropertyPlainStyle, Text, Element
from typing import Union


def sin(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("sin")), arg)


def cos(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("cos")), arg)


def tan(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("tan")), arg)
