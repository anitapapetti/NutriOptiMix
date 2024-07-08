# Copyright: (c) 2024, Anita Papetti <anitapapetti.dev@gmail.com>
#
# This file is part of NutriOptiMix
#
# NutriOptiMix is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# NutriOptiMix is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NutriOptiMix.  If not, see <http://www.gnu.org/licenses/>.

Write-Host "********************************************"
Write-Host "NutriOptiMix Project - Installer for Windows"
Write-Host "********************************************"

# go into app's directory
Set-Location $PSScriptRoot

# create venv (venv directory will be in current directory)
Write-Host "Creating virtual environment..."
Write-Host " "
python -m venv venv

# activate new venv
venv\Scripts\activate

# install dependencies
Write-Host "Installing requirements..."
pip install -r requirements.txt

# deactivate venv
deactivate

Write-Host " "
Write-Host "Creating launcher files..."
# create execute file
New-Item -Path $PSScriptRoot -Type file -Name "executeGUI.ps1" -Force
"Set-Location $PSScriptRoot" > executeGUI.ps1
"$PSScriptRoot\venv\Scripts\python.exe $PSScriptRoot\main.py" >> executeGUI.ps1

# create launcher file
New-Item -Path $PSScriptRoot -Type file -Name "launcher.ps1" -Force
"PowerShell.exe -WindowStyle hidden $PSScriptRoot\executeGUI.ps1" > launcher.ps1

# create shortcut to launcher and save it in user's desktop
Write-Host "Creating launcher shortcut in user's Desktop..."
$ShortcutPath = [Environment]::GetFolderPath("Desktop") + "\NutriOptiMix.lnk"
$WScriptObj = New-Object -ComObject ("WScript.Shell")
$shortcut = $WscriptObj.CreateShortcut($ShortcutPath)
$shortcut.TargetPath = "$PSScriptRoot\launcher.ps1"
$shortcut.Save()

Write-Host " "
Write-Host "*****************************"
Write-Host "    Installation complete    "
Write-Host "*****************************"
Write-Host " "
Write-Host "To use NutriOptiMix: right-click on NutriOptiMix shortcut and select 'Execute with PowerShell'"
Write-Host " "
Write-Host "Press any key to exit"
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown');