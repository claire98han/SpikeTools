"""Tests for spiketools.plts.trials"""

import numpy as np

from spiketools.tests.tutils import plot_test
from spiketools.tests.tsettings import TEST_PLOTS_PATH

from spiketools.plts.trials import *

###################################################################################################
###################################################################################################

@plot_test
def test_plot_trial_rasters():

    data = [[-750, -300, 125, 250, 750],
            [-500, -400, -50, 100, 125, 500, 800],
            [-850, -500, -250, 100, 400, 750, 950]]

    plot_trial_rasters(data,
                       file_path=TEST_PLOTS_PATH, file_name='tplot_trial_rasters.png')


@plot_test
def test_plot_binned_spike_rates():

    x_vals = np.array([1, 2, 3, 4, 5])
    y_vals1 = np.array([[2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [4, 4, 4, 4, 4]])
    y_vals2 = np.array([[3, 3, 3, 3, 3], [4, 4, 4, 4, 4], [5, 5, 5, 5, 5]])

    plot_binned_spike_rates(x_vals, np.mean(y_vals1, 0),
                            file_path=TEST_PLOTS_PATH, file_name='tplot_binned_spike_rates1.png')

    plot_binned_spike_rates(x_vals, [y_vals1, y_vals2], average='median', shade='sem',
                            labels=['A', 'B'], stats=[0.5, 0.01, 0.5, 0.01, 0.5],
                            file_path=TEST_PLOTS_PATH, file_name='tplot_binned_spike_rates2.png')
