import hipercam as hcam
import numpy as np

def extract_lc(hlg, ccd='1', targ='1', comp='2', tstart=None, ra=None, dec=None):
    "Divide the target by comparison and convert times to BJD."

    from LIGHTCURVE_UTILS.time_utils import BJDConvert
    
    targ = hlg.tseries(ccd,targ) 
    comp = hlg.tseries(ccd,comp)
    
    lc = targ / comp
    lc.t = BJDConvert(lc.t, ra, dec, telescope='La Silla Observatory', scale='tdb').value
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

    import os
    from pyphot import (unit, Filter)    

    # filter_dir = os.path.dirname(__file__)+'/Filter_Response/'
    filter_dir = "/home/echickle/work/ULTRACAM_UTILS/ULTRACAM_UTILS/Filter_Response/"
    
    data = np.loadtxt(filter_dir+'super_u_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_u = Filter(wave, transmit, name='super_u', dtype='photon', unit='nm')

    data = np.loadtxt(filter_dir+'super_g_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_g = Filter(wave, transmit, name='super_g', dtype='photon', unit='nm')

    data = np.loadtxt(filter_dir+'super_r_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_r = Filter(wave, transmit, name='super_r', dtype='photon', unit='nm')

    data = np.loadtxt(filter_dir+'super_i_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_i = Filter(wave, transmit, name='super_i', dtype='photon', unit='nm')

    data = np.loadtxt(filter_dir+'super_z_asbuilt.txt')
    wave = data[:,0] * unit['nm']
    transmit = data[:,1]
    super_z = Filter(wave, transmit, name='super_z', dtype='photon', unit='nm')

    return super_u, super_g, super_r, super_i, super_z

def clip_lc(lc, pos_iqr=10, neg_iqr=10, ensig=5):
    from LIGHTCURVE_UTILS.clip_utils import clip_iqr, clip_err
    
    new_lc = []

    t, y, dy = lc[0], lc[1], lc[2]
    t, y, dy = clip_iqr(t, y, dy, pos_iqr=pos_iqr, neg_iqr=neg_iqr)
    t, y, dy = clip_err(t, y, dy, ensig=ensig)
    new_lc.append(t)
    new_lc.append(y)
    new_lc.append(dy)

    t, y, dy = lc[3], lc[4], lc[5]
    t, y, dy = clip_iqr(t, y, dy, pos_iqr=pos_iqr, neg_iqr=neg_iqr)
    t, y, dy = clip_err(t, y, dy, ensig=ensig)
    new_lc.append(t)
    new_lc.append(y)
    new_lc.append(dy)

    t, y, dy = lc[6], lc[7], lc[8]
    t, y, dy = clip_iqr(t, y, dy, pos_iqr=pos_iqr, neg_iqr=neg_iqr)
    t, y, dy = clip_err(t, y, dy, ensig=ensig)
    new_lc.append(t)
    new_lc.append(y)
    new_lc.append(dy)

    return new_lc
    
def make_dat(lc, logfile, out_dir='./', filt='g'):

    if filt == 'r' or filt == 'i':
        t, y, dy = lc[0], lc[1], lc[2]
        ccd = '1'
    elif filt == 'g':
        t, y, dy = lc[3], lc[4], lc[5]
        ccd = '2'
    elif filt == 'u':
        t, y, dy = lc[6], lc[7], lc[8]
        ccd = '3'
    
    hlg = hcam.hlog.Hlog.rascii(logfile)

    arr = np.ones(t.shape)
    
    exptime = np.median(hlg[ccd]['Exptim'] / 86400)
    exptime = arr * exptime

    data = [t, exptime, y, dy, arr, arr]
    data = np.array(data).T

    out = out_dir+filt+'.dat'
    np.savetxt(out, data)
    print('Saved '+out)
    
