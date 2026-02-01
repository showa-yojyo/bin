# Export the WSL distribution to a VHDX file.
#
# Make sure to replace "Ubuntu" with the name of your WSL distribution if it's
# different. Also, change the path in the FILENAME variable to your desired
# backup location.

wsl --shutdown

# yyyymmdd format for the filename
$today = Get-Date -Format "yyyy-MM-dd"

$backup_dest = "E:\Ubuntu-${today}.vhdx"
wsl --export --format vhd Ubuntu "$backup_dest"
