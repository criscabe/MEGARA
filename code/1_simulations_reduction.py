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


from astropy.io import fits



def simulR(sigma_c): 
    naxis2, naxis1 = sigma_c.shape
    z1 = np.random.rand(naxis2,naxis1)
    z2 = np.random.rand(naxis2,naxis1)
    R = np.sqrt(2)*sigma_c * np.sqrt(-np.log(1-z1))*np.cos(2 * np.pi * z2)
    return R



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Run MEGARA DRP')
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
    
    nsimul = 50
    
    h = 0

###########
    image_bias = 'data/0003396335-20220505-MEGARA-MegaraBiasImage.fits'


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

###########

    os.system('cp data/0003396335-20220505-MEGARA-MegaraBiasImage.fits data/0003396335-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396336-20220505-MEGARA-MegaraBiasImage.fits data/0003396336-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396337-20220505-MEGARA-MegaraBiasImage.fits data/0003396337-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396338-20220505-MEGARA-MegaraBiasImage.fits data/0003396338-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396339-20220505-MEGARA-MegaraBiasImage.fits data/0003396339-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396340-20220505-MEGARA-MegaraBiasImage.fits data/0003396340-20220505-MEGARA-MegaraBiasImage_simul.fits')
    os.system('cp data/0003396341-20220505-MEGARA-MegaraBiasImage.fits data/0003396341-20220505-MEGARA-MegaraBiasImage_simul.fits')
    ######
    os.system('cp data/0003396350-20220505-MEGARA-MegaraTraceMap.fits data/0003396350-20220505-MEGARA-MegaraTraceMap_simul.fits')
    os.system('cp data/0003396351-20220505-MEGARA-MegaraTraceMap.fits data/0003396351-20220505-MEGARA-MegaraTraceMap_simul.fits')
    os.system('cp data/0003396352-20220505-MEGARA-MegaraTraceMap.fits data/0003396352-20220505-MEGARA-MegaraTraceMap_simul.fits')
    ######
    os.system('cp data/0003396354-20220505-MEGARA-MegaraArcCalibration.fits data/0003396354-20220505-MEGARA-MegaraArcCalibration_simul.fits')
    os.system('cp data/0003396355-20220505-MEGARA-MegaraArcCalibration.fits data/0003396355-20220505-MEGARA-MegaraArcCalibration_simul.fits')
    os.system('cp data/0003396356-20220505-MEGARA-MegaraArcCalibration.fits data/0003396356-20220505-MEGARA-MegaraArcCalibration_simul.fits')
    ######
    os.system('cp data/0003396137-20220505-MEGARA-MegaraLcbImage.fits data/0003396137-20220505-MEGARA-MegaraLcbImage_simul.fits')
    os.system('cp data/0003396138-20220505-MEGARA-MegaraLcbImage.fits data/0003396138-20220505-MEGARA-MegaraLcbImage_simul.fits')
    os.system('cp data/0003396139-20220505-MEGARA-MegaraLcbImage.fits data/0003396139-20220505-MEGARA-MegaraLcbImage_simul.fits')
    ######
    os.system('cp data/0003396202-20220505-MEGARA-MegaraLcbImage.fits data/0003396202-20220505-MEGARA-MegaraLcbImage_simul.fits')
    os.system('cp data/0003396203-20220505-MEGARA-MegaraLcbImage.fits data/0003396203-20220505-MEGARA-MegaraLcbImage_simul.fits')
    os.system('cp data/0003396204-20220505-MEGARA-MegaraLcbImage.fits data/0003396204-20220505-MEGARA-MegaraLcbImage_simul.fits')

