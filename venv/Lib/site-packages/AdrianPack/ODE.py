import numpy as np
from typing import Callable

try:
    from Helper import test_inp, binomial, central_point_derivative,\
        backward_point_derivative, forward_point_derivative, ode_decorator
except ImportError:
    from .Helper import test_inp, binomial, central_point_derivative,\
        backward_point_derivative, forward_point_derivative, ode_decorator


@ode_decorator
def euler(fx: Callable, lower: float, upper: float, dt: float,
          x0: float = 0) -> tuple:
    """
    Evaluate differential equations (df/dx = f(x, t)) using eulers method

    USAGE:
        # define the derivative of a function fx that takes an "x" and a "t"
        # input

        def fx(x, t):
            return np.sin(x) * -t**3

        # define lower and upper boundaries, a timestep dt and *optional*
        # a starting position x0
        lower = 5
        upper = 10
        dt = 0.0001
        x0 = 3

        # call the function and assign the returns to tpoints and xpoints
        tpoints, xpoint = euler(fx=fx, lower=lower, upper=upper, dt=dt, x0=x0)

    :param: fx
        ObjectType -> Function
        Function, dx/dt = f(x, t), that takes x, t and returns a value y.
        EXAMPLE:
        The function df/dx = x * t is defined as:
        def f(x, t):
            return x * t

    :param: lower
        ObjectType -> float
        Lower boundary for the solution of the differential equation.

    :param: upper
        ObjectType -> float
        Upper boundary for the solution of the differential equation.

    :param: dt
        ObjectType -> float
        Time step for the function, this defines the length of the returned
        array, lowering this value will impact the time it takes to return
        the values.
    :param: x0
        ObjectType -> float
        Starting point of the graph x0.

    :returns:
        ObjectType -> Union[np.ndarray, np.ndarray]
        returns tpoints and xpoints of the original function Fx.

    """

    N = int(np.abs((lower - upper)) / dt)

    tpoints: np.ndarray = np.linspace(lower, upper, N)
    xpoints: np.ndarray = np.zeros(N)

    xpoints[0] = x0
    for i in range(len(tpoints) - 1):
        xpoints[i + 1] = xpoints[i] + dt * fx(xpoints[i], tpoints[i])
    return tpoints, xpoints

@ode_decorator
def runga_kutta_4(fx: Callable, lower: float, upper: float, dt: float,
                x0: float = 0) -> tuple:
    """
        Evaluate differential equations (df/dx = f(x, t)) using a 4th order
         Runga-Kutta approximation

        USAGE:
            # define the derivative of a function fx that takes an "x" and a "t"
            # input

            def fx(x, t):
                return np.sin(x) * -t**3

            # define lower and upper boundaries, a timestep dt and *optional*
            # a starting position x0
            lower = 5
            upper = 10
            dt = 0.0001
            x0 = 3

            # call the function and assign the returns to tpoints and xpoints
            tpoints, xpoint = euler(fx=fx, lower=lower, upper=upper, dt=dt, x0=x0)

        :param: fx
            ObjectType -> Function
            Function, dx/dt = f(x, t), that takes x, t and returns a value y.
            EXAMPLE:
            The function df/dx = x * t is defined as:
            def f(x, t):
                return x * t
        :param: lower
            ObjectType -> float
            Lower boundary for the solution of the differential equation.

        :param: upper
            ObjectType -> float
            Upper boundary for the solution of the differential equation.

        :param: dt
            ObjectType -> float
            Time step for the function, this defines the length of the returned
            array, lowering this value will impact the time it takes to return
            the values.
        :param: x0
            ObjectType -> float
            Starting point of the graph x0.

        :returns:
            ObjectType -> Union[np.ndarray, np.ndarray]
            returns tpoints and xpoints of the original function Fx.

        """

    N = int(np.abs((lower - upper)) / dt)

    tpoints: np.ndarray = np.linspace(lower, upper, N)
    xpoints: np.ndarray = np.zeros(N)

    xpoints[0] = x0
    for i in range(len(tpoints) - 1):
        kutta_constants = np.zeros(4)
        kutta_constants[0] = dt * fx(xpoints[i], tpoints[i])
        kutta_constants[1] = dt * fx(xpoints[i] + 1/2 * kutta_constants[0],
                                     tpoints[i] + 1/2 * dt)
        kutta_constants[2] = dt * fx(xpoints[i] + 1/2 * kutta_constants[1],
                                     tpoints[i] + 1/2 * dt)
        kutta_constants[3] = dt * fx(xpoints[i] + kutta_constants[2],
                                         tpoints[i] + dt)

        xpoints[i + 1] = xpoints[i] + 1/6 * (sum(2 * kutta_constants[1:-1]) +
                                             kutta_constants[0] + kutta_constants[-1])
    return tpoints, xpoints

@ode_decorator
def runga_kutta_2(fx: Callable, lower: float, upper: float, dt: float,
                  x0: float = 0) -> tuple:
    """
        Evaluate differential equations (df/dx = f(x, t))
         using a 2nd order Runga-Kutta approximation

        USAGE:
            # define the derivative of a function fx that takes an "x" and a "t"
            # input

            def fx(x, t):
                return np.sin(x) * -t**3

            # define lower and upper boundaries, a timestep dt and *optional*
            # a starting position x0
            lower = 5
            upper = 10
            dt = 0.0001
            x0 = 3

            # call the function and assign the returns to tpoints and xpoints
            tpoints, xpoint = euler(fx=fx, lower=lower, upper=upper, dt=dt, x0=x0)

        :param: fx
            ObjectType -> Function
            Function, dx/dt = f(x, t), that takes x, t and returns a value y.
            EXAMPLE:
            The function df/dx = x * t is defined as:
            def f(x, t):
                return x * t

        :param: lower
            ObjectType -> float
            Lower boundary for the solution of the differential equation.

        :param: upper
            ObjectType -> float
            Upper boundary for the solution of the differential equation.

        :param: dt
            ObjectType -> float
            Time step for the function, this defines the length of the returned
            array, lowering this value will impact the time it takes to return
            the values.
        :param: x0
            ObjectType -> float
            Starting point of the graph x0.

        :returns:
            ObjectType -> Union[np.ndarray, np.ndarray]
            returns tpoints and xpoints of the original function Fx.

        """

    N = int(np.abs((lower - upper)) / dt)

    tpoints: np.ndarray = np.linspace(lower, upper, N)
    xpoints: np.ndarray = np.zeros(N)

    xpoints[0] = x0
    for i in range(len(tpoints) - 1):
        kutta_constants = np.zeros(2)
        kutta_constants[0] = dt * fx(xpoints[i], tpoints[i])
        kutta_constants[1] = dt * fx(xpoints[i] + 1/2 * kutta_constants[0],
                                     tpoints[i] + 1/2 * dt)
        xpoints[i + 1] = xpoints[i] + kutta_constants[1]

    return tpoints, xpoints

@ode_decorator
def num_der(fx, lower, upper, dt, x0, mode="central"):

    return None


if __name__ == "__main__":
    from Aplot import Default

    def f(x, t):
        return x * t
    print(runga_kutta_2(f, 0, [3, 4], dt=1))