#
# Copyright 2022-2023 Universidad Complutense de Madrid
#
# This file software has been employed to analyze
# simulated reduced data from the MEGARA IFU instrument at GTC
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

def check_directory(path):
    '''Create a directory if it does not exist.
    '''
    if (os.path.isdir(path) == False):
        os.mkdir(path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ANALYZE the RSS images')
    parser.add_argument("nsimul",
                        help="Number of simulations",type=int)
    parser.add_argument("initializer",
                        help="Initializer of simulations",type=int)
    parser.add_argument('VPH',
                        help="VPH used during the observations")
    parser.add_argument('target',
                        help="Name of the target")
    ##
    parser.add_argument("--Halpha", help = "Analyze the Halpha line",
                        action="store_true")
    parser.add_argument("--NII6584", help = "Analyze the NII6584 line",
                        action="store_true")
    parser.add_argument("--analyze", help = "Analyze the corresponding line",
                        action="store_true")
    parser.add_argument("--plots", help = "Create and save the figures",
                        action="store_true")
    args = parser.parse_args()
    
    #####################################

    np.random.seed(70)
    
    nsimul = int(args.nsimul)
    h = int(args.initializer)
    
    VPH = str(args.VPH)
    target = str(args.target)
    
    ###########
        
    if args.Halpha:
        name = 'Halpha'
        print('.............................')
        print('--------Analyze the ' + str(name) + ' line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/' + str(name) + '/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_c.py -s results_SIMUL/' + str(target) + '_' + str(VPH) + '_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 5 -w 6563 -k -O ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -o ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf -z 0.003465 -v -LW1 6553 -LW2 6573 -CW1 6495 -CW2 6540 -PW1 6500 -PW2 6650')
                os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/' + str(name) + '/')
                os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/' + str(name) + '/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/' + str(name) + '/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/' + str(name) + '/plots/'
                check_directory(file_path)
                
            
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 300 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 6E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut -10 --max-cut 550 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1030 --max-cut 1080 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 22 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
    if args.NII6584:
        name = 'NII6584'
        print('.............................')
        print('--------Analyze the ' + str(name) + ' line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/' + str(name) + '/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_c.py -s results_SIMUL/' + str(target) + '_' + str(VPH) + '_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 3 -w 6584 -k -O ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -o ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf -z 0.003465 -v -LW1 6580 -LW2 6590 -CW1 6495 -CW2 6540 -PW1 6500 -PW2 6650')
                os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/' + str(name) + '/')
                os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/' + str(name) + '/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/' + str(name) + '/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/' + str(name) + '/plots/'
                check_directory(file_path)
   
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 10 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut 10 --max-cut 100 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1060 --max-cut 1100 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 33 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
    
    
    
