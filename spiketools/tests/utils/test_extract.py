"""Tests for spiketools.utils.extract"""

import numpy as np

from pytest import raises

from spiketools.utils.extract import *
from spiketools.utils.extract import _reinstate_range_1d

###################################################################################################
###################################################################################################

def test_create_mask():

    data = np.array([0.5, 1., 1.5, 2., 2.5])
    min_value = 1
    max_value = 2
    mask = create_mask(data, min_value, max_value)
    assert isinstance(mask, np.ndarray)
    assert np.array_equal(mask, np.array([False, True, True, True, False]))

def test_get_range():

    data = np.array([0.5, 1., 1.5, 2., 2.5])

    out1 = get_range(data, min_value=1.)
    assert np.array_equal(out1, np.array([1., 1.5, 2., 2.5]))

    out2 = get_range(data, max_value=2.)
    assert np.array_equal(out2, np.array([0.5, 1., 1.5, 2.]))

    out3 = get_range(data, min_value=1., max_value=2.)
    assert np.array_equal(out3, np.array([1., 1.5, 2.]))

    out4 = get_range(data, min_value=1., max_value=2., reset=1.)
    assert np.array_equal(out4, np.array([0., 0.5, 1.0]))

def test_get_value_range():

    times = np.array([1., 2., 3., 4., 5.])
    data = np.array([0.5, 1., 1.5, 2., 2.5])

    out_times, out_data = get_value_range(times, data, min_value=1., max_value=2.)
    assert np.array_equal(out_times, np.array([2., 3., 4.]))
    assert np.array_equal(out_data, np.array([1., 1.5, 2.]))

def test_get_ind_by_time():

    times = np.array([1, 2, 3, 4, 5])

    # test 1d & 2d data cases
    ind = get_ind_by_time(times, 3.25)
    assert ind == 2
    ind = get_ind_by_time(times, 3.25)
    assert ind == 2

    # test with threshold
    ind = get_ind_by_time(times, 3.15, threshold=0.25)
    assert ind == 2
    ind = get_ind_by_time(times, 3.5, threshold=0.25)
    assert ind == -1

def test_get_inds_by_times():

    times = np.array([1, 2, 3, 4, 5])

    extract = [3.25, 3.75]
    inds = get_inds_by_times(times, extract)
    assert np.array_equal(inds, np.array([2, 3]))
    inds = get_inds_by_times(times, extract)
    assert np.array_equal(inds, np.array([2, 3]))

    extract = [3.5, 4.15, 4.85]
    inds = get_inds_by_times(times, extract, threshold=0.25, drop_null=True)
    np.array_equal(inds, np.array([np.nan, 3, 4]), equal_nan=True)
    inds = get_inds_by_times(times, extract, threshold=0.25, drop_null=False)
    np.array_equal(inds, np.array([3, 4]), equal_nan=True)

def test_get_value_by_time():

    times = np.array([1, 2, 3, 4, 5])
    values_1d = np.array([5, 8, 4, 6, 7])
    values_2d = np.array([[5, 8, 4, 6, 7], [5, 8, 4, 6, 7]])

    value_out = get_value_by_time(times, values_1d, 3)
    assert value_out == values_1d[2]

    value_out = get_value_by_time(times, values_1d, 3.4)
    assert value_out == values_1d[2]

    value_out = get_value_by_time(times, values_2d, 3)
    assert np.array_equal(value_out, values_2d[:, 2])

def test_get_values_by_times():

    times = np.array([1, 2, 3, 4, 5])
    values_1d = np.array([5, 8, 4, 6, 7])
    values_2d = np.array([[5, 8, 4, 6, 7], [5, 8, 4, 6, 7]])

    timepoints = np.array([1.75, 4.15])

    outputs = get_values_by_times(times, values_1d, timepoints)
    assert len(outputs) == len(timepoints)
    assert np.array_equal(outputs, np.array([8, 6]))

    outputs = get_values_by_times(times, values_2d, timepoints)
    assert len(outputs) == len(timepoints)
    assert np.array_equal(outputs, np.array([[8, 6], [8, 6]]))

