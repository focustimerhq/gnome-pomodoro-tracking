# Odoo Timesheet Integration


### Required modules

Is importan installed `projects` and `sale_timesheet` modules in your instance odoo.

### Enable plugin

Copy and paste this command in terminal
```bash
gnome-pomodoro-tracking --plugin odoo
```


### Generate Your gRPC Token:

* Visit your odoo instance 
* Go to My Profile  > Account Security  > API Keys > Generate New Token

Copy this command adn paste in terminal replacing PASS with your token

  ```bash
  gnome-pomodoro-tracking odoo --database DB --url URL --username USER --password PASS
  ```

### Start tracking

Before you start tracking, you need to set up a project. It is usually set up once. If don't set up, it will use the first workspace and project.


Projects, you can list and set using this command this command.

List
```bash
gnome-pomodoro-tracking odoo --projects  
```

Set
```bash
gnome-pomodoro-tracking odoo --projects --set ID
```

Tasks, if you want add time logging in a task, you can list and set using this command. Is optional

List
```bash
gnome-pomodoro-tracking odoo --tasks
```
Set
```bash
gnome-pomodoro-tracking odoo --tasks --set ID
```


For advanced CLI usage and customization, please refer to the guide: [README.md](../README.md)



### Versions Supported

| Odoo Version  |  Community  | Enterprise  |
| -  |  -  | -  |
| 19.0 | ✅  | ✅  |
