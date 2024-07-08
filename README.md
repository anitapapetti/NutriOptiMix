# NutriOptiMix
NutriOptiMix is a decision support system for enteral nutrition in intensive care units (ICU), meant for use by ICU medical doctors.
NutriOptiMix will help you find the optimal mix of enteral nutrition formulas and solutions for your patient, taylored to their needs.

## Use NutriOptiMix
At the moment, NutriOptiMix is published only on GitHub.
Please, download the project files from GitHub and execute the installer file. 

In Windows, right-click [installer-windows.ps1](installer-windows.ps1) and select "Execute with PowerShell". 

In Unix-like systems, like Linux or macOS, open a terminal window and execute [installer-unix.sh](installer-unix.sh) with `sh` command.
Linux users should also have package [xclip](https://github.com/astrand/xclip) or [xsel](https://github.com/kfish/xsel) installed, if they wish to copy results to clipboard.

## External libraries
NutriOptiMix is written in Python 3. 
External libraries used are:
* standard Python library [Tkinter](https://github.com/python/cpython/blob/3.11/Lib/tkinter/__init__.py) (except rare exceptions, it should have been installed with Python interpreter);
* [Pandas](https://github.com/pandas-dev/pandas) library;
* [Python-MIP](https://github.com/coin-or/python-mip) package.

Note: for devices with ARM processors using macOS, [Python-MIP](https://github.com/coin-or/python-mip) package should be supported following release 1.16.0, which supposedly was to be released in July 2024.

## Contributing
At this moment, I'm planning to continue developing NutriOptiMix without external contributions.
Unfortunately, I don't have the resources to maintain an active project now.
This may change in the future.

## Author
NutriOptiMix was created by [Anita Papetti](https://github.com/anitapapetti) in 2024.

## License
GNU General Public License v3.0 or later.

See [COPYING](COPYING.txt) to read the full text.
