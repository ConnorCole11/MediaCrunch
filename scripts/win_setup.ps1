$scriptDir = $PSScriptRoot
$projDir = Join-Path $scriptDir ".."

cd $projDir
rm -r venvMedia

python -m venv venvMedia
.\venvMedia\Scripts\Activate.ps1
pip install -r requirements.txt