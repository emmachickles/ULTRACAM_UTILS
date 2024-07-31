import hipercam as hcam
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_aper(logfile, redfile, apefile, ccdfile, targ=1, output_dir='./',
              data_dir='./', ra=None, dec=None):

    os.chdir(data_dir)
    
    hlg = hcam.hlog.Hlog.rascii(logfile)
    hrd = hcam.reduction.Rfile.read(redfile)
    hap = hcam.MccdAper.read(apefile)
    mccd = hcam.MCCD.read(ccdfile)

    ccd_list = ['1', '2', '3']
    ccd_filt = ['r', 'g', 'b']
    
    targ = str(targ)
    aper_list = hlg.apnames['1']  # list of reference star apertures
    comp_list = aper_list.copy()
    comp_list.remove(targ)

    fig, ax = plt.subplots(ncols=3, figsize=(10,5))
    for i, ccd in enumerate(ccd_list):
        ax[i].set_aspect('equal', adjustable='box')
        ax[i].set_title('CCD '+ccd_list[i], c=ccd_filt[i])
        xaper = [hap[ccd][aper].x for aper in aper_list]
        yaper = [hap[ccd][aper].y for aper in aper_list]
        xrng = np.max(xaper) - np.min(xaper)
        yrng = np.max(yaper) - np.min(yaper)
        side = int( np.max( [xrng, yrng] ) * 1.50 )
        xpad = (side - xrng)/2
        ypad = (side - yrng)/2
        ax[i].set_xlim([np.min(xaper)-xpad, np.max(xaper)+xpad])
        ax[i].set_ylim([np.min(yaper)-ypad, np.max(yaper)+ypad])
        hcam.mpl.pCcd(ax[i], mccd[ccd])
        hcam.mpl.pCcdAper(ax[i], hap[ccd])
    plt.tight_layout()
    fname = output_dir+'ape_'+apefile[:-4]+'_field.png'
    plt.savefig(fname, dpi=300)
    print('Saved '+fname)

    
    fig, ax = plt.subplots(ncols=3, figsize=(10,5))
    for i, ccd in enumerate(ccd_list):
        ax[i].set_aspect('equal', adjustable='box')

        s = 'targ: {}xFWHM\nsky1: {}xFWHM\nsky2: {}xFWHM'
        params = hrd['extraction'][ccd].copy()
    
        params = [str(p) for p in params]
        ax[i].set_title(s.format(params[2],params[5],params[8]), c=ccd_filt[i])
        
        pad = 50
        xlo = hap[ccd][targ].x - pad
        xhi = hap[ccd][targ].x + pad
        ylo = hap[ccd][targ].y - pad
        yhi = hap[ccd][targ].y + pad

        ax[i].set_xlim([xlo, xhi])
        ax[i].set_ylim([ylo, yhi])

        starg = hrd['extraction'][ccd][2] # scale factor relative to FWHM
        ssky1 = hrd['extraction'][ccd][5]
        ssky2 = hrd['extraction'][ccd][8]
        fwhm = np.nanmean(hlg[ccd]['mfwhm'])
        
        hap[ccd][targ].rtarg = starg * fwhm
        hap[ccd][targ].rsky1 = ssky1 * fwhm
        hap[ccd][targ].rsky2 = ssky2 * fwhm

        hcam.mpl.pCcd(ax[i], mccd[ccd])
        hcam.mpl.pCcdAper(ax[i], hap[ccd])
    plt.tight_layout()
    fname = output_dir+'ape_'+logfile[:-4]+'_targ.png'
    plt.savefig(fname, dpi=300)
    print('Saved '+fname)

    for comp in comp_list:
        fig, ax = plt.subplots(ncols=2, nrows=3, figsize=(10,8), gridspec_kw={'width_ratios': [1,3]})
        for i, ccd in enumerate(ccd_list):
            ax[2-i][1].set_title(ccd+' = '+str(hrd['extraction'][ccd]))
            t,y,ye=extract_lc(hlg, ccd, targ, str(comp), ra=ra, dec=dec)
            ax[2-i][1].errorbar(t,y,ye,c=ccd_filt[i],ls=' ',elinewidth=1,capsize=1)

            ax[2-i][0].set_aspect('equal', adjustable='box')
            pad = 50
            xlo = hap[ccd][comp].x - pad
            xhi = hap[ccd][comp].x + pad
            ylo = hap[ccd][comp].y - pad
            yhi = hap[ccd][comp].y + pad

            ax[2-i][0].set_xlim([xlo, xhi])
            ax[2-i][0].set_ylim([ylo, yhi])

            starg = hrd['extraction'][ccd][2] # scale factor relative to FWHM
            ssky1 = hrd['extraction'][ccd][5]
            ssky2 = hrd['extraction'][ccd][8]
            fwhm = np.nanmean(hlg[ccd]['mfwhm'])

            hap[ccd][comp].rtarg = starg * fwhm
            hap[ccd][comp].rsky1 = ssky1 * fwhm
            hap[ccd][comp].rsky2 = ssky2 * fwhm

            hcam.mpl.pCcd(ax[2-i][0], mccd[ccd])
            hcam.mpl.pCcdAper(ax[2-i][0], hap[ccd])
            
        plt.tight_layout()
        fname = output_dir+'ape_'+logfile[:-4]+'_comp{}.png'.format(comp)
        plt.savefig(fname, dpi=300)
        print('Saved '+fname)
