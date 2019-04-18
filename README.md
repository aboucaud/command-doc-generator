CCS command documentation helper
================================

List the available commands information such as the name, the level, the type and the description.


Usage
-----
Use the command-line tool `parse-commands` to list the commands either on a given file or in a directory.

- on a single file
    ```
    parse-commands JavaFile.java
    ```
- on a full directory to process recursively all .java files
    ```
    parse-commands java_project_dir
    ```

Example
-------

#### Working example

```bash
$ parse-commands SimuEPOSController.java
SimuEPOSController.java:
Command(name=setPosition, type=ACTION, level=ENGINEERING1, desc=For simulator only : Update position with a position given as argument.)
Command(name=checkFault, type=QUERY, level=ENGINEERING1, desc=Check if the Controller is in fault.)
```

#### Missing argument example

```bash
$ parse-commands SimuLoaderStandalonePlutoGateway.java
SimuLoaderStandalonePlutoGateway.java:
=> simulation/SimuLoaderStandalonePlutoGateway.java: issue at line 39: Missing command argument 'description'.
```

Installation
------------
```
pip install git+https://github.com/aboucaud/command-doc-generator.git
```

Author
------
Alexandre Boucaud <aboucaud@apc.in2p3.fr>