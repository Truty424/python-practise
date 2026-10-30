# uv, Ruff & Git — Cheat Sheet

### Project Initialization

```bash
uv init --bare          # Create a minimal pyproject.toml
```

### Dependency Management

```bash
uv add <package>        # Add a dependency
uv add --dev <package>  # Add a development dependency
uv remove <package>     # Remove a dependency
```

### Environment & Lockfile

```bash
uv sync                 # Sync dependencies with .venv
uv lock                 # Generate/update uv.lock
uv lock --upgrade       # Upgrade all compatible dependencies
```

### Ruff — Lint & Format

```bash
uv run ruff check .        # Check code quality
uv run ruff check . --fix  # Auto-fix lint issues
uv run ruff format .       # Format code
uv run ruff format --check . 
```

### pytest — Testing

```bash
uv run pytest              # Run all tests
uv run pytest -v           # Run tests with detailed output
```

- `assert` — Verify that a condition is true.
- `@pytest.mark.parametrize` — Run one test with multiple sets of inputs.
- `@pytest.fixture` — Prepare and inject reusable test data or resources.
- `test_` — Prefix for automatic test function discovery.
- `conftest.py` — Share fixtures across multiple test files.

### Git — Branch, Commit & Push

```bash
git switch -c <branch-name>        # Create and switch to a new branch
git status                         # Check changed files
git add .                          # Stage all changes
git commit -m "Commit message"     # Commit changes
git push -u origin <branch-name>   # Push branch to remote
```

### Git — Useful Commands

```bash
git branch                         # List local branches
git switch main                    # Switch to main
git pull origin main               # Update local main
git log --oneline -5               # Show last 5 commits
git reset --soft HEAD~1            # Undo last commit, keep changes staged
```

### Key Files

- `pyproject.toml` — Project configuration and dependencies.
- `uv.lock` — Locked dependency versions.
- `.venv/` — Virtual environment (add to `.gitignore`).
- `.idea/` — PyCharm settings (add to `.gitignore`).