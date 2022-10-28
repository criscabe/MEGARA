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


def check_directory(path):
    '''Create a directory if it does not exist.
    '''
    if (os.path.isdir(path) == False):
        os.mkdir(path)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ANALYZE the RSS images')
    parser.add_argument("--OIII5007", help = "Analyze the OIII5007 line",
                        action="store_true")
    parser.add_argument("--OIII4959", help = "Analyze the OIII4959 line",
                        action="store_true")
    parser.add_argument("--OIII4363", help = "Analyze the OIII4363 line",
                        action="store_true")
    parser.add_argument("--Hbeta", help = "Analyze the Hbeta line",
                        action="store_true")
    parser.add_argument("--Hgamma", help = "Analyze the Hgamma line",
                        action="store_true")
    parser.add_argument("--HeI4471", help = "Analyze the HeI4471 line",
                        action="store_true")
    parser.add_argument("--analyze", help = "Analyze the corresponding line",
                        action="store_true")
    parser.add_argument("--plots", help = "Create and save the figures",
                        action="store_true")

    args = parser.parse_args()
    
    
    
    # number of simulations
    nsimul = 50


    h = 0
    
    
    if args.OIII5007:
        print('.............................')
        print('--------Analyze the OIII5007 line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/OIII5007/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 5 -w 5007 -k -O OIII5007_UM461_SIMUL_' + str(h+j+1) + '.fits -o OIII5007_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 5005 -LW2 5010 -CW1 5020 -CW2 5030 -PW1 5000 -PW2 5050')
                os.system('mv OIII5007_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/OIII5007/')
                os.system('mv OIII5007_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/OIII5007/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/OIII5007/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/OIII5007/plots/'
                check_directory(file_path)
                
                
                name = 'OIII5007'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 400 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 6E-16 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 6E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut -10 --max-cut 500 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1040 --max-cut 1090 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 32 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 22 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
            
            

    if args.OIII4959:
        print('.............................')
        print('--------Analyze the OIII4959 line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/OIII4959/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 5 -w 4959 -k -O OIII4959_UM461_SIMUL_' + str(h+j+1) + '.fits -o OIII4959_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 4949 -LW2 4969 -CW1 4970 -CW2 4980 -PW1 4950 -PW2 5000')
                os.system('mv OIII4959_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/OIII4959/')
                os.system('mv OIII4959_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/OIII4959/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/OIII4959/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/OIII4959/plots/'
                check_directory(file_path)
                
                
                
                name = 'OIII4959'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 400 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 3E-16 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 9E-15 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 3E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 9E-15 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut -10 --max-cut 700 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1040 --max-cut 1090 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 32 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 18 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
            
            

    if args.OIII4363:
        print('.............................')
        print('--------Analyze the OIII4363 line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/OIII4363/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 3 -w 4363 -k -O OIII4363_UM461_SIMUL_' + str(h+j+1) + '.fits -o OIII4363_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 4353 -LW2 4373 -CW1 4367 -CW2 4374 -PW1 4350 -PW2 4400')
                os.system('mv OIII4363_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/OIII4363/')
                os.system('mv OIII4363_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/OIII4363/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/OIII4363/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/OIII4363/plots/'
                check_directory(file_path)
                
                
                
                name = 'OIII4363'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 150 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut -10 --max-cut 50 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1040 --max-cut 1110 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 42 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 38 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
            
            
            
    
    if args.Hbeta:
        print('.............................')
        print('--------Analyze the Hbeta line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/Hbeta/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 5 -w 4861 -k -O Hbeta_UM461_SIMUL_' + str(h+j+1) + '.fits -o Hbeta_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 4851 -LW2 4871 -CW1 4870 -CW2 4890 -PW1 4850 -PW2 4900')
                os.system('mv Hbeta_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/Hbeta/')
                os.system('mv Hbeta_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/Hbeta/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/Hbeta/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')

            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/Hbeta/plots/'
                check_directory(file_path)
                


                name = 'Hbeta'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 150 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 8E-17 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 8E-17 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut 30 --max-cut 170 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1070 --max-cut 1120 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 38 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 33 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
            
            
            
            
    if args.Hgamma:
        print('.............................')
        print('--------Analyze the Hgamma line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/Hgamma/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 3 -w 4340 -k -O Hgamma_UM461_SIMUL_' + str(h+j+1) + '.fits -o Hgamma_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 4330 -LW2 4350 -CW1 4351 -CW2 4360 -PW1 4300 -PW2 4390')
                os.system('mv Hgamma_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/Hgamma/')
                os.system('mv Hgamma_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/Hgamma/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/Hgamma/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')                

            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/Hgamma/plots/'
                check_directory(file_path)

            
            
                name = 'Hgamma'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 150 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut 10 --max-cut 100 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1070 --max-cut 1140 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 38 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 33 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
                
                
                
        
    if args.HeI4471:
        print('.............................')
        print('--------Analyze the HeI4471 line--------')
        print('.............................')
        
        file_path = 'results_SIMUL/LINES/HeI4471/'
        check_directory(file_path)
        
        for j in range(nsimul):
            
            if args.analyze:
                print('......... ANALYSIS ..........')
                os.system('python tools/analyze_rss_v2.py -s results_SIMUL/UM461_LRB_SIMUL_' + str(h+j+1) + '.fits -f 0 -S 3 -w 4471 -k -O HeI4471_UM461_SIMUL_' + str(h+j+1) + '.fits -o HeI4471_UM461_SIMUL_' + str(h+j+1) + '.pdf -z 0.00347 -v -LW1 4461 -LW2 4481 -CW1 4476 -CW2 4486 -PW1 4460 -PW2 4500')
                os.system('mv HeI4471_UM461_SIMUL_' + str(h+j+1) + '.pdf results_SIMUL/LINES/HeI4471/')
                os.system('mv HeI4471_UM461_SIMUL_' + str(h+j+1) + '.fits results_SIMUL/LINES/HeI4471/')
                os.system('mv LINE_FIT_region.pdf results_SIMUL/LINES/HeI4471/LINE_FIT_region_SIMUL_' + str(h+j+1) + '.pdf')
                
            if args.plots:
                print('......... PLOTS ..........')
            
                file_path = 'results_SIMUL/LINES/HeI4471/plots/'
                check_directory(file_path)
                
                
                
                name = 'HeI4471'
                
                # SNR # 3 S/N at the peak of the line
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 4  --min-cut 0 --max-cut 50 --title ' + str(name) + '_SNR --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_SNR_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXD # 4 Flux from window_data - window_continuum
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 5  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 6 Flux from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-16 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_SIMUL_' + str(h+j+1) + '.pdf')
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 7  --min-cut 0.00000 --max-cut 1E-14 --title ' + str(name) + '_FLUX_FIT --label "erg/s/cm2" --wcs-grid --stretch log')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_flux_fit_log_SIMUL_' + str(h+j+1) + '.pdf')
                # FLUXF # 7 EW from best-fitting function(s)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 8  --min-cut 0 --max-cut 10 --title ' + str(name) + '_EW --label "A" --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_EW_SIMUL_' + str(h+j+1) + '.pdf')
                # H1KS # 16 velocity in km/s from H1 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 17  --min-cut 1070 --max-cut 1140 --label "km/s" --title ' + str(name) + '_velocity --colormap jet --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_velocity_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KS # 17 sigma in km/s from H2 (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 18  --min-cut 22 --max-cut 38 --label "km/s" --title ' + str(name) + '_sigma --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_SIMUL_' + str(h+j+1) + '.pdf')
                # H2KLC # 18 sigma in km/s from H2 corrected from instrumental sigma (1st g)
                os.system('python N/visualization_v2.py results_SIMUL/LINES/' + str(name) + '/' + str(name) + '_UM461_SIMUL_' + str(h+j+1) + '.fits -c 19  --min-cut 10 --max-cut 33 --label "km/s" --title ' + str(name) + '_sigma_corrected --wcs-grid')
                os.system('mv visualization_map.pdf results_SIMUL/LINES/' + str(name) + '/plots/' + str(name) + '_sigma_corrected_SIMUL_' + str(h+j+1) + '.pdf')
    
    
    
    
    
    

