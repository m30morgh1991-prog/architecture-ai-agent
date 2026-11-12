[CmdletBinding()]
param(
    [string]$AutoCADManagedDir = (Join-Path $env:ProgramFiles "Autodesk\AutoCAD 2020")
)

$ErrorActionPreference = "Stop"
$Project = Join-Path $PSScriptRoot "AIE.Autodesk.ReadOnlyExtractor.csproj"
$RequiredAssemblies = @("AcCoreMgd.dll", "AcDbMgd.dll", "AcMgd.dll")

Write-Host "AIE AutoCAD 2020 read-only adapter build" -ForegroundColor Cyan
Write-Host "Host assemblies: $AutoCADManagedDir"

if (-not (Test-Path $Project)) {
    throw "Project file not found: $Project"
}

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
    throw "The .NET SDK is missing. Install a current .NET SDK, then run this script again."
}

$Missing = @($RequiredAssemblies | Where-Object { -not (Test-Path (Join-Path $AutoCADManagedDir $_)) })
if ($Missing.Count -gt 0) {
    throw "AutoCAD 2020 managed assemblies were not found: $($Missing -join ', '). Check AutoCADManagedDir. No drawing was opened or changed."
}

$TargetingPack = Join-Path "$env:ProgramFiles(x86)" "Reference Assemblies\Microsoft\Framework\.NETFramework\v4.7"
if (-not (Test-Path $TargetingPack)) {
    Write-Warning ".NET Framework 4.7 reference assemblies were not found in the standard location. The build may fail unless the .NET Framework 4.7 Developer/Targeting Pack is installed."
}

Push-Location (Split-Path $Project -Parent)
try {
    dotnet build (Split-Path $Project -Leaf) -c Release -f net47 "-p:AutoCADManagedDir=$AutoCADManagedDir"
    if ($LASTEXITCODE -ne 0) {
        throw "Build failed with exit code $LASTEXITCODE. No DWG was opened or modified."
    }

    $Output = Join-Path (Get-Location) "bin\Release\net47\AIE.Autodesk.ReadOnlyExtractor.dll"
    if (-not (Test-Path $Output)) {
        throw "Build reported success but the expected plugin DLL is missing: $Output"
    }

    Write-Host ""
    Write-Host "BUILD PASSED" -ForegroundColor Green
    Write-Host "Plugin: $Output"
    Write-Host "Next: open a disposable DWG copy in AutoCAD 2020, use NETLOAD, select this DLL, then run AIEEXPORTREADONLY."
    Write-Host "Do not test against the immutable Golden DWG originals. Do not save the test drawing."
}
finally {
    Pop-Location
}
