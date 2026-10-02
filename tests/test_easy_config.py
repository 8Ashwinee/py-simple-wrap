import git
import pytest

from py_simple_package.src.py_simple.easy_config import (
    EasyConfigError,
    gitignore_config,
)
from py_simple import gitignore_config as top_level_gitignore_config


def test_gitignore_config_creates_file_at_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    gitignore_config()

    gitignore_file = tmp_path / ".gitignore"
    assert gitignore_file.exists()
    content = gitignore_file.read_text(encoding="utf-8")
    assert "__pycache__/" in content
    assert "*.py[cod]" in content
    assert ".venv/" in content
    assert ".env" in content


def test_gitignore_config_does_not_overwrite_existing_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    gitignore_file = tmp_path / ".gitignore"
    gitignore_file.write_text("custom gitignore\n", encoding="utf-8")

    gitignore_config()

    assert gitignore_file.read_text(encoding="utf-8") == "custom gitignore\n"


def test_gitignore_config_can_target_repository_root(tmp_path, monkeypatch):
    git.Repo.init(tmp_path)
    nested = tmp_path / "nested"
    nested.mkdir()
    monkeypatch.chdir(nested)

    gitignore_config(at_root=False)

    gitignore_file = tmp_path / ".gitignore"
    assert gitignore_file.exists()
    content = gitignore_file.read_text(encoding="utf-8")
    assert "__pycache__/" in content
    assert not (nested / ".gitignore").exists()


def test_gitignore_config_wraps_template_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def missing_template(_package):
        raise FileNotFoundError("template missing")

    monkeypatch.setattr(
        "py_simple_package.src.py_simple.easy_config.files", missing_template
    )

    with pytest.raises(EasyConfigError, match="template missing"):
        gitignore_config()


def test_gitignore_config_wraps_git_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    with pytest.raises(EasyConfigError):
        gitignore_config(at_root=False)


def test_gitignore_config_wraps_permission_errors(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def mock_open(*args, **kwargs):
        raise PermissionError("Permission denied")

    monkeypatch.setattr("builtins.open", mock_open)

    with pytest.raises(EasyConfigError, match="Permission denied"):
        gitignore_config()


def test_gitignore_config_imported_from_py_simple():
    assert callable(top_level_gitignore_config)
