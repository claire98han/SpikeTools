"""Utility functions for working with timestamps."""

import numpy as np

###################################################################################################
###################################################################################################

def infer_time_unit(time_values):
    """Infer the time unit of given time values.

    Parameters
    ----------
    time_values : 1d array
        Time values.

    Returns
    -------
    time_unit : {'seconds', 'milliseconds'}
        The inferred time unit of the input data.

    Examples
    --------
    Infer the time unit of an array of time values:

    >>> time_values = np.array([0.002, 0.01, 0.05, 0.1, 2])
    >>> infer_time_unit(time_values)
    'seconds'
    """

    time_unit = None

    # Infer seconds if there are any two spikes within the same time unit,
    if len(np.unique((time_values).astype(int))) < len(np.unique(time_values)):
        time_unit = 'seconds'

    # Infer seconds if the mean time between spikes is low
    elif np.mean(np.diff(time_values)) < 10:
        time_unit = 'seconds'

    # Otherwise, infer milliseconds
    else:
        time_unit = 'milliseconds'

    return time_unit


def convert_ms_to_sec(ms):
    """Convert time value(s) from milliseconds to seconds.

    Parameters
    ----------
    ms : float
        Time value(s), in milliseconds.

    Returns
    -------
    float or array
        Time value(s), in seconds.

    Examples
    --------
    Convert milliseconds to seconds:

    >>> convert_ms_to_sec(500)
    0.5
    """

    return ms / 1000


def convert_sec_to_min(sec):
    """Convert time value(s) from seconds to minutes.

    Parameters
    ----------
    sec : float or array
        Time value(s), in seconds.

    Returns
    -------
    float or array
        Time value(s), in minutes.

    Examples
    --------
    Convert seconds to minutes:

    >>> convert_sec_to_min(210)
    3.5
    """

    return sec / 60


def convert_min_to_hour(mins):
    """Convert time value(s) from minutes to hours.

    Parameters
    ----------
    ms : float or array
        Time value(s), in minutes.

    Returns
    -------
    float or array
        Time value(s), in hours.

    Examples
    --------
    Convert minutes to hours:

    >>> convert_min_to_hour(270)
    4.5
    """

    return mins / 60


def convert_ms_to_min(ms):
    """Convert time value(s) from milliseconds to minutes.

    Parameters
    ----------
    ms : float or array
        Time value(s), in milliseconds.

    Returns
    -------
    float or array
        Time value(s), in minutes.

    Examples
    --------
    Convert milliseconds to minutes:

    >>> convert_ms_to_min(150000)
    2.5
    """

    return convert_sec_to_min(convert_ms_to_sec(ms))


def convert_nsamples_to_time(n_samples, fs):
    """Convert a number of samples into the corresponding time length.

    Parameters
    ----------
    n_samples : int
        Number of samples.
    fs : int
        Sampling rate.

    Returns
    -------
    time : float
        Time duration.

    Examples
    --------
    Convert a number of samples to a time length:

    >>> convert_nsamples_to_time(5, fs=1000)
    0.005
    """

    time = n_samples / fs

    return time


def convert_time_to_nsamples(time, fs):
    """Convert a time length into the corresponding number of samples.

    Parameters
    ----------
    time : float
        Time duration.
    fs : int
        Sampling rate.

    Returns
    -------
    n_samples : int
        Number of samples.

    Examples
    --------
    Convert a time length to a number of samples:

    >>> convert_time_to_nsamples(0.005, fs=1000)
    5
    """

    n_samples = int(np.ceil(time * fs))

    return n_samples


def split_time_value(sec):
    """Split a time value from seconds to hours / minutes / seconds.

    Parameters
    ----------
    sec : float
        Time value, in seconds.

    Returns
    -------
    hours, minutes, seconds : float
        Time value, split up into hours, minutes, and seconds.

    Examples
    --------
    Split seconds into hours, minutes, and seconds:

    >>> split_time_value(15000)
    (4, 10, 0)
    """

    minutes, seconds = divmod(sec, 60)
    hours, minutes = divmod(minutes, 60)

    return hours, minutes, seconds


def format_time_string(hours, minutes, seconds):
    """Format a time value into a string.

    Parameters
    ----------
    hours, minutes, seconds : float
        Time value, represented as hours, minutes, and seconds.

    Returns
    -------
    str
        A string representation of the time value.

    Examples
    --------
    Format a time stored as hours, minutes, and seconds into a string:

    >>> format_time_string(4, 10, 20)
    '4.00 hours, 10.00 minutes, and 20.00 seconds.'
    """

    base = '{:1.2f} hours, {:1.2f} minutes, and {:1.2f} seconds.'
    return base.format(hours, minutes, seconds)
