#!/usr/bin/env python3

import doctest
from typing import Union, List


class Polynomial:
    """Class representing a math polynomial"""

    def __init__(self, *args: Union[list, int], **kwargs: int):
        """
        Class initializer

        Components of polynomial could be speicifed in 3 ways:
         - as one argument of type list with components in reverse order (ax^0 + bx^1 + cx^2 + ...) --> [a, b, c, ...]
         - as any number of int arguments (reverse order again) --> a, b, c, ...
         - as named arguments with key like xN and value of type int --> x0=a, x1=b, x2=c, ...

        :param args: Given unnamed arguments stored in tuple (implementation detail)
        :param kwargs: Given named arguments stored in dictionary {arg_name: arg_value, ...} (implementaion detail)

        Tests (and examples of correct input):
        >>> pol1 = Polynomial([1,-3,0,2])
        >>> pol2 = Polynomial(1,-3,0,2)
        >>> pol3 = Polynomial(x0=1,x3=2,x1=-3)
        >>> pol4 = Polynomial()
        """
        if len(args) > 0 and isinstance(args[0], list):
            self.__components = args[0]
        elif len(args) > 0:
            self.__components = list(args)
        elif len(kwargs) > 0:
            highest_degree = 0

            # Find the highest degree (keys of kwargs are: "xN", where N is degree)
            for degree in kwargs:
                if int(degree[1:]) > highest_degree:
                    highest_degree = int(degree[1:])

            self.__components = [
                kwargs[f"x{degree}"] if f"x{degree}" in kwargs else 0 for degree in range(highest_degree + 1)
            ]
        else:
            self.__components = [0]

    @property
    def components(self) -> List[int]:
        """
        Getter for components property

        :return: Components of polynomial (only with non-zero coefficients)
        """
        return self.__components

    def __multiply_components(self, base_components: List[int]) -> List[int]:
        """
        Counts multiplication of specified components with this polynomial's components

        :param base_components: Base components to multipy with polynomial's components
        :return: Components multiplication result
        """
        # Source: https://stackoverflow.com/a/43249599
        result_components = [0] * (len(self.__components) + len(base_components) - 1)

        for outer_degree in range(len(base_components)):
            outer_coefficient = base_components[outer_degree]
            for inner_degree in range(len(self.__components)):
                result_components[outer_degree + inner_degree] += outer_coefficient * self.__components[inner_degree]

        return result_components

    def __count_value(self, x_value: Union[float, int]) -> Union[float, int]:
        """
        Counts polynom value for specified x

        :param x_value: X value to use
        :return: Polynom value for x
        """
        accumulator = 0

        for degree, coefficient in enumerate(self.__components):
            accumulator += coefficient * (x_value ** degree)

        return accumulator

    def derivative(self) -> 'Polynomial':
        """
        Derives the polynomial

        :return: Derived polynomial

        Tests:
        >>> pol1 = Polynomial([1,-3,0,2])
        >>> print(pol1.derivative())
        6x^2 - 3
        """
        result_components = [0] * (len(self.__components) - 1)

        for degree, coefficient in enumerate(self.__components):
            # Skip absolute component (derivation makes 0 from it)
            if degree == 0:
                continue

            result_components[degree - 1] = coefficient * degree

        return Polynomial(result_components)

    def at_value(self, x_1: Union[float, int], x_2: Union[float, int] = None) -> Union[float, int]:
        """
        Counts value of polynom for specified x (x_1) or subtraction of two values for x_1 and x_2

        :param x_1: First value of x
        :param x_2: Second value of x (optional)
        :return: Value of polynom for specified x or subtraction of two values for specified xs

        Tests:
        >>> pol1 = Polynomial([1,-3,0,2])
        >>> print(pol1.at_value(2))
        11
        >>> print(pol1.at_value(2,3))
        35
        """
        value_1 = self.__count_value(x_1)

        # Only count value of polynom for x = x_1
        if x_2 is None:
            return value_1

        # Count subtraction of two values
        value_2 = self.__count_value(x_2)

        return value_2 - value_1

    def __str__(self) -> str:
        """
        Automatically converts polynomial in usual format

        :return: Polynomial in string form

        Tests:
        >>> pol2 = Polynomial(1,-3,0,2)
        >>> print(pol2)
        2x^3 - 3x + 1
        >>> print(Polynomial(1,1,-1))
        - x^2 + x + 1
        >>> print(Polynomial(x2=0))
        0
        """
        string_form = str()
        polynomial_degree = len(self.__components) - 1

        # Polynomial with no component (or with zero components only) is understood as 0
        if self.__components.count(0) == len(self.__components):
            return "0"

        for degree_complement, coefficient in enumerate(reversed(self.__components)):
            # Skip zero coefficients
            if coefficient == 0:
                continue

            # Get degree from its complement (complement is used due to reversed iteration)
            degree = polynomial_degree - degree_complement

            # Add sign mark
            string_form += " + " if coefficient > 0 else " - "
            # Add coefficient number
            string_form += f"{abs(coefficient)}" if abs(coefficient) != 1 or degree == 0 else ""
            # Add x^degree if degree isn't too low (linear and absolute component)
            string_form += f"x^{degree}" if degree > 1 else ("x" if degree == 1 else "")

        # Remove leading sign mark if the coefficient of the highest degree is positive or leading space for negative
        return string_form[3:] if string_form.startswith(" +") else string_form[1:]

    def __eq__(self, other: object) -> bool:
        """
        Checks if this polynomial equals to other

        :param other: Other polynomial
        :return: Is this polynomial equal to other

        Tests:
        >>> pol1 = Polynomial([1,-3,0,2])
        >>> pol2 = Polynomial(1,-3,0,2)
        >>> pol1 == pol2
        True
        >>> Polynomial(1, 0, 1) == Polynomial(1, 0, 1, 0)
        True
        >>> Polynomial(1, 0, 1, 0) == Polynomial(1, 0, 1)
        True
        >>> Polynomial(1, 0, 1) == Polynomial(1, 0, 1, 1)
        False
        >>> Polynomial(1, 0, 1, 1) == Polynomial(1, 0, 1)
        False
        """
        # Only comparison of two Polynomial objects is supported
        if not isinstance(other, Polynomial):
            return NotImplemented

        min_length = min(len(self.__components), len(other.components))

        # Compare common components
        if self.__components[:min_length] != other.components[:min_length]:
            return False

        # Compare the rest components in higher (longer) polynomial
        if len(self.__components) > len(other.components):
            return self.__components[min_length:].count(0) == len(self.__components[min_length:])

        return other.components[min_length:].count(0) == len(other.components[min_length:])

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        """
        Counts addition of this polynomial and other

        :param other: Other polynomial to add
        :return: Result polynomial

        Tests:
        >>> print(Polynomial(1,-3,0,2) + Polynomial(0, 2, 1))
        2x^3 + x^2 - x + 1
        >>> print(Polynomial(0, 2, 1) + Polynomial(1,-3,0,2))
        2x^3 + x^2 - x + 1
        """
        highest_common_degree = min(len(self.__components), len(other.components)) - 1

        # Count summaries of common components
        components_summaries = [
            other.components[degree] + self.__components[degree] for degree in range(highest_common_degree + 1)
        ]

        # Append components of polynomial with higher degree
        if len(other.components) < len(self.__components):
            components_summaries.extend(self.__components[highest_common_degree + 1:])
        else:
            components_summaries.extend(other.components[highest_common_degree + 1:])

        return Polynomial(components_summaries)

    def __pow__(self, power: int) -> 'Polynomial':
        """
        Counts power of the polynomial

        :param power: Power exponent
        :return: Result polynomial

        Tests:
        >>> print(Polynomial(-1, 1) ** 2)
        x^2 - 2x + 1
        >>> print(Polynomial(-1, 1) ** 3)
        x^3 - 3x^2 + 3x - 1
        """
        result_components = [1]
        for _ in range(power):
            result_components = self.__multiply_components(result_components)

        return Polynomial(result_components)


