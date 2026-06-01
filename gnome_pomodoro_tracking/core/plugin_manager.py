# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import importlib
import logging
import os
import pkgutil

import gnome_pomodoro_tracking.plugins as plugins_pkg


class PluginManager:
    def __init__(self, config):
        self.config = config
        self.plugins = {}
        self.logger = logging.getLogger(__name__)
        self.discover_plugins()

    def discover_plugins(self):
        pkg_path = os.path.dirname(plugins_pkg.__file__)
        for _, name, ispkg in pkgutil.iter_modules([pkg_path]):
            if not ispkg and name != "base":
                try:
                    module = importlib.import_module(f"gnome_pomodoro_tracking.plugins.{name}")
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (
                            isinstance(attr, type)
                            and hasattr(attr, "name")
                            and attr.__name__ != "BasePlugin"
                        ):
                            # Basic heuristic: class has 'name' attribute
                            from gnome_pomodoro_tracking.plugins.base import BasePlugin

                            if issubclass(attr, BasePlugin):
                                self.plugins[attr.name] = attr
                except Exception as e:
                    self.logger.error(f"Error loading plugin {name}: {e}")

    def get_plugin(self, name):
        plugin_class = self.plugins.get(name)
        if plugin_class:
            return plugin_class(self.config)
        return None
