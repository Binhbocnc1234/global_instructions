[CmdletBinding()]
param(
    [Parameter()]
    [string]$Path = (Get-Location).Path,

    [Parameter()]
    [ValidateRange(1, [int]::MaxValue)]
    [int]$MaxLines = 250,

    [Parameter()]
    [string[]]$Extensions = @(
        '.cs', '.css', '.go', '.java', '.js', '.jsx', '.kt', '.php', '.py',
        '.rb', '.rs', '.scss', '.swift', '.ts', '.tsx', '.vue'
    )
)

$resolvedPath = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
$excludedDirectories = @('.git', '.next', 'bin', 'build', 'coverage', 'dist', 'node_modules', 'obj', 'vendor')

$files = Get-ChildItem -LiteralPath $resolvedPath -File -Recurse | Where-Object {
    $_.Extension -in $Extensions -and
    -not ($_.FullName -split '[\\/]' | Where-Object { $_ -in $excludedDirectories })
}

$violations = foreach ($file in $files) {
    $lineCount = (Get-Content -LiteralPath $file.FullName | Measure-Object -Line).Lines
    if ($lineCount -gt $MaxLines) {
        [PSCustomObject]@{
            File  = $file.FullName
            Lines = $lineCount
        }
    }
}

if ($violations) {
    $violations | Sort-Object Lines -Descending | Format-Table -AutoSize
    Write-Error "$($violations.Count) source file(s) exceed the $MaxLines-line limit."
    exit 1
}

Write-Host "PASS: $($files.Count) source file(s) are at or below $MaxLines lines."
