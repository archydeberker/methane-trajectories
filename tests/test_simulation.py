import plotly.express as px

import matplotlib.pyplot as plt
from methane.simulation import Simulation
from methane import constants


def test_emissions_simulation():
    emissions_trajectory = Simulation.get_emissions(level=5, peak_year=2035, years_to_zero=3)

    assert emissions_trajectory[0] == 5
    assert emissions_trajectory[-1] == 0
    assert emissions_trajectory[16] < 5


def test_exp_curve():
    curve = Simulation._exponential_curve(half_life=10)
    c_i = 1.1
    for c in curve:
        assert c < c_i
        c_i = c


def test_concentrations_simulation():
    emissions_trajectory = Simulation.get_emissions(level=5, peak_year=2035, years_to_zero=3)
    conc_trajectory = Simulation.simulate_concentrations(emissions_trajectory, half_life=5.0)

    plt.scatter(range(constants.START_YEAR, constants.HORIZON), conc_trajectory)
    plt.scatter(range(constants.START_YEAR, constants.HORIZON), emissions_trajectory, color='r')

    plt.show()
