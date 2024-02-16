from pathlib import Path
import tempfile


def usePath(rel_path: str):
    """
    return the corrected path

    :param rel_path: the relative path that needs to be resolved.
    """
    path = Path(rel_path)
    absolute_path = (
        path.resolve() if "~" not in rel_path else path.expanduser().resolve()
    )
    return absolute_path


import os
import sys


def useTemp():
    """
    returns the path to the AZio temp folder
    """
    temp_dir = tempfile.TemporaryDirectory()

    return temp_dir


def useBin():
    """
    returns the path to the AZio Bin
    """

    azio_bin = Path.home() / ".azio" / "bin"

    if not azio_bin.exists():
        # Create the directory, including any parents
        azio_bin.mkdir(parents=True, exist_ok=True)
        home = Path.home()
        shell_profile_paths = [
            home / ".bashrc",
            home / ".bash_profile",
            home / ".zshrc",
        ]

        # Detect which shell profile file exists
        for profile_path in shell_profile_paths:
            if profile_path.exists():
                with open(profile_path, "a") as file:
                    file.write(f'\nexport PATH="{azio_bin}:$PATH"\n')
                break
        else:
            print(
                "No known shell profile file found. Please manually add '$HOME/.azio/bin' to your $PATH."
            )

    return azio_bin
