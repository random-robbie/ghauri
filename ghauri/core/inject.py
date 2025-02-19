#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=R,W,E,C

"""

Author  : Nasir Khan (r0ot h3x49)
Github  : https://github.com/r0oth3x49
License : MIT


Copyright (c) 2016-2025 Nasir Khan (r0ot h3x49)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the
Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import random
from ghauri.common.config import conf
from ghauri.core.request import request
from ghauri.logger.colored_logger import logger
from ghauri.common.lib import re, time, collections, quote, unquote, URLError
from ghauri.common.utils import (
    prepare_attack_request,
)


def inject_expression(
    url,
    data,
    proxy,
    delay=0,
    timesec=5,
    timeout=30,
    headers=None,
    parameter=None,
    expression=None,
    is_multipart=False,
    injection_type=None,
):
    attack = None
    attack_url = url
    attack_data = data
    attack_headers = headers
    # expression = (
    #     urlencode(value=expression)
    #     if injection_type.upper() not in ["HEADER"]
    #     else expression
    # )
    if conf.timeout and conf.timeout > 30:
        timeout = conf.timeout
    if injection_type in ["HEADER", "COOKIE"]:
        attack_headers = prepare_attack_request(
            headers,
            expression,
            param=parameter,
            injection_type=injection_type,
        )
    if injection_type == "GET":
        attack_url = prepare_attack_request(
            url,
            expression,
            param=parameter,
            encode=True,
            injection_type=injection_type,
        )

    if injection_type == "POST":
        attack_data = prepare_attack_request(
            data,
            expression,
            param=parameter,
            encode=True,
            injection_type=injection_type,
        )
    try:
        attack = request.perform(
            url=attack_url,
            data=attack_data,
            proxy=conf.proxy,
            headers=attack_headers,
            is_multipart=conf.is_multipart,
            timeout=timeout,
        )
        if attack.status_code == 401:
            logger.warning(
                "It seems the session got expired, update the session and re-run"
            )
            logger.end("ending")
            exit(0)
    except URLError as e:
        logger.critical(f"error: {e}")
        logger.end("ending")
        exit(0)
    except ConnectionAbortedError as e:
        raise e
    except ConnectionRefusedError as e:
        raise e
    except ConnectionResetError as e:
        raise e
    except KeyboardInterrupt as e:
        raise e
    except TimeoutError as e:
        raise e
    except Exception as e:
        raise e
    return attack
