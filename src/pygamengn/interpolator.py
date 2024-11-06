import abc
import numpy

from enum import StrEnum, auto


class InterpolationMode(StrEnum):
    EASE_IN = auto()
    EASE_OUT = auto()
    EASE_ALL = auto()
    LINEAR = auto()


class Interpolator(abc.ABC):
    """Base class for all supported time-based interpolation types."""

    def __init__(self, duration: int, from_value = 0.0, to_value = 1.0):
        self._duration = duration
        self.__from_value = from_value
        self.__to_value = to_value


    def get(self, t: int):
        if t < 0:
            return self.__from_value
        elif t > self._duration:
            return self.__to_value
        else:
            return self.__from_value + self._func(t) * (self.__to_value - self.__from_value)


    def _normalize(self, t: int):
        return (value - self.__from_value) / (self.__to_value - self.__from_value)


    @abc.abstractmethod
    def _func(self, t: int):
        pass



class EaseInInterpolator(Interpolator):
    """Interpolator that eases in. It uses f(x) = x^2 in the range [0.0, 1.0] as its function."""

    def _func(self, t: float) -> float:
        return (t / self._duration) ** 2



class EaseOutInterpolator(Interpolator):
    """Interpolator that eases in. It uses f(x) = -(x - 1)^2 + 1 in the range [0.0, 1.0] as its function."""

    def _func(self, t: int) -> float:
        return -(((t / self._duration) - 1.0) ** 2) + 1



class EaseAllInterpolator(Interpolator):
    """Interpolator that eases in and out. It uses f(x) = (1 - cos(x*Pi)) / 2 in the range [0.0, 1.0] as its function."""

    def _func(self, t: int) -> float:
        return (1.0 - numpy.cos((t / self._duration) * numpy.pi)) / 2.0



class LinearInterpolator(Interpolator):
    """Linear interpolator. It uses f(x) = x in the range [0.0, 1.0] as its function."""

    def _func(self, t: int) -> float:
        return (t / self._duration)
