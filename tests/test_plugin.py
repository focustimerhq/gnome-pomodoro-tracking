# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse
import os
import unittest

from gnome_pomodoro_tracking.core.config import ConfigManager
from gnome_pomodoro_tracking.core.plugin_manager import PluginManager
from gnome_pomodoro_tracking.core.tracker import Tracker


class TestPlugin(unittest.TestCase):
    def setUp(self) -> None:
        self.config_path = "gnome-pomodoro-tracking.template"
        self.config = ConfigManager(self.config_path)
        self.plugin_manager = PluginManager(self.config)
        self.tracker = Tracker(self.config, self.plugin_manager)

    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def execute_cli(self, plugin_name, **kwargs):
        plugin = self.plugin_manager.get_plugin(plugin_name)
        if not plugin:
            return None
        args = argparse.Namespace(**kwargs)
        plugin.execute_subcommand(args)

    def test_set_name_starts_session(self):
        self.tracker.set_name("abc")
        self.assertEqual(self.config.get("tracker", "name"), "abc")
        self.assertEqual(self.config.get("tracker", "type"), "Pomodoro")
        self.assertTrue(self.config.get("tracker", "start"))

    def test_set_name_keeps_active_session_start(self):
        self.tracker.start("pomodoro", "first")
        start = self.config.get("tracker", "start")
        self.tracker.set_name("second")
        self.assertEqual(self.config.get("tracker", "name"), "second")
        self.assertEqual(self.config.get("tracker", "start"), start)

    def test_set_tag(self):
        self.tracker.set_tag("dev,urgent")
        self.assertEqual(self.config.get("tracker", "tag"), "dev,urgent")
