#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJ_DIR=$SCRIPT_DIR/..

cd $PROJ_DIR
rm -rf venvMedia

python3.13 -m venv venvMedia
source venvMedia/bin/activate

pip install -r requirements.txt
deactivate