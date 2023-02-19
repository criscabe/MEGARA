# MEGARA

This is the source code repository for the python routines employed to automatically reduce and analyze the data from the MEGARA IFU instrument at GTC, 
including the method developed to estimate the random uncertainties associated to the emission line properties.

This software was created by C. Cabello as part of her thesis work, developed under the supervision of N. Cardiel and J. Gallego, at the Departamento de Física de la Tierra y Astrofísica of the Universidad Complutense de Madrid.

The program is first mentioned in Cabello, C. - PhD Thesis 2023, and Cabello et al. 2023 in prep.

Maintainer: Cristina Cabello, criscabe@ucm.es 

Webpage (source): https://github.com/criscabe/MEGARA

<br/><br/>


<p align="center">
<img src="images/MEGARA_pic.png" width="80%"></a>
</p>


--------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------


**1) 1_simulations_reduction.py**: Add Gaussian noise to the images taken with the MEGARA IFU instrument at GTC and automatically reduce the simulated data.

The following command will run all the steps of MEGARA DRP:

_$ python 1_simulations_reduction.py --all_

In case we are interested in running a particular step of MEGARA DRP (e.g., step 3: wavelength calibration), we can specify it as:

_$ python 1_simulations_reduction.py --stage3_


2) Analyze simulated reduced data

3) Compute the median of simulations and residuals

4) Compute the uncertainties of different parameters
