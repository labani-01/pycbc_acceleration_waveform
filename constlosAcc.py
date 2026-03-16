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

    non_rel = np.absolute(v0 + acc * time) < n
    filtered_array = time[non_rel]
    hp = hp_base[non_rel]
    hc = hc_base[non_rel]

    zero_idx = np.argmin(np.abs(filtered_array))
    t0 = filtered_array[zero_idx]
 
    dt_array = np.full(len(filtered_array) - 1, dt)
    t_left = filtered_array[:-1]
    dt_new = (1 + v0 + acc * t_left) * dt_array
    t_new = np.concatenate([[filtered_array[0]], filtered_array[0] + np.cumsum(dt_new)])

    t_shift = t_new[zero_idx] - t0
    t_new_shifted = t_new - t_shift

    t_min = t_new_shifted.min()
    t_max = t_new_shifted.max()
    t_val = np.arange(t_min, t_max + dt, dt)

    k = 3
    hp_spline = make_interp_spline(t_new_shifted, hp, k=k)
    hc_spline = make_interp_spline(t_new_shifted, hc, k=k)
    hp_interp = hp_spline(t_val)
    hc_interp = hc_spline(t_val)
 
    hp_new = TimeSeries(hp_interp, delta_t=dt, epoch=t_val[0])
    hc_new = TimeSeries(hc_interp, delta_t=dt, epoch=t_val[0])
 
    hp_taper = hp_new.taper_timeseries('start', tapermethod='constant', taper_window=0.3)
    hc_taper = hc_new.taper_timeseries('start', tapermethod='constant', taper_window=0.3)

    return(hp_taper, hc_taper)
