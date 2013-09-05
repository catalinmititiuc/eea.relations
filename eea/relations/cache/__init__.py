""" Caching module
"""
try:
    from eea.cache import cache as eeacache
    from eea.cache import event
    # pyflakes
    InvalidateCacheEvent = event.InvalidateCacheEvent
    ramcache = eeacache
except ImportError:
    # Fail quiet if required cache packages are not installed in order to use
    # this package without caching
    from eea.relations.cache.nocache import ramcache

__all__ = [
    ramcache.__name__,
    InvalidateCacheEvent.__name__,
]
