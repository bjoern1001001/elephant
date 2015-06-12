# -*- coding: utf-8 -*-
"""
docstring goes here.

:copyright: Copyright 2014-2015 by the Elephant team, see AUTHORS.txt.
:license: Modified BSD, see LICENSE.txt for details.
"""

from __future__ import division, print_function

from itertools import chain

from neo.core.container import unique_objs

import numpy as np
import neo.core
import quantities as pq
from warnings import warn



def extract_neo_attrs(obj, parents=True, child_first=True,
                      skip_array=False, skip_none=False):
    """Given a neo object, return a dictionary of attributes and annotations.

    Parameters
    ----------

    obj : neo object
    parents : bool, optional
              Also include attributes and annotations from parent neo
              objects (if any).
    child_first : bool, optional
                  If True (default True), values of child attributes are used
                  over parent attributes in the event of a name conflict.
                  If False, parent attributes are used.
                  This parameter does nothing if `parents` is False.
    skip_array : bool, optional
                 If True (default False), skip attributes that store non-scalar
                 array values.
    skip_none : bool, optional
                If True (default False), skip annotations and attributes that
                have a value of `None`.

    Returns
    -------

    dict
        A dictionary where the keys are annotations or attribute names and
        the values are the corresponding annotation or attribute value.

    """
    attrs = obj.annotations.copy()
    for attr in obj._necessary_attrs + obj._recommended_attrs:
        if skip_array and len(attr) >= 3 and attr[2]:
            continue
        attr = attr[0]
        if attr == getattr(obj, '_quantity_attr', None):
            continue
        attrs[attr] = getattr(obj, attr, None)

    if skip_none:
        for attr, value in attrs.copy().items():
            if value is None:
                del attrs[attr]

    if not parents:
        return attrs

    for parent in getattr(obj, 'parents', []):
        if parent is None:
            continue
        newattr = extract_neo_attrs(parent, parents=True,
                                    child_first=child_first,
                                    skip_array=skip_array,
                                    skip_none=skip_none)
        if child_first:
            newattr.update(attrs)
            attrs = newattr
        else:
            attrs.update(newattr)

    return attrs


def _get_all_objs(container, classname):
    """Get all `neo` objects of a given type from a container.

    The objects can be any list, dict, or other iterable or mapping containing
    neo objects of a particular class, as well as any neo object that can hold
    the object.
    Objects are searched recursively, so the objects can be nested (such as a
    list of blocks).

    Parameters
    ----------

    container : list, tuple, iterable, dict, neo container
                The container for the neo objects.
    classname : str
                The name of the class, with proper capitalization
                (so `SpikeTrain`, not `Spiketrain` or `spiketrain`)

    Returns
    -------

    list
        A list of unique `neo` objects

    """
    if container.__class__.__name__ == classname:
        return [container]
    classholder = classname.lower() + 's'
    if hasattr(container, classholder):
        vals = getattr(container, classholder)
    elif hasattr(container, 'list_children_by_class'):
        vals = container.list_children_by_class(classname)
    elif hasattr(container, 'values') and not hasattr(container, 'ndim'):
        vals = container.values()
    elif hasattr(container, '__iter__'):
        vals = container
    else:
        raise ValueError('Cannot handle object of type %s' % type(container))
    res = list(chain.from_iterable(_get_all_objs(obj, classname)
                                   for obj in vals))
    return unique_objs(res)


def get_all_spiketrains(container):
    """Get all `neo.Spiketrain` objects from a container.

    The objects can be any list, dict, or other iterable or mapping containing
    spiketrains, as well as any neo object that can hold spiketrains:
    `neo.Block`, `neo.RecordingChannelGroup`, `neo.Unit`, and `neo.Segment`.

    Containers are searched recursively, so the objects can be nested
    (such as a list of blocks).

    Parameters
    ----------

    container : list, tuple, iterable, dict,
                neo Block, neo Segment, neo Unit, neo RecordingChannelGroup
                The container for the spiketrains.

    Returns
    -------

    list
        A list of the unique `neo.SpikeTrain` objects in `container`.

    """
    return _get_all_objs(container, 'SpikeTrain')


