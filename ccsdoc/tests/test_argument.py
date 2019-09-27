from ccsdoc.argument import Argument

NAME = "filterId"
TYPE = "str"


def test_argument_simple():
    arg = Argument(name=NAME, ptype=TYPE)

    assert repr(arg) == f"{TYPE} {NAME}"
    assert str(arg) == f"Argument[name={NAME}, type={TYPE}]"
