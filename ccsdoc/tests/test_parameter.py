from ccsdoc.parameter import Argument
from ccsdoc.parameter import ConfigurationParameter

NAME = "standbyPosition"
TYPE = "int"
DESCRIPTION = "Position at standby on the trucks in microns"


def test_configparameter_simple():
    cmd = ConfigurationParameter(name=NAME, ptype=TYPE, description=DESCRIPTION)

    assert repr(cmd) == f"{TYPE} {NAME}: {DESCRIPTION}"
    assert str(cmd) == f"ConfigurationParameter[name={NAME}, type={TYPE}, desc='{DESCRIPTION}']"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{TYPE},{DESCRIPTION}\n"

def test_configparameter_nodescription():
    cmd = ConfigurationParameter(name=NAME, ptype=TYPE, description=None)

    assert repr(cmd) == f"{TYPE} {NAME}"
    assert str(cmd) == f"ConfigurationParameter[name={NAME}, type={TYPE}]"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{TYPE},\n"

def test_configparameter_deprecated():
    cmd = ConfigurationParameter(name=NAME, ptype=TYPE, description=DESCRIPTION, is_deprecated=True)

    assert repr(cmd) == f"{TYPE} {NAME}: {DESCRIPTION}"
    assert str(cmd) == f"ConfigurationParameter[name={NAME}, type={TYPE}, desc='{DESCRIPTION}'](DEPRECATED)"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{TYPE},{DESCRIPTION}\n"

def test_configparameter_nodescription_deprecated():
    cmd = ConfigurationParameter(name=NAME, ptype=TYPE, description=None, is_deprecated=True)

    assert repr(cmd) == f"{TYPE} {NAME}"
    assert str(cmd) == f"ConfigurationParameter[name={NAME}, type={TYPE}](DEPRECATED)"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{TYPE},\n"


def test_argument_simple():
    cmd = Argument(name=NAME, ptype=TYPE)

    assert repr(cmd) == f"{TYPE} {NAME}"
    assert str(cmd) == f"Argument[name={NAME}, type={TYPE}]"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{TYPE},\n"
