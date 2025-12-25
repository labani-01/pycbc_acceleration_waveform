def const_los_Acc_td(v0, acc, base_model, n, **kwds):
    dt = kwds['delta_t']
    from pycbc.waveform import get_td_waveform
    from pycbc.types import TimeSeries
    import numpy as np
    from scipy.interpolate import make_interp_spline
    if 'approximant' in kwds:
        kwds.pop('approximant')
    hp_base,hc_base = get_td_waveform(approximant = base_model, **kwds)
     
    time = hp_base.sample_times
    filtered_array = time[np.absolute(acc * time) < n]
    hp = hp_base[np.absolute(acc * time) < n]
    hc = hc_base[np.absolute(acc * time) < n]

    peak_idx = np.argmax(np.abs(hp))
 
    dt_array = np.diff(filtered_array)
    t_left = filtered_array[:-1]
    dt_new = (1 + v0 + acc * t_left) * dt_array
    t_new = np.concatenate([[filtered_array[0]], filtered_array[0] + np.cumsum(dt_new)])

    t_new_peak = t_new[peak_idx]
    t_new_shifted = t_new - t_new_peak
    
    n_samples = int(np.round((np.max(t_new_shifted) - np.min(t_new_shifted)) / dt)) + 1
    t_val = np.linspace(np.min(t_new_shifted), np.max(t_new_shifted), n_samples)

    k = 3
    hp_spline = make_interp_spline(t_new_shifted, hp, k=k)
    hc_spline = make_interp_spline(t_new_shifted, hc, k=k)
    hp_interp = hp_spline(t_val)
    hc_interp = hc_spline(t_val)
 
    hp_new = TimeSeries(hp_interp, delta_t=dt, epoch=t_val[0])
    hc_new = TimeSeries(hc_interp, delta_t=dt, epoch=t_val[0])
 
    hp_taper = hp_new.taper_timeseries('startend')
    hc_taper = hc_new.taper_timeseries('startend')

    return(hp_taper, hc_taper)
