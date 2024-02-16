import sys


def useSystem(linux_and_mac_callback, win_callback):
    """
    return the corrected path

    :param linux_and_mac_callback: the callback for mac and linux-based systems
    :param win_callback: the callback for windows
    """
    if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
        # Linux and macOS
        return linux_and_mac_callback
    elif sys.platform.startswith("win"):
        # Windows
        return win_callback
