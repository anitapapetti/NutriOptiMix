#!/bin/sh

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


echo "NutriOptiMix Project - Installer for Unix-like systems"

# go into app's directory
SCRIPT_DIRECTORY=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &>/dev/null && pwd )
cd $SCRIPT_DIRECTORY

# create venv (venv directory will be in current directory)
echo "Creating virtual environment..."
python3 -m venv venv

# activate new venv
source venv/bin/activate

# install dependencies
echo "Installing requirements..."
pip install -r requirements.txt

# deactivate venv
deactivate

# create launcher file
echo "Creating launcher file..."
echo "#!/bin/sh" > launcher
echo "cd $SCRIPT_DIRECTORY" >> launcher
echo "venv/bin/python3 main.py" >> launcher

# create soft link to launcher and save it in user's desktop
echo "Creating launcher soft link in user's desktop..."

LINK_PATH="$HOME/NutriOptiMix"
if [ -d "$HOME/Desktop" ]; then
    LINK_PATH="$HOME/Desktop/NutriOptiMix"
elif [ -d "$HOME/Scrivania" ]; then
    LINK_PATH="$HOME/Scrivania/NutriOptiMix"
else
    echo "Warning: could not find user's desktop. Launcher soft link will be created in user's home"
fi
ln -sf "$SCRIPT_DIRECTORY/launcher" "$LINK_PATH"
chmod +x launcher

echo "Installation complete"
echo "Execute NutriOptiMix app with: $LINK_PATH"