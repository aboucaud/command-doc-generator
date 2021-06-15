CCS command documentation helper
================================

[![License][license-badge]][license-web]
[![CI][ci-badge]][ci-web]
[![PyPI][pypi-badge]][pypi-web]

List the available commands information such as the name, the level, the type and the description.

[ci-web]: https://github.com/aboucaud/command-doc-generator/actions
[ci-badge]: https://github.com/aboucaud/command-doc-generator/workflows/test%20suite/badge.svg?style=flat
[license-badge]: https://img.shields.io/badge/license-BSD-blue.svg?style=flat
[license-web]: https://choosealicense.com/licenses/bsd-3-clause/
[pypi-badge]: https://badge.fury.io/py/ccsdoc.svg?style=flat
[pypi-web]: https://pypi.org/project/ccsdoc/

Usage
-----

#### parse

Use the command-line tool `ccsdoc` to list the commands and configuration parameters either on a given file or in a directory.

- on a single file
    ```
    ccsdoc parse --path JavaFile.java
    ```
- on a full directory to process recursively all .java files
    ```
    ccsdoc parse --path java_project_dir
    ```

Commands or configuration parameters can be output to a directory.
```
ccsdoc parse --path JavaFile.java --to javafile_commands.csv
```

By default, both commands and configuration parameters are returned. In case only one of them is desired, pass in the corresponding flag: `--commands` or `--params`.

Use `ccsdoc parse -h` for details about the available options.
#### convert

The CSV table containing the commands can be converted to the desired format using [`pandoc`][pandoc]
```
# e.g. here to Microsoft Word
ccsdoc convert javafile_commands.csv --to docx
```

[pandoc]: https://pandoc.org/


Examples
--------

#### Working examples

```bash
$ ccsdoc parse --path simulation/SimuEPOSController.java
SimuEPOSController: simulation/SimuEPOSController.java

Command[name=setPosition, type=ACTION, level=ENGINEERING1, desc='For simulator only : update position with a position given as argument.', args=(int actualPosition)]
Command[name=checkFault, type=QUERY, level=ENGINEERING1, desc='Check if the controller is in fault.']
Command[name=enableAndWriteRelativePosition, type=ACTION, level=ENGINEERING3, desc='Enable controller and go to relative position. Doesn't check condition. Danger !!!!', args=(int pos)]
```

```bash
$ ccsdoc parse --path Autochanger.java --params
Autochanger: Autochanger.java

ConfigurationParameter[name=timeToUpdateProtectionSystem, type=long, desc='Time to wait until protection system signals are updated', category=autochanger, units=milliseconds, range=[UNDEFINED, UNDEFINED]]
ConfigurationParameter[name=waitTimeForBrakeOC, type=int, desc='Time to wait between activatebrake and disableoperation for online clamps', category=autochanger, units=milliseconds, range=[UNDEFINED, UNDEFINED]]
ConfigurationParameter[name=waitTimeForBrakeLR, type=int, desc='Time to wait between activatebrake and disableoperation for linear rails', category=autochanger, units=milliseconds, range=[UNDEFINED, UNDEFINED]]
```
#### Missing argument example

```bash
$ ccsdoc parse --path SimuLoaderStandalonePlutoGateway.java
SimuLoaderStandalonePlutoGateway:
=> simulation/SimuLoaderStandalonePlutoGateway.java: issue at line 39: Missing command argument 'description'.
```

Installation
------------
```
pip install ccsdoc
```

Author
------
Alexandre Boucaud <aboucaud@apc.in2p3.fr> (CNRS/IN2P3)

License
-------
BSD 3-Clause license, see the [LICENSE file](LICENSE) for more information
