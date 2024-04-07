import click
import uvicorn
from alembic.command import upgrade
from alembic.config import Config
from argon2 import PasswordHasher
from os import path

from pixelperfect import __application__, __version__
from pixelperfect.db import crud
from pixelperfect.db.database import get_db


@click.group()
@click.version_option(prog_name=__application__, version=__version__)
def main():
    pass


@main.command()
def migrate():
    config = Config(file_=path.join(path.dirname(__file__), "alembic.ini"))
    config.set_main_option("script_location", path.join(path.dirname(__file__), "alembic"))
    upgrade(config, "head")


@main.command()
@click.option('--host', default='127.0.0.1', show_default=True)
@click.option('--port', default=8000, show_default=True)
@click.option('--log-level', default="info", show_default=True,
              type=click.Choice(['critical', 'error', 'warning', 'info', 'debug', 'trace'], case_sensitive=False))
@click.option('--workers', default=10, show_default=True)
def runserver(host, port, log_level, workers):
    config = uvicorn.Config("pixelperfect.app:app", host=host, port=port, log_level=log_level, workers=workers)
    server = uvicorn.Server(config)
    server.run()


def reset_password(username: str, password: str):
    db = next(get_db())
    user = crud.get_user(db=db, username=username)
    crud.update_user_password(db=db, db_user=user, hashed_password=PasswordHasher().hash(password))
    click.echo("Password updated")


@main.command()
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def reset_password_admin(password):
    reset_password(username='admin', password=password)


@main.command()
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def reset_password_viewer(password):
    reset_password(username='viewer', password=password)


if __name__ == "__main__":
    main()
