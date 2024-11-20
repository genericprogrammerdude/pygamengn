import numpy

from enum import StrEnum, auto


class InterpolationMode(StrEnum):
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_ALL = auto()
    LINEAR = auto()


class Interpolator:
    """Base class for all supported time-based interpolation types."""

    def __init__(
        self,
        duration: int,
        from_value = 0.0,
        to_value = 1.0,
        mode: InterpolationMode = InterpolationMode.LINEAR
    ):
        self.__duration = duration
        self.__from_value = from_value
        self.__to_value = to_value
        self.__diff = self.__to_value - self.__from_value

        if mode == InterpolationMode.LINEAR:
            self.__func = self.__linear
        elif mode == InterpolationMode.EASE_IN:
            self.__func = self.__ease_in
        elif mode == InterpolationMode.EASE_OUT:
            self.__func = self.__ease_out
        elif mode == InterpolationMode.EASE_ALL:
            self.__func = self.__ease_all
        else:
            raise ValueError(f"Unknown interpolation mode: {mode}")

    def get(self, t: int):
        if t < 0:
            return self.__from_value
        elif t > self.__duration:
            return self.__to_value
        else:
            return self.__from_value + self.__func(t) * self.__diff

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, d):
        self.__duration = d

    @property
    def from_value(self):
        return self.__from_value

    @property
    def to_value(self):
        return self.__to_value

    def __ease_in(self, t: float) -> float:
        """Interpolator that eases in. It uses f(x) = x^2 in the range [0.0, 1.0] as its function."""
        return (t / self.__duration) ** 2

    def __ease_out(self, t: int) -> float:
        """Interpolator that eases out. It uses f(x) = -(x - 1)^2 + 1 in the range [0.0, 1.0] as its function."""
        return -(((t / self.__duration) - 1.0) ** 2) + 1

    def __ease_all(self, t: int) -> float:
        """Interpolator that eases in and out. It uses f(x) = (1 - cos(x*Pi)) / 2 in the range [0.0, 1.0] as its function."""
        return (1.0 - numpy.cos((t / self.__duration) * numpy.pi)) / 2.0

    def __linear(self, t: int) -> float:
        """Linear interpolator. It uses f(x) = x in the range [0.0, 1.0] as its function."""
        return (t / self.__duration)
