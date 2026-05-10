from typing import Optional, Sequence, Tuple, TypeAlias, Union
from typing import Literal
import pygame

RGBAOutput: TypeAlias = Tuple[int, int, int, int]
ColorValue: TypeAlias = Optional[
    Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
]


Variant: TypeAlias = Literal["default", "outlined", "filled", "text"]
