from .main import Function, Run, RunPropertyPlainStyle, Text, Element, SuperscriptObject
from typing import Union


def sin(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("sin")), arg)


def cos(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("cos")), arg)


def tan(arg: Union[Element, str]):
    return Function(Run(RunPropertyPlainStyle(), Text("tan")), arg)


def square(arg: Union[Element, str]):
    return SuperscriptObject(Run(arg), "2")


def cube(arg: Union[Element, str]):
    return SuperscriptObject(Run(arg), "3")
