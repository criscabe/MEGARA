#
# Copyright 2022-2023 Universidad Complutense de Madrid
#
# This file software has been employed to compute
# the median of the simulations,
# the residuals (real data - median of the simulations),
# and the random uncertainties of different parameters derived
# from the data of the MEGARA IFU instrument at GTC
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
import cmd
import glob
import shutil


def check_directory(path):
    '''Create a directory if it does not exist.
    '''
    if (os.path.isdir(path) == False):
        os.mkdir(path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Compute the median, residuals, and uncertainties of different parameters')
    parser.add_argument('target',
                        help="Name of the target")
    parser.add_argument('-LINE', help = "Name of the emission line", type=str)
    parser.add_argument("--median", help = "Compute the median values of the simulations",
                        action="store_true")
    parser.add_argument("--residuals", help = "Compute the residuals (real values - median of simulations)",
                        action="store_true")
    parser.add_argument("--uncertainties", help = "Compute the random uncertainties",
                        action="store_true")
    parser.add_argument("--plots", help = "Create and save the figures",
                        action="store_true")
    args = parser.parse_args()
    
    ###########################################
    
    target = str(args.target)
    name = str(args.LINE)
        
    ###########################################
    
    print('.............................')
    print('--------Compute parameters for the ' + str(name) + ' line--------')
    print('.............................')
    
    
    images_list = sorted(glob.glob('results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_*.fits'))

    
    IMAGES_SIMUL_snr = []
    IMAGES_SIMUL_flux_fit = []
    IMAGES_SIMUL_EW = []
    IMAGES_SIMUL_velocity = []
    IMAGES_SIMUL_sigma_corrected = []
        
        
    for i in range(len(images_list)):
        with fits.open(images_list[i], mode='readonly') as hdulist:
            image = hdulist[0].data
    
        IMAGES_SIMUL_snr.append(image[:,3])  ## SNR # 3 S/N at the peak of the line
        IMAGES_SIMUL_flux_fit.append(image[:,6])  ## FLUXF # 6 Flux from best-fitting function(s)
        IMAGES_SIMUL_EW.append(image[:,7])  ## FLUXF # 7 EW from best-fitting function(s)
        IMAGES_SIMUL_velocity.append(image[:,16])  ## H1KS # 16 velocity in km/s from H1 (1st g)
        IMAGES_SIMUL_sigma_corrected.append(image[:,18])  ## H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)


    #####################################################################
        
    ####### MEDIAN OF THE SIMULATIONS ###########
    
    if args.median or args.residuals:
        print('.............................')
        print('--------Compute the MEDIAN images for the ' + str(name) + ' line--------')
        print('.............................')
        
        median_simul_snr = np.nanmedian(IMAGES_SIMUL_snr,axis=0)
        median_simul_flux_fit = np.nanmedian(IMAGES_SIMUL_flux_fit,axis=0)
        median_simul_EW = np.nanmedian(IMAGES_SIMUL_EW,axis=0)
        median_simul_velocity = np.nanmedian(IMAGES_SIMUL_velocity,axis=0)
        median_simul_sigma_corrected = np.nanmedian(IMAGES_SIMUL_sigma_corrected,axis=0)
            
        
        file = 'results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_1.fits'
        shutil.copy2(file,file.replace('SIMUL_1.fits', 'MEDIAN_SIMULATIONS.fits'))
        
        
        print('.............................')
        print('Saving FITS file.......')
        with fits.open('results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits', mode='update') as hdulist:
            hdulist[0].data[:,3] = median_simul_snr
            hdulist[0].data[:,6] = median_simul_flux_fit
            hdulist[0].data[:,7] = median_simul_EW
            hdulist[0].data[:,16] = median_simul_velocity
            hdulist[0].data[:,18] = median_simul_sigma_corrected
        

    ####### PLOTS ###########
        
        if args.plots:
            file_path = 'results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/'
            check_directory(file_path)
            
            
            # SNR # 3 S/N at the peak of the line
            mincut = input("mincut S/N at the peak of the line (MEDIAN image): ")
            maxcut = input("maxcut S/N at the peak of the line (MEDIAN image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits -c 4  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title MEDIAN_' + str(name) + '_SNR --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS_SNR.pdf')
                
            # FLUXF # 6 Flux from best-fitting function(s)
            mincut = input("mincut Flux (cgs) (MEDIAN image): ")
            maxcut = input("maxcut Flux (cgs) (MEDIAN image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits -c 7   --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + '  --title MEDIAN_' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS_flux_fit.pdf')
                
            # FLUXF # 7 EW from best-fitting function(s)
            mincut = input("mincut EW (A) (MEDIAN image): ")
            maxcut = input("maxcut EW (A) (MEDIAN image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits -c 8  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title MEDIAN_' + str(name) + '_EW --label "A" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS_EW.pdf')
                
            # H1KS # 16 velocity in km/s from H1 (1st g)
            mincut = input("mincut velocity (km/s) (MEDIAN image): ")
            maxcut = input("maxcut velocity (km/s) (MEDIAN image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits -c 17  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title MEDIAN_' + str(name) + '_velocity --label "km/s" --colormap jet --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS_velocity.pdf')
                
            # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
            mincut = input("mincut sigma (km/s) corrected from instrumental sigma (MEDIAN image): ")
            maxcut = input("maxcut sigma (km/s) corrected from instrumental sigma (MEDIAN image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS.fits -c 19  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title MEDIAN_' + str(name) + '_sigma_corrected --label "km/s"  --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_MEDIAN/' + str(name) + '_' + str(target) + '_MEDIAN_SIMULATIONS_sigma_corrected.pdf')
            
        
        
    #####################################################################
        
    ####### RESIDUALS = REAL DATA - MEDIAN OF THE SIMULATIONS ###########
        
    if args.residuals:
        print('.............................')
        print('-------- Compute the residuals = real data - median of the simulations --------')
        print('-------- for the ' + str(name) + ' line--------')
        print('.............................')
        
        with fits.open('results/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '.fits', mode='readonly') as hdulist:
            image = hdulist[0].data
            
        
        residuals_snr = image[:,3] - median_simul_snr
        residuals_flux_fit = image[:,6] - median_simul_flux_fit
        residuals_EW = image[:,7] - median_simul_EW
        residuals_velocity = image[:,16] - median_simul_velocity
        residuals_sigma_corrected = image[:,18] - median_simul_sigma_corrected
            
        
        
        shutil.copy2(file,file.replace('SIMUL_1.fits', 'RESIDUALS.fits'))
        
        
        print('.............................')
        print('Saving FITS file.......')
        
        with fits.open('results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits', mode='update') as hdulist:
            hdulist[0].data[:,3] = residuals_snr
            hdulist[0].data[:,6] = residuals_flux_fit
            hdulist[0].data[:,7] = residuals_EW
            hdulist[0].data[:,16] = residuals_velocity
            hdulist[0].data[:,18] = residuals_sigma_corrected


    ####### PLOTS ###########
        if args.plots:
            file_path = 'results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/'
            check_directory(file_path)
            
            # SNR # 3 S/N at the peak of the line
            mincut = input("mincut S/N at the peak of the line (RESIDUALS image): ")
            maxcut = input("maxcut S/N at the peak of the line (RESIDUALS image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits -c 4  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title RESIDUALS_' + str(name) + '_SNR --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/' + str(name) + '_' + str(target) + '_RESIDUALS_SNR.pdf')
                
            # FLUXF # 6 Flux from best-fitting function(s)
            mincut = input("mincut Flux (cgs) (RESIDUALS image): ")
            maxcut = input("maxcut Flux (cgs) (RESIDUALS image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits -c 7   --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + '  --title RESIDUALS_' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/' + str(name) + '_' + str(target) + '_RESIDUALS_flux_fit.pdf')
                
            # FLUXF # 7 EW from best-fitting function(s)
            mincut = input("mincut EW (A) (RESIDUALS image): ")
            maxcut = input("maxcut EW (A) (RESIDUALS image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits -c 8  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title RESIDUALS_' + str(name) + '_EW --label "A" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/' + str(name) + '_' + str(target) + '_RESIDUALS_EW.pdf')
                
            # H1KS # 16 velocity in km/s from H1 (1st g)
            mincut = input("mincut velocity (km/s) (RESIDUALS image): ")
            maxcut = input("maxcut velocity (km/s) (RESIDUALS image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits -c 17  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title RESIDUALS_' + str(name) + '_velocity --label "km/s" --colormap jet --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/' + str(name) + '_' + str(target) + '_RESIDUALS_velocity.pdf')
                
            # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
            mincut = input("mincut sigma (km/s) corrected from instrumental sigma (RESIDUALS image): ")
            maxcut = input("maxcut sigma (km/s) corrected from instrumental sigma (RESIDUALS image): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_RESIDUALS.fits -c 19  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title RESIDUALS_' + str(name) + '_sigma_corrected --label "km/s"  --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_RESIDUALS/' + str(name) + '_' + str(target) + '_RESIDUALS_sigma_corrected.pdf')


    #####################################################################
        
    ####### UNCERTAINTIES ###########
    
    if args.uncertainties:
        print('.............................')
        print('--------Compute the UNCERTAINTIES for the ' + str(name) + ' line--------')
        print('.............................')
        
        std_simul_snr = np.nanstd(IMAGES_SIMUL_snr,axis=0)
        std_simul_flux_fit = np.nanstd(IMAGES_SIMUL_flux_fit,axis=0)
        std_simul_EW = np.nanstd(IMAGES_SIMUL_EW,axis=0)
        std_simul_velocity = np.nanstd(IMAGES_SIMUL_velocity,axis=0)
        std_simul_sigma_corrected = np.nanstd(IMAGES_SIMUL_sigma_corrected,axis=0)
            
        
        shutil.copy2(file,file.replace('SIMUL_1.fits', 'STD_SIMULATIONS.fits'))
    
        print('.............................')
        print('Saving FITS file.......')
        with fits.open('results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits', mode='update') as hdulist:
            hdulist[0].data[:,3] = std_simul_snr
            hdulist[0].data[:,6] = std_simul_flux_fit
            hdulist[0].data[:,7] = std_simul_EW
            hdulist[0].data[:,16] = std_simul_velocity
            hdulist[0].data[:,18] = std_simul_sigma_corrected

    ####### PLOTS ###########
        if args.plots:
            file_path = 'results_SIMUL/LINES/' + str(name) + '/plots_STD/'
            check_directory(file_path)
            
            # SNR # 3 S/N at the peak of the line
            mincut = input("mincut S/N at the peak of the line (UNCERTAINTIES): ")
            maxcut = input("maxcut S/N at the peak of the line (UNCERTAINTIES): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits -c 4  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title STD_' + str(name) + '_SNR --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_STD/' + str(name) + '_' + str(target) + '_STD_SNR.pdf')
                
            # FLUXF # 6 Flux from best-fitting function(s)
            mincut = input("mincut Flux (cgs) (UNCERTAINTIES): ")
            maxcut = input("maxcut Flux (cgs) (UNCERTAINTIES): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits -c 7   --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + '  --title STD_' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_STD/' + str(name) + '_' + str(target) + '_STD_flux_fit.pdf')
                
            # FLUXF # 7 EW from best-fitting function(s)
            mincut = input("mincut EW (A) (UNCERTAINTIES): ")
            maxcut = input("maxcut EW (A) (UNCERTAINTIES): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits -c 8  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title STD_' + str(name) + '_EW --label "A" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_STD/' + str(name) + '_' + str(target) + '_STD_EW.pdf')
                
            # H1KS # 16 velocity in km/s from H1 (1st g)
            mincut = input("mincut velocity (km/s) (UNCERTAINTIES): ")
            maxcut = input("maxcut velocity (km/s) (UNCERTAINTIES): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits -c 17  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title STD_' + str(name) + '_velocity --label "km/s" --colormap jet --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_STD/' + str(name) + '_' + str(target) + '_STD_velocity.pdf')
                
            # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
            mincut = input("mincut sigma (km/s) corrected from instrumental sigma (UNCERTAINTIES): ")
            maxcut = input("maxcut sigma (km/s) corrected from instrumental sigma (UNCERTAINTIES): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_STD_SIMULATIONS.fits -c 19  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title STD_' + str(name) + '_sigma_corrected --label "km/s"  --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots_STD/' + str(name) + '_' + str(target) + '_STD_sigma_corrected.pdf')
