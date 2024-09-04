#!/usr/bin/env python
import os
import sys
import re
import logging
from typing import List


django_server_logger = logging.getLogger("django.server")


class StatusLogKiller(logging.Filter):
    """Strictly for noise reduction in development/testing."""

    def __init__(self, items: List[str], name: str = ""):
        super().__init__(name)
        self.items = items

    def filter(self, record):
        return (
            0 if any(re.search(x, record.args[0]) for x in self.items) else 1
        )

django_server_logger.addFilter(StatusLogKiller(["GET /a/.*/status/.*/"]))


class HostHeaderLogFilter(logging.Filter):
    """To suppress 'Invalid HTTP_HOST header' errors"""

    def filter(self, record):
        if 'Invalid HTTP_HOST header' in record.getMessage():
            return False
        return True

django_server_logger.addFilter(HostHeaderLogFilter())



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
