# Map the V drive if not mapped
if (-NOT (Get-PsDrive | Where-Object { $_.Name -eq 'V'}))
{
  # Not mapped currently, so map it.
  Write-Host "Mapping share \\svm21\nsroot as V:"
  New-PSDrive -Name "V" -PSProvider FileSystem -Root "\\svm21\nsroot" -Persist -Scope global
}

$plink="C:\Program Files (x86)\PuTTY\plink.exe"
$keyfile = "C:\LOD\config\keys\private.ppk"

# In preparation for file generation, if svm21:/ isn't already mounted
# on rhel1, mount it now. 
$result = &($plink) rhel1 -l root -batch -i $keyfile "mount | grep /svm21"
if ($result -eq $null)
{
  # Make mount point if it doesn't exist
  &($plink) rhel1 -l root -batch -i $keyfile "mkdir -p /svm21"
  # Mount the volume
  &($plink) rhel1 -l root -batch -i $keyfile "mount svm21:/ /svm21"
}

# Run the file generation script on rhel1, which is much more efficient
# for generating these file than is trying to do so natively in PowerShell.
&($plink) rhel1 -l root -batch -i $keyfile randomfiles -p /svm21/vol1
Write-Host ""
Write-Host "Creation of files complete."
pause