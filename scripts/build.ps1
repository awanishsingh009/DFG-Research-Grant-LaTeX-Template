param(
    [ValidateSet("", "english", "german", "all")][string]$Language = "",
    [ValidateSet("xelatex", "lualatex", "pdflatex")][string]$Engine = "xelatex",
    [string]$Source = "",
    [switch]$Strict,
    [switch]$Portable
)
$ErrorActionPreference = "Stop"
$pythonCommand = $null
foreach ($candidate in @("python", "python3", "py")) {
    $resolved = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($resolved) {
        & $resolved.Source -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" 2>$null
        if ($LASTEXITCODE -eq 0) { $pythonCommand = $resolved.Source; break }
    }
}
if (-not $pythonCommand) { throw "Python 3.10+ is required for this helper. Install it or compile directly in your TeX editor. See docs/SETUP.md." }
$buildArgs = @((Join-Path $PSScriptRoot "build.py"), "--engine", $Engine)
if ($Language) { $buildArgs += @("--language", $Language) }
if ($Source) { $buildArgs += @("--source", $Source) }
if ($Strict) { $buildArgs += "--release" }
if ($Portable) { $buildArgs += "--portable" }
& $pythonCommand @buildArgs
exit $LASTEXITCODE
