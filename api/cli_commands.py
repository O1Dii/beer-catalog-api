import click

from api import app
from api.data_loader import DataLoader, db


@app.cli.command('create_db')
def create_db():
    db.create_all()


@app.cli.command('drop_db')
def drop_db():
    db.drop_all()


@app.cli.command('load_data')
@click.argument('pages')
def load_data(pages):
    DataLoader.load_data(pages)
