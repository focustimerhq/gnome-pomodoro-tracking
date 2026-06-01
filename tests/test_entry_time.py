# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import argparse
import unittest
from unittest.mock import MagicMock

import gnome_pomodoro_tracking.utils as utils
from gnome_pomodoro_tracking.frontends.entry_time import EntryTime


class TestEntryTime(unittest.TestCase):
    def setUp(self):
        self.tracker = MagicMock()
        self.frontend = EntryTime(config=MagicMock(), tracker=self.tracker)

    def _handle(self, **kwargs):
        kwargs.setdefault("et_name", None)
        kwargs.setdefault("et_minutes", None)
        kwargs.setdefault("name", None)
        return self.frontend.handle(argparse.Namespace(**kwargs))

    def test_ignored_when_no_minutes(self):
        self.assertFalse(self._handle())
        self.tracker.add_time_entry.assert_not_called()

    def test_int_minutes(self):
        self.assertTrue(self._handle(et_name="Coding", et_minutes="10"))
        _, kwargs = self.tracker.add_time_entry.call_args
        self.assertEqual(kwargs["minutes"], 10)
        self.assertEqual(kwargs["name"], "Coding")

    def test_float_minutes_cast_to_int(self):
        self.assertTrue(self._handle(et_name="Review", et_minutes="10.4"))
        _, kwargs = self.tracker.add_time_entry.call_args
        self.assertEqual(kwargs["minutes"], 10)

    def test_start_is_minutes_before_end(self):
        self.assertTrue(self._handle(et_minutes="30"))
        _, kwargs = self.tracker.add_time_entry.call_args
        elapsed = utils.time_elapsed(kwargs["start"], kwargs["end"], formatter="minutes")
        self.assertEqual(int(elapsed), 30)

    def test_invalid_minutes_does_not_add(self):
        self.assertTrue(self._handle(et_minutes="abc"))
        self.tracker.add_time_entry.assert_not_called()

    def test_non_positive_minutes_does_not_add(self):
        self.assertTrue(self._handle(et_minutes="0"))
        self.tracker.add_time_entry.assert_not_called()

    def test_falls_back_to_global_name(self):
        self.assertTrue(self._handle(et_minutes="5", name="Global"))
        _, kwargs = self.tracker.add_time_entry.call_args
        self.assertEqual(kwargs["name"], "Global")


if __name__ == "__main__":
    unittest.main()
