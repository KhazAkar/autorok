# AGENTS.md - Project Notes for Autorok

This file contains project-specific notes and guidelines for developers and agents working on this repository.

## Project Setup

### Python Version
- **Required**: Python 3.13+
- The project uses modern Python features including PEP 604 union types (`X | Y`)

### Package Manager: uv

This project uses [uv](https://docs.astral.sh/uv/) as its package manager and Python package installer.

#### Installation

First, install uv:

```bash
# Install uv globally
pip install uv

# Or on some systems
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Creating a Virtual Environment

To create a project-specific virtual environment:

```bash
# Create a virtual environment with Python 3.13
uv venv -p 3.13

# This creates a .venv directory in your project root
```

#### Activating the Virtual Environment

```bash
# On Linux/macOS
source .venv/bin/activate

# On Windows (PowerShell)
.\.venv\Scripts\activate

# On Windows (cmd.exe)
.\.venv\Scripts\activate.bat
```

#### Syncing Dependencies

The **recommended** way to install all dependencies (including dev dependencies):

```bash
# Sync all dependencies from pyproject.toml
uv sync --all-extras

# This will:
# - Create/activate the virtual environment if needed
# - Install the project in editable mode
# - Install all dependencies (including dev dependencies from [project.optional-dependencies])
```

**Alternative sync options:**

```bash
# Sync only the project (no dev dependencies)
uv sync

# Sync with specific extras
uv sync --extra dev

# Sync all extras
uv sync --all-extras

# Sync only dev dependencies
uv sync --only-dev
```

#### Running Commands

After syncing, use `uv run` to execute commands in the project's environment:

```bash
# Run ruff linting
uv run ruff check autorok/ tests/

# Run ruff formatting check
uv run ruff format --check autorok/ tests/

# Run tests
uv run pytest tests/ -v

# Run all checks
uv run ruff check autorok/ tests/ && \
  ruff format --check autorok/ tests/ && \
  pytest tests/ -v
```

#### Manual Installation (Alternative)

If you prefer not to use `uv sync`, you can manually install:

```bash
# Install the project in editable mode
uv pip install -e .

# Install dev dependencies
uv pip install ruff pytest pytest-cov
```

However, **`uv sync` is the recommended approach** as it ensures consistent environments.

## Development Workflow

### Linting and Formatting

This project uses [ruff](https://docs.astral.sh/ruff/) for both linting and formatting.

```bash
# Check linting
uv run ruff check autorok/ tests/

# Apply lint fixes (where possible)
uv run ruff check --fix autorok/ tests/

# Check formatting
uv run ruff format --check autorok/ tests/

# Apply formatting
uv run ruff format autorok/ tests/
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=autorok --cov-report=term
```

## CI/CD Notes

The GitHub Actions workflow uses the following pattern:

1. Set up Python 3.13
2. Install uv
3. Create virtual environment with `uv venv -p 3.13`
4. Sync dependencies with `uv sync --all-extras`
5. Install sigrok-cli (system package)
6. Run linting with `uv run ruff check ...`
7. Run formatting check with `uv run ruff format --check ...`
8. Run tests with `uv run pytest ...`

**Important**: Always ensure your local development matches this pattern by using `uv sync --all-extras`.

## Common Issues

### "No virtual environment found"

If you see this error, you need to create a virtual environment first:

```bash
uv venv -p 3.13
```

### "uv: command not found"

Install uv first:

```bash
pip install uv
```

### "Python 3.13 not found"

Ensure you have Python 3.13+ installed. On Ubuntu:

```bash
# Install Python 3.13
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

## Project Structure

```
autorok/
├── __init__.py          # Package exports
├── autorok.py           # Main Autorok class
├── common.py            # Abstract base classes and enums
├── devices.py           # Device definitions
├── exceptions.py        # Custom exceptions
├── libsigrok.py         # libsigrok driver (stub)
└── sigrokcli.py         # sigrok-cli driver implementation

tests/
└── test_sigrokcli.py    # Tests for SigrokCLI driver

.github/
└── workflows/
    └── python-package.yml # GitHub Actions CI workflow

AGENTS.md                # This file - project notes
pyproject.toml           # Project configuration for uv
```

## Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [Python 3.13 Documentation](https://docs.python.org/3.13/)
- [sigrok-cli Documentation](https://sigrok.org/wiki/Sigrok-cli)

## Always Check

Before committing or pushing changes:

1. ✅ Run `uv run ruff check autorok/ tests/` - all lint checks pass
2. ✅ Run `uv run ruff format --check autorok/ tests/` - all formatting checks pass
3. ✅ Run `uv run pytest tests/ -v` - all tests pass
4. ✅ Use `uv sync --all-extras` to ensure your environment matches CI

**Remember**: The CI uses `uv sync --all-extras`, so always use the same command locally to ensure consistency.
