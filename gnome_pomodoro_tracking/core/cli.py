# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse
import logging
import sys

from gnome_pomodoro_tracking.core.config import ConfigManager
from gnome_pomodoro_tracking.core.frontend_manager import FrontendManager
from gnome_pomodoro_tracking.core.plugin_manager import PluginManager
from gnome_pomodoro_tracking.core.tracker import Tracker


def configure_logger():
    logger = logging.getLogger("gnome_pomodoro_tracking")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(levelname)-8s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main():
    logger = configure_logger()
    config = ConfigManager()
    plugin_manager = PluginManager(config)
    tracker = Tracker(config, plugin_manager)
    frontend_manager = FrontendManager(config, tracker)

    parser = argparse.ArgumentParser(prog="gnome-pomodoro-tracking")
    parser.add_argument("--plugin", help="Set active plugin")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--start", action="store_true", help="Start pomodoro")
    parser.add_argument("--stop", action="store_true", help="Stop pomodoro")
    parser.add_argument("--name", help="Name of the task")
    parser.add_argument("--tag", help="Tag for the task")

    # Let frontends register their arguments
    frontend_manager.register_arguments(parser)

    subparsers = parser.add_subparsers(dest="command", help="Plugin commands")

    # Let plugins register their subparsers
    for name, plugin_class in plugin_manager.plugins.items():
        plugin_instance = plugin_manager.get_plugin(name)
        if plugin_instance:
            plugin_instance.register_subcommand(subparsers)

    args, unknown = parser.parse_known_args()

    # Let frontends handle execution if they matched their triggers
    if frontend_manager.handle(args):
        return

    if args.plugin:
        config.set("settings", "plugin", args.plugin)
        logger.info(f"Plugin set to {args.plugin}")

    if args.start:
        tracker.start("pomodoro", args.name, args.tag)
        logger.info("Timer started")
    elif args.stop:
        tracker.stop()
        logger.info("Timer stopped")
    elif args.status:
        tracker.status()

    # Dispatch to plugin command
    if args.command:
        plugin = plugin_manager.get_plugin(args.command)
        if plugin:
            plugin.execute_subcommand(args)


if __name__ == "__main__":
    main()