def get_all_events(container):
    """Get all `neo.Event` objects from a container.

    The objects can be any list, dict, or other iterable or mapping containing
    events, as well as any neo object that can hold events:
    `neo.Block` and `neo.Segment`.

    Containers are searched recursively, so the objects can be nested
    (such as a list of blocks).

    Parameters
    ----------

    container : list, tuple, iterable, dict, neo Block, neo Segment
                The container for the events.

    Returns
    -------

    list
        A list of the unique `neo.Event` objects in `container`.

    """
    return _get_all_objs(container, 'Event')


def get_all_epochs(container):
    """Get all `neo.Epoch` objects from a container.

    The objects can be any list, dict, or other iterable or mapping containing
    epochs, as well as any neo object that can hold epochs:
    `neo.Block` and `neo.Segment`.

    Containers are searched recursively, so the objects can be nested
    (such as a list of blocks).

    Parameters
    ----------

    container : list, tuple, iterable, dict, neo Block, neo Segment
                The container for the epochs.

    Returns
    -------

    list
        A list of the unique `neo.Epoch` objects in `container`.

    """
    return _get_all_objs(container, 'Epoch')

def get_all_epocharrays(container):
    """
    Get all `neo.EpochArray` objects from a container.

    The objects can be any list, dict, or other iterable or mapping containing
    epochArrays, as well as any neo object that can hold epochArrays:
    `neo.Block` and `neo.Segment`.

    Containers are searched recursively, so the objects can be nested
    (such as a list of blocks).

    Parameters
    ----------

    container : list, tuple, iterable, dict, neo Block, neo Segment
                The container for the epochs.

    Returns
    -------

    list
        A list of the unique `neo.EpochArray` objects in `container`.

    """
    return _get_all_objs(container, 'EpochArray')


def filter_epocharray(container, properties=None):
    """
    Selects `neo.EpochArray` objects according to the given properties from
    `container` object.
    If properties is `None` returns all `neo.EpochArrays` found inside the
    `container` object.

    Parameters
    ----------
    container : an arbitrary neo object
        A neo object which will be filtered according the given properties.

    properties : dict
        A dictionary that contains selection criteria. Each
        key of the dictionary is matched to *any* annotation or attribute
        of the given `container`.

    Returns
    -------
    list : list of neo.core.EpochArrays
        A list of filtered `neo.core.EpochArrays` will be returned.
        If no `EpochArray` object is found an empty array will be returned.
    """
    if properties is None:
        get_all_epochs(container)
    else:
        return container.filter(targdict=properties, objects=neo.EpochArray)


def filter_epochs(epochs, properties):
    """
    This function selects `neo.Epoch` objects from a list of
    `neo.core.EpochArrays`.

    The function returns a list of arrays with boolean values (mask).

    Parameters
    ----------
    epochs : list
        List object to extract data from.
    properties : dictionary
        A dictionary that contains selection criteria for the Epoch objects.
        Each key of the dictionary is matched to an annotation of the
        EpochArray that contains a list of values for a certain property
        of that object (e.g., the ID). The value associated with
        the key contains the set of allowed values, i.e., which objects
        are to be considered.
        Note: If an epoch does not have a specific annotation, it is rejected.

    Returns:
    --------
    mask : list of arrays with boolean values
        Each of the masks corresponds to a `neo.core.EpochArray` object and
        defines which objects are to be considered. The mask is obtained
        according the given properties.
    """

    # TODO: Cannot deal with AnalogSignalArray and similar (although
    # soon redundant).
    if properties is None:
        raise ValueError("Properties are empty.")
    if type(epochs) is not list:
        epochs = [epochs]
    # List to store the boolean masks
    lst = []
    for ep in epochs:
        # by default take all objects
        take_ep = np.array(
            [True for _ in range(len(ep.durations))])
        # now remove epochs based on user input
        # operation does a binary addition for each of the epochs over all
        # epoch annotations and properties
        # Starts with e.g. [1,1,1,1,1] and adds e.g. [1,1,0,1,1] = [1,1,0,1,1]
        # next step would then add to [1,1,0,1,1] a new boolean array etc.
        for k in properties.keys():
            take_ep = \
                take_ep & \
                np.array([
                             _ in properties[k] for _ in ep.annotations[k]])
        lst.append(take_ep)
    return lst


