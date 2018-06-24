from cogwheels.versioning import get_version

# major.minor.patch.release.number
# release must be one of alpha, beta, rc, or final
VERSION = (0, 0, 1, 'alpha', 1)
__version__ = get_version(VERSION)
