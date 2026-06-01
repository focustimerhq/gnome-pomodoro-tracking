# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse
import logging


class BaseFrontend:
    name = "base"

    def __init__(self, config, tracker):
        self.config = config
        self.tracker = tracker
        self.logger = logging.getLogger(__name__)

    def register_arguments(self, parser: argparse.ArgumentParser):
        pass

    def handle(self, args: argparse.Namespace) -> bool:
        """
        Return True if the frontend handled the command and execution should stop.
        """
        return False
