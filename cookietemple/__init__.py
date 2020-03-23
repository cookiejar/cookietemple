# -*- coding: utf-8 -*-
try:
    import importlib.metadata as metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata

__version__ = metadata.version('cookietemple')