def test_get_values_by_time_range():

    times = np.array([1, 2, 3, 4, 5])
    values = np.array([5, 8, 4, 6, 7])

    times_out, values_out = get_values_by_time_range(times, values, 2, 4)
    assert np.array_equal(times_out, np.array([2, 3, 4]))
    assert np.array_equal(values_out, np.array([8, 4, 6]))

def test_threshold_spikes_by_times():

    spikes = np.array([0.5, 1., 1.5, 2., 2.5])
    times = np.array([0.5, 1.1, 1.9, 3])
    threshold = 0.25

    out = threshold_spikes_by_times(spikes, times, threshold)
    assert isinstance(out, np.ndarray)
    assert np.array_equal(out, np.array([0.5, 1., 2.]))

def test_threshold_spikes_by_values():

    spikes = np.array([0.5, 1., 1.5, 2., 2.5])
    times = np.array([0.5, 1.1, 1.9, 2.4])
    values = np.array([0, 1, 1, 0])
    tthresh = 0.25
    dthresh = 0.5

    out1 = threshold_spikes_by_values(spikes, times, values, dthresh, tthresh, data_comparison='greater')
    assert np.array_equal(out1, np.array([1., 2.]))

    out2 = threshold_spikes_by_values(spikes, times, values, dthresh, tthresh, data_comparison='less')
    assert np.array_equal(out2, np.array([0.5, 2.5]))

def test_drop_range():

    spikes = np.array([0.5, 1.5, 1.9, 4.1, 5.4, 5.9])
    time_range = [2, 4]

    out = drop_range(spikes, time_range)
    assert isinstance(out, np.ndarray)
    assert spikes.shape == out.shape
    assert np.allclose(out, np.array([0.5, 1.5, 1.9, 2.1, 3.4, 3.9]))

    # check that error is raised with no empty range
    with raises(AssertionError):
        out = drop_range(spikes, [1.5, 4])

    # Test multiple time ranges
    spikes = np.array([0.5, 1.5, 1.9, 4.1, 5.4, 5.9, 8.2, 9.7])
    time_ranges = [[2, 4], [6, 8]]
    out = drop_range(spikes, time_ranges)
    assert isinstance(out, np.ndarray)
    assert spikes.shape == out.shape
    assert np.allclose(out, np.array([0.5, 1.5, 1.9, 2.1, 3.4, 3.9, 4.2, 5.7]))

def test_reinstate_range_1d():

    spikes = np.array([0.5, 1.5, 1.9, 2.1, 3.4, 3.9])
    time_range = [2, 4]

    out = _reinstate_range_1d(spikes, time_range)
    assert isinstance(out, np.ndarray)
    assert spikes.shape == out.shape
    assert get_range(out, *time_range).size == 0
    assert np.allclose(out, np.array([0.5, 1.5, 1.9, 4.1, 5.4, 5.9]))

def test_reinstate_range():

    spikes = np.array([[0.5, 1.5, 1.9, 2.1, 3.4, 3.9],
                       [0.2, 0.8, 1.2, 1.8, 2.5, 3.2]])
    time_range = [2, 4]

    out = reinstate_range(spikes, time_range)

    assert isinstance(out, np.ndarray)
    for row in out:
        assert len(row) == spikes.shape[1]
        assert get_range(row, *time_range).size == 0
    assert np.allclose(out, np.array([[0.5, 1.5, 1.9, 4.1, 5.4, 5.9],
                                      [0.2, 0.8, 1.2, 1.8, 4.5, 5.2]]))

    # Test multiple time ranges
    time_ranges = [[1, 2], [3, 4]]
    out = reinstate_range(spikes, time_ranges)

    assert isinstance(out, np.ndarray)
    for row in out:
        assert len(row) == spikes.shape[1]
        for time_range in time_ranges:
            assert get_range(row, *time_range).size == 0
    assert np.allclose(out, np.array([[0.5, 2.5, 2.9, 4.1, 5.4, 5.9],
                                      [0.2, 0.8, 2.2, 2.8, 4.5, 5.2]]))
