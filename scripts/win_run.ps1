$scriptDir = $PSScriptRoot
$projDir = Join-Path $scriptDir ".."

cd $projDir
.\venvMedia\Scripts\Activate.ps1
python -m src.main