###########

    list_bias = ['data/0003396335-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396336-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396337-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396338-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396339-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396340-20220505-MEGARA-MegaraBiasImage.fits',
            'data/0003396341-20220505-MEGARA-MegaraBiasImage.fits']

    list_arcs = ['data/0003396354-20220505-MEGARA-MegaraArcCalibration.fits',
            'data/0003396355-20220505-MEGARA-MegaraArcCalibration.fits',
            'data/0003396356-20220505-MEGARA-MegaraArcCalibration.fits']


    list_flat = ['data/0003396350-20220505-MEGARA-MegaraTraceMap.fits',
            'data/0003396351-20220505-MEGARA-MegaraTraceMap.fits',
            'data/0003396352-20220505-MEGARA-MegaraTraceMap.fits']

    list_obj = ['data/0003396202-20220505-MEGARA-MegaraLcbImage.fits',
            'data/0003396203-20220505-MEGARA-MegaraLcbImage.fits',
            'data/0003396204-20220505-MEGARA-MegaraLcbImage.fits']

    list_star = ['data/0003396137-20220505-MEGARA-MegaraLcbImage.fits',
            'data/0003396138-20220505-MEGARA-MegaraLcbImage.fits',
            'data/0003396139-20220505-MEGARA-MegaraLcbImage.fits']

###########

    list_bias_simul = ['data/0003396335-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396336-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396337-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396338-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396339-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396340-20220505-MEGARA-MegaraBiasImage_simul.fits',
                'data/0003396341-20220505-MEGARA-MegaraBiasImage_simul.fits']
    
    list_arcs_simul = ['data/0003396354-20220505-MEGARA-MegaraArcCalibration_simul.fits',
                'data/0003396355-20220505-MEGARA-MegaraArcCalibration_simul.fits',
                'data/0003396356-20220505-MEGARA-MegaraArcCalibration_simul.fits']
    
    
    list_flat_simul = ['data/0003396350-20220505-MEGARA-MegaraTraceMap_simul.fits',
                'data/0003396351-20220505-MEGARA-MegaraTraceMap_simul.fits',
                'data/0003396352-20220505-MEGARA-MegaraTraceMap_simul.fits']
    
    list_obj_simul = ['data/0003396202-20220505-MEGARA-MegaraLcbImage_simul.fits',
                'data/0003396203-20220505-MEGARA-MegaraLcbImage_simul.fits',
                'data/0003396204-20220505-MEGARA-MegaraLcbImage_simul.fits']
    
    list_star_simul = ['data/0003396137-20220505-MEGARA-MegaraLcbImage_simul.fits',
                'data/0003396138-20220505-MEGARA-MegaraLcbImage_simul.fits',
                'data/0003396139-20220505-MEGARA-MegaraLcbImage_simul.fits']

###########
    
    for j in range(nsimul):
        print('Simulation: ' + str(h+j+1))
        time00 = time.perf_counter()
    #### BIAS #######
        print('----> Simulando BIAS')
        for i in range(len(list_bias)):
            with fits.open(list_bias[i], mode='readonly') as hdulist:
                bias  = hdulist[0].data

            resta = bias - bias_artificial
            image_positive = np.copy(resta)
            image_positive[np.where(resta <= 0)] = 0.0

            sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )
            
            bias_simul = bias + simulR(sigma_c)
                
            with fits.open(list_bias_simul[i], mode='update') as hdulist:
                hdulist[0].data = bias_simul - 32768

        
#### ARC #######
        print('----> Simulando ARCS')
        for i in range(len(list_arcs)):
            with fits.open(list_arcs[i], mode='readonly') as hdulist:
                arcs  = hdulist[0].data
            
            resta = arcs - bias_artificial
            image_positive = np.copy(resta)
            image_positive[np.where(resta <= 0)] = 0.0

            sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )

            
            arcs_simul = arcs + simulR(sigma_c)
            
            with fits.open(list_arcs_simul[i], mode='update') as hdulist:
                hdulist[0].data = arcs_simul - 32768
            
            
#### FLAT #######        
        print('----> Simulando FLATS')     
        for i in range(len(list_flat)):
            with fits.open(list_flat[i], mode='readonly') as hdulist:
                flat  = hdulist[0].data
            
            resta = flat - bias_artificial
            image_positive = np.copy(resta)
            image_positive[np.where(resta <= 0)] = 0.0

            sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )
    
            
            flat_simul = flat + simulR(sigma_c)
            
            with fits.open(list_flat_simul[i], mode='update') as hdulist:
                hdulist[0].data = flat_simul - 32768
            
            
