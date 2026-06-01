# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import importlib
import logging
import os
import pkgutil

import gnome_pomodoro_tracking.frontends as frontends_pkg


class FrontendManager:
    def __init__(self, config, tracker):
        self.config = config
        self.tracker = tracker
        self.frontends = []
        self.logger = logging.getLogger(__name__)
        self.discover_frontends()

    def discover_frontends(self):
        pkg_path = os.path.dirname(frontends_pkg.__file__)
        for _, name, ispkg in pkgutil.iter_modules([pkg_path]):
            if not ispkg and name != "base":
                try:
                    module = importlib.import_module(f"gnome_pomodoro_tracking.frontends.{name}")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and hasattr(attr, "name")
                            and attr.__name__ != "BaseFrontend"
                        ):
                            # Basic heuristic: class has 'name' attribute
                            from gnome_pomodoro_tracking.frontends.base import BaseFrontend

                            if issubclass(attr, BaseFrontend):
                                self.frontends.append(attr(self.config, self.tracker))
                except Exception as e:
                    self.logger.error(f"Error loading frontend {name}: {e}")

    def register_arguments(self, parser):
        for frontend in self.frontends:
            frontend.register_arguments(parser)

    def handle(self, args):
        for frontend in self.frontends:
            if frontend.handle(args):
                return True
        return False
