import subprocess
import sys

import click

from ..helper import useSystem


@click.group()
def kallisto():
    "This is the wrapper for kallisto, the ultimate pseudoalignment tool we all love! It is developed and maintained by the Pachter Lab at CalTech."

    try:
        win_callback = lambda: subprocess.run(
            ["where", "kallisto"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        mac_linux_callback = lambda: subprocess.run(
            ["which", "kallisto"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        useSystem(mac_linux_callback, win_callback)()

        click.secho(
            "We've found kallisto in your PATH! You can start aligning.",
            bold=True,
            fg="cyan",
        )
    except:
        click.secho(
            "It seems like you don't have kallisto installed in your PATH. If you have it on your machine, include it in your PATH. If you don't, make sure to install it first.",
            bold=True,
            fg="red",
        )


@kallisto.command(name="index")
@click.option(
    "-i",
    "--index",
    type=click.Path(exists=False),
    prompt="Path to build index to",
    help="Path to build index to",
    required=True,
)
@click.option(
    "-f",
    "--fasta",
    prompt="Path to raw fasta files",
    help="Path to raw fasta files. You can also pass it in as the argument",
    type=click.Path(exists=True),
    required=False,
)
@click.argument("fasta", type=click.Path(exists=True), required=False)
@click.option(
    "-k",
    "--kmer-size",
    type=click.INT,
    help="k-mer (odd) length (default: 31, max value: 31)",
)
@click.option(
    "-d",
    "--d-list",
    help="Path to a FASTA-file containing sequences to mask from quantification",
    type=click.Path(exists=True),
)
@click.option(
    "--make-unique",
    is_flag=True,
    help="Replace repeated target names with unique names",
)
@click.option(
    "--aa",
    is_flag=True,
    help="Generate index from a FASTA-file containing amino acid sequences",
)
@click.option(
    "--distinguish",
    is_flag=True,
    help="Generate index where sequences are distinguished by the sequence name",
)
@click.option(
    "-t",
    "--threads",
    type=click.INT,
    help="Number of threads to use (default: 1). You can get the number of available processors on Linux systems by `nproc`",
)
@click.option(
    "-m",
    "--min-size",
    type=click.INT,
    help="Length of minimizers (default: automatically chosen)",
)
@click.option(
    "-e",
    "--ec-max-size",
    type=click.INT,
    help="Maximum number of targets in an equivalence class (default: no maximum)",
)
def index(
    index,
    fasta,
    kmer_size,
    d_list,
    make_unique,
    aa,
    distinguish,
    threads,
    min_size,
    ec_max_size,
):
    """Builds a kallisto transcriptome index from a fasta file"""

    command = ["kallisto", "index", "-i", index, fasta]

    if fasta is None:
        return click.echo(
            "Either pass in the fasta files with `-f` or as the arguments"
        )

    if "fasta" not in fasta:
        return click.echo(
            "The raw fasta file should be in either in .fasta format or a gzipped fasta."
        )

    if kmer_size:
        if kmer_size % 2 == 0 or kmer_size < 5 or kmer_size > 31:
            return click.echo("kmer-size must be odd and within [5, 31]")
        command += ["--kmer-size", kmer_size]

    if d_list:
        command += ["--d-list", d_list]

    if make_unique:
        command += ["--make-unique"]

    if aa:
        command += ["--aa"]

    if distinguish:
        command += ["--distinguish"]

    if threads:
        command += ["--threads", threads]

    if min_size:
        command += ["--min-size", min_size]

    if ec_max_size:
        command += ["--ec-max-size", ec_max_size]

    result = subprocess.run(command)

    try:
        result.check_returncode()
        click.echo(result.stdout)
    except:
        click.echo(result.stderr)


@kallisto.command(name="bus")
def bus():
    subprocess.run(["kallisto", "bus"])
