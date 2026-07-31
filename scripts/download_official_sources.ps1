# Author: Dr. Awanish Pratap Singh
param(
    [string]$Destination = "official-dfg-documents"
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$destinationPath = Join-Path $projectRoot $Destination
New-Item -ItemType Directory -Path $destinationPath -Force | Out-Null

$sources = @(
    @{ Name = "1-91-en.pdf"; Uri = "https://www.dfg.de/resource/blob/167386/1-91-en.pdf" },
    @{ Name = "10-206-en.pdf"; Uri = "https://www.dfg.de/resource/blob/167422/10-206-en.pdf" },
    @{ Name = "50-01-en.pdf"; Uri = "https://www.dfg.de/resource/blob/168072/50-01-en.pdf" },
    @{ Name = "52-01-en.pdf"; Uri = "https://www.dfg.de/resource/blob/168130/52-01-en.pdf" },
    @{ Name = "52-14-en.pdf"; Uri = "https://www.dfg.de/resource/blob/168182/52-14-en.pdf" },
    @{ Name = "53-01-en-elan.rtf"; Uri = "https://www.dfg.de/resource/blob/168206/53-01-en-elan.rtf" },
    @{ Name = "53-200-en-elan.rtf"; Uri = "https://www.dfg.de/resource/blob/168274/53-200-en-elan.rtf" },
    @{ Name = "54-01-en.pdf"; Uri = "https://www.dfg.de/resource/blob/168314/54-01-en.pdf" },
    @{ Name = "54-020-en.pdf"; Uri = "https://www.dfg.de/resource/blob/331878/54-020-en.pdf" },
    @{ Name = "55-03-de.pdf"; Uri = "https://www.dfg.de/resource/blob/168402/55-03-de.pdf" },
    @{ Name = "55-04-en.pdf"; Uri = "https://www.dfg.de/resource/blob/168406/55-04-en.pdf" },
    @{ Name = "form-changes.pdf"; Uri = "https://www.dfg.de/resource/blob/334100/sachbeihilfe-info-vordrucksaenderungen.pdf" }
)

foreach ($source in $sources) {
    $outputPath = Join-Path $destinationPath $source.Name
    Write-Host "Downloading $($source.Name)"
    Invoke-WebRequest -Uri $source.Uri -OutFile $outputPath
}

$hashLines = Get-ChildItem -LiteralPath $destinationPath -File |
    Where-Object Name -ne "README.md" |
    Sort-Object Name |
    ForEach-Object {
        $hash = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        "$hash  $($_.Name)"
    }

$hashLines | Set-Content -LiteralPath (Join-Path $destinationPath "SHA256SUMS.sha256") -Encoding utf8
Write-Host "Official-source snapshot written to: $destinationPath"
