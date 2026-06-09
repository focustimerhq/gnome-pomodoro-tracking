# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import logging

import gnome_pomodoro_tracking.utils as utils


class Tracker:
    def __init__(self, config, plugin_manager):
        self.config = config
        self.plugin_manager = plugin_manager
        self.logger = logging.getLogger(__name__)

    def start(self, state, name, tag=None):
        self.config.set("tracker", "type", state.title())
        self.config.set("tracker", "name", name or "")
        self.config.set("tracker", "tag", tag or "")
        self.config.set("tracker", "start", utils.now())

    def _ensure_session(self):
        """Begin a tracking session if none is active."""
        if not self.config.get("tracker", "name") and not self.config.get(
            "tracker", "start"
        ):
            self.config.set("tracker", "type", "Pomodoro")
            self.config.set("tracker", "start", utils.now())

    def set_name(self, name):
        self._ensure_session()
        self.config.set("tracker", "name", name)

    def set_tag(self, tag):
        self._ensure_session()
        self.config.set("tracker", "tag", tag)

    def stop(self):
        self.add_time_entry()

    def add_time_entry(self, name=None, start=None, end=None, minutes=None, tags=None):
        try:
            name = (
                name
                or self.config.get("tracker", "name")
                or self.config.get("tracker", "type")
            )
            start = start or self.config.get("tracker", "start")
            end = end or utils.now()

            if not start:
                return

            if minutes is None:
                minutes = utils.time_elapsed(start, end, formatter="minutes")

            mt = self.config.get("settings", "mintrace", "0")
            mintrace = int(mt) if str(mt).isdigit() else 0

            if tags is None:
                tag_attr = self.config.get("tracker", "tag", "")
                tags = tag_attr.split(",") if tag_attr else []

            if minutes > mintrace:
                plugin_name = self.config.get("settings", "plugin")
                if plugin_name:
                    plugin = self.plugin_manager.get_plugin(plugin_name)
                    if plugin:
                        result = plugin.add_time_entry(
                            name=name, start=start, end=end, minutes=minutes, tags=tags
                        )
                        if result:
                            utils.printtbl([result])

            self._clean()
        except Exception as e:
            self.logger.error(f"Tracker Error: {e}")

    def _clean(self):
        for k in ["start", "type", "name", "tag"]:
            self.config.set("tracker", k, "")

    def status(self):
        plugin_name = self.config.get("settings", "plugin")
        items = [
            {
                "key": "Plugin",
                "value": str(plugin_name).title() if plugin_name else "None",
            }
        ]

        dt_start = utils.now()
        start = self.config.get("tracker", "start")
        if start:
            dt_start = start

        for k in ["type", "start", "name", "tag"]:
            val = self.config.get("tracker", k)
            if val:
                items.append({"key": str(k).title(), "value": val})

        elapsed = utils.time_elapsed(dt_start, utils.now(), formatter="minutes")
        items.append({"key": "Elapsed", "value": f"{elapsed:.2f} Min"})
        utils.printtbl(items)

        if plugin_name:
            plugin = self.plugin_manager.get_plugin(plugin_name)
            if plugin and hasattr(plugin, "status"):
                plugin.status()