def cut_by_epocharray(selected_epochs, selected_trials, obj,
                      signal_props=None, reset_times=True, cut_in_range=False):
    """
        This function cuts trial data from a list of  `neo.core.EpochArray`
        objects, according to a list of boolean values (a mask).

        The function returns a neo Block where each trial is represented as a
        neo.Segment in the Block, to which the cut SpikeTrain and/or
        AnalogSignal object are attached.

        A dictionary contains restrictions on which trials, and which data
        is included in the final data set. To this end, it is possible to
        specify accepted (valid) values of specific annotations on the source
        objects. Only those objects that match these restrictions are included
        in the final result.

        The resulting trials may either retain their original time stamps, or
        shifted to a common time axis.

        Parameters
        ----------
        selected_epochs : list of neo.core.EpochArray objects
            The list of `neo.core.Epoch` objects to extract data from.
        selected_trials :
        signal_prop : dictionary
            A dictionary that contains selection criteria for trials. Each
            key of the dictionary is matched to an annotation of the
            EpochArray that contains a list of values for a certain property
            of that trial (e.g., the trial ID). The value associated with
            the key contains the set of allowed values, i.e., which trials
            are to be considered.
            Note: If an epoch does not have a specific annotation,
            it is rejected.
        reset_times : bool
            If True  the times stamps of all resulting object are set to fall
            in the range (0 *pq.s, epoch duration).
            If False, original time stamps are retained. Here the trials the
            Default is True
        cut_in_range : bool
            False: If the trial duration is longer than or exceeds the signal,
            the AnalogSignal will not be considered.
            True: If the trial duration is longer than a data object and tstart
                of the signal lies in the trial then the data object will be
                considered in the output.
            Default: False

        Returns:
        --------
        Block: neo.Block
            Per trial a neo.Segment with AnalogSignal or SpikeTrain Objects
            will be attached to a Block, if the properties of each object are
            matching to the user given properties.
        """
    # Check if string or not, and convert to
    if isinstance(obj, basestring):
        if obj.lower() == 'spiketrain':
            obj = neo.core.SpikeTrain
        elif obj.lower() == 'analogsignal':
            obj = neo.core.AnalogSignal
    block = neo.core.Block()
    for ep in selected_epochs:
        parent = ep.segment
        if parent is None:
            raise ValueError("%s is not attached to a neo.core.Segment." % str(
                type(ep)))
        if signal_props is None:
            filtered_items = [x for x in parent.children_recur
                              if type(x) == obj]
        else:
            filtered_items = parent.filter(targdict=signal_props,
                                           objects=obj)
        segs = {}
        for item in filtered_items:
            for i, t in enumerate(selected_trials):
                if i not in segs:
                    segs[i] = neo.core.Segment()
                if type(item) is neo.core.AnalogSignal:
                    if _is_in_range(
                            ep.times[i], ep.durations[i],
                            item.t_start, item.t_stop,
                            cut_in_range):
                        analog_sig = _cut_analogsignal(
                            ep, item, reset_times, i)
                        # check if there is an AnalogSignal
                        if np.size(analog_sig) > 0:
                            segs[i].analogsignals.append(analog_sig)
                if type(item) is neo.core.SpikeTrain:
                    if _is_in_range(ep.times[i],
                                    ep.durations[i],
                                    item.t_start, item.t_stop,
                                    cut_in_range):
                        # TODO: Use slice function of neo.SpikeTrain
                        st_sig = _cut_spiketrain(ep, item, reset_times, i)
                        # Check if there is a SpikeTrain
                        if np.size(st_sig) > 0:
                            segs[i].spiketrains.append(
                                st_sig)
        for s in sorted(segs):
            block.segments.append(segs[s])
    block.create_relationship(force=True, recursive=True)
    return block


