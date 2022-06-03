# Package Management

Example of using pip to add a dependency:
```shell
pip install python-decouple
```

Then update `requirements.txt` using `freeze` (which outputs installed packages in requirements format):
```shell
pip freeze > requirements.txt
```