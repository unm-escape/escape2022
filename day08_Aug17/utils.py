import numpy as np
import math
#from scipy.signal.windows import triang
#from scipy.signal import convolve2d as conv2

##================================ 1) Plot SEG-Y ===========================
def plot_segy(segyFile, normalizeTraces=False, normalizeGlobal=False, scale=1, title=None, tstart=None, tend=None, saveFigure=False):
    """
    Returns a waveform plot of the input SEG-Y file

    Parameters
    ----------
    segyFile (SEG-Y file): to plotted e.g a shot gather
    normalizeTrace(bool): True or False
    normalizeGlobal(bool): True or False
    scale(int or float):
    title(str):
    tstart(float, int or noneType):
    tend(float, int or noneType):
    saveFigure(bool): True or False
    """
    import numpy as np
    import matplotlib
    #%matplotlib inline
    from matplotlib import pyplot as plt
    #import matplotlib.pyplot as plt
    from obspy import Stream, read

    #stream = read(str(segyFile), format='SEGY', check_compression=False, unpack_trace_headers=True)
    #st = stream.copy()

    if type(segyFile) is Stream:
        st = segyFile.copy()
    else:
        stream = read(str(segyFile), format='SEGY', check_compression=False, unpack_trace_headers=True)
        st = stream.copy()

    if normalizeTraces:
        st.normalize(global_max=False)
    else:
        pass

    if normalizeGlobal:
        st.normalize(global_max=True)
    else:
        pass

    fig, ax = plt.subplots(1,1,figsize=(16,9))
    for tr in st:
        loc = tr.stats.segy.trace_header.trace_sequence_number_within_line
        #loc = tr.stats.segy.trace_header.distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group
        x = (scale*tr.data)+loc
        y = tr.times()
        z = np.zeros(len(x))+loc # zero axis for each x
        ax.plot(x, y, color='k', lw=1.0, zorder=1)
        ax.fill_betweenx(y,x,z,where= x > z,facecolor='k',zorder=2, alpha=0.5)

    shot = st[0].stats.segy.trace_header.ensemble_number

    if title is None:
        pass
    if title is not None and type(title) != str:
        raise Exception('Title input must be a str or None')
    elif title is not None and type(title) == str:
        plt.title(str(title), fontsize=20, fontweight='bold')

    # Tight axis
    plt.tight_layout()
    ## Set plot limits
    #plt.xlim(0-1,len(st)+1)
    plt.xlim(st[0].stats.segy.trace_header.trace_sequence_number_within_line-1, st[len(st)-1].stats.segy.trace_header.trace_sequence_number_within_line+1)
    #plt.xlim(st[0].stats.segy.trace_header.distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group,
    #st[len(st)-1].stats.segy.trace_header.distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group)

    if tstart is not None:
        plt.ylim(tstart, tend)
    else:
        pass

    # Reverse time axis
    plt.gca().invert_yaxis()
    # Label axes
    ax.set_xlabel('Trace Number', fontsize=15, fontweight='bold')
    ax.set_ylabel('TWTT (s)', fontsize=15, fontweight='bold')

    if saveFigure:
        #fig.savefig('./shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight", transparent=True)
        fig.savefig('./shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight")

    plt.show()

##================================ 2) Pick SEG-Y ===========================
def pick_segy(segyFile, normalizeTraces=True, normalizeGlobal=False, scale=1, title=None, tstart=None, tend=None, saveFigure=False):
    """
    Returns a waveform plot of the input SEG-Y file

    Parameters
    ----------
    segyFile (SEG-Y file): to plotted e.g a shot gather
    normalizeTrace(bool): True or False, default is True
    normalizeGlobal(bool): True or False, default is False
    scale(int or float): Default is 1
    title(str or None): Default is None
    tstart(float, int or noneType):
    tend(float, int or noneType):
    saveFigure(bool): True or False
    """
    import numpy as np
    import matplotlib
    matplotlib.use('TkAgg')
    #%matplotlib inline
    from matplotlib import pyplot as plt
    #import matplotlib.pyplot as plt
    from obspy import Stream, read
    #import sys

    #stream = read(str(segyFile), format='SEGY', check_compression=False, unpack_trace_headers=True)
    #st = stream.copy()

    if type(segyFile) is Stream:
        st = segyFile.copy()
    else:
        stream = read(str(segyFile), format='SEGY', check_compression=False, unpack_trace_headers=True)
        st = stream.copy()

    if normalizeTraces:
        st.normalize(global_max=False)
    else:
        pass

    if normalizeGlobal:
        st.normalize(global_max=True)
    else:
        pass

    fig, ax = plt.subplots(1,1,figsize=(16,9))
    for tr in st:
        loc = tr.stats.segy.trace_header.trace_sequence_number_within_line
        x = (scale*tr.data)+loc
        y = tr.times()
        z = np.zeros(len(x))+loc # zero axis for each x
        ax.plot(x, y, color='k', lw=1.0, zorder=1)
        ax.fill_betweenx(y,x,z,where= x > z,facecolor='k',zorder=2, alpha=0.5)

    shot = st[0].stats.segy.trace_header.ensemble_number

    if title is None:
        pass
    if title is not None and type(title) != str:
        raise Exception('Title input must be a str or None')
    elif title is not None and type(title) == str:
        plt.title(str(title), fontsize=20, fontweight='bold')

    # Tight axis
    plt.tight_layout()
    ## Set plot limits
    #plt.xlim(0-1,len(st)+1)
    plt.xlim(st[0].stats.segy.trace_header.trace_sequence_number_within_line-1, st[len(st)-1].stats.segy.trace_header.trace_sequence_number_within_line+1)

    if tstart is not None:
        plt.ylim(tstart, tend)
    else:
        pass

    # Reverse time axis
    plt.gca().invert_yaxis()
    # Label axes
    ax.set_xlabel('Trace Number', fontsize=15, fontweight='bold')
    ax.set_ylabel('TWTT (s)', fontsize=15, fontweight='bold')

    ## Get picks
    num_points = len(st)
    picks = plt.ginput(num_points)
    #picks = plt.ginput(10)
    picks = np.array(picks)
    px = picks[:,0]
    py = picks[:,1]

    trc_nums = np.rint(px)
    time_picks = py 

    offsets = []
    for trc_num in trc_nums:
        idx = round(trc_num)
        for tr in st:
            if tr.stats.segy.trace_header.trace_sequence_number_within_line == idx:
                offsets.append(tr.stats.segy.trace_header.distance_from_center_of_the_source_point_to_the_center_of_the_receiver_group)

    ## Plot picks
    #ax.plot(np.rint(px), py, 'r', lw=2)
    #plt.scatter(np.rint(px), py, marker='x', color='r', s=60)
    ax.plot(trc_nums, time_picks, 'r', lw=2)
    plt.scatter(trc_nums, time_picks, marker='x', color='r', s=60)
    print("Success! Picks Ready.")

    #fig.canvas.start_event_loop(sys.float_info.min) #workaround for Exception in Tkinter callback

    if saveFigure:
        #fig.savefig('./shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight", transparent=True)
        fig.savefig('./shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight")
    #plt.show()
    plt.close()
    #return np.rint(px), py
    return trc_nums, time_picks, offsets

##=================================3) Plot picks ==================================
def plot_segy_picks(segyFile, normalizeTraces=True, normalizeGlobal=False, scale=1, title=None, tstart=None, tend=None, picksX=None, picksY=None, saveFigure=False):
    """
    Returns a waveform plot of the input SEG-Y file with p-arrival picks

    Parameters
    ----------
    segyFile (SEG-Y file or obspy stream): to plotted e.g a shot gather
    normalizeTrace(bool): True or False, default is True
    normalizeGlobal(bool): True or False, default is False
    scale(int or float): Default is 1
    title(str or None): Default is None
    tstart(float, int or noneType):
    tend(float, int or noneType):
    saveFigure(bool): True or False
    """
    import numpy as np
    import matplotlib
    #matplotlib.use('TkAgg')

    from matplotlib import pyplot as plt
    #import matplotlib.pyplot as plt
    from obspy import Stream, read

    if type(segyFile) is Stream:
        st = segyFile.copy()
    else:
        stream = read(str(segyFile), format='SEGY', check_compression=False, unpack_trace_headers=True)
        st = stream.copy()

    if normalizeTraces:
        st.normalize(global_max=False)
    else:
        pass

    if normalizeGlobal:
        st.normalize(global_max=True)
    else:
        pass

    fig, ax = plt.subplots(1,1,figsize=(16,9))
    for tr in st:
        loc = tr.stats.segy.trace_header.trace_sequence_number_within_line
        x = (scale*tr.data)+loc
        y = tr.times()
        z = np.zeros(len(x))+loc # zero axis for each x
        ax.plot(x, y, color='k', lw=1.0, zorder=1)
        ax.fill_betweenx(y,x,z,where= x > z,facecolor='k',zorder=2, alpha=0.5)

    shot = st[0].stats.segy.trace_header.ensemble_number

    if title is None:
        pass
    if title is not None and type(title) != str:
        raise Exception('Title input must be a str or None')
    elif title is not None and type(title) == str:
        plt.title(str(title), fontsize=20, fontweight='bold')

    # Tight axis
    plt.tight_layout()
    ## Set plot limits
    #plt.xlim(0-1,len(st)+1)
    plt.xlim(st[0].stats.segy.trace_header.trace_sequence_number_within_line-1, st[len(st)-1].stats.segy.trace_header.trace_sequence_number_within_line+1)

    if tstart is not None:
        plt.ylim(tstart, tend)
    else:
        pass

    # Reverse time axis
    plt.gca().invert_yaxis()
    # Label axes
    ax.set_xlabel('Trace Number', fontsize=15, fontweight='bold')
    ax.set_ylabel('TWTT (s)', fontsize=15, fontweight='bold')

    if picksX is not None and picksY is not None:
        ## Plot picks
        ax.plot(picksX, picksY, 'cyan', lw=1)
        plt.scatter(picksX, picksY, marker='x', color='r', s=50)
        #ax.plot(picksX, picksY, 'cyan', lw=1)

    ## Plot picks
    #ax.plot(np.rint(px), py, 'r', lw=1)
    #plt.scatter(np.rint(px), py, marker='x', color='r', s=50)

    if saveFigure:
        #fig.savefig('./shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight", transparent=True)
        fig.savefig('./picks_shot#'+ str(shot)+'.png', dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

## ================================ 4) t^2 Gain =============================
def gain(stream, normalizeTraces=False):
    """
    Returns t^2 gained obspy stream

    Parameters:
    stream (obspy stream): Input data
    normalizeTraces (bool): False normalizes with global maximum, True normalize each trace by it's max amplitude
    """
    import numpy as np
    from obspy import Stream, read

    st = stream.copy()
    t_squared = np.square(st[0].times())
    for tr in st:
        tr.data = tr.data*t_squared

    if normalizeTraces:
        st.normalize(global_max=False)
    else:
        st.normalize(global_max=True)

    return st
