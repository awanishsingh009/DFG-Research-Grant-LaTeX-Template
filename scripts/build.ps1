# Author: Dr. Awanish Pratap Singh
param(
    [string]$Source = "main.tex",
    [switch]$Strict,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$buildDir = Join-Path $projectRoot "build"
$sourcePath = Join-Path $projectRoot $Source

if (-not (Test-Path -LiteralPath $sourcePath)) {
    throw "Source file not found: $sourcePath"
}

New-Item -ItemType Directory -Path $buildDir -Force | Out-Null
Push-Location $projectRoot

try {
    $xelatex = Get-Command xelatex -ErrorAction SilentlyContinue

    if ($Clean) {
        Get-ChildItem -LiteralPath $buildDir -File |
            Where-Object Extension -In ".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk" |
            Remove-Item -Force
        exit 0
    }

    $built = $false
    if ($xelatex) {
        & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$Source"
        if ($LASTEXITCODE -ne 0) { throw "First XeLaTeX pass failed with exit code $LASTEXITCODE" }
        & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$Source"
        if ($LASTEXITCODE -ne 0) { throw "Second XeLaTeX pass failed with exit code $LASTEXITCODE" }
        $built = $true
    }

    if (-not $built) {
        throw "XeLaTeX was not found. Install TeX Live or MiKTeX and retry."
    }

    $pdfName = [System.IO.Path]::GetFileNameWithoutExtension($Source) + ".pdf"
    $pdfPath = Join-Path $buildDir $pdfName
    $validator = Join-Path $PSScriptRoot "validate_dfg_pdf.py"
    $python = Get-Command python -ErrorAction SilentlyContinue

    if ($python -and (Test-Path -LiteralPath $validator)) {
        $qaArgs = @($validator, $sourcePath, $pdfPath)
        if (-not $Strict) { $qaArgs += "--allow-guidance" }
        & python @qaArgs
        if ($LASTEXITCODE -ne 0) { throw "DFG QA failed with exit code $LASTEXITCODE" }
    } else {
        Write-Warning "Python validator was not run. Install Python 3 for automated QA."
    }

    Write-Host "Built: $pdfPath"
} finally {
    Pop-Location
}