def _cut_analogsignal(ep, fp, reset_times, i):
    """
    Helper function to cut an AnalogSignal Object

    Parameter:
    ---------
    ep : neo.EpochArray
    fp : neo.AnalogSignal
    reset_times : bool
    i : int
        Actual index of the loop

    Returns:
    -------
    neo.AnalogSignal:
        A cut AnalogSignal Object.
    None:
        Only if the trial doesn't match inside the range and thus a
        AnalogSignal Object couldn't be constructed.
    """
    # Range between edges
    ind1 = int(((ep.times[i] - fp.t_start) / (fp.t_stop - fp.t_start)).rescale(
        'dimensionless') * len(fp))
    ind2 = int((ind1 + ep.durations[i].rescale(
        fp.t_start.units) / fp.sampling_period).base)
    # Don't trespass edge
    if ind2 > fp.t_start.magnitude + len(fp):
        ind2 = fp.t_start.magnitude + len(fp)

    # setting zero time to beginning of analogsignal
    if type(reset_times) == bool and reset_times is True:
        (t_start, t_stop) = (0 * ep.durations[i].units, ep.durations[i])

    # keep time stamps of original spiketrain
    elif type(reset_times == bool) and reset_times is False:
        (t_start, t_stop) = (ep.times[i], ep.times[i] + ep.durations[i])
    else:
        raise TypeError(
            "Provided data type %s for reset times is not supported" % (
                type(reset_times)))
    analog_sig = neo.core.AnalogSignal(fp[ind1:ind2],
                                       t_stop=t_stop,
                                       sampling_rate=fp.sampling_rate,
                                       units=fp.units,
                                       t_start=t_start,
                                       trial_id=ep.annotations['trial_id'][i],
                                       **fp.annotations)
    return analog_sig


def _cut_spiketrain(ep, st, reset_times, i):
    """
    Helper function to cut a SpikeTrain Object

    Parameter:
    ---------
    ep : neo.EpochArray
    fp : neo.AnalogSignal
    reset_times : bool
    i : int
        Actual index of the loop

    Returns:
    -------
    neo.SpikeTrain:
        A cut SpikeTrain Object.
    None:
        Only if the trial doesn't match inside the range and thus a SpikeTrain
        Object couldn't be constructed.
    """
    # setting zero time to beginning of spiketrain
    if type(reset_times) == bool and reset_times is True:
        (t_start, t_stop) = (0 * st.units, ep.durations[i])
        spikingtimes = st.times[np.nonzero(
            np.logical_and(
                st.times >= ep.times[i],
                st.times < ep.times[i] + ep.durations[i]))] - \
                       ep.times[i]
    # keep time stamps of original spiketrain
    elif type(reset_times == bool) and reset_times is False:
        (t_start, t_stop) = (ep.times[i], ep.times[i] + ep.durations[i])
        spikingtimes = st.times[np.nonzero(
            np.logical_and(st.times >= ep.times[i],
                           st.times < ep.times[i] + ep.durations[i]))]

    else:
        raise TypeError(
            "Provided data type %s for reset times is not supported" % (
                type(reset_times)))

    if st.waveforms is not None:
        trial_waveforms = st.waveforms[np.nonzero(
            np.logical_and(st.times >= ep.times[i],
                           st.times < ep.times[i] + ep.durations[i]))]

    if len(spikingtimes) < 1:
        warn('Empty SpikeTrain at trial %d' % i)
    trial_spiketrain = neo.core.SpikeTrain(
        pq.Quantity(spikingtimes.magnitude, units=spikingtimes.units),
        t_stop=t_stop,
        units=st.units,
        t_start=t_start,
        trial_id=ep.annotations['trial_id'][i],
        **st.annotations)
    if st.waveforms is not None:
        trial_spiketrain.waveforms = trial_waveforms
    return trial_spiketrain


def _is_in_range(ep_times, ep_durations, fp_start, fp_stop, cut_half):
    """
    Helper Function, checks if cutting in (some) range is
    possible.

    Parameter:
    ----------
    ep_times : int
        Starting time of neo.Epoch object.
    ep_durations : int
        Duration of neo.Epoch object.
    fp_start : int
        Starting time of signal.
    fp_stop : int
        Stopping time of signal
    cut_half : bool
        False: If the trial duration is longer than or exceeds the signal, the
        AnalogSignal Object will not be considered and appended to the list.
        (default)
        True: Even if the trial duration is longer than the signal and the
        staring point of the signal lies somewhere in the given range than the
        AnalogSignal Object will be considered and appended to the list.

    Returns:
    --------
    bool:
        True, if the cutting in given range is possible
        False, otherwise.
    """
    if cut_half:
        if fp_start <= ep_times <= fp_stop or fp_start <= ep_times + \
                ep_durations <= fp_stop:
            return True
    else:
        if ep_times >= fp_start and ep_times + ep_durations <= fp_stop:
            return True
    return False

