# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse

import gnome_pomodoro_tracking.utils as utils
from gnome_pomodoro_tracking.frontends.base import BaseFrontend


class EntryTime(BaseFrontend):
    name = "entry_time"

    def register_arguments(self, parser: argparse.ArgumentParser):
        group = parser.add_argument_group("Manual Time Entry")
        group.add_argument(
            "-etn", "--et-name", dest="et_name", help=argparse.SUPPRESS
        )
        group.add_argument(
            "-etm", "--et-minutes", dest="et_minutes", help=argparse.SUPPRESS
        )

    def handle(self, args: argparse.Namespace) -> bool:
        raw_minutes = getattr(args, "et_minutes", None)
        if raw_minutes is None:
            return False

        try:
            minutes = int(float(raw_minutes))
        except (TypeError, ValueError):
            self.logger.error(f"Invalid minutes value: {raw_minutes}")
            return True

        if minutes <= 0:
            self.logger.error("Minutes must be greater than 0")
            return True

        name = getattr(args, "et_name", None) or getattr(args, "name", None)
        end = utils.now()
        start = utils.minutes_before(end, minutes)

        self.tracker.add_time_entry(
            name=name, start=start, end=end, minutes=minutes, tags=[]
        )
        self.logger.info(f"Manual time entry added ({minutes} min)")
        return True
