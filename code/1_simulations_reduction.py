#
# Copyright 2022-2023 Universidad Complutense de Madrid
#
# This file software has been employed to add Gaussian noise to  
# the images taken with the MEGARA IFU instrument at GTC
# and automatically reduce the simulated data
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
import time
import shutil
import glob
from astropy.io import ascii, fits





def simulR(sigma_c): 
    naxis2, naxis1 = sigma_c.shape
    z1 = np.random.rand(naxis2,naxis1)
    z2 = np.random.rand(naxis2,naxis1)
    R = np.sqrt(2)*sigma_c * np.sqrt(-np.log(1-z1))*np.cos(2 * np.pi * z2)
    return R

def simulImages(list_images, list_images_simul):
    for i in range(len(list_images)):
        with fits.open(list_images[i], mode='readonly') as hdulist:
            image  = hdulist[0].data

        resta = image - bias_artificial
        image_positive = np.copy(resta)
        image_positive[np.where(resta <= 0)] = 0.0

        sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )
            
        image_simul = image + simulR(sigma_c)
                
        with fits.open(list_images_simul[i], mode='update') as hdulist:
            hdulist[0].data = image_simul - 32768



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run MEGARA DRP')
    parser.add_argument("nsimul",
                        help="Number of simulations",type=int)
    parser.add_argument("initializer",
                        help="Initializer of simulations",type=int)
    parser.add_argument('VPH',
                        help="VPH used during the observations")
    parser.add_argument('target',
                        help="Name of the target")
    parser.add_argument('OB',
                        help="Observing Block")
    ##
    parser.add_argument("--stage0", help = "Run step 0: BIAS",
                        action="store_true")
    parser.add_argument("--stage1", help = "Run step 1: TraceMap",
                        action="store_true")
    parser.add_argument("--stage2", help = "Run step 2: ModelMap",
                        action="store_true")
    parser.add_argument("--stage3", help = "Run step 3: Wavelength calibration",
                        action="store_true")
    parser.add_argument("--stage4", help = "Run step 4: FiberFlat",
                        action="store_true")
    parser.add_argument("--stage5", help = "Run step 5: TwilightFlat",
                        action="store_true")
    parser.add_argument("--stage6", help = "Run step 6: LCB adquisition",
                        action="store_true")
    parser.add_argument("--stage7", help = "Run step 7: Standard Star",
                        action="store_true")
    parser.add_argument("--stage8", help = "Run step 8: Reduce LCB",
                        action="store_true")
    parser.add_argument("--all", help = "Run all the steps of MEGARA DRP",
                        action="store_true")


    args = parser.parse_args()
    
    abs_path = os.path.abspath(os.getcwd())

#####################################

    np.random.seed(70) 
    
    nsimul = int(args.nsimul)
    h = int(args.initializer)
    
    VPH = str(args.VPH)
    target = str(args.target)
    OB = str(args.OB)

###########

    list_bias1 = sorted(glob.glob(f'{abs_path}/data/*-MEGARA-MegaraBiasImage.fits'))
    list_arcs1 = sorted(glob.glob(f'{abs_path}/data/*-MegaraArcCalibration.fits'))
    list_flat1 = sorted(glob.glob(f'{abs_path}/data/*-MEGARA-MegaraTraceMap.fits'))
    
    # Create list_obj.txt with the object images
    
    objects = ascii.read('list_obj.txt', names=['images'], data_start=0)

    list_obj = []
    for i in range(len(objects)):
        list_obj.append(objects[i][0])
    
    # Create list_star.txt with the object images
    
    stars = ascii.read('list_star.txt', names=['images'], data_start=0)

    list_star = []
    for i in range(len(stars)):
        list_star.append(stars[i][0])

###########


    list_bias = []
    list_arcs = []
    list_flat = []


    list_bias_simul = []
    list_arcs_simul = []
    list_flat_simul = []
    list_obj_simul = []
    list_star_simul = []

    for file in list_bias1:
        shutil.copy2(file, file.replace('.fits', '_simul.fits'))
        list_bias.append('/'.join(file.split('/')[-2:]))
        a = file.replace('.fits', '_simul.fits')
        list_bias_simul.append('/'.join(a.split('/')[-2:]))

    for file in list_arcs1:
        shutil.copy2(file, file.replace('.fits', '_simul.fits'))
        list_arcs.append('/'.join(file.split('/')[-2:]))
        a = file.replace('.fits', '_simul.fits')
        list_arcs_simul.append('/'.join(a.split('/')[-2:]))
        
    for file in list_flat1:
        shutil.copy2(file, file.replace('.fits', '_simul.fits'))
        list_flat.append('/'.join(file.split('/')[-2:]))
        a = file.replace('.fits', '_simul.fits')
        list_flat_simul.append('/'.join(a.split('/')[-2:]))
        
    for file in list_obj:
        shutil.copy2(file, file.replace('.fits', '_simul.fits'))
        list_obj_simul.append(file.replace('.fits', '_simul.fits'))
        
    for file in list_star:
        shutil.copy2(file, file.replace('.fits', '_simul.fits'))
        list_star_simul.append(file.replace('.fits', '_simul.fits'))
    
