from dataclasses import dataclass
import numpy as np
from functools import lru_cache

from methane.constants import START_YEAR, HORIZON, CO2_RELATIVE_GWP, METHANE_RELATIVE_GWP, CO2_HALFLIFE_YEARS, \
    METHANE_HALFLIFE_YEARS, CO2_EMISSIONS_PA_MT, METHANE_EMISSIONS_PA_MT


@dataclass
class Simulation:
    """
    Holds gases and temperatures
    """

    peak_methane_year: int
    peak_co2_year: int

    gwp_methane: float = METHANE_RELATIVE_GWP
    gwp_co2: float = CO2_RELATIVE_GWP

    half_life_methane: float = METHANE_HALFLIFE_YEARS
    half_life_co2: float = CO2_HALFLIFE_YEARS

    current_emissions_methane: float = METHANE_EMISSIONS_PA_MT
    current_emissions_co2: float = CO2_EMISSIONS_PA_MT

    def __post_init__(self):
        self.methane_emissions = self.get_emissions(
            level=self.current_emissions_methane, peak_year=self.peak_methane_year
        )

    @staticmethod
    def get_emissions(
        level: float, peak_year: int, start_year: int = START_YEAR, end_year: int = HORIZON, years_to_zero: int = 0
    ):
        return np.array(
            [level] * (peak_year - start_year)
            + [level / (x + 1) for x in range(years_to_zero)]
            + [0] * (end_year - (peak_year + years_to_zero))
        )

    @classmethod
    def simulate_concentrations(cls, emissions: list, half_life: float):
        # Each year contributes an exponentially decaying curve
        contributions = np.zeros((len(emissions), len(emissions)))

        for year, emissions in enumerate(emissions):
            curve = emissions * cls._exponential_curve(half_life)
            truncated = curve[0 : (len(curve) - year)]
            contributions[year, year : len(curve)] = truncated

        # Sum across those curves to obtain total concentrations
        total_concentrations = contributions.sum(axis=0)

        return total_concentrations

    def total_radiative_forcing(self, methane_conc: float, co2_conc: float):

        ...

    def total_warming(self):
        ...

    @classmethod
    @lru_cache
    def _exponential_curve(cls, half_life: float):
        return np.array([1 * 2 ** (-t / half_life) for t in range(HORIZON - START_YEAR)])
