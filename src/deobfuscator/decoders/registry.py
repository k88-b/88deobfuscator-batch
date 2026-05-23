# -*- coding: utf-8 -*-

import re
from dataclasses import dataclass
from typing import Type
from itertools import zip_longest

from core.config import AppConfig
from core.patterns import Patterns
from core.abstract_decoder import BaseDecoder
from .baseX_decoder import BaseXDecoder
from .compression_decoder import CompressionUtilsDecoder
from .baseX_compression_decoder import BaseCompressionUtilsDecoder
from .blank_decoder import BlankObfDeobfuscator
from .rendy_decoder import RendyDecoder
from .christian_decoder import ChristianObfDeobfuscator
from .clever_decoder import CleverObfDeobfuscator
from .grandiosee_decoder import GrandioseeObfDeobfuscator
from .xindex_decoder import XindexObfDeobfuscator
from .impostor_decoder import ImpostorObfDeobfuscator

config = AppConfig()


@dataclass(frozen=True)
class ObfuscationInfo:
    key: str
    pattern: re.Pattern | None
    decoder_class: Type[BaseDecoder]


REGISTRY = [
    ObfuscationInfo("base64", Patterns.BASE64_PATTERN, BaseXDecoder),
    ObfuscationInfo("base32", Patterns.BASE32_PATTERN, BaseXDecoder),
    ObfuscationInfo("base16", Patterns.BASE16_PATTERN, BaseXDecoder),
    ObfuscationInfo("zlib", Patterns.ZLIB_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo("gzip", Patterns.GZIP_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo("lzma", Patterns.LZMA_PATTERN, CompressionUtilsDecoder),
    ObfuscationInfo(
        "base64+zlib", Patterns.BASE64_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base64+gzip", Patterns.BASE64_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base64+lzma", Patterns.BASE64_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+zlib", Patterns.BASE32_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+gzip", Patterns.BASE32_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base32+lzma", Patterns.BASE32_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+zlib", Patterns.BASE16_ZLIB_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+gzip", Patterns.BASE16_GZIP_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo(
        "base16+lzma", Patterns.BASE16_LZMA_PATTERN, BaseCompressionUtilsDecoder
    ),
    ObfuscationInfo("rendy", Patterns.RENDY_OBF_PATTERN, RendyDecoder),
    ObfuscationInfo("christian", None, ChristianObfDeobfuscator),
    ObfuscationInfo("blank", Patterns.BLANK_OBF_PATTERN, BlankObfDeobfuscator),
    ObfuscationInfo("clever", Patterns.CLEVER_OBF_PATTERN, CleverObfDeobfuscator),
    ObfuscationInfo(
        "grandiosee", Patterns.GRANDIOSEE_OBF_PATTERN, GrandioseeObfDeobfuscator
    ),
    ObfuscationInfo("xindex", Patterns.XINDEX_OBF_PATTERN, XindexObfDeobfuscator),
    ObfuscationInfo("impostor", Patterns.IMPOSTOR_OBF_PATTERN, ImpostorObfDeobfuscator),
]


DECODER_REGISTRY = {info.key: info.decoder_class for info in REGISTRY}


