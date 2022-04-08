import click
from root import bh


@bh.command()
def download():
    """Command on cli1"""
    pass

cli = click.CommandCollection(sources=[bh])

if __name__ == '__main__':
    cli()