# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import logging
from typing import Any

import requests


class BasePlugin:
    name = "base"
    required_config: list[str] = []

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.session = {}

    def setup(self):
        pass

    def check_config(self):
        missing = []
        for key in self.required_config:
            if not self.config.get(self.name, key):
                missing.append(key)
        return missing

    def auth(self) -> bool:
        raise NotImplementedError

    def add_time_entry(self, **kwargs) -> Any:
        raise NotImplementedError

    def register_subcommand(self, subparsers):
        # Optional override for plugins to add their own CLI args
        pass

    def execute_subcommand(self, args):
        # Executed if a subcommand is matched
        pass

    def rget(self, url, **kwargs):
        return requests.get(url, **kwargs)

    def rpost(self, url, **kwargs):
        return requests.post(url, **kwargs)

    def status(self):
        pass
