from ccsdoc.parameter import ConfigParameter

NAME = "standbyPosition"
DESCRIPTION = "Position at standby on the trucks in microns"


def test_configparameter_simple():
    cmd = ConfigParameter(name=NAME, description=DESCRIPTION)

    assert repr(cmd) == f"{NAME}: {DESCRIPTION}"
    assert str(cmd) == f"ConfigParameter[name={NAME}, desc='{DESCRIPTION}']"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{DESCRIPTION}\n"

def test_configparameter_deprecated():
    cmd = ConfigParameter(name=NAME, description=DESCRIPTION, deprecated=True)

    assert repr(cmd) == f"{NAME}: {DESCRIPTION}"
    assert str(cmd) == f"ConfigParameter[name={NAME}, desc='{DESCRIPTION}']"
    assert cmd.to_csv("Toto") == f"Toto,{NAME},{DESCRIPTION}\n"
