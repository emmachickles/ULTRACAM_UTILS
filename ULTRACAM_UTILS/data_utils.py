import hipercam as hcam
import numpy as np
import __init__

def extract_lc(hlg, ccd='1', targ='1', comp='2', tstart=None, ra=None, dec=None):
    "Divide the target by comparison and convert times to BJD."
    targ = hlg.tseries(ccd,targ) 
    comp = hlg.tseries(ccd,comp)

    lc = targ / comp
    lc.t = BJDConvert(lc.t, ra, dec, telescope='La Silla Observatory').value
    if tstart is not None:
        inds = np.nonzero(lc.t > tstart)
        lc.t, lc.y, lc.ye = lc.t[inds], lc.y[inds], lc.ye[inds]
    median=np.nanmedian(lc.y)
    lc.y=lc.y/median
    lc.ye=lc.ye/median
    return lc.t, lc.y, lc.ye

def read_log(logfile, targ='1', comp=['2', '2', '2'], tstart=None, ra=None, dec=None):
    "Read log files written by hipercam reduce and convert times to BJD."
    
    hlg = hcam.hlog.Hlog.rascii(logfile)
    t_r, y_r, ye_r = extract_lc(hlg, ccd='1', targ=targ, comp=comp[0],
                                tstart=tstart, ra=ra, dec=dec)
    t_g, y_g, ye_g = extract_lc(hlg, ccd='2', targ=targ, comp=comp[1],
                                tstart=tstart, ra=ra, dec=dec)
    t_u, y_u, ye_u = extract_lc(hlg, ccd='3', targ=targ, comp=comp[2],
                                tstart=tstart, ra=ra, dec=dec)
    return t_r, y_r, ye_r, t_g, y_g, ye_g, t_u, y_u, ye_u

def define_passbands():
    # Super SDSS urgiz in ULTRACAM
    # central wavelength 3526 4732 6199 7711 9156
    # FWHM               827  1493 1374 1467 1694

    import json
    with open('paths.json', 'r') as f:
        paths = json.load(f)
    
    data = np.loadtxt(paths['filter_directory']+'/super_u_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_u = Filter(wave, transmit, name='super_u', dtype='photon', unit='nm')

    data = np.loadtxt(paths['filter_directory']+'/super_g_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_g = Filter(wave, transmit, name='super_g', dtype='photon', unit='nm')

    data = np.loadtxt(paths['filter_directory']+'/super_r_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_r = Filter(wave, transmit, name='super_r', dtype='photon', unit='nm')

    data = np.loadtxt(paths['filter_directory']+'/super_i_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_i = Filter(wave, transmit, name='super_i', dtype='photon', unit='nm')

    data = np.loadtxt(paths['filter_directory']+'/super_z_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_z = Filter(wave, transmit, name='super_z', dtype='photon', unit='nm')

    return super_u, super_g, super_r, super_i, super_z

