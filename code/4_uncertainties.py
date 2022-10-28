#
# Copyright 2022-2023 Universidad Complutense de Madrid
#
# This file software has been employed to compute 
# the standard deviation of different parameters derived
# from the simulated data of the MEGARA IFU instrument at GTC
#
# Authors: Cristina Cabello (criscabe@ucm.es), 
#          Nicolás Cardiel (cardiel@ucm.es)
#          Jesús Gallego (j.gallego@ucm.es)
#
# SPDX-License-Identifier: GPL-3.0+
# License-Filename: LICENSE.txt
#

import os
import argparse
import numpy as np
from astropy.io import ascii
from astropy.io import fits


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute the standard deviation of different parameters')
    parser.add_argument("--OIII5007", help = "STD of the OIII5007 line",
                        action="store_true")

    args = parser.parse_args()
    
    
    
    if args.OIII5007:
        print('.............................')
        print('--------Compute STD of the OIII5007 line--------')
        print('.............................')
        
        
        os.system('ls results_SIMUL/LINES/OIII5007/OIII5007_UM461_SIMUL_*.fits > list_OIII5007_SIMUL.txt')
        
        images_list = ascii.read('list_OIII5007_SIMUL.txt', data_start =0, names=['IMAGES'])
        
        
        
        IMAGES_SIMUL_OIII5007_noise = []
        IMAGES_SIMUL_OIII5007_snr = []
        IMAGES_SIMUL_OIII5007_flux = []
        IMAGES_SIMUL_OIII5007_flux_fit = []
        IMAGES_SIMUL_OIII5007_EW = []
        IMAGES_SIMUL_OIII5007_velocity = []
        IMAGES_SIMUL_OIII5007_sigma = []
        IMAGES_SIMUL_OIII5007_sigma_corrected = []
        
        
        for i in range(len(images_list)):
            with fits.open(images_list[i][0], mode='readonly') as hdulist:
                image = hdulist[0].data
                
                
            IMAGES_SIMUL_OIII5007_noise.append(image[:,2])  ## NOISE # 2 rms in cgs
            IMAGES_SIMUL_OIII5007_snr.append(image[:,3])  ## SNR # 3 S/N at the peak of the line
            IMAGES_SIMUL_OIII5007_flux.append(image[:,4])  ## FLUXD # 4 Flux from window_data - window_continuum
            IMAGES_SIMUL_OIII5007_flux_fit.append(image[:,6])  ## FLUXF # 6 Flux from best-fitting function(s)
            IMAGES_SIMUL_OIII5007_EW.append(image[:,7])  ## FLUXF # 7 EW from best-fitting function(s)
            IMAGES_SIMUL_OIII5007_velocity.append(image[:,16])  ## H1KS # 16 velocity in km/s from H1 (1st g)
            IMAGES_SIMUL_OIII5007_sigma.append(image[:,17])  ## H2KS # 17 sigma in km/s from H2 (1st g)
            IMAGES_SIMUL_OIII5007_sigma_corrected.append(image[:,18])  ## H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)


        std_simul_noise = np.nanstd(IMAGES_SIMUL_OIII5007_noise,axis=0)
        std_simul_snr = np.nanstd(IMAGES_SIMUL_OIII5007_snr,axis=0)    
        std_simul_flux = np.nanstd(IMAGES_SIMUL_OIII5007_flux,axis=0)
        std_simul_flux_fit = np.nanstd(IMAGES_SIMUL_OIII5007_flux_fit,axis=0)
        std_simul_EW = np.nanstd(IMAGES_SIMUL_OIII5007_EW,axis=0)
        std_simul_velocity = np.nanstd(IMAGES_SIMUL_OIII5007_velocity,axis=0)
        std_simul_sigma = np.nanstd(IMAGES_SIMUL_OIII5007_sigma,axis=0)
        std_simul_sigma_corrected = np.nanstd(IMAGES_SIMUL_OIII5007_sigma_corrected,axis=0)
        
        os.system('cp results_SIMUL/LINES/OIII5007/OIII5007_UM461_SIMUL_1.fits  results_SIMUL/LINES/OIII5007/OIII5007_UM461_STD_SIMULATIONS.fits')
    
        print('.............................')
        print('Saving FITS file.......')
        with fits.open('results_SIMUL/LINES/OIII5007/OIII5007_UM461_STD_SIMULATIONS.fits', mode='update') as hdulist:
            hdulist[0].data[:,2] = std_simul_noise
            hdulist[0].data[:,3] = std_simul_snr
            hdulist[0].data[:,4] = std_simul_flux
            hdulist[0].data[:,6] = std_simul_flux_fit
            hdulist[0].data[:,7] = std_simul_EW
            hdulist[0].data[:,16] = std_simul_velocity
            hdulist[0].data[:,17] = std_simul_sigma
            hdulist[0].data[:,18] = std_simul_sigma_corrected

            
        name = 'OIII5007'


        print('Saving PDF file.......')
        # NOISE # 2 rms in cgs
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 3  --min-cut 0 --max-cut 1E-18 --title STD_' + str(name) + '_NOISE --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_noise.pdf')
        # SNR # 3 S/N at the peak of the line
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 4  --min-cut 0.00000 --max-cut 50 --title STD_' + str(name) + '_SNR --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_SNR.pdf')
        # FLUXD # 4 Flux from window_data - window_continuum
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 5  --min-cut 0.00000 --max-cut 3E-17 --title STD_' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_flux.pdf')
        # FLUXF # 6 Flux from best-fitting function(s)
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 7  --min-cut 0.00000 --max-cut 3E-17 --title STD_' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_flux_fit.pdf')
        # FLUXF # 7 EW from best-fitting function(s)
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 8  --min-cut 0.00000 --max-cut 50 --title STD_' + str(name) + '_EW --label "A" --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_EW.pdf')
        # H1KS # 16 velocity in km/s from H1 (1st g)
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 17  --min-cut 0.00000 --max-cut 2 --title STD_' + str(name) + '_velocity --label "km/s" --colormap jet --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_velocity.pdf')
        # H2KS # 17 sigma in km/s from H2 (1st g)
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 18  --min-cut 0.00000 --max-cut 2 --title STD_' + str(name) + '_sigma --label "km/s"  --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_sigma.pdf')
        # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
        os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_STD_SIMULATIONS.fits -c 19  --min-cut 0.00000 --max-cut 2 --title STD_' + str(name) + '_sigma_corrected --label "km/s"  --wcs-grid')
        os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_std/' + str(name) + '_UM461_STD_SIMULATIONS_sigma_corrected.pdf')


