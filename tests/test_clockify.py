# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

from unittest.mock import patch

from tests.test_plugin import TestPlugin


class TestClockify(TestPlugin):
    plugin = "clockify"
    token = "X/oWnmt2eyj4ZCbh"

    workspaces_data = [
        {"id": "5e9ca62da2686b699ed5748d", "name": "Workspace C1"},
        {"id": "5e9ca62da2786b699ed5748d", "name": "Workspace C2"},
    ]
    projects_data = [
        {
            "id": "5eab188c991f8972bb9a1fa3",
            "name": "Project C1",
            "workspaceId": "5e9ca62da2686b699ed5748d",
        },
    ]

    time_entry = {"id": "6065003e9341062dc3acf936", "name": "Time entry"}

    def setUp(self) -> None:
        super().setUp()
        self.config.set("settings", "plugin", self.plugin)
        self.config.set(self.plugin, "token", self.token)

        patch(
            "gnome_pomodoro_tracking.plugins.clockify.Clockify.auth", return_value=True
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.clockify.Clockify.workspaces",
            return_value=self.workspaces_data,
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.clockify.Clockify.projects",
            return_value=self.projects_data,
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.clockify.Clockify.add_time_entry",
            return_value=self.time_entry,
        ).start()

    def test_cli(self):
        # Workspaces
        self.execute_cli(
            self.plugin,
            workspaces=True,
            projects=False,
            token=None,
            set="5e9ca62da2686b699ed5748d",
        )
        assert (
            self.config.get(self.plugin, "workspace_id") == "5e9ca62da2686b699ed5748d"
        )

        # Projects
        self.execute_cli(
            self.plugin,
            workspaces=False,
            projects=True,
            token=None,
            set="5eab188c991f8972bb9a1fa3",
        )
        assert self.config.get(self.plugin, "project_id") == "5eab188c991f8972bb9a1fa3"
