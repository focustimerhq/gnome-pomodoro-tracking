# Contribution Guide

## Setup your workspace 
* Install `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

* Initialize the project
```bash
uv sync --extra dev
```

## Running the application locally

You can test the CLI locally using `uv run`:

```bash 
uv run gnome-pomodoro-tracking --start --name "Testing plugin"
```

To test GNOME Pomodoro specific triggers:
```bash
uv run gnome-pomodoro-tracking -gps "pomodoro" -gpt "start" -gpd "25" -gpe "0"
```

## Code Quality

Format and lint the code using `ruff`:
```bash
uv run ruff format .
uv run ruff check . --fix
```

## Test using pytest
```bash
uv run pytest tests/
```

## Publish on PyPI

Build the package using `build`:
```bash
uv run python -m build
```
Upload via Twine:
```bash
uv run twine upload --verbose dist/*
```