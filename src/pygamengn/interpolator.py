import abc
import numpy


class Interpolator(abc.ABC):
    """Base class for all supported interpolation types."""

    def __init__(self, from_value: float = 0.0, to_value: float = 1.0):
        self._from_value = from_value
        self._to_value = to_value
        self.__inverted_range = to_value < from_value
        if from_value == to_value:
            raise ValueError(f"Interpolator does not support from_value == to_value")


    def get(self, value: float) -> float:
        if value >= self._from_value and value <= self._to_value or (
            self.__inverted_range and value <= self._from_value and value >= self._to_value
        ):
            return self._from_value + self._func(value) * (self._to_value - self._from_value)
        else:
            raise ValueError(f"Value is outside Interpolator's range [{self._from_value}, {self._to_value}]")


    def _normalize(self, value: float) -> float:
        return (value - self._from_value) / (self._to_value - self._from_value)


    @abc.abstractmethod
    def _func(self, x: float) -> float:
        pass



class EaseInInterpolator(Interpolator):
    """Interpolator that eases in. It uses f(x) = x^2 in the range [0.0, 1.0] as its function."""

    def _func(self, x: float) -> float:
        return self._normalize(x) ** 2



class EaseOutInterpolator(Interpolator):
    """Interpolator that eases in. It uses f(x) = -(x - 1)^2 + 1 in the range [0.0, 1.0] as its function."""

    def _func(self, x: float) -> float:
        return -((self._normalize(x) - 1.0) ** 2) + 1



class EaseAllInterpolator(Interpolator):
    """Interpolator that eases in and out. It uses f(x) = (1 - cos(x*Pi)) / 2 in the range [0.0, 1.0] as its function."""

    def _func(self, x: float) -> float:
        return (1.0 - numpy.cos(self._normalize(x) * numpy.pi)) / 2.0



class LinearInterpolator(Interpolator):
    """Interpolator that eases in and out. It uses f(x) = (1 - cos(x*Pi)) / 2 in the range [0.0, 1.0] as its function."""

    def _func(self, x: float) -> float:
        return self._normalize(x)
