import subprocess
import click


def _run(command: list[str]):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as err:
        click.echo(f"Error encountered: {err}", err=True)
        raise click.Abort()


@click.command()
@click.option("--mypy", is_flag=True, default=False, help="Run mypy type checks")
@click.option("--pytest", is_flag=True, default=False, help="Run pytest tests")
@click.option("--ruff", is_flag=True, default=False, help="Run ruff linting")
def run(mypy: bool = False, pytest: bool = False, ruff: bool = False):
    """Run mypy, pytest, and ruff checks on the project."""
    if mypy:
        click.echo("Running mypy type checks...")
        _run(["mypy", "."])

    if pytest:
        click.echo("Running pytest tests...")
        _run(["pytest", "."])

    if ruff:
        click.echo("Running ruff linting...")
        _run(["ruff", "check"])

    click.echo("All checks passed successfully!")
