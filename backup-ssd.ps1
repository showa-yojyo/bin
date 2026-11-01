# A backup script of robocopy version.
# Usage: backup-ssd.ps1

$BACKUP_DEST_ROOT = "E:\backup"
$BACKUP_SRC_ROOT = $env:APPDATA

# Back up %APPDATA% packages.

$robo_opts = @(
    "/L"
    "/MIR"
    "/R:0"
    "/W:1"
)

$targets = @(
    "DeepL_SE"
    "draw.io"
    #"FastStone"
    "GIMP\3.2"
    "inkscape"
    "LibreOffice\4\user"
    #"Microsoft"
    "Mozilla"
    "NuGet"
    #"obs-studio"
    "Thunderbird\Profiles"
    #"vlc"
    #"Zoom"
)
$exclude_dirs = @(
    "*Cache*"
    "logs"
)
$dest_root = "${BACKUP_DEST_ROOT}\AppData\Roaming"
foreach ($dir in $targets){
    robocopy "${BACKUP_SRC_ROOT}\$dir" "${dest_root}\$dir" /XD @exclude_dirs $robo_opts
}

## Back up %USERPROFILE% without folders.

$robo_opts = @(
    "/L"
    "/S"
    "/XO"
    "/XX"
    "/R:0"
    "/W:1"
)
$exclude_files = @(
    "NTUSER*"
    "*.lnk"
)

robocopy "$env:USERPROFILE" "${BACKUP_DEST_ROOT}" /LEV:1 /XF @exclude_files $robo_opts

# Back up %USERPROFILE% folders.

$robo_opts = @(
    "/L"
    "/S"
    "/XO"
    "/XX"
    "/R:0"
    "/W:1"
)
$targets = @(
    ".ssh"
    #".vscode"
    "devel"
    "Documents"
    "Music"
    "Pictures"
    "Saved Games"
    #"Videos"
)

foreach ($dir in $targets){
    robocopy "$env:USERPROFILE\$dir" "${BACKUP_DEST_ROOT}\$dir" /XD @exclude_dirs $robo_opts
}
