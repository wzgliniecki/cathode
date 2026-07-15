from .ascii import ASCIIconverter
from .color_blocks import ColorBlocksConverter

CONVERTERS = {
    "ascii": ASCIIconverter,
    "color_blocks": ColorBlocksConverter,
}
