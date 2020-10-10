import numpy as np
import pandas as pd
from scipy.integrate import odeint


RHO_MIN = 0.5
RHO_MAX = 40.0
RHO_STEP = 2.0

BETA_MIN = 0.1
BETA_MAX = 10.0
BETA_STEP = 0.2

INITIAL = [1.0, 1.0, 1.0]

rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0


def simulate(
        initial=INITIAL,
        rho=rho,
        sigma=10.0,
        beta=beta,
        t_increment=0.01,
        t_max=40.0,
) -> pd.DataFrame:
    def f(state, t):
        x, y, z = state  # Unpack the state vector
        return sigma * (y - x), x * (rho - z) - y, x * y - beta * z
    state0 = initial
    t = np.arange(0.0, t_max, t_increment)
    states = odeint(f, state0, t)
    return pd.DataFrame(
        data=np.concatenate(
            (states, np.transpose(np.array([t]))),
            axis=1
        ),
        columns=["x", "y", "z", "t"],
        index=t)
    # return pd.DataFrame(
    #     data=states,
    #     columns=["x", "y", "z"],
    #     index=t)
