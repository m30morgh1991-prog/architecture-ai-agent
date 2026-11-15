"""Provider-neutral CAD conversion adapters, validators, and comparators."""
from .dxf_comparator import DxfComparator, DxfComparisonReport, compare_dxf_files
from .dxf_validator import DxfValidationReport, DxfValidator, validate_dxf
from .engine import CadConversionEngine, ProviderRegistry
from .oda_file_converter import ConversionError, ConversionResult, ODAFileConverter, ODAFileConverterConfig
from .provider import CadConversionProvider

__all__ = [
    "CadConversionEngine",
    "CadConversionProvider",
    "ConversionError",
    "ConversionResult",
    "DxfComparator",
    "DxfComparisonReport",
    "DxfValidationReport",
    "DxfValidator",
    "ODAFileConverter",
    "ODAFileConverterConfig",
    "ProviderRegistry",
    "compare_dxf_files",
    "validate_dxf",
]
