<!--
SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
SPDX-License-Identifier: MPL-2.0
-->

# RA Utils

RA Utils is a collection of utilities used by [OS2mo](https://github.com/OS2mo/os2mo) and friends.

## Requirements

Python 3.8+

Dependencies:

* <a href="https://more-itertools.readthedocs.io/" class="external-link" target="_blank">More Itertools</a>

## Installation

```console
$ pip install ra-utils
```
or:
```console
$ pip install ra-utils[all]
```
To install with all optional dependencies

## Usage
Usage depends on the utility used, but as an example `apply` can be used as:

```Python
from ra_utils.apply import apply

@apply
def dual(key, value):
    return value

print(dual(('k', 'v')))  # --> 'v'
```

## Optional Dependencies

* <a href="https://jinja.palletsprojects.com/" class="external-link" target="_blank">Jinja</a>
* <a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>
* <a href="https://docs.python-requests.org/" class="external-link" target="_blank">Requests</a>
* <a href="https://github.com/python/typeshed" class="external-link" target="_blank">Typeshed (types-requests)</a>

## License

This project is licensed under the terms of the MPL-2.0 license.
