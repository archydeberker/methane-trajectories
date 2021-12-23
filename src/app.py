import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

from methane import constants
from methane.constants import METHANE_HALFLIFE_YEARS, CO2_HALFLIFE_YEARS
from methane.simulation import Simulation
import plotly.io as pio

pio.templates.default = "plotly_white"


def plot(emissions_trajectory, conc_trajectory, title=None):
        df = pd.DataFrame(
                np.array([emissions_trajectory, conc_trajectory]).T,
                columns=["Emissions", "Concentration"],
                index=range(constants.START_YEAR, constants.HORIZON),
        )
        fig = px.line(df, y=["Concentration", "Emissions"], title=title)
        fig.update_layout(
                yaxis=dict(range=[0, 150], showgrid=False),
                xaxis=dict(showgrid=False),
        )

        st.write(fig)

st.header("Temporal Dynamics of CO2")
st.write("CO2 has a long half-life. This means that emitted CO2 hangs around for a long" "time.")
st.write("Move the slider below to change when we hit Net Zero, and see how" "it affects peak CO2 concentrations.")

co2_peak_year = st.slider(label="Peak Emissions", min_value=2025, max_value=2050)

co2_emissions_trajectory = Simulation.get_emissions(level=5, peak_year=co2_peak_year, years_to_zero=3)
co2_conc_trajectory = Simulation.simulate_concentrations(co2_emissions_trajectory, half_life=CO2_HALFLIFE_YEARS)

plot(co2_emissions_trajectory, co2_conc_trajectory, title='CO2')
methane_peak_year = st.slider(label="Peak Methane Emissions", min_value=2025, max_value=2050)

methane_emissions_trajectory = Simulation.get_emissions(level=5, peak_year=methane_peak_year, years_to_zero=3)
methane_conc_trajectory = Simulation.simulate_concentrations(methane_emissions_trajectory, half_life=METHANE_HALFLIFE_YEARS)
plot(methane_emissions_trajectory
     , methane_conc_trajectory, title='CO2')