[CmdletBinding()]
param(
    [string]$RepositoryRoot = (Join-Path $PSScriptRoot '..')
)

$ErrorActionPreference = 'Stop'
$root = [System.IO.Path]::GetFullPath($RepositoryRoot)
$errors = [System.Collections.Generic.List[string]]::new()

$requiredFiles = @(
    'README.md',
    'EXECUTIVE-BRIEF.md',
    'ROADMAP.md',
    'NOTICE.md',
    'LICENSE.md',
    'docs/source-register.md',
    'framework/prove-method.md',
    'framework/schemas/governance-decision-contract.schema.json',
    'framework/templates/governance-decision-contract.example.json'
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        $errors.Add("Missing required file: $relativePath")
    }
}

$files = Get-ChildItem -LiteralPath $root -Recurse -File | Where-Object {
    $_.FullName -notmatch '[\\/](\.git|\.local-conversation|\.conversations|\.chat-history|\.codex|\.agents)[\\/]'
}

foreach ($jsonFile in $files | Where-Object Extension -eq '.json') {
    try {
        $null = Get-Content -LiteralPath $jsonFile.FullName -Raw | ConvertFrom-Json
    }
    catch {
        $relativePath = $jsonFile.FullName.Substring($root.Length).TrimStart('\', '/')
        $errors.Add("Invalid JSON: $relativePath - $($_.Exception.Message)")
    }
}

$linkPattern = [regex]'\[[^\]]+\]\((?<target>[^)]+)\)'
foreach ($markdownFile in $files | Where-Object Extension -eq '.md') {
    $content = Get-Content -LiteralPath $markdownFile.FullName -Raw
    $relativeMarkdownPath = $markdownFile.FullName.Substring($root.Length).TrimStart('\', '/')

    if ($content.Contains([char]0xFFFD)) {
        $errors.Add("Unicode replacement character found: $relativeMarkdownPath")
    }

    foreach ($match in $linkPattern.Matches($content)) {
        $target = $match.Groups['target'].Value.Trim()
        if ($target -match '^(https?://|mailto:|#)') {
            continue
        }

        if ($target.StartsWith('<') -and $target.EndsWith('>')) {
            $target = $target.Substring(1, $target.Length - 2)
        }

        $target = ($target -split '#', 2)[0]
        if ([string]::IsNullOrWhiteSpace($target)) {
            continue
        }

        $target = [System.Uri]::UnescapeDataString($target)
        $resolvedTarget = Join-Path $markdownFile.DirectoryName $target
        if (-not (Test-Path -LiteralPath $resolvedTarget)) {
            $errors.Add("Broken local link in ${relativeMarkdownPath}: $target")
        }
    }
}

if ($errors.Count -gt 0) {
    foreach ($validationError in $errors) {
        Write-Error $validationError
    }
    exit 1
}

Write-Output "Repository validation passed: $($files.Count) files checked."
