# Copyright (c) Tencent Inc. All rights reserved.
import importlib.metadata as importlib_metadata
from .models import *  # noqa
from .datasets import *  # noqa
from .engine import *  # noqa

try:
    __version__ = importlib_metadata.version(__package__ or __name__)
except importlib_metadata.PackageNotFoundError:
    __version__ = '0.0.0'

from mmengine.registry import MODELS as MMENGINE_MODELS
from mmyolo.registry import MODELS as MMYOLO_MODELS

def _register_custom_modules():
    """register mmengine MODELS"""
    for name, module_class in MMYOLO_MODELS.module_dict.items():
        if name not in MMENGINE_MODELS.module_dict:
            MMENGINE_MODELS.register_module(name=name, module=module_class)
            # print(f"Auto-registered {name} to mmengine registry from yolo_world")

_has_registered = getattr(MMENGINE_MODELS, '_yolo_world_registered', False)
if not _has_registered:
    _register_custom_modules()
    MMENGINE_MODELS._yolo_world_registered = True