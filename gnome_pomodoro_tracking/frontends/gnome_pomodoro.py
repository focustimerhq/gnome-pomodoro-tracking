# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse

from gnome_pomodoro_tracking.frontends.base import BaseFrontend


class GnomePomodoro(BaseFrontend):
    name = "gnome_pomodoro"

    def register_arguments(self, parser: argparse.ArgumentParser):
        frontend_group = parser.add_argument_group("GNOME Pomodoro Integration")
        frontend_group.add_argument(
            "-gps", "--gp-state", dest="gp_state", help=argparse.SUPPRESS
        )
        frontend_group.add_argument(
            "-gpt", "--gp-trigger", dest="gp_trigger", help=argparse.SUPPRESS
        )
        frontend_group.add_argument(
            "-gpd", "--gp-duration", dest="gp_duration", help=argparse.SUPPRESS
        )
        frontend_group.add_argument(
            "-gpe", "--gp-elapsed", dest="gp_elapsed", help=argparse.SUPPRESS
        )

    def handle(self, args: argparse.Namespace) -> bool:
        if getattr(args, "gp_state", None) and getattr(args, "gp_trigger", None):
            if "start" in args.gp_trigger or "resume" in args.gp_trigger:
                self.tracker.start(
                    args.gp_state,
                    getattr(args, "name", None),
                    getattr(args, "tag", None),
                )
                self.logger.info("Timer started (via GP)")
            elif (
                "skip" in args.gp_trigger
                or "pause" in args.gp_trigger
                or "complete" in args.gp_trigger
            ):
                self.tracker.stop()
                self.logger.info("Timer stopped (via GP)")
            return True
        return False
