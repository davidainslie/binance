# Setup

## Python

```shell
brew update
brew upgrade python

vim ~/.zshrc

# Add the following:
alias python=/usr/local/bin/python3

# Then
source ~/.zshrc

python
Python 3.9.4 (default, Apr  5 2021, 01:50:46)
```

## Pyenv

```shell
brew install pyenv

pyenv install --list

pyenv install 3.9.4

pyenv global 3.9.4

pyenv versions
  system
  3.7.0
* 3.9.4 (set by /Users/davidainslie/.pyenv/version)
```

## Python style (format)

```shell
brew install pycodestyle
```

```shell
vim ~/.config/pycodestyle

[pycodestyle]
indent-size = 2
```

Shadowing names:
- Disable in Pycharm via: `Settings/Preferences > Editor > Inspections > Shadowing Names`.

## Package Management

Example of using pip to add a dependency:
```shell
pip install python-decouple
```

Then update `requirements.txt` using `freeze` (which outputs installed packages in requirements format):
```shell
pip freeze > requirements.txt
```

## Jupyter notebook

To pick up changes to external functions used in a notebook, have the following initial cell in your notebook:
```jupyter
%load_ext autoreload
%autoreload 2
```