# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import logging
import sys
from shrike.compliant_logging import DataCategory


def a_method():
    log = logging.getLogger(__name__)
    log.info("hi from a", category=DataCategory.PUBLIC)
