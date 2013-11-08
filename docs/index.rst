.. LIGO-CIS documentation master file, created by
   sphinx-quickstart on Thu Nov  7 14:39:30 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################
LIGO Channel Information System client
######################################

The Laser Interferometer Gravitational-wave Observatory (LIGO) operate two kilometre-scale gravitational-wave observatories in the United States, aiming to observe astrophysical events through their emission of energy as gravitational radiation.

The Channel Information System (CIS) automatically records and describes each of the ~100,000 instrumental data signals used in operation of the instrument and calibration of the data.

The `cis` package provides an python client to the RESTful interface for the CIS, primarily through the following two classes:

.. autosummary::
   :nosignatures:
   :toctree: _generated

   ~cis.channel.Channel
   ~cis.description.Description

Each of these items are used to translate the abstract channel name, e.g. ``H1:LSC-DARM_ERR`` into a human-readable description of the source of that signal within the instrument, and its purpose.

==================
What is a channel?
==================

.. py:currentmodule:: cis.channel

In LIGO parlance, a `Channel` is a single data source within the instrument -- a photodiode signal, a seismometer readout, for example -- whose time-series is recorded continuously and stored on disk.
These channels are used to control the instrument on the operating point through continual feedback and actuation, and to readout environmental sensing information, and the gravitational-wave strain amplitude detected by the instrument.

Each `Channel` is recorded with the following metadata attributes

.. autosummary::

   ~Channel.description
   ~Channel.sample_rate
   ~Channel.unit

=======================
How do I query the CIS?
=======================

The primary purpose of the `cis` package is to allow users to search for channels and retrieve their descriptions.
This can be done as follows::

    >>> from cis import Channel
    >>> mychannel = Channel.query('L1:PSL-ODC_CHANNEL_OUT_DQ')
    >>> mychannel
    <Channel("L1:PSL-ODC_CHANNEL_OUT_DQ",
             description="PSL ODC State Vector",
             sample_rate=32768.0)>
    >>> print(mychannel)
    L1:PSL-ODC_CHANNEL_OUT_DQ

Alternatively, you can query the CIS for a set of channels, either if you're not sure of the name of one, or if looking for a set of them:

    >>> from cis import ChannelList
    >>> mylist = ChannelList.query('H1:*ODC_CHANNEL_OUT_DQ')
    >>> mylist
    [<Channel("H1:HPI-BS_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-ETMX_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-ETMY_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM1_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM2_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM3_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM4_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM5_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-HAM6_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-ITMX_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:HPI-ITMY_ODC_CHANNEL_OUT_DQ", sample_rate=1024.0)>,
     <Channel("H1:ISI-BS_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-ETMX_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-ETMY_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-HAM2_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-HAM3_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-HAM4_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-HAM5_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-HAM6_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-ITMX_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-ITMY_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:ISI-TST_ODC_CHANNEL_OUT_DQ", sample_rate=4096.0)>,
     <Channel("H1:PSL-ODC_CHANNEL_OUT_DQ",
              description="PSL ODC State Vector",
              sample_rate=32768.0)>,
     <Channel("H1:SUS-BSTST_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-BS_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-ETMX_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-ETMY_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-ITMX_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-ITMY_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-MC1_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-MC2_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-MC3_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-OMC_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-PR2_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-PR3_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-PRM_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-QUADTST_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-SR2_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-SR3_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>,
     <Channel("H1:SUS-SRM_ODC_CHANNEL_OUT_DQ", sample_rate=256.0)>]

From the output of this query, you can see that not every channel is completely described in the CIS, due to the sheer number of channels recorded in the database.

====================
Channel descriptions
====================

The name of each `Channel` in the CIS is composed of a number of individual parts, in the following convention:

.. code::

    {IFO}:{SYSTEM}-{SUBSYSTEM}_SIGNAL

with each part digging deeper into the source of that signal within the instrument.
Each of the component parts delimited by any of ``:``, ``-``, or ``_``, can be, and probably are, described in the CIS, with a human-readable explanation of the acronym.
These are represented by a :class:`~cis.description.Description` object, each of which are downloaded along with each channel::

    >>> from cis import Channel
    >>> mychannel = Channel.query('L1:PSL-ISS_PDB_OUT_DQ')
    >>> print(mychannel.descriptions)
    PSL: Pre-Stabilized Laser
    ISS: Intensity Stabilization Servo
    PDB: Photo Diode B
    OUT: Output of Filter Bank
    DQ: Raw Channel Recorded by Data Acquisition System
