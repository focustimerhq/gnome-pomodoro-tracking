# Copyright (c) gnome-pomodoro-tracking contributors. SPDX-License-Identifier: MIT
# Authors: Jose Hernandez <josehbez@outlook.com>

from gnome_pomodoro_tracking.plugins.base import BasePlugin
from gnome_pomodoro_tracking.utils import (
    config_attrs,
    find_by_id,
    join_url,
    only_columns,
    printtbl,
)


class Toggl(BasePlugin):
    name = "toggl"
    url = "https://api.track.toggl.com/api/v9"
    required_config = ["token"]

    def http_auth(self):
        token = self.config.get(self.name, "token", "")
        return (token, "api_token")

    def register_subcommand(self, subparsers):
        parser = subparsers.add_parser(self.name, help="Toggl plugin commands")
        parser.add_argument(
            "-w", "--workspaces", action="store_true", help="List workspaces"
        )
        parser.add_argument(
            "-p", "--projects", action="store_true", help="List projects"
        )
        parser.add_argument("--token", action="store", help="Set authentication token")
        parser.add_argument("--set", action="store", help="Set workspace or project ID")

    def auth(self):
        try:
            req = self.rget(join_url(self.url, "me"), auth=self.http_auth())
            if req.ok:
                data = req.json()
                return bool(data.get("id"))
            else:
                self.logger.error(req.text)
        except Exception as e:
            self.logger.exception(e)
        return False

    def execute_subcommand(self, args):
        if args.token:
            self.config.set(self.name, "token", args.token)
            if self.auth():
                print("Authenticated successfully.")
            else:
                print("Fail auth check your token!")
            return

        if args.workspaces:
            rows = self.workspaces()
            if rows:
                rows = only_columns(rows)
                if args.set:
                    row = find_by_id(rows, args.set)
                    if row:
                        self.config.set(self.name, "workspace_id", row.get("id"))
                        self.config.set(self.name, "workspace_name", row.get("name"))
                        self.config.set(self.name, "project_id", "")
                        self.config.set(self.name, "project_name", "")
                        printtbl([row])
                    else:
                        print("The workspace ID was not found")
                else:
                    printtbl(rows)

        elif args.projects:
            workspace_id = self.config.get(self.name, "workspace_id")
            if not workspace_id:
                workspace = self.workspaces(filter="first")
                workspace_id = workspace.get("id") if workspace else None

            if workspace_id:
                rows = self.projects(workspace_id)
                if rows:
                    rows = only_columns(rows)
                    if args.set:
                        row = find_by_id(rows, args.set)
                        if row:
                            self.config.set(self.name, "project_id", row.get("id"))
                            self.config.set(self.name, "project_name", row.get("name"))
                            printtbl([row])
                        else:
                            print("The project ID was not found")
                    else:
                        printtbl(rows)

    def workspaces(self, filter=""):
        url = join_url(self.url, "workspaces")
        try:
            req = self.rget(url, auth=self.http_auth())
            if req.ok:
                data = req.json()
                if filter == "first" and data:
                    return data[0]
                return data
            else:
                self.logger.error(req.text)
        except Exception as e:
            self.logger.exception(e)
        return None

    def projects(self, workspace_id, filter=""):
        url = join_url(self.url, f"workspaces/{workspace_id}/projects")
        try:
            req = self.rget(url, auth=self.http_auth())
            if req.ok:
                data = req.json()
                if filter == "first" and data:
                    return data[0]
                return data
            else:
                self.logger.error(req.text)
        except Exception as e:
            self.logger.exception(e)
        return None

    def add_time_entry(self, **kwargs):
        name = kwargs.get("name")
        start = kwargs.get("start")
        end = kwargs.get("end")
        tags = kwargs.get("tags", [])

        workspace_id = self.config.get(self.name, "workspace_id")
        if not workspace_id:
            workspace = self.workspaces(filter="first")
            workspace_id = workspace.get("id") if workspace else None

        project_id = self.config.get(self.name, "project_id")

        time_entry = {
            "start": start,
            "description": name,
            "stop": end,
            "created_with": "gnome_pomodoro_tracking",
        }

        if workspace_id:
            time_entry.update({"workspace_id": int(workspace_id)})

        if project_id:
            time_entry.update({"project_id": int(project_id)})

        if tags:
            time_entry.update({"tags": tags})

        try:
            url = join_url(self.url, f"workspaces/{workspace_id}/time_entries")
            req = self.rpost(url, auth=self.http_auth(), json=time_entry)
            if req.ok:
                data = req.json()
                return {"id": data["id"], "name": name}
            else:
                self.logger.error(req.text)
        except Exception as e:
            self.logger.exception(e)
        return None

    def status(self):
        attrs = ["workspace_name", "project_name"]
        items = config_attrs(self.config, self.name, attrs, formatter="status")
        printtbl(items)
