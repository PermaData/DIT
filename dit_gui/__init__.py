from os.path import dirname, basename, join, isfile
import glob

this_level = dirname(__file__)
level_up = join("..", this_level)
modules = glob.glob(level_up + "/*.py")
modules.extend(glob.glob(this_level + "/*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]
