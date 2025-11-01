"""Provider registry."""
from __future__ import annotations

from typing import Dict, List, Type

from . import aldi, asda, iceland, lidl, morrisons, ocado, sainsburys, tesco, waitrose
from .base import BaseProvider

PROVIDER_CLASSES: List[Type[BaseProvider]] = [
    tesco.TescoProvider,
    sainsburys.SainsburysProvider,
    asda.AsdaProvider,
    morrisons.MorrisonsProvider,
    aldi.AldiProvider,
    lidl.LidlProvider,
    waitrose.WaitroseProvider,
    ocado.OcadoProvider,
    iceland.IcelandProvider,
]


def get_providers() -> Dict[str, BaseProvider]:
    """Instantiate and return providers keyed by retailer name."""

    return {provider_cls.retailer: provider_cls() for provider_cls in PROVIDER_CLASSES}

