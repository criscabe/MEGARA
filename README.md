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

### Examples and help with the codes

**[1_simulations_reduction.py](https://github.com/criscabe/MEGARA/blob/main/code/1_simulations_reduction.py)**: This file software has been employed to add Gaussian noise to the images taken with the MEGARA IFU instrument at GTC and automatically reduce the simulated data.

The help function will provide information about the required and optional arguments:

```bash
$  python 1_simulations_reduction.py -h                       
usage: 1_simulations_reduction.py [-h] [--stage0] [--stage1] [--stage2]
                                  [--stage3] [--stage4] [--stage5] [--stage6]
                                  [--stage7] [--stage8] [--all]
                                  nsimul initializer VPH target OB

Run MEGARA DRP

positional arguments:
  nsimul       Number of simulations
  initializer  Initializer of simulations
  VPH          VPH used during the observations
  target       Name of the target
  OB           Observing Block

optional arguments:
  -h, --help   show this help message and exit
  --stage0     Run step 0: BIAS
  --stage1     Run step 1: TraceMap
  --stage2     Run step 2: ModelMap
  --stage3     Run step 3: Wavelength calibration
  --stage4     Run step 4: FiberFlat
  --stage5     Run step 5: TwilightFlat
  --stage6     Run step 6: LCB adquisition
  --stage7     Run step 7: Standard Star
  --stage8     Run step 8: Reduce LCB
  --all        Run all the steps of MEGARA DRP
  ```

The following command will run all the steps of MEGARA DRP performing 100 simulations on data taken with the LRR VPH:
  
```bash
$ python 1_simulations_reduction.py 100 0 LRR target_name ob1 --all
```

The user must replace _'target_name'_ for the name of the target, and _'ob1'_ for the observing block ID that is being reduced in the MEGARA DRP step 8. 

In case the user is interested in running a particular step of MEGARA DRP (e.g., step 3: wavelength calibration), it should be specified as:
```bash
$ python 1_simulations_reduction.py 100 0 LRR target_name ob1 --stage3
```
- - - - - - - - - - - - -

**[2_lines_analysis.py](https://github.com/criscabe/MEGARA/blob/main/code/2_lines_analysis.py)**: This file software has been employed to analyze simulated reduced MEGARA data (RSS images) and generate the maps with the emission-line properties.

The help function will provide information about the required and optional arguments:
```bash
$ python 2_lines_analysis.py -h
usage: 2_lines_analysis.py [-h] [-LINE LINE] [--analyze] [--plots]
                           [-f {0,1,2}] [-S S] [-w W] [-z Z] [-LW1 LW1]
                           [-LW2 LW2] [-CW1 CW1] [-CW2 CW2] [-PW1 PW1]
                           [-PW2 PW2]
                           nsimul initializer VPH target

ANALYZE the RSS images

positional arguments:
  nsimul       Number of simulations
  initializer  Initializer of simulations
  VPH          VPH used during the observations
  target       Name of the target

optional arguments:
  -h, --help   show this help message and exit
  -LINE LINE   Name of the emission line
  --analyze    Analyze the corresponding line
  --plots      Create and save the figures
  -f {0,1,2}   Fitting function (0=gauss_hermite, 1=gauss, 2=double_gauss)
  -S S         Mininum Signal-to-noise ratio in each spaxel
  -w W         Central rest-frame wavelength of the emission line (AA)
  -z Z         Redshift of the target
  -LW1 LW1     Lower rest-frame wavelength (AA) for the emission-line fitting
  -LW2 LW2     Upper rest-frame wavelength (AA) for the emission-line fitting
  -CW1 CW1     Lower rest-frame wavelength (AA) for the continuum fitting
  -CW2 CW2     Upper rest-frame wavelength (AA) for the continuum fitting
  -PW1 PW1     Lower (observed) wavelength (AA) for the plot
  -PW2 PW2     Upper (observed) wavelength (AA) for the plot

```
The following command shows an example of the Hα emission-line analysis (100 simulated images, LRR VPH):

```bash
$ python 2_lines_analysis.py 100 0 LRR target_name -LINE Halpha  --analyze 
-f 0 -S 10 -w 6563 -z 0.003465 -LW1 6553 -LW2 6573 -CW1 6495 -CW2 6540 -PW1 6500 -PW2 6650
```
The parameter _'plots'_ allows the user to create and save the maps of the emission-line properties (S/N, Flux, EW, velocity, velocity dispersion). The scale of each figure will be setted in the terminal during the first iteration of the simulated images. Warning: to avoid the generation of multiple (and maybe unnecessary) images, the number of simulations can be reduced to 2-5 in this step.

```bash
$  python 2_lines_analysis.py 5 0 LRR galaxy_name -LINE Halpha --plots
```

- - - - - - - - - - - - -

**[3_residuals.py](https://github.com/criscabe/MEGARA/blob/main/code/3_residuals.py)**: This file software has been employed to compute both the median value of different parameters derived from the simulated MEGARA data, and the residuals (real data - median of the simulations).

In this case, the user should just specify the emission line of interest (e.g., [OIII]5007):
```bash
$ python 3_residuals.py --OIII5007 
```
- - - - - - - - - - - - -

**[4_uncertainties.py](https://github.com/criscabe/MEGARA/blob/main/code/4_uncertainties.py)**: This file software has been employed to compute the uncertainties of different parameters derived from the simulated MEGARA data.

In this case, the user should just specify the emission line of interest (e.g., [OIII]5007):
```bash
$ python 4_uncertainties.py --OIII5007 
```
