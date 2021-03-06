import sys
import os
import psutil
import pyglet
import importlib
import pkgutil


def get_system_info():

    # Three lines for getting screen resolution
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_default_screen()

    mem = psutil.virtual_memory()

    return {
        'OS': sys.platform,
        'PYTHON': sys.version,
        'RESOLUTION': [screen.width, screen.height],
        'AVAILMEMORYMB': mem.available/1024./1024
    }


def force_pypath():

    # Get current files path
    temp = os.path.dirname(os.path.abspath(__file__))

    # Find /bci in temp and change to different os notations
    BCI_PATH = temp[0:temp.rfind('bci')+3] # Notation for windows
    BCI_PATH2 = BCI_PATH.replace('\\','/') # Notation used on unix and mac

    # Add to path if not already included.
    if BCI_PATH not in sys.path:
        sys.path.append(BCI_PATH)

    if BCI_PATH2 not in sys.path:
        sys.path.append(BCI_PATH2)


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages.
    https://stackoverflow.com/questions/3365740/how-to-import-all-submodules

    Parameters
    ----------
        package : str | package
            name of package or package instance
        recursive : bool, optional

    Returns
    -------
        dict[str, types.ModuleType]
    """
    if type(package) == str or type(package) == unicode:
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        if name.startswith('test'):
            continue
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results
