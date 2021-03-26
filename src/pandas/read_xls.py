import pytest

import numpy as np
import pandas as pd


class TestPandas:

    def test_pd(self):
        pd.Series([1, 3, 5, np.nan, 6, 8])
