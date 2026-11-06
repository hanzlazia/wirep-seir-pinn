"""Real outbreak data.

Influenza A (H1N1) outbreak in an English boarding school, January 1978
(Anonymous, BMJ 1978;1:587; distributed as `influenza_england_1978_school`
in the R package `outbreaks`). 763 boys; number confined to bed on each day
from 22 Jan (day 1) to 4 Feb (day 14). One infective at day 0 is the standard
initial condition used for this dataset.
"""

BOARDING_SCHOOL_IN_BED = [3, 8, 26, 76, 225, 298, 258, 233, 189, 128, 68, 29, 14, 4]

REAL_DATASETS = {
    "BoardingSchool-1978": dict(
        name="BoardingSchool-1978", N=763.0, T=14.0, E0=0.0, I0=1.0,
        t=list(range(1, 15)), I=BOARDING_SCHOOL_IN_BED,
        train_days=10,                     # days 11-14 held out for forecasting
        init={"beta": 1.0, "sigma": 1.0, "gamma": 0.5},
        tau_ic=0.02,
    ),
}
