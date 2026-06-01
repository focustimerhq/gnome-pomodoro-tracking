# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

from unittest.mock import patch

from tests.test_plugin import TestPlugin


class TestToggl(TestPlugin):
    plugin = "toggl"
    token = "19c98455494ab3f5d72d91de5c26b116"

    workspaces_data = [
        {"id": 4755497, "name": "Workspace T1"},
    ]
    projects_data = [
        {"id": 164238639, "name": "Project T1", "wid": 4755497},
    ]

    time_entry = {"id": 1950743713, "name": "Time entry"}

    def setUp(self) -> None:
        super().setUp()
        self.config.set("settings", "plugin", self.plugin)
        self.config.set(self.plugin, "token", self.token)

        patch("gnome_pomodoro_tracking.plugins.toggl.Toggl.auth", return_value=True).start()
        patch(
            "gnome_pomodoro_tracking.plugins.toggl.Toggl.workspaces",
            return_value=self.workspaces_data,
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.toggl.Toggl.projects",
            return_value=self.projects_data,
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.toggl.Toggl.add_time_entry",
            return_value=self.time_entry,
        ).start()

    def test_cli(self):
        # Workspaces
        self.execute_cli(
            self.plugin, workspaces=True, projects=False, token=None, set="4755497"
        )
        assert self.config.get(self.plugin, "workspace_id") == "4755497"

        # Projects
        self.execute_cli(
            self.plugin, workspaces=False, projects=True, token=None, set="164238639"
        )
        assert self.config.get(self.plugin, "project_id") == "164238639"
