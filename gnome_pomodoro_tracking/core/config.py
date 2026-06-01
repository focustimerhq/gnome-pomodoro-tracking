# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import configparser
import os


class ConfigManager:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser(
            "~/.local/share/gnome-pomodoro-tracking/config.ini"
        )
        self.config = configparser.ConfigParser()
        self._setup()

    def _setup(self):
        dirname = os.path.dirname(self.config_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        if not os.path.exists(self.config_path):
            self.config.add_section("settings")
            self.config.set("settings", "plugin", "")
            self.config.set("settings", "mintrace", "0")
            self.config.add_section("tracker")
            self.config.set("tracker", "type", "")
            self.config.set("tracker", "name", "")
            self.config.set("tracker", "start", "")
            self._write_config()
        else:
            self.config.read(self.config_path)

    def _write_config(self):
        with open(self.config_path, "w") as f:
            self.config.write(f)

    def get(self, section, key, default=None):
        try:
            val = self.config.get(section, key)
            return val if val != "" else default
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
        self._write_config()

    def get_all(self, section):
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}
