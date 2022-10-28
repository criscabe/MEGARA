#
# Copyright 2022-2023 Universidad Complutense de Madrid
#
# This file software has been employed to compute 
# the median value of different parameters derived
# from the simulated data of the MEGARA IFU instrument at GTC
# We also compute the residuals (real data - median of the simulations)
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

    parser = argparse.ArgumentParser(description='Compute the median value and residuals of different parameters')
    parser.add_argument("--OIII5007", help = "MEDIAN and RESIDUALS of the OIII5007 line",
                        action="store_true")

    args = parser.parse_args()
    
    
    
    if args.OIII5007:
        print('.............................')
        print('--------Compute MEDIAN and RESIDUALS of the OIII5007 line--------')
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


        median_simul_noise = np.nanmedian(IMAGES_SIMUL_OIII5007_noise,axis=0)
        median_simul_snr = np.nanmedian(IMAGES_SIMUL_OIII5007_snr,axis=0)    
        median_simul_flux = np.nanmedian(IMAGES_SIMUL_OIII5007_flux,axis=0)
        median_simul_flux_fit = np.nanmedian(IMAGES_SIMUL_OIII5007_flux_fit,axis=0)
        median_simul_EW = np.nanmedian(IMAGES_SIMUL_OIII5007_EW,axis=0)
        median_simul_velocity = np.nanmedian(IMAGES_SIMUL_OIII5007_velocity,axis=0)
        median_simul_sigma = np.nanmedian(IMAGES_SIMUL_OIII5007_sigma,axis=0)
        median_simul_sigma_corrected = np.nanmedian(IMAGES_SIMUL_OIII5007_sigma_corrected,axis=0)
        
        os.system('cp results_SIMUL/LINES/OIII5007/OIII5007_UM461_SIMUL_1.fits  results_SIMUL/LINES/OIII5007/OIII5007_UM461_MEDIAN_SIMULATIONS.fits')
    
        print('.............................')
        print('Saving FITS file.......')
        with fits.open('results_SIMUL/LINES/OIII5007/OIII5007_UM461_MEDIAN_SIMULATIONS.fits', mode='update') as hdulist:
            hdulist[0].data[:,2] = median_simul_noise
            hdulist[0].data[:,3] = median_simul_snr
            hdulist[0].data[:,4] = median_simul_flux
            hdulist[0].data[:,6] = median_simul_flux_fit
            hdulist[0].data[:,7] = median_simul_EW
            hdulist[0].data[:,16] = median_simul_velocity
            hdulist[0].data[:,17] = median_simul_sigma
            hdulist[0].data[:,18] = median_simul_sigma_corrected

        #####################################################################
        
        ####### RESIDUALS = REAL DATA - MEDIAN OF THE SIMULATIONS ###########
        
        with fits.open('results/LINES/SIN_modelmap/OIII5007/OIII5007_UM461.fits', mode='readonly') as hdulist:
            image = hdulist[0].data
            
        
        resta_realsimul_noise = image[:,2] - median_simul_noise
        resta_realsimul_snr = image[:,3] - median_simul_snr
        resta_realsimul_flux = image[:,4] - median_simul_flux
        resta_realsimul_flux_fit = image[:,6] - median_simul_flux_fit
        resta_realsimul_EW = image[:,7] - median_simul_EW
        resta_realsimul_velocity = image[:,16] - median_simul_velocity
        resta_realsimul_sigma = image[:,17] - median_simul_sigma 
        resta_realsimul_sigma_corrected = image[:,18] - median_simul_sigma_corrected
        
        
        os.system('cp results_SIMUL/LINES/OIII5007/OIII5007_UM461_SIMUL_1.fits  results_SIMUL/LINES/OIII5007/OIII5007_UM461_REAL_MENOS_SIMUL.fits')
    
        print('.............................')
        print('Saving FITS file.......')
        with fits.open('results_SIMUL/LINES/OIII5007/OIII5007_UM461_REAL_MENOS_SIMUL.fits', mode='update') as hdulist:
            hdulist[0].data[:,2] = resta_realsimul_noise
            hdulist[0].data[:,3] = resta_realsimul_snr 
            hdulist[0].data[:,4] = resta_realsimul_flux
            hdulist[0].data[:,6] = resta_realsimul_flux_fit
            hdulist[0].data[:,7] = resta_realsimul_EW
            hdulist[0].data[:,16] = resta_realsimul_velocity
            hdulist[0].data[:,17] = resta_realsimul_sigma
            hdulist[0].data[:,18] = resta_realsimul_sigma_corrected

