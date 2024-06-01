import nox


@nox.session(python=["3.10", "3.11", "3.12"], venv_backend="uv")
def tests(session):
    session.install("-e", ".[dev]")
    session.run(
        "coverage",
        "run",
        "--source=src",
        "--rcfile=pyproject.toml",
        "-m",
        "unittest",
        "discover",
        "tests",
    )
    session.run("coverage", "report", "--rcfile=pyproject.toml")
    session.run("coverage", "html", "--rcfile=pyproject.toml")


@nox.session(python="3.10", reuse_venv=True, venv_backend="uv")
def docs(session):
    session.install("-e", ".[docs]")
    session.run("mkdocs", "build")


@nox.session(python="3.10", reuse_venv=True, venv_backend="uv")
@nox.parametrize("package", ["src", "tests"])
def ruff(session, package):
    session.install("ruff")
    session.run("ruff", "format", package)
    session.run("ruff", "check", "--fix", package)