###########

    image_bias = list_bias[0]

    with fits.open(image_bias, mode='readonly') as hdulist:
        bias  = hdulist[0].data
        header = hdulist[0].header
        
    bias_artificial = np.zeros(bias.shape)

    bias_artificial[0:2106,:] = 2087.0
    bias_artificial[2106:,:] = 2054.0
    
    # Gain
    g = np.zeros(bias.shape)

    g[0:2106,:] = 1.6
    g[2106:,:] = 1.73
    
    # readout noise
    sigma_rms = 2.0

#################################

    for j in range(nsimul):
        print('Simulation: ' + str(h+j+1))
        time00 = time.perf_counter()

        simulImages(list_bias,list_bias_simul)
        simulImages(list_arcs,list_arcs_simul)
        simulImages(list_flat,list_flat_simul)
        simulImages(list_obj,list_obj_simul)
        simulImages(list_star,list_star_simul)

        time11 = time.perf_counter()
        print(f"Runtime simulation : {time11 - time00:0.2f} seconds")
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
#####################################

        time0 = time.perf_counter()
        
        if (args.stage0 or args.all):
            print('.............................')
            print('--------Running step 0: BIAS--------')
            print('.............................')
            os.system('numina run 0_bias_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid0_bias_test_SIMUL_results/master_bias.fits   ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterBias')
        
        time1 = time.perf_counter()
        
        if (args.stage1 or args.all):
            print('.............................')
            print('--------Running step 1: TraceMap--------')
            print('.............................')
            os.system('numina run 1_tracemap_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid1_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_traces.json   ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/TraceMap/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
            
        time2 = time.perf_counter()
    
        if (args.stage2 or args.all):
            print('.............................')
            print('--------Running step 2: ModelMap--------')
            print('.............................')
            os.system('numina run 2_modelmap_' + str(VPH) + '_simul.yaml  --link-files -r ../control.yaml')
            os.system('cp obsid2_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_model.json ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/ModelMap/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
            
        time3 = time.perf_counter()
    
        if (args.stage3 or args.all):
            print('.............................')
            print('--------Running step 3: Wavelength calibration--------')
            print('.............................')
            os.system('numina run 3_wavecalib_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid3_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_wlcalib.json ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/WavelengthCalibration/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
            
        time4 = time.perf_counter()
    
        if (args.stage4 or args.all):
            print('.............................')
            print('--------Running step 4: FiberFlat--------')
            print('.............................')
            os.system('numina run 4_fiberflat_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid4_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_fiberflat.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterFiberFlat/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
            
        time5 = time.perf_counter()
    
        if (args.stage5 or args.all):
            print('.............................')
            print('--------Running step 5: TwilightFlat--------')
            print('.............................')
            os.system('numina run 5_twilight_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid5_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_twilightflat.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterTwilightFlat/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
    
        time6 = time.perf_counter()
    
        if (args.stage6 or args.all):
            print('.............................')
            print('--------Running step 6: LCB adquisition--------')
            print('.............................')
            os.system('numina run 6_Lcbadquisition_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
    #        os.system('more obsid6_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/processing.log ')
    
        time7 = time.perf_counter()
    
        if (args.stage7 or args.all):
            print('.............................')
            print('--------Running step 7: Standard Star--------')
            print('.............................')
            os.system('numina run 7_Standardstar_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid7_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_SIMUL_results/master_sensitivity.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterSensitivity/LCB/' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '/')
        
        time8 = time.perf_counter()
        
        if (args.stage8 or args.all):
            print('.............................')
            print('--------Running step 8: Reduce LCB--------')
            print('.............................')
            os.system('numina run 8_reduce_LCB_' + str(VPH) + '_simul.yaml --link-files -r ../control.yaml')
            
            
            os.system('cp obsid8_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_' + str(target) + '_' + str(OB) + '_SIMUL_results/final_rss.fits ../results_SIMUL/' + str(target) + '_' + str(VPH) + '_SIMUL_' + str(h+j+1) + '.fits')
            os.system('megaradrp-cube obsid8_' + str(VPH[0:2]) + '-' + str(VPH[-1]) + '_' + str(target) + '_' + str(OB) + '_SIMUL_results/final_rss.fits -p 0.4 -o cube_' + str(VPH) + '.fits --wcs-pa-from-header')
            os.system('mv cube_' + str(VPH) + '.fits ../results_SIMUL/cube_' + str(VPH) + '_SIMUL_' + str(h+j+1) + '.fits')
 
            
        time9 = time.perf_counter()
    
        print("----------------------------------------------")
        print("----------------------------------------------")
        print(f"Runtime total : {time9 - time0:0.2f} seconds")
        print("%%%%%%")
        print(f"Runtime Step 0: {time1 - time0:0.2f} seconds")
        print(f"Runtime Step 1: {time2 - time1:0.2f} seconds")
        print(f"Runtime Step 2: {time3 - time2:0.2f} seconds")
        print(f"Runtime Step 3: {time4 - time3:0.2f} seconds")
        print(f"Runtime Step 4: {time5 - time4:0.2f} seconds")
        print(f"Runtime Step 5: {time6 - time5:0.2f} seconds")
        print(f"Runtime Step 6: {time7 - time6:0.2f} seconds")
        print(f"Runtime Step 7: {time8 - time7:0.2f} seconds")
        print(f"Runtime Step 8: {time9 - time8:0.2f} seconds")
        print("----------------------------------------------")
        print("----------------------------------------------")


