"""Functions to convert spiking data to different representations."""

import numpy as np

from spiketools.utils.data import smooth_data
from spiketools.utils.checks import check_time_bins

###################################################################################################
###################################################################################################

def convert_times_to_train(spikes, fs=1000, length=None):
    """Convert spike times into a binary spike train.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    fs : int, optional, default: 1000
        The sampling rate to use for the computed spike train, in Hz.
    length : float, optional
        The total length of the spike train to create, in seconds.
        If not provided, the length is set at the maximum timestamp in the input spike times.

    Returns
    -------
    spike_train : 1d array
        Spike train.

    Examples
    --------
    Convert 6 spike times into a corresponding binary spike train

    >>> spikes = [0.002, 0.250, 0.500, 0.750, 1.000, 1.250, 1.500]
    >>> convert_times_to_train(spikes)
    array([0, 0, 1, ..., 0, 0, 1])
    """

    if not length:
        length = np.max(spikes)

    spike_train = np.zeros(int(length * fs) + 1).astype(int)
    inds = [int(ind * fs) for ind in spikes if ind * fs <= spike_train.shape[-1]]
    spike_train[inds] = 1

    return spike_train


def convert_train_to_times(train, fs=1000):
    """Convert a spike train representation into spike times, in seconds.

    Parameters
    ----------
    train : 1d array
        Spike train.
    fs : int, optional, default: 1000
        The sampling rate of the computed spike train, in Hz.

    Returns
    -------
    spikes : 1d array
        Spike times, in seconds.

    Examples
    --------
    Convert a spike train into spike times.

    >>> spike_train = [0,0,0,1,0,1,0,0,1,0,1,1,0,1]
    >>> convert_train_to_times(spike_train)
    array([0.004, 0.006, 0.009, 0.011, 0.012, 0.014])
    """

    spikes = np.where(train)[0] + 1
    spikes = spikes * (1 / fs)

    return spikes


def convert_isis_to_times(isis, offset=0, add_offset=True):
    """Convert a sequence of inter-spike intervals to spike times.

    Parameters
    ----------
    isis : 1d array
        Distribution of interspike intervals, in seconds.
    offset : float, optional
        An offset value to add to generated spike times.
    add_offset : bool, optional, default: True
        Whether to prepend the offset value to the beginning of the spike times.

    Returns
    -------
    spikes : 1d array
        Spike times, in seconds.

    Examples
    --------
    Convert a sequence of 6 inter-spike intervals to their corresponding spike times, in seconds.

    >>> isis = [0.3, 0.6, 0.8, 0.2, 0.7]
    >>> convert_isis_to_times(isis, offset=0, add_offset=True)
    array([0. , 0.3, 0.9, 1.7, 1.9, 2.6])
    """

    spikes = np.cumsum(isis, axis=-1)

    if offset:
        spikes = spikes + offset
    if add_offset:
        spikes = np.concatenate((np.array([offset]), spikes))

    return spikes


def convert_times_to_rates(spikes, bins, trange=None, smooth=None):
    """Convert spike times to continuous firing rate.

    Parameters
    ----------
    spikes : 1d array
        Spike times, in seconds.
    bins : float or 1d array
        The binning to apply to the spiking data.
        If float, the length of each bin.
        If array, precomputed bin definitions.
    trange : list of [float, float]
        Time range, in seconds, to create the binned firing rate across.
        Only used if `bins` is a float.
    smooth : float, optional
        If provided, the kernel to use to smooth the continuous firing rate.

    Returns
    -------
    cfr : 1d array
        Continuous firing rate, compute across time bins.

    Examples
    --------
    Convert 10 spike times (in seconds) to continuous firing rate across bins.

    >>> spikes = np.array([0.002, 0.250, 0.450, 0.500, 0.750, 1.000, 1.250, 1.300, 1.400, 1.500])
    >>> bins = 0.2
    >>> convert_times_to_rates(spikes, bins) 
    array([ 5.,  5., 10.,  5.,  0.,  5., 15.,  5.])
    """

    bins = check_time_bins(bins, spikes, trange)
    bin_counts, _ = np.histogram(spikes, bins)
    cfr = bin_counts / np.diff(bins)

    if smooth:
        cfr = smooth_data(cfr, smooth)

    return cfr