def test() -> None:
    """Tests Polynomial class"""
    assert str(Polynomial(0, 1, 0, -1, 4, -2, 0, 1, 3, 0)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial([-5, 1, 0, -1, 4, -2, 0, 1, 3, 0])) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x - 5"
    assert str(Polynomial(x7=1, x4=4, x8=3, x9=0, x0=0, x5=-2, x3=-1, x1=1)) == "3x^8 + x^7 - 2x^5 + 4x^4 - x^3 + x"
    assert str(Polynomial(x2=0)) == "0"
    assert str(Polynomial(x0=0)) == "0"
    assert Polynomial(x0=2, x1=0, x3=0, x2=3) == Polynomial(2, 0, 3)
    assert Polynomial(x2=0) == Polynomial(x0=0)
    assert str(Polynomial(x0=1) + Polynomial(x1=1)) == "x + 1"
    assert str(Polynomial([-1, 1, 1, 0]) + Polynomial(1, -1, 1)) == "2x^2"
    pol1 = Polynomial(x2=3, x0=1)
    pol2 = Polynomial(x1=1, x3=0)
    assert str(pol1 + pol2) == "3x^2 + x + 1"
    assert str(pol1 + pol2) == "3x^2 + x + 1"
    assert str(Polynomial(x0=-1, x1=1) ** 1) == "x - 1"
    assert str(Polynomial(x0=-1, x1=1) ** 2) == "x^2 - 2x + 1"
    pol3 = Polynomial(x0=-1, x1=1)
    assert str(pol3 ** 4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(pol3 ** 4) == "x^4 - 4x^3 + 6x^2 - 4x + 1"
    assert str(Polynomial(x0=2).derivative()) == "0"
    assert str(Polynomial(x3=2, x1=3, x0=2).derivative()) == "6x^2 + 3"
    assert str(Polynomial(x3=2, x1=3, x0=2).derivative().derivative()) == "12x"
    pol4 = Polynomial(x3=2, x1=3, x0=2)
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert str(pol4.derivative()) == "6x^2 + 3"
    assert Polynomial(-2, 3, 4, -5).at_value(0) == -2
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3) == 20
    assert Polynomial(x2=3, x0=-1, x1=-2).at_value(3, 5) == 44
    pol5 = Polynomial([1, 0, -2])
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-2.4) == -10.52
    assert pol5.at_value(-1, 3.6) == -23.92
    assert pol5.at_value(-1, 3.6) == -23.92


if __name__ == "__main__":
    doctest.testmod()
    test()
