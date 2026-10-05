# Render preserved kernel output to PNG; these are output images, not UI captures.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$repoRoot = (Get-Location).Path
$outputDirectory = Join-Path $repoRoot 'submission/screenshots'
New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
$font = New-Object System.Drawing.Font('Consolas', 13)
$titleFont = New-Object System.Drawing.Font('Consolas', 16, [System.Drawing.FontStyle]::Bold)
$foreground = [System.Drawing.Brushes]::Black
try {
    foreach ($log in Get-ChildItem -LiteralPath (Join-Path $repoRoot 'submission/logs') -Filter '0*.txt') {
        $lines = [System.Collections.Generic.List[string]]::new()
        foreach ($line in [IO.File]::ReadAllLines($log.FullName, [Text.Encoding]::UTF8)) {
            if ($line.Length -eq 0) { $lines.Add('') }
            for ($offset = 0; $offset -lt $line.Length; $offset += 135) {
                $lines.Add($line.Substring($offset, [Math]::Min(135, $line.Length - $offset)))
            }
        }
        # Each page is readable at original resolution and preserves all output.
        $pageCount = [Math]::Max(1, [Math]::Ceiling($lines.Count / 65.0))
        for ($page = 0; $page -lt $pageCount; $page++) {
            $start = $page * 65
            $count = [Math]::Min(65, $lines.Count - $start)
            $bitmap = New-Object System.Drawing.Bitmap(1640, (110 + $count * 23))
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            try {
                $graphics.Clear([System.Drawing.Color]::White)
                $graphics.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
                $graphics.DrawString(($log.BaseName + ' | preserved Jupyter output'), $titleFont, $foreground, 24, 16)
                $graphics.DrawString(('Rendered from logs/' + $log.Name + ' | page ' + ($page + 1) + '/' + $pageCount + ' | not a UI screenshot'), $font, $foreground, 24, 52)
                for ($i = 0; $i -lt $count; $i++) {
                    $graphics.DrawString($lines[$start + $i], $font, $foreground, 24, (91 + $i * 23))
                }
                $name = '{0}_{1:00}.png' -f $log.BaseName, ($page + 1)
                $bitmap.Save((Join-Path $outputDirectory $name), [System.Drawing.Imaging.ImageFormat]::Png)
                Write-Output $name
            } finally { $graphics.Dispose(); $bitmap.Dispose() }
        }
    }
} finally { $font.Dispose(); $titleFont.Dispose() }
