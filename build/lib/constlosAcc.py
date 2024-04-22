def const_los_Acc_td(v0, acc, i, **kwds):
    dt = kwds['delta_t']
    from pycbc.waveform import get_td_waveform
    from pycbc.waveform import td_approximants, fd_approximants
    from pycbc.types import TimeSeries
    import numpy as np
    if 'approximant' in kwds:
        kwds.pop('approximant')
    hp,hc = get_td_waveform(approximant =td_approximants()[i], **kwds)
    t1 = hp.sample_times[np.argmax(hp)+1:-1] #after zero
    t2 = hp.sample_times[1:np.argmax(hp)+2]
    dt1 = np.full((len(t1),), dt, dtype=float)
    dt2 = np.full((len(t2),), dt, dtype=float)
    dt1_new = (1 + v0 + acc * t1)* dt1
    dt1_new = np.insert(dt1_new, 0, hp.sample_times[np.argmax(hp)+1])
    dt2_new = -(1 + v0 + acc * t2)* dt2
    dt2_new = np.insert(dt2_new, np.argmax(hp)+1, hp.sample_times[np.argmax(hp)+1])
    t1_new = np.cumsum(dt1_new)
    t2_new = np.cumsum(dt2_new[::-1])[::-1]
    t2_new = t2_new[:-1]
    t_new = np.concatenate([t2_new, t1_new])
    t_val = np.arange(np.min(t_new), np.max(t_new), dt)
    hp_interp = np.interp(t_val, t_new, hp)
    hc_interp = np.interp(t_val, t_new, hc)
    hp_new = TimeSeries(hp_interp, delta_t=dt, epoch=min(t_val))
    hc_new = TimeSeries(hc_interp, delta_t=dt, epoch=min(t_val))
    return(hp_new, hc_new)
    
