import click
import subprocess
import sys


@click.group()
@click.version_option()
def cli():
    "Hey there! Welcome to AZio, the promptful wrapper for useful biopackages."


from .alignment.kallisto import kallisto

cli.add_command(kallisto)

from .util.install import install

cli.add_command(install)