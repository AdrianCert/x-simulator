import nox


@nox.session(python=["3.10"], reuse_venv=True)
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
