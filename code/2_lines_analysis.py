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
import cmd

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
    parser.add_argument('-LINE', help = "Name of the emission line", type=str)
    parser.add_argument("--analyze", help = "Analyze the corresponding line",
                        action="store_true")
    parser.add_argument("--plots", help = "Create and save the figures",
                        action="store_true")
    ##
    parser.add_argument('-f', default=0, choices=[0,1,2], help='Fitting function (0=gauss_hermite, 1=gauss, 2=double_gauss)', type=int)
    parser.add_argument('-S', default=5, help='Mininum Signal-to-noise ratio in each spaxel', type=float)
    parser.add_argument('-w', help='Central rest-frame wavelength of the emission line (AA)',
                        type=float)
    parser.add_argument('-z', help='Redshift of the target', type=float)
    parser.add_argument('-LW1', help='Lower rest-frame wavelength (AA) for the emission-line fitting',
                        type=float)
    parser.add_argument('-LW2', help='Upper rest-frame wavelength (AA) for the emission-line fitting',
                        type=float)
    parser.add_argument('-CW1', help='Lower rest-frame wavelength (AA) for the continuum fitting',
                        type=float)
    parser.add_argument('-CW2', help='Upper rest-frame wavelength (AA) for the continuum fitting',
                        type=float)
    parser.add_argument('-PW1', help='Lower (observed) wavelength (AA) for the plot',
                        type=float)
    parser.add_argument('-PW2', help='Upper (observed) wavelength (AA) for the plot',
                        type=float)

    args = parser.parse_args()
    
    #####################################

    np.random.seed(70)
    
    nsimul = int(args.nsimul)
    h = int(args.initializer)
    
    VPH = str(args.VPH)
    target = str(args.target)
    
    f = args.f
    snr = args.S
    w = args.w
    z = args.z
    lw1= args.LW1
    lw2= args.LW2
    cw1 = args.CW1
    cw2 = args.CW2
    pw1 = args.PW1
    pw2 = args.PW2

    
    ###########
        
    
    name = str(args.LINE)
    print('.............................')
    print('--------Analyze the ' + str(name) + ' line--------')
    print('.............................')
        
    file_path = 'results_SIMUL/LINES/' + str(name) + '/'
    check_directory(file_path)
        
    for j in range(nsimul):
        if args.analyze:
            print('......... ANALYSIS ..........')
            os.system('python tools/analyze_rss_c.py -s results_SIMUL/' + str(target) + '_' + str(VPH) + '_SIMUL_' + str(h+j+1) + '.fits -f ' + str(f) + ' -S ' + str(snr) + ' -w ' + str(w) + ' -k -O ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -o ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf -z ' + str(z) + ' -v -LW1 ' + str(lw1) + ' -LW2 ' + str(lw2) + ' -CW1 ' + str(cw1) + ' -CW2 ' + str(cw2) + ' -PW1 ' + str(pw1) + ' -PW2 ' + str(pw2) + '')
            os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/' + str(name) + '/')
            os.system('mv ' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/' + str(name) + '/')
            os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/' + str(name) + '/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
        if args.plots:
            print('......... PLOTS ..........')
            
            file_path = 'results_SIMUL/LINES/' + str(name) + '/plots/'
            check_directory(file_path)
                

            
            # SNR # 3 S/N at the peak of the line
            if j == 0:
                mincut = input("mincut S/N at the peak of the line: ")
                maxcut = input("maxcut S/N at the peak of the line: ")
            
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title ' + str(name) + '_SNR --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
            
            # FLUXF # 6 Flux from best-fitting function(s)
            if j == 0:
                mincut = input("mincut Flux (cgs): ")
                maxcut = input("maxcut Flux (cgs): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
            
            # FLUXF # 7 EW from best-fitting function(s)
            if j == 0:
                mincut = input("mincut EW (A): ")
                maxcut = input("maxcut EW (A): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --title ' + str(name) + '_EW --label "A" --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
            
            # H1KS # 16 velocity in km/s from H1 (1st g)
            if j == 0:
                mincut = input("mincut velocity (km/s): ")
                maxcut = input("maxcut velocity (km/s): ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
            
            # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
            if j == 0:
                mincut = input("mincut sigma (km/s) corrected from instrumental sigma: ")
                maxcut = input("maxcut sigma (km/s) corrected from instrumental sigma: ")
            os.system('python N/visualization_c.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_' + str(target) + '_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut ' + str(mincut) + ' --max-cut ' + str(maxcut) + ' --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
            os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
    
