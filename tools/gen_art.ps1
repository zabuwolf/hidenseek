# Sinh lại toàn bộ ảnh của game:  powershell -ExecutionPolicy Bypass -File tools\gen_art.ps1
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$src  = Get-Content -Raw -Encoding UTF8 (Join-Path $here "Art.cs")
Add-Type -TypeDefinition $src -ReferencedAssemblies System.Drawing -Language CSharp
[Art]::Run((Join-Path (Split-Path -Parent $here) "game"))
