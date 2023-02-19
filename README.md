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

## Examples and help with the codes

**1_simulations_reduction.py**: This file software has been employed to add Gaussian noise to the images taken with the MEGARA IFU instrument at GTC and automatically reduce the simulated data.

The following command will run all the steps of MEGARA DRP:

```bash
$ python 1_simulations_reduction.py --all
```

In case we are interested in running a particular step of MEGARA DRP (e.g., step 3: wavelength calibration), we can specify it as:
```bash
$ python 1_simulations_reduction.py --stage3
```

**2_lines_analysis.py**: This file software has been employed to analyze simulated reduced MEGARA data (RSS images) and generate the maps with the emission-line properties.

The following command shows an example of the [OIII]5007 emission-line analysis:

```bash
$ python 2_lines_analysis.py --OIII5007 --analyze
```
In this step the user must take into account additional parameters such as the redshift of the target, the wavelenght range required to fit the continuum and the emission line, and the minimum signal-to-noise ratio to perform the fit. The parameter _'plots'_ allows the user to create and save the figures.

```bash
$ python 2_lines_analysis.py --OIII5007 --analyze --plots
```
The analysis can be performed with more than one emission line (e.g., [OIII]5007 and Hbeta):

```bash
$ python 2_lines_analysis.py --OIII5007 --Hbeta --analyze --plots
```


**3_residuals.py**: This file software has been employed to compute both the median value of different parameters derived from the simulated MEGARA data, and the residuals (real data - median of the simulations).

In this case, the user should just specify the emission line of interest (e.g., [OIII]5007):
```bash
$ python 3_residuals.py --OIII5007 
```

**4_uncertainties.py**: This file software has been employed to compute the uncertainties of different parameters derived from the simulated MEGARA data.

In this case, the user should just specify the emission line of interest (e.g., [OIII]5007):
```bash
$ python 4_uncertainties.py --OIII5007 
```