#### OBJECT #######  
        print('----> Simulando OBJECT')  
        for i in range(len(list_obj)):
            with fits.open(list_obj[i], mode='readonly') as hdulist:
                obj  = hdulist[0].data

            
            resta = obj - bias_artificial
            image_positive = np.copy(resta)
            image_positive[np.where(resta <= 0)] = 0.0
            
            sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )
            
 
            obj_simul = obj + simulR(sigma_c)
            
            with fits.open(list_obj_simul[i], mode='update') as hdulist:
                 hdulist[0].data = obj_simul - 32768
           
            
    
#### STAR #######  
        print('----> Simulando STAR')  
        for i in range(len(list_star)):
            with fits.open(list_star[i], mode='readonly') as hdulist:
                star  = hdulist[0].data

            resta = star - bias_artificial
            image_positive = np.copy(resta)
            image_positive[np.where(resta <= 0)] = 0.0

            sigma_c = np.sqrt(image_positive /g + sigma_rms**2 )
    
                
            star_simul = star + simulR(sigma_c)
            
            with fits.open(list_star_simul[i], mode='update') as hdulist:
                hdulist[0].data = star_simul - 32768
            
          
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
            os.system('numina run 1_tracemap_LRB_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid1_LR-B_SIMUL_results/master_traces.json   ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/TraceMap/LCB/LR-B')
            
        time2 = time.perf_counter()
    
        if (args.stage2 or args.all):
            print('.............................')
            print('--------Running step 2: ModelMap--------')
            print('.............................')
            os.system('numina run 2_modelmap_LRB_simul.yaml  --link-files -r ../control.yaml')
            os.system('cp obsid2_LR-B_SIMUL_results/master_model.json ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/ModelMap/LCB/LR-B/')
            
        time3 = time.perf_counter()
    
        if (args.stage3 or args.all):
            print('.............................')
            print('--------Running step 3: Wavelength calibration--------')
            print('.............................')
            os.system('numina run 3_wavecalib_LRB_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid3_LR-B_SIMUL_results/master_wlcalib.json ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/WavelengthCalibration/LCB/LR-B')
            
        time4 = time.perf_counter()
    
        if (args.stage4 or args.all):
            print('.............................')
            print('--------Running step 4: FiberFlat--------')
            print('.............................')
            os.system('numina run 4_fiberflat_LRB_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid4_LR-B_SIMUL_results/master_fiberflat.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterFiberFlat/LCB/LR-B')
            
        time5 = time.perf_counter()
    
        if (args.stage5 or args.all):
            print('.............................')
            print('--------Running step 5: TwilightFlat--------')
            print('.............................')
            os.system('numina run 5_twilight_LRB_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid5_LR-B_SIMUL_results/master_twilightflat.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterTwilightFlat/LCB/LR-B/')
    
        time6 = time.perf_counter()
    
        if (args.stage6 or args.all):
            print('.............................')
            print('--------Running step 6: LCB adquisition--------')
            print('.............................')
            os.system('numina run 6_Lcbadquisition_LRB_simul.yaml --link-files -r ../control.yaml')
    #        os.system('more obsid6_LR-B_SIMUL_results/processing.log ')
    
        time7 = time.perf_counter()
    
        if (args.stage7 or args.all):
            print('.............................')
            print('--------Running step 7: Standard Star--------')
            print('.............................')
            os.system('numina run 7_Standardstar_LRB_simul.yaml --link-files -r ../control.yaml')
            os.system('cp obsid7_LR-B_SIMUL_results/master_sensitivity.fits ../ca3558e3-e50d-4bbc-86bd-da50a0998a48/MasterSensitivity/LCB/LR-B/')
        
        time8 = time.perf_counter()
        
        if (args.stage8 or args.all):
            print('.............................')
            print('--------Running step 8: Reduce LCB--------')
            print('.............................')
            os.system('numina run 8_reduce_LCB_LRB_simul.yaml --link-files -r ../control.yaml')
            
            
            os.system('cp obsid8_LR-B_UM461_ob2_SIMUL_results/final_rss.fits ../results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits')
            os.system('megaradrp-cube obsid8_LR-B_UM461_ob2_SIMUL_results/final_rss.fits -p 0.4 -o cube_LRB.fits --wcs-pa-from-header')
            os.system('mv cube_LRB.fits ../results_SIMUL/cube_LRB_SIMUL_' + str(h+j+1) + '.fits')
 
            
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

