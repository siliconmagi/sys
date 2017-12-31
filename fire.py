import click


@click.command()
@click.option('--rep',
              default='Plane',
              help='Replace String')
def cli(rep):
    """Return String"""
    click.echo('Hello {}!'.format(rep))
