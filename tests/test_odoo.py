# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

from unittest.mock import patch

from tests.test_plugin import TestPlugin


class TestOdoo(TestPlugin):
    plugin = "odoo"
    url = "http://local.host"
    database = "localhost"
    username = "username@local.host"
    password = "password@local.host"

    projects_data = [{"id": 1, "name": "Project O1"}]
    tasks_data = [
        {"id": 13, "name": "Task O1", "project_id": 1, "project_name": "Project O1"}
    ]

    time_entry = {"id": 4, "name": "Time entry"}

    def setUp(self) -> None:
        super().setUp()
        self.config.set("settings", "plugin", self.plugin)
        self.config.set(self.plugin, "url", self.url)
        self.config.set(self.plugin, "database", self.database)
        self.config.set(self.plugin, "username", self.username)
        self.config.set(self.plugin, "password", self.password)

        patch("gnome_pomodoro_tracking.plugins.odoo.Odoo.auth", return_value=True).start()
        patch(
            "gnome_pomodoro_tracking.plugins.odoo.Odoo.projects", return_value=self.projects_data
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.odoo.Odoo.tasks", return_value=self.tasks_data
        ).start()
        patch(
            "gnome_pomodoro_tracking.plugins.odoo.Odoo.add_time_entry",
            return_value=self.time_entry,
        ).start()

    def test_cli(self):
        # Projects
        self.execute_cli(
            self.plugin,
            projects=True,
            tasks=False,
            username=None,
            password=None,
            url=None,
            database=None,
            set="1",
        )
        assert self.config.get(self.plugin, "project_id") == "1"

        # Tasks
        self.execute_cli(
            self.plugin,
            projects=False,
            tasks=True,
            username=None,
            password=None,
            url=None,
            database=None,
            set="13",
        )
        assert self.config.get(self.plugin, "task_id") == "13"
