from dataclasses import dataclass
import numpy as np

START_YEAR = 2021
HORIZON = 2100

CO2_RELATIVE_GWP = 1
METHANE_RELATIVE_GWP = (
    45  # https://www.realclimate.org/index.php/archives/2021/09/the-definitive-co2-ch4-comparison-post/
)


CO2_HALFLIFE_YEARS = 120
METHANE_HALFLIFE_YEARS = 10.5  # https://meteor.geol.iastate.edu/gccourse/forcing/lifetimes.html

CO2_CONC = 410
METHANE_CONC = 1.87  # https://www.realclimate.org/index.php/archives/2021/09/the-definitive-co2-ch4-comparison-post/

CO2_EMISSIONS_PA_MT = 36.44e3  # https://ourworldindata.org/co2-emissions
METHANE_EMISSIONS_PA_MT = 570  # https://www.iea.org/reports/methane-tracker-2020


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

    def simulate_concentrations(self, end_year: int):
        """
        Simulate concentrations of methane and CO2 out until `year`

        We assume current emissions constant until the reduction year then instantaneous stop
        """

    def total_radiative_forcing(self, methane_conc: float, co2_conc: float):

        ...

    def total_warming(self):
        ...
