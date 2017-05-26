[![Join the FISSA chat](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/rochefort-lab/fissa)
[![Shippable](https://img.shields.io/shippable/56391d7a1895ca4474227917.svg)](https://app.shippable.com/projects/56391d7a1895ca4474227917)

FISSA
=====

FISSA (Fast Image Source Separation Analysis) is a Python library for extracting
somatic signals from 2-photon calcium imaging data.
It requires images in tiff format as well as predefined ROIs around somas.

FISSA offers the use of ICA and several NMF algorithms to do so, as well as
ROI manipulation routines for generating neuropil ROIs.

Currently, FISSA is only available for Python 2.7, and has been tested on
Ubuntu 15.04 and on Windows 7 with the
[WinPython 2.7.10.3](http://sourceforge.net/projects/winpython/files/WinPython_2.7/2.7.10.3/)
distribution.

If you encounter a specific problem please
[open a new issue](https://github.com/rochefort-lab/fissa/issues/new).
For general discussion and help with installation or setup, please see the
[Gitter chat](https://gitter.im/rochefort-lab/fissa).


Installation
------------

### Installation on Linux

Before installing FISSA, you will need to make sure you have all of its dependencies
(and the dependencies of its dependencies) installed.

Here we will outline how to do all of these steps, assuming you already have both
Python 2.7 and pip installed. It is highly likely that your Linux distribution ships with these.

#### Dependencies of dependencies

* To install the developmental version of FISSA, you will need to have
  [Git](https://git-scm.com/download/linux) installed.

* [scipy](https://pypi.python.org/pypi/scipy/) requires a
  [Fortran compiler and BLAS/LAPACK/ATLAS](http://www.scipy.org/scipylib/building/linux.html#installation-from-source).

* [shapely](https://pypi.python.org/pypi/Shapely) requires GEOS.

These packages can be installed on *Debian/Ubuntu* with the following shell
commands.

```bash
sudo apt-get update
sudo apt-get install git
sudo apt-get install gfortran libopenblas-dev liblapack-dev libatlas-dev libatlas-base-dev
sudo apt-get install libgeos-dev
```

#### Installation into user site-packages

You can download the package source from GitHub, and then install FISSA and its
dependencies as follows:

```bash
git clone https://github.com/rochefort-lab/fissa.git
pip install --user -r fissa/requirements_first.txt
pip install --user -r fissa/requirements.txt
pip install --user -e fissa
```

The `--user` flag ensures the packages are installed into your usr site-packages
folder.

To generate the plots in the iPython Notebooks, you will also need to install
the optional dependencies:

```bash
pip install --user -r fissa/requirements_plots.txt
```

### Installation on Windows

These instructions for installing FISSA on Windows assume you are using
WinPython for your Python environment, and has been tested with
WinPython 2.7.10.3, available from
<http://sourceforge.net/projects/winpython/files/WinPython_2.7/2.7.10.3/>.

(Another option is using Anaconda, from
<https://www.continuum.io/why-anaconda>, but FISSA has not been tested
in this environment yet.)

From the `WinPython Command Prompt.exe`, which can be found in the WinPython
installation folder, you can download the FISSA source from GitHub and install
most of its dependencies as follows:

```
git clone https://github.com/rochefort-lab/fissa.git
pip install -r fissa/requirements_first.txt
pip install -r fissa/requirements_windows.txt
pip install -r fissa/requirements_plots.txt
```

If you don't have Git installed globally, you can't do all these steps in the
WinPython command prompt.
You can instead download a zipped copy of FISSA from GitHub and skip the first
step.

Next, you need to download a windows specific version of shapely from
<http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely>.
Browse to where you downloaded the wheel (which should be named something like
`Shapely‑1.5.13‑cp27‑none‑win_amd64.whl`) and pip install it using the WinPython
command prompt:

```
pip install filename
```

Finally, if everything above worked well, you can install FISSA as
follows (from the folder above fissa).

```
pip install -e fissa
```

Folder Structure
----------------

### examples
Contains example code. You can load the notebooks as .ipynb directly in GitHub,
or on your system if you know how to use ipython notebooks
(http://ipython.org/ipython-doc/stable/notebook/index.html).
You can open the .html pages instead.

For a basic tutorial of using FISSA see ```Basic usage.ipynb``` or ```Basic usage.html```. An example workflow is shown in ```basic_usage.py```.

For integrating FISSA with another toolbox (in this case SIMA)
see ```SIMA example.ipynb``` or ```SIMA example.html```.


### exampleData
Contains example data. It a zipfile with region of interests from ImageJ.
It also contains three tiff stacks, which have been downsampled and cropped
from full data from the Rochefort lab.

### fissa
Contains the toolbox.


Citing FISSA
------------

If you use FISSA for your research, please cite the following paper
in any resulting publications:

_Paper in preparation_


License
-------

Unless otherwise stated in individual files, all code is
Copyright (c) 2015, Sander Keemink, Scott Lowe, and Nathalie Rochefort.
All rights reserved.

This program is currently closed source; you can not redistribute it unless
under the express permission of one of the copyright holders.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
