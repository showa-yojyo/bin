# A backup script of robocopy version.
# Usage: backup-ssd.ps1

# Note: To perform a real backup, manually set the $DRY_RUN variable to an empty
# string.
$DRY_RUN = ""

# Back up %APPDATA% packages.

$TARGETS = @("GIMP/3.0", "inkscape", "LibreOffice/4/user")
$SRC_ROOT = $env:APPDATA
$BACKUP_DEST_ROOT = "E:\backup"
$DEST_ROOT = "${BACKUP_DEST_ROOT}\AppData\Roaming"

foreach ($i in $TARGETS){
    robocopy "${SRC_ROOT}\$i" "${DEST_ROOT}\$i" $DRY_RUN /MIR /E /ZB /COPYALL /DCOPY:t /XJ /R:0 /W:1
}

# Back up %USERPROFILE% without folders.

robocopy "$env:USERPROFILE" "${BACKUP_DEST_ROOT}" $DRY_RUN /LEV:1 /R:1 /W:1 /ZB /XF "NTUSER*" "*.lnk"

# Back up %USERPROFILE% folders.

$TARGETS = @("devel", "Documents", "Music", "Pictures")
foreach ($i in $TARGETS){
    robocopy "$env:USERPROFILE\$i" "${BACKUP_DEST_ROOT}\$i" $DRY_RUN /E /ZB /COPYALL /DCOPY:t /XJ /R:0 /W:1
}
