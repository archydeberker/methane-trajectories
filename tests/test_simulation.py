from src.simulation import Simulation


def test_emissions_simulation():
    emissions_trajectory = Simulation.get_emissions(level=5, peak_year=2035, years_to_zero=3)

    assert emissions_trajectory[0] == 5
    assert emissions_trajectory[-1] == 0
    assert emissions_trajectory[16] <5
