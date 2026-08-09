# AGENTS.md - Agent Operating Procedures for Autorok

This file contains **mandatory** operating procedures and guidelines for AI agents, bots, and developers working on the Autorok codebase. **All agents MUST follow these instructions when operating on this repository.**

---

## 📋 Table of Contents

1. [Repository Overview](#-repository-overview)
2. [Project Structure](#-project-structure)
3. [Development Environment](#-development-environment)
4. [Code Style Guidelines](#-code-style-guidelines)
5. [Feature Development Methodology](#-feature-development-methodology)
6. [Backend Architecture](#-backend-architecture)
7. [Testing Strategy](#-testing-strategy)
8. [Common Workflows](#-common-workflows)
9. [Quality Checklist](#-quality-checklist)

---

## 🏗️ Repository Overview

**Autorok** is a Python wrapper library that provides a unified interface to sigrok-based tools (sigrok-cli, libsigrok, libsigrok4DSL) for hardware testing automation.

### Purpose
- Provide a consistent Python API for sigrok functionality
- Abstract away differences between various sigrok backends
- Enable easy automation of hardware testing tasks
- Support multiple measurement devices through a common interface

### Supported Backends
| Backend | Status | Description |
|---------|--------|-------------|
| sigrok-cli | ✅ Working | Command-line interface to sigrok |
| libsigrok | 📋 Planned | Direct Python bindings to libsigrok |
| libsigrok4DSL | 📋 Planned | For DreamSourceLabs devices |

---

## 🗂️ Project Structure

```
autorok/
├── __init__.py          # Package exports and public API
├── autorok.py           # Main Autorok class (user-facing interface)
├── common.py            # Abstract base classes and shared types
├── devices.py           # Device definitions and metadata
├── exceptions.py        # Custom exception hierarchy
├── sigrokcli.py         # sigrok-cli backend implementation
└── libsigrok.py         # libsigrok backend (stub for future implementation)

tests/
├── __init__.py
└── test_sigrokcli.py    # Tests for SigrokCLI backend

.github/
└── workflows/
    └── python-package.yml # GitHub Actions CI/CD workflow

# Root files
AGENTS.md                # This file - agent operating procedures
pyproject.toml           # Project configuration (uv, ruff, pyright)
README.md                # Project documentation
.gitignore               # Git ignore patterns
```

### Module Responsibilities

| Module | Responsibility | Dependencies |
|--------|---------------|--------------|
| `autorok.py` | Main user interface, orchestrates backends | `common.py`, `sigrokcli.py` |
| `common.py` | Abstract base classes (`SigrokDriver`), enums (`OutputType`, `InputType`) | None |
| `devices.py` | Device metadata and definitions (`Device` dataclass, `DeviceList`) | `dataclasses` |
| `exceptions.py` | Custom exception hierarchy for error handling | None |
| `sigrokcli.py` | sigrok-cli backend implementation | `subprocess`, `common.py` |
| `libsigrok.py` | libsigrok backend placeholder | `common.py` |

---

## 💻 Development Environment

### Python Version
- **Required**: Python 3.13+
- **Recommended**: Python 3.13.x
- The project uses modern Python features:
  - PEP 604 union types: `X | Y` instead of `typing.Union[X, Y]`
  - Type parameter syntax (PEP 695)
  - Exception groups (PEP 654)

### Package Manager: uv

**All agents MUST use uv for dependency management.**

This project uses [uv](https://docs.astral.sh/uv/) as its package manager and Python package installer.

#### Installation

```bash
# Install uv globally (required for all operations)
pip install uv

# Or on some systems
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Creating a Virtual Environment

**Always create a project-specific virtual environment:**

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

**The RECOMMENDED and MANDATORY way to install dependencies:**

```bash
# Sync all dependencies from pyproject.toml (including dev dependencies)
uv sync --all-extras

# This will:
# - Create/activate the virtual environment if needed
# - Install the project in editable mode
# - Install all dependencies (including dev dependencies)
```

**Alternative sync options (use only when necessary):**

```bash
# Sync only the project (no dev dependencies)
uv sync

# Sync with specific extras
uv sync --extra dev

# Sync only dev dependencies
uv sync --only-dev
```

#### Running Commands

**Always use `uv run` to execute commands in the project's environment:**

```bash
# Run ruff linting
uv run ruff check autorok/ tests/

# Run ruff formatting check
uv run ruff format --check autorok/ tests/

# Run tests
uv run pytest tests/ -v

# Run type checking
uv run pyright autorok/

# Run all checks (RECOMMENDED before committing)
uv run ruff check autorok/ tests/ && \
  ruff format --check autorok/ tests/ && \
  pyright autorok/ && \
  pytest tests/ -v
```

---

## 🎨 Code Style Guidelines

### Formatting
- **Tool**: [ruff](https://docs.astral.sh/ruff/) (replaces black, isort, flake8, pylint)
- **Configuration**: See `pyproject.toml`
- **Line length**: 120 characters
- **Target Python version**: 3.13

### Type Hints
- **Required**: All public functions and methods MUST have type hints
- **Style**: Use PEP 604 union syntax (`X | Y` instead of `typing.Union[X, Y]`)
- **Imports**: Use `from __future__ import annotations` if needed for forward references
- **Optional types**: Use `X | None` instead of `Optional[X]`

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `SigrokCLI`, `Autorok`)
- **Functions/Methods**: `snake_case` (e.g., `scan_devices`, `configure_measurement`)
- **Variables**: `snake_case` (e.g., `active_device`, `measurement_cfg`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`)
- **Private members**: `_leading_underscore` (e.g., `_sigrok_path`, `_active_device`)
- **Enums**: `PascalCase` members (e.g., `OutputType.CSV`, `InputType.BINARY`)

### Docstrings
- **Format**: Google-style docstrings
- **Required**: All public classes, functions, and methods
- **Content**: Include Parameters, Returns, Raises sections where applicable

Example:
```python
"""
Scans for connected devices.

Parameters
----------
driver : str, optional
    The driver to scan with, by default "demo".

Returns
-------
list[Device]
    List of detected Device instances.

Raises
------
SigrokNotFoundError
    If sigrok-cli is not available.
"""
```

### Error Handling
- **Custom exceptions**: Use the exception hierarchy from `exceptions.py`
- **Validation**: Validate inputs early, raise descriptive errors
- **Subprocess calls**: Use `check=True` and handle `subprocess.CalledProcessError`

### Imports
- **Order**: Standard library, third-party, local (absolute imports)
- **Grouping**: One import per line, alphabetically sorted within groups
- **Wildcard imports**: Avoid (except in `__init__.py` for package exports)

---

## 🏗️ Feature Development Methodology

**All agents MUST follow Test-Driven Development (TDD) when adding new features.**

### TDD Workflow

```
1. Write a failing test for the new feature
   ↓
2. Run test - it should FAIL (red)
   ↓
3. Write minimal code to make test pass
   ↓
4. Run test - it should PASS (green)
   ↓
5. Refactor code (improve design without changing behavior)
   ↓
6. Run all tests - all should PASS
   ↓
7. Run linting and formatting checks
   ↓
8. Commit changes
```

### Adding a New Backend

The architecture follows the **Strategy Pattern** with a common interface. To add a new backend:

#### 1. Define the Interface (Already Done)
The abstract base class `SigrokDriver` in `common.py` defines the interface:

```python
class SigrokDriver(ABC):
    @abstractmethod
    def scan_devices(self) -> list[Device]: ...
    
    @abstractmethod
    def select_measurement_device(self, device: Device) -> Device: ...
    
    @abstractmethod
    def configure_channels(self, ch_list: list[str] | str, all_ch: bool = False) -> list[str]: ...
    
    @abstractmethod
    def configure_measurement(self, ...) -> None: ...
    
    @abstractmethod
    def start_sampled_measurement(self, samples: int, decode: bool = False) -> subprocess.CompletedProcess[str]: ...
    
    @abstractmethod
    def start_framed_measurement(self, frames: int, decode: bool = False) -> subprocess.CompletedProcess[str]: ...
    
    @abstractmethod
    def start_timed_measurement(self, sampling_time: int, decode: bool = False) -> subprocess.CompletedProcess[str]: ...
```

#### 2. Implement the Backend
Create a new module (e.g., `libsigrok.py`) that:
- Inherits from `SigrokDriver`
- Implements all abstract methods
- Handles backend-specific logic

Example structure:
```python
from autorok.common import SigrokDriver, OutputType
from autorok.devices import Device


class LibSigrok(SigrokDriver):
    """Driver using libsigrok Python bindings."""

    def __init__(self) -> None:
        # Initialize libsigrok connection
        self._context = None
        self._session = None

    def scan_devices(self) -> list[Device]:
        # Use libsigrok API to scan for devices
        # Return list of Device instances
        ...

    # Implement all other abstract methods...
```

#### 3. Register the Backend
Add the new backend to `SigrokInterface` enum in `autorok.py`:

```python
class SigrokInterface(enum.Enum):
    SIGROK_CLI = SigrokCLI
    LIB_SIGROK = LibSigrok  # New backend
    LIB_SIGROK_4DSL = LibSigrok4DSL  # Future backend
```

#### 4. Write Tests
Create comprehensive tests in `tests/test_<backend>.py`:

```python
import pytest
from autorok.autorok import Autorok, SigrokInterface


@pytest.fixture
def backend():
    return Autorok(iface=SigrokInterface.LIB_SIGROK)


def test_scan_devices(backend):
    devices = backend.scan_devices()
    assert isinstance(devices, list)
    assert all(isinstance(d, Device) for d in devices)


def test_configure_measurement(backend):
    # Test configuration
    ...
```

#### 5. Update Documentation
- Update `AGENTS.md` with backend-specific notes
- Update README.md if needed

### Adding New Features to Existing Backends

1. **Add to Abstract Base Class First**
   - If the feature is common to all backends, add the method to `SigrokDriver`
   - Make it `@abstractmethod` so all backends must implement it

2. **Implement in Each Backend**
   - Implement the method in each concrete backend class
   - Maintain consistent behavior across backends

3. **Add to Main Interface**
   - Add wrapper method in `Autorok` class that delegates to the active backend

4. **Write Tests**
   - Test the new feature in each backend
   - Test edge cases and error conditions

---

## 🧪 Testing Strategy

### Test Structure
```
tests/
├── __init__.py
├── conftest.py          # Shared fixtures
├── test_sigrokcli.py    # SigrokCLI backend tests
├── test_libsigrok.py    # Future: libsigrok backend tests
└── test_autorok.py       # Main Autorok class tests
```

### Test Types
1. **Unit Tests**: Test individual functions/methods in isolation
2. **Integration Tests**: Test interactions between components
3. **Backend Tests**: Test backend-specific functionality
4. **Error Tests**: Test error handling and edge cases

### Test Guidelines
- Use `pytest` framework
- Use fixtures for common setup (e.g., `sigrok` fixture)
- Test both happy paths and error conditions
- Use mocking for external dependencies (e.g., `subprocess.run`)
- Keep tests fast and deterministic

### Mocking Example
```python
from unittest.mock import Mock, patch
import pytest


def test_scan_devices_with_mock():
    with patch("autorok.sigrokcli.subprocess.run") as mock_run:
        # Setup mock response
        mock_result = Mock()
        mock_result.stdout = "sigrok-cli version\ndemo\n"
        mock_result.returncode = 0
        mock_run.return_value = mock_result

        # Test
        sigrok = Autorok(iface=SigrokInterface.SIGROK_CLI)
        devices = sigrok.scan_devices()

        # Assert
        assert len(devices) > 0
        mock_run.assert_called_once()
```

---

## 🔄 Common Workflows

### Adding a New Device Definition
1. Add to `devices.py`:
```python
class DeviceList:
    # Existing devices...
    new_device = Device(
        driver="new-driver",
        port="",
        analog_ch=["A0", "A1"],
        digital_ch=["D0", "D1", "D2"],
    )
```

2. Test the new device is detected (if applicable)

### Adding a New Configuration Option
1. Add to `OutputType` or `InputType` enum in `common.py` (if it's an output/input type)
2. Update backend implementation to support the option
3. Add tests for the new option

### Fixing a Bug
1. Write a test that reproduces the bug
2. Run test - it should FAIL
3. Fix the code
4. Run test - it should PASS
5. Run all tests to ensure no regressions

---

## ✅ Quality Checklist

**Before committing or pushing any changes, agents MUST verify:**

### Code Quality
- [ ] All public functions/methods have type hints
- [ ] All public classes/functions have docstrings (Google style)
- [ ] Code follows naming conventions
- [ ] No unused imports
- [ ] No print statements in library code (use logging if needed)
- [ ] Error handling is comprehensive
- [ ] Custom exceptions are used where appropriate

### Testing
- [ ] All existing tests pass
- [ ] New functionality has corresponding tests
- [ ] Edge cases are tested
- [ ] Error conditions are tested

### Linting & Formatting
- [ ] `uv run ruff check autorok/ tests/` - all lint checks pass
- [ ] `uv run ruff format --check autorok/ tests/` - all formatting checks pass
- [ ] `uv run pyright autorok/` - all type checks pass

### Documentation
- [ ] AGENTS.md is updated if workflows change
- [ ] New public APIs are documented
- [ ] Breaking changes are noted

### Git
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Commit messages are descriptive and concise
- [ ] Related changes are in a single commit

---

## 📚 Additional Resources

- [uv Documentation](https://docs.astral.sh/uv/)
- [ruff Documentation](https://docs.astral.sh/ruff/)
- [Python 3.13 Documentation](https://docs.python.org/3.13/)
- [sigrok-cli Documentation](https://sigrok.org/wiki/Sigrok-cli)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Google Style Docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

---

## ⚠️ Important Notes for Agents

1. **ALWAYS use `uv sync --all-extras`** - This ensures your environment matches CI
2. **ALWAYS run all checks before committing** - Lint, format, type check, tests
3. **ALWAYS follow TDD** - Write tests first, then implementation
4. **ALWAYS maintain backward compatibility** - Don't break existing APIs
5. **ALWAYS use the abstract interface** - Don't bypass `SigrokDriver` methods
6. **NEVER commit broken code** - All tests must pass
7. **NEVER push directly to master** - Always use feature branches and PRs

---

*Last updated: $(date)*
*Maintainer: KhazAkar*
