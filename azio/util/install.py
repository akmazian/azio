import subprocess
import zipfile

import click

from ..helper import useBin, usePath, useSystem, useTemp


@click.command(name="install")
@click.option(
    "--method",
    "-m",
    help="The method to use for installation",
    type=click.Choice(["conda", "pip", "brew"]),
)
@click.argument("package")
def install(package):
    """This helper command installs packages you might need.
    
    THIS COMMAND IS NOT READY FOR USE YET.

    This install command mostly takes care of packages not available via common distributors, but will also work for bioconda or pip packages.

    AZio defaults to bioconda when installing packages. If you want other options, tweak the --method option.

    Here's the list of packages available for downloading with AZio:

    Alignment tools

    """

    if package in []:
        temp_dir = useTemp()

        temp_path = temp_dir / f"{package}.zip"

        subprocess.run(["mkdir", temp_path])

        linux_and_mac_callback = f"curl -L {{url}} --output {temp_path}"
        win_callback = (
            f'powershell -Command "Invoke-WebRequest -Uri {{url}} -OutFile {temp_path}"'
        )

        download_command = useSystem(linux_and_mac_callback, win_callback)

        subprocess.run(download_command.format(url=url))

        dest_dir = useBin()

        dest_path = dest_dir / package

        try:
            with zipfile.ZipFile(temp_path, "r") as zip_ref:
                zip_ref.extractall(dest_path)
                print(f"Extracted {package} to {dest_path}")
        except zipfile.BadZipFile:
            print("Error: The file is not a zip file or it is corrupted.")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        base_command = ["conda", "install", "--channel", "bioconda"]
        
        subprocess.run([*base_command, package])
