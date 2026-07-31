# Author: Dr. Awanish Pratap Singh
param(
    [ValidateSet("english", "german", "all")]
    [string]$Language = "english",
    [string]$Source = "",
    [switch]$Strict,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot

if ($Language -eq "all" -and $Source) {
    throw "A custom -Source can only be used with one language."
}

$targets = switch ($Language) {
    "english" { @(@{ Language = "english"; Source = $(if ($Source) { $Source } else { "main.tex" }) }) }
    "german" { @(@{ Language = "german"; Source = $(if ($Source) { $Source } else { "main-de.tex" }) }) }
    "all" {
        @(
            @{ Language = "english"; Source = "main.tex" },
            @{ Language = "german"; Source = "main-de.tex" }
        )
    }
}

Push-Location $projectRoot

try {
    $xelatex = Get-Command xelatex -ErrorAction SilentlyContinue
    if (-not $xelatex -and -not $Clean) {
        throw "XeLaTeX was not found. Install TeX Live or MiKTeX and retry."
    }

    $validator = Join-Path $PSScriptRoot "validate_dfg_pdf.py"
    $python = Get-Command python -ErrorAction SilentlyContinue

    foreach ($target in $targets) {
        $targetLanguage = $target.Language
        $targetSource = $target.Source
        $sourcePath = Join-Path $projectRoot $targetSource
        $buildDir = Join-Path $projectRoot (Join-Path "build" $targetLanguage)

        if (-not (Test-Path -LiteralPath $sourcePath)) {
            throw "Source file not found: $sourcePath"
        }

        New-Item -ItemType Directory -Path $buildDir -Force | Out-Null

        if ($Clean) {
            Get-ChildItem -LiteralPath $buildDir -File |
                Where-Object Extension -In ".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk" |
                Remove-Item -Force
            continue
        }

        & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$targetSource"
        if ($LASTEXITCODE -ne 0) { throw "First XeLaTeX pass failed for $targetLanguage with exit code $LASTEXITCODE" }
        & xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$targetSource"
        if ($LASTEXITCODE -ne 0) { throw "Second XeLaTeX pass failed for $targetLanguage with exit code $LASTEXITCODE" }

        $pdfName = [System.IO.Path]::GetFileNameWithoutExtension($targetSource) + ".pdf"
        $pdfPath = Join-Path $buildDir $pdfName

        if ($python -and (Test-Path -LiteralPath $validator)) {
            $qaArgs = @($validator, $sourcePath, $pdfPath, "--language", $targetLanguage)
            if (-not $Strict) { $qaArgs += "--allow-guidance" }
            & python @qaArgs
            if ($LASTEXITCODE -ne 0) { throw "DFG QA failed for $targetLanguage with exit code $LASTEXITCODE" }
        } else {
            Write-Warning "Python validator was not run. Install Python 3 for automated QA."
        }

        Write-Host "Built $targetLanguage template: $pdfPath"
    }

    if ($Language -eq "all" -and $python) {
        & python (Join-Path $PSScriptRoot "check_language_parity.py") "main.tex" "main-de.tex"
        if ($LASTEXITCODE -ne 0) { throw "English/German structure parity check failed." }
    }
} finally {
    Pop-Location
}
