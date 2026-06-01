<p align="center">
  <img src="docs/img/how-does-it-workv4.png" width="1200">
</p>

<p align="center">  
  <a href="LICENSE">  
    <img src="https://img.shields.io/github/license/focustimerhq/gnome-pomodoro-tracking?style=flat-square" />
  </a>
  <a>
       <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gnome-pomodoro-tracking">

  </a>
</p>

# Welcome to Timesheet Sync!
Our CLI tool integrates with Toggl, Clockify, and Odoo to provide accurate time logging for your tasks and projects. It can be used directly from the terminal or seamlessly integrated with Focus Timer (formerly gnome-pomodoro).


----
## Getting Started

### 1. Install
To get started, simply install the package using pip or uv:

```bash
pip install -U gnome-pomodoro-tracking
```

### 2. Choose Your Time Tracking Service

We support three popular services:
* **Toggl**:  [Learn More](docs/toggl.md)
* **Clockify**: [Learn More](docs/clockify.md)
* **Odoo**: [Learn More](docs/odoo.md)

### 3. Usage (CLI)

Use the command line to interact with the plugin:

```bash
usage: gnome-pomodoro-tracking [-h] [--plugin PLUGIN] [--status] [--start] [--stop]
                      [--name NAME] [--tag TAG]
                      {clockify,odoo,toggl} ...

positional arguments:
  {clockify,odoo,toggl}
                        Plugin commands
    clockify            Clockify plugin commands
    odoo                Odoo plugin commands
    toggl               Toggl plugin commands

options:
  -h, --help            show this help message and exit
  --plugin PLUGIN       Set active plugin
  --status              Show current status
  --start               Start pomodoro
  --stop                Stop pomodoro
  --name NAME           Name of the task
  --tag TAG             Tag for the task
```

#### --start and --stop

Allow create manually time entry, the time is calculated automatically based on when you started and stopped.
```bash
gnome-pomodoro-tracking --start
# After some time...
gnome-pomodoro-tracking --stop
```

#### --name
A name for the time entry.
```bash
gnome-pomodoro-tracking --start --name "My Entry Name"
```

#### --tag
Add tag to the time entry, if you want add many tags, use `,` . e.g  `tag1,tag2,tag3`
```bash
gnome-pomodoro-tracking --start --tag "dev,urgent"
```
NOTE: 
* Is only supported by Toggl and Clockify

#### --status
Allows you to print the current status of your active tracking.
```bash
gnome-pomodoro-tracking --status
```

### 4. Integration with GNOME Pomodoro (Optional)

* Open Gnome Pomodoro Preferences.
* Navigate to "Plugins" > "Custom Actions (Execute shell scripts)".
* Click "Add" and paste one of the following commands depending on how you installed the application:

**If installed globally:**
```bash
gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

**If installed in a virtual environment (venv):**
Replace `/path/to/venv` with the actual path to your virtual environment.
```bash
/path/to/venv/bin/gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```

**If using `uv` (for development):**
Replace `/path/to/project` with the path where you cloned the repository.
```bash
cd /path/to/project && uv run gnome-pomodoro-tracking -gps "$(state)" -gpt "$(triggers)" -gpd "$(duration)" -gpe "$(elapsed)"
```
