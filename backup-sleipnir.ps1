<#
.SYNOPSIS
    A backup script for Sleipnir 6
.DESCRIPTION
    TBW
.EXAMPLE
    backup-sleipnir "E:\backup\AppData\Roaming\Fenrir Inc\Sleipnir5\setting"
#>

param(
    # back up essential files into target_path
    [parameter(mandatory=$true)][string]$target_path
)

if(Get-Process sleipnir)
{
    echo "Sleipnir is still running."
    exit 1
}

$source_path = Join-Path $Env:APPDATA "Fenrir Inc\Sleipnir5\setting"

# Note: To perform a real backup, comment out /L.
$robo_opts = @(
    #"/L"
    #"/LOG+:backup-sleipnir.log"
    "/MIR"
    "/R:0"
    "/W:1"
)

# 1. Back up "client" folder

$sleipnir_client = "client"
$client_source_path = Join-Path $source_path $sleipnir_client
$client_target_path = Join-Path $target_path $sleipnir_client

$include = @("*.ini", "*.json")

robocopy "$client_source_path" "$client_target_path" @include /LEV:1 $robo_opts

# 2. Back up "ChromeViewer" folder, the user data folder of Google Chrome

$chrome_user_data = "modules"
$chrome_profile_source = Join-Path $source_path $chrome_user_data
$chrome_profile_target = Join-Path $target_path $chrome_user_data

$exclude_files = @(
    "*.bak.dat"
    "*.tmp"
    "*-journal"
)
$exclude_dirs = @(
    "temp"
    "IEBrowser"
    "superdrag"
    "*Cache*"
    "CertificateTransparency"
    "component_crx_cache"
    "hyphen-data"
    "Service Worker"
    "ZxcvbnData"
)

robocopy "$chrome_profile_source" "$chrome_profile_target" $robo_opts /XF $exclude_files /XD $exclude_dirs
