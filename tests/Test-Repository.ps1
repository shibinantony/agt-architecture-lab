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
    'framework/templates/agent-governance-decision.example.json'
    'lab/policy.yaml'
    'lab/runtime.py'
    'integrations/mcp_server.py'
    'docs/lab-guide.md'
    'docs/cli-integration.md'
    'docs/agt-reference.md'
    'docs/validation.md'
    'examples/upstream-agt/run.py'
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $root $relativePath
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        $errors.Add("Missing required file: $relativePath")
    }
}

$excludedDirectories = @(
    '.git', '.local-conversation', '.conversations', '.chat-history',
    '.codex', '.agents', '.gemini', '.venv', '.venv-agt', '__pycache__',
    '.pytest_cache', 'node_modules', 'artifacts', 'out', 'reports', 'evidence'
)

function Get-ProjectFiles([string]$Directory) {
    foreach ($item in Get-ChildItem -LiteralPath $Directory -Force) {
        if ($item.PSIsContainer) {
            if ($item.Name -notin $excludedDirectories -and
                -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
                Get-ProjectFiles $item.FullName
            }
        }
        else {
            $item
        }
    }
}
$files = @(Get-ProjectFiles $root)

foreach ($jsonFile in $files | Where-Object Extension -eq '.json') {
    try {
        $null = Get-Content -LiteralPath $jsonFile.FullName -Raw -Encoding UTF8 | ConvertFrom-Json
    }
    catch {
        $relativePath = $jsonFile.FullName.Substring($root.Length).TrimStart('\', '/')
        $errors.Add("Invalid JSON: $relativePath - $($_.Exception.Message)")
    }
}

$linkPattern = [regex]'\[[^\]]+\]\((?<target>[^)]+)\)'
foreach ($markdownFile in $files | Where-Object Extension -eq '.md') {
    $content = Get-Content -LiteralPath $markdownFile.FullName -Raw -Encoding UTF8
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
        Write-Error $validationError -ErrorAction Continue
    }
    exit 1
}

Write-Output "Repository validation passed: $($files.Count) files checked."
