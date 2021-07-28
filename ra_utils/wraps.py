#!/usr/bin/env python3
# --------------------------------------------------------------------------------------
# SPDX-FileCopyrightText: 2021 Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
# --------------------------------------------------------------------------------------
from functools import wraps
from inspect import Parameter
from inspect import signature
from typing import Callable


def wraps_and_append_kwargs(original_func: Callable) -> Callable:
    """Like functools.wraps, but appends the original functions keyword arguments.

    Example:
        def foo(a, b):
            return a + b

        @wraps_and_append_kwargs(foo)
        def bar(*args, c, **kwargs):
            return foo(*args, **kwargs) * c

        # 'c' is appended to foo's signature
        # as such: signature(foo) == (a, b)
        # as such: signature(bar) == (a, b, *, c)

        assert bar(1, 2, c=3) == 9
        assert bar(1, c=2, b=3) == 8
        assert bar(c=1, b=2, a=3) == 5

        # Type error as c is a keyword-only argument
        bar(1, 2, 3)

    Example:
        from fastapi import FastAPI
        app = FastAPI()

        @app.get("/hello")
        def hello(name: str):
            return {"Hello": name}

        @app.get("/hello_fullname")
        @wraps_and_append_kwargs(hello)
        def hello_fullname(*args, lastname: str, **kwargs):
            result = hello(*args, **kwargs)
            result["Hello"] += " " + lastname
            return result

        Run and tested with:
        $ uvicorn filename:app
        $ curl http://localhost:8000/hello?name=John
        {"Hello": "John"}
        $ curl http://localhost:8000/hello_fullname?name=John&lastname=Deere
        {"Hello": "John Deere"}
    """

    def decorator(func: Callable) -> Callable:
        funcsig = signature(func)
        params_to_add = dict(funcsig.parameters)
        params_to_add.pop("args", None)
        params_to_add.pop("kwargs", None)
        params_to_add.pop("cls", None)
        params_to_add.pop("self", None)

        # Only support pure keyword arguments, as they can be appended safely
        error_msg = "'wraps_and_append_kwargs' only support pure keywork arguments"
        for param in params_to_add.values():
            assert param.kind == Parameter.KEYWORD_ONLY, error_msg

        # Create our wrapper function, and append our kwargs to it
        wrapper = wraps(original_func)(func)
        funcsig = signature(wrapper)
        params_in_original = funcsig.parameters
        params = list(params_in_original.values())
        params.extend(params_to_add.values())

        # Replace signature with modified version
        modified_signature = funcsig.replace(parameters=params)
        wrapper.__signature__ = modified_signature  # type: ignore
        return wrapper

    return decorator
