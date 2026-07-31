# Author: Dr. Awanish Pratap Singh
param(
    [ValidateSet("english", "german", "all")]
    [string]$Language = "english",
    [ValidateSet("xelatex", "pdflatex")]
    [string]$Engine = "xelatex",
    [string]$Source = "",
    [switch]$Strict,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot

if ($Language -eq "all" -and $Source) {
    throw "A custom -Source can only be used with one language."
}
if ($Strict -and $Engine -eq "pdflatex") {
    throw "Strict submission builds require XeLaTeX and Arial; pdfLaTeX is drafting-only."
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
    $compiler = Get-Command $Engine -ErrorAction SilentlyContinue
    if (-not $compiler -and -not $Clean) {
        throw "$Engine was not found. Install TeX Live or MiKTeX and retry."
    }

    $validator = Join-Path $PSScriptRoot "validate_dfg_pdf.py"
    $python = Get-Command python -ErrorAction SilentlyContinue

    foreach ($target in $targets) {
        $targetLanguage = $target.Language
        $targetSource = $target.Source
        $sourcePath = Join-Path $projectRoot $targetSource
        $buildRoot = if ($Engine -eq "xelatex") { "build" } else { Join-Path "build" "pdflatex" }
        $buildDir = Join-Path $projectRoot (Join-Path $buildRoot $targetLanguage)

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

        & $Engine -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$targetSource"
        if ($LASTEXITCODE -ne 0) { throw "First $Engine pass failed for $targetLanguage with exit code $LASTEXITCODE" }
        & $Engine -interaction=nonstopmode -halt-on-error -file-line-error -output-directory="$buildDir" "$targetSource"
        if ($LASTEXITCODE -ne 0) { throw "Second $Engine pass failed for $targetLanguage with exit code $LASTEXITCODE" }

        $pdfName = [System.IO.Path]::GetFileNameWithoutExtension($targetSource) + ".pdf"
        $pdfPath = Join-Path $buildDir $pdfName

        if ($python -and (Test-Path -LiteralPath $validator)) {
            $qaArgs = @($validator, $sourcePath, $pdfPath, "--language", $targetLanguage)
            if (-not $Strict) { $qaArgs += "--allow-guidance" }
            if ($Engine -eq "pdflatex") { $qaArgs += "--allow-draft-font" }
            & python @qaArgs
            if ($LASTEXITCODE -ne 0) { throw "DFG QA failed for $targetLanguage with exit code $LASTEXITCODE" }
        } else {
            Write-Warning "Python validator was not run. Install Python 3 for automated QA."
        }

        Write-Host "Built $targetLanguage template with ${Engine}: $pdfPath"
    }

    if ($Language -eq "all" -and $python) {
        & python (Join-Path $PSScriptRoot "check_language_parity.py") "main.tex" "main-de.tex"
        if ($LASTEXITCODE -ne 0) { throw "English/German structure parity check failed." }
    }
} finally {
    Pop-Location
}
