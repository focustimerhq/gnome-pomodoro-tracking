# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

import xmlrpc.client
from datetime import datetime
from urllib.parse import urlparse

from gnome_pomodoro_tracking.plugins.base import BasePlugin
from gnome_pomodoro_tracking.utils import config_attrs, find_by_id, join_url, printtbl


class Odoo(BasePlugin):
    name = "odoo"
    required_config = ["username", "password", "url", "database"]

    def register_subcommand(self, subparsers, parents=None):
        parser = subparsers.add_parser(
            self.name, help="Odoo plugin commands", parents=parents or []
        )
        parser.add_argument(
            "-p", "--projects", action="store_true", help="List projects"
        )
        parser.add_argument("-t", "--tasks", action="store_true", help="List tasks")
        parser.add_argument("--username", action="store", help="Set username")
        parser.add_argument("--password", action="store", help="Set password")
        parser.add_argument("--database", action="store", help="Set database")
        parser.add_argument("--url", action="store", help="Set url")
        parser.add_argument("--set", action="store", help="Set project or task ID")

    def auth(self):
        url = self.config.get(self.name, "url", "")
        if not url:
            return False
        up = urlparse(url)
        clean_url = "{}://{}".format(up.scheme or "https", up.netloc)
        self.config.set(self.name, "url", clean_url)
        try:
            uid = self.common().authenticate(
                self.config.get(self.name, "database"),
                self.config.get(self.name, "username"),
                self.config.get(self.name, "password"),
                {},
            )
            self.session["uid"] = uid
            return bool(uid)
        except Exception as e:
            self.logger.error(e)
            return False

    def common(self):
        url = self.config.get(self.name, "url", "")
        return xmlrpc.client.ServerProxy(join_url(url, "xmlrpc/2/common"))

    def models(self, model, method, domain, options=False):
        uid = self.session.get("uid")
        if not uid:
            self.auth()
            uid = self.session.get("uid")
            if not uid:
                return False

        url = self.config.get(self.name, "url", "")
        password = self.config.get(self.name, "password", "")
        database = self.config.get(self.name, "database", "")

        x = xmlrpc.client.ServerProxy(join_url(url, "xmlrpc/2/object"))
        return x.execute_kw(database, uid, password, model, method, domain, options)

    def execute_subcommand(self, args):
        if args.username or args.password or args.url or args.database:
            if args.username:
                self.config.set(self.name, "username", args.username)
            if args.password:
                self.config.set(self.name, "password", args.password)
            if args.url:
                self.config.set(self.name, "url", args.url)
            if args.database:
                self.config.set(self.name, "database", args.database)

            if self.auth():
                print("Authenticated successfully.")
            else:
                print("Fail auth check your credentials!")
            return

        if args.projects:
            rows = self.projects()
            if args.set:
                row = find_by_id(rows, args.set)
                if row:
                    self.config.set(self.name, "project_id", row.get("id"))
                    self.config.set(self.name, "project_name", row.get("name"))
                    self.config.set(self.name, "task_id", "")
                    self.config.set(self.name, "task_name", "")
                    printtbl([row])
                else:
                    print("The project ID was not found")
            else:
                printtbl(rows)

        elif args.tasks:
            rows = self.tasks()
            if args.set:
                row = find_by_id(rows, args.set)
                if row:
                    self.config.set(self.name, "task_id", row.get("id"))
                    self.config.set(self.name, "task_name", row.get("name"))
                    self.config.set(self.name, "project_id", row.get("project_id"))
                    self.config.set(self.name, "project_name", row.get("project_name"))
                    printtbl([row])
                else:
                    print("The task ID was not found")
            else:
                printtbl(rows)

    def data_order(self, rows):
        nrows = []
        for row in rows:
            nrows.append(dict(sorted(row.items(), key=lambda c: str(c[1]))))
        return len(nrows) and nrows or rows

    def projects(self):
        projects = self.models(
            "project.project",
            "search_read",
            [[["active", "=", True]]],
            {"fields": ["id", "name"]},
        )
        if projects:
            return self.data_order(projects)
        return []

    def tasks(self):
        project_id = self.config.get(self.name, "project_id")
        if project_id and str(project_id).isdigit():
            domain = [[["active", "=", True], ["project_id", "=", int(project_id)]]]
        else:
            domain = [[["active", "=", True]]]

        tasks = self.models(
            "project.task",
            "search_read",
            domain,
            {"fields": ["id", "name", "project_id"]},
        )
        if tasks:
            tasks = self.data_order(tasks)
            ntasks = []
            for t in tasks:
                tb = t.pop("project_id")
                if tb:
                    ntasks.append({**t, "project_id": tb[0], "project_name": tb[1]})
                else:
                    ntasks.append({**t, "project_id": False, "project_name": ""})
            return ntasks
        return []

    def add_time_entry(self, **kwargs):
        name = kwargs.get("name")
        minutes = float(kwargs.get("minutes", 0))

        project_id = self.config.get(self.name, "project_id")
        if not project_id:
            self.logger.error("First select the project")
            return None

        project_id = int(project_id)
        task_id = self.config.get(self.name, "task_id")
        task_id = int(task_id) if task_id and str(task_id).isdigit() else False

        try:
            id = self.models(
                "account.analytic.line",
                "create",
                [
                    {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "name": name,
                        "project_id": project_id,
                        "task_id": task_id,
                        "unit_amount": minutes / 60,
                    }
                ],
            )
            return {"id": id, "name": name}
        except Exception as e:
            self.logger.exception(e)
        return None

    def status(self):
        attrs = ["project_name", "task_name"]
        items = config_attrs(self.config, self.name, attrs, formatter="status")
        printtbl(items)
