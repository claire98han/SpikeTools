"""Tests for spiketools.utils.epoch"""

import numpy as np

from spiketools.utils.epoch import *

###################################################################################################
###################################################################################################

def test_epoch_spikes_by_event():

    spikes = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    events = np.array([5, 10, 15])
    window = [-1, 1]

    trials = epoch_spikes_by_event(spikes, events, window)
    assert isinstance(trials, list)
    assert isinstance(trials[0], np.ndarray)
    assert len(trials) == len(events)
    assert np.array_equal(trials[0], np.array([4.25, 5.5]) - events[0])
    assert np.array_equal(trials[1], np.array([9.25, 9.75, 10.5]) - events[1])
    assert np.array_equal(trials[2], np.array([14.1, 15.2, 15.9]) - events[2])

def test_epoch_spikes_by_range():

    spikes = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    start_times = np.array([5, 12])
    stop_times = np.array([10, 15])

    trials = epoch_spikes_by_range(spikes, start_times, stop_times)
    assert isinstance(trials, list)
    assert isinstance(trials[0], np.ndarray)
    assert len(trials) == len(start_times)
    assert np.array_equal(trials[0], np.array([5.5, 6.1, 8., 9.25, 9.75]))
    assert np.array_equal(trials[1], np.array([12., 14.1]))

    # Check with time reseting
    trials = epoch_spikes_by_range(spikes, start_times, stop_times, reset=True)
    assert np.array_equal(trials[0], np.array([5.5, 6.1, 8., 9.25, 9.75]) - start_times[0])
    assert np.array_equal(trials[1], np.array([12., 14.1]) - start_times[1])

def test_epoch_spikes_by_segment():

    spikes = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    segments = np.array([2, 5, 10, 15, 20])

    seg_spikes = epoch_spikes_by_segment(spikes, segments)
    assert isinstance(seg_spikes, list)
    assert len(seg_spikes) == len(segments) - 1
    assert np.array_equal(seg_spikes[0], np.array([2.5, 3.5, 4.25]))
    assert np.array_equal(seg_spikes[-1], np.array([15.2, 15.9]))

def test_epoch_data_by_time():

    times = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    timepoints = np.array([5, 10, 15])

    tvalues = epoch_data_by_time(times, values, timepoints)
    assert isinstance(tvalues, list)
    assert len(tvalues) == len(timepoints)
    assert np.array_equal(tvalues, np.array([3, 7, 11]))

def test_epoch_data_by_event():

    times = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    events = np.array([5, 10, 15])
    window = [-1, 1]

    ttimes, tvalues = epoch_data_by_event(times, values, events, window)
    assert isinstance(ttimes, list)
    assert isinstance(tvalues, list)
    assert isinstance(ttimes[0], np.ndarray)
    assert isinstance(tvalues[0], np.ndarray)
    assert len(ttimes) == len(tvalues) == len(events)

    assert np.array_equal(ttimes[0], np.array([4.25, 5.5]) - events[0])
    assert np.array_equal(tvalues[0], np.array([2, 3]))
    assert np.array_equal(ttimes[1], np.array([9.25, 9.75, 10.5]) - events[1])
    assert np.array_equal(tvalues[1], np.array([6, 7, 8]))
    assert np.array_equal(ttimes[2], np.array([14.1, 15.2, 15.9]) - events[2])
    assert np.array_equal(tvalues[2], np.array([10, 11, 12]))

def test_epoch_data_by_range():

    times = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    start_times = np.array([5, 12])
    stop_times = np.array([10, 15])

    ttimes, tvalues = epoch_data_by_range(times, values, start_times, stop_times)
    assert isinstance(ttimes, list)
    assert isinstance(tvalues, list)
    assert isinstance(ttimes[0], np.ndarray)
    assert isinstance(tvalues[0], np.ndarray)
    assert len(ttimes) == len(tvalues) == len(start_times)

    assert np.array_equal(ttimes[0], np.array([5.5, 6.1, 8., 9.25, 9.75]))
    assert np.array_equal(tvalues[0], np.array([3, 4, 5, 6, 7]))
    assert np.array_equal(ttimes[1], np.array([12.0, 14.1]))
    assert np.array_equal(tvalues[1], np.array([9, 10]))

    # Check with time reseting
    ttimes, tvalues = epoch_data_by_range(times, values, start_times, stop_times, reset=True)
    assert np.array_equal(ttimes[0], np.array([5.5, 6.1, 8., 9.25, 9.75]) - start_times[0])
    assert np.array_equal(tvalues[0], np.array([3, 4, 5, 6, 7]))
    assert np.array_equal(ttimes[1], np.array([12.0, 14.1]) - start_times[1])
    assert np.array_equal(tvalues[1], np.array([9, 10]))

def test_epoch_data_by_segment():

    times = np.array([2.5, 3.5, 4.25, 5.5, 6.1, 8., 9.25, 9.75, 10.5, 12., 14.1, 15.2, 15.9])
    values = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    segments = np.array([2, 5, 10, 15, 20])

    seg_times, seg_values = epoch_data_by_segment(times, values, segments)
    assert isinstance(seg_times, list)
    assert isinstance(seg_values, list)
    assert isinstance(seg_times[0], np.ndarray)
    assert isinstance(seg_values[0], np.ndarray)
    assert len(seg_times) == len(seg_values) == len(segments) - 1
    assert np.array_equal(seg_times[0], np.array([2.5, 3.5, 4.25]))
    assert np.array_equal(seg_values[0], np.array([0, 1, 2]))
