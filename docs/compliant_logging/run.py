# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from a import a_method
import logging
import sys
from shrike.compliant_logging import enable_compliant_logging, DataCategory

enable_compliant_logging()
log = logging.getLogger(__name__)

if __name__ == "__main__":
    a_method()
    log.info("hi from entry point", category=DataCategory.PUBLIC)
