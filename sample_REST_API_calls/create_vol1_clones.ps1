# PowerShell script to create a source volume snapshot and then clone the source volume
# N times from that snapshot. The names of the resulting cloned volumes will follow
# the format "{source_vol_name}_cloneN", and will be mounted into the SVM namespace
# as "/{source_vol_name}_cloneN".

##### Editable script control variables #####

$cluster = 'cluster2.demo.netapp.com'  # Target cluster FQDN
$volname = "vol1"              # Name of source volume
$svmname = "svm21"             # Name of SVM hosting source volume
$snapshot = "Clone Source"     # Name of snapshot to create on source volume
$numclones = 10                # Number of volume clones to create
$maxtries = 10                 # Maxmimum number of attempts to query job status before timeout

# response type and base64-encoded credentials data for -header parameter 
$header = @{"accept" = "application/hal+json"; "authorization" = "Basic YWRtaW46TmV0YXBwMSE=" }

################################################################################################
########## under normal conditions, no editing should be necessary beyond this point. ##########
################################################################################################

$clusterurl = "https://$cluster" # base URL for ONTAP REST API calls to the specified cluster

##### Get the uuid of the source volume.

# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/storage/volumes"
$parameters = "?name=" + $volname + "&fields=*&return_records=true&return_timeout=15"
$uri = $clusterurl + $methodpath + $parameters
# Invoke the method to get the volume uuid
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
} catch {
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$voluuid = $response.records.uuid  # uuid of source volume

##### Submit a request to create a snapshot on the source volume.

# construct the URI for the method
$methodtype = "POST"
$methodpath = '/api/storage/volumes/' + $voluuid + '/snapshots'
$parameters = ""
$uri = $clusterurl + $methodpath + $parameters
# Create payload record for create snapshot request body
if (Get-Variable -name payload -ErrorAction Ignore)
{
  Remove-Variable payload # so we can re-initialize it
}
$payload = @{
  'name' = $snapshot
}
$payloadJSON = $payload | ConvertTo-json
# Invoke the method to create the snapshot
try {
  $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri -Body $payloadJSON
} catch {
  # If API call generates an exception then abort the script.
  $apierror = $_ | ConvertFrom-json
  throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
}
$jobuuid = $response.job.uuid   # uuid of create snapshot job

##### Validate that the snapshot create job completed successfully.

# Construct the URI for the method
$methodtype = "GET"
$methodpath = "/api/cluster/jobs/" + $jobuuid
$parameters = ""
$uri = $clusterurl + $response.job._links.self.href
# Monitor snapshot create job until completion
$tries = 0       # Number of times we've checked the job status
while($true)
{
  Start-Sleep -Seconds 1   # Sleep 1 second
  # Invoke the method to query the job status
  try {
    $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri
  } catch {
    # If the API call generated an exception then abort the script.
    $apierror = $_ | ConvertFrom-json
    throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
  }
  # Check job state
  if ($response.state -eq "failure")
  {
    throw "method " + $methodtype + " " + $methodpath + " reports " + $response.state + ": " + $response.message
  }
  elseif ($response.state -eq "success")
  {
    Write-Host "Clone source snapshot successfully created on source volume $volname."
    break   # job finished, exit monitoring loop
  }
  else
  {
    if ($tries -ge $maxtries) 
    {
      # If we don't get a success response within specified maximum tries (retry interval is 1 second)
      # then abort with timeout error.
      throw "Timeout of method " + $methodtype + " " + $methodpath + " reports " + $response.state
    }
  }
  $tries++
}

##### Submit requests to create the volume FlexClones from the snapshot.

# Construct the URI for the method
$methodtype = "POST"
$methodpath = '/api/storage/volumes/'
$parameters = ""
$uri = $clusterurl + $methodpath + $parameters

# Create payload record for volume clone request body
if (Get-Variable -name payload -ErrorAction Ignore)
{
  Remove-Variable payload # so we can re-initialize it
}
$payload = @{
  'name'  = "";
  'clone' = @{'is_flexclone' = $true;
              'parent_snapshot' = @{'name' = $snapshot};
              'parent_volume' = @{'name' = $volname}
             };
  'nas'   = @{'path' = ""};
  'svm'   = @{'name' = $svmname}
}

$clones = @()     # array of hashes for tracking clone operations
$numwidth = $numclones.ToString().Length   # for calculating number of numeric digits in volume clone name
# Process each volume clone request
for ($i = 0; $i -lt $numclones; $i++)
{
  # update the payload record for this specific clone.
  $clonename = "{0}_clone{1:d$numwidth}" -f $volname, $($i + 1)
  $payload.name = $clonename
  $payload.nas.path = '/' + $clonename
  $payloadJSON = $payload | ConvertTo-json

  # Invoke the API method to create the volume clone
  try {
    $response = Invoke-RestMethod -header $header -method $methodtype -uri $uri -Body $payloadJSON
    # Capture job tracking info
    $joburi = $clusterurl + $response.job._links.self.href
    # add hash entry for this clone job to the clone tracking array.
    $clones+=@{'volume' = $clonename; 'uuid' = $response.job.uuid; 'state' = 'submitted'; 'joburi' = $joburi; 'message' = ""; 'tries' = 0}
  } catch {
    # If API call generates an exception then abort the script.
    $apierror = $_ | ConvertFrom-json
    throw "method " + $methodtype + " " + $methodpath + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
  }

}

##### Validate that the submitted volume clone jobs completed successfully.

# Monitor the submitted volume clone jobs
while ($true)
{
  Start-Sleep -Seconds 1   # Sleep 1 second
  $activejobs = 0  # assume no jobs running
  # process the jobs
  for ($i = 0; $i -lt $numclones; $i++)
  {
    # Process running jobs
    if ($clones[$i].state -ne "success" -And $clones[$i].state -ne "failure" -And $clones[$i].state -ne "timeout")
    {
      $activejobs = 1  # there is at least one job still running
      try {
        # query the job status
        $response = Invoke-RestMethod -header $header -method 'GET' -uri $clones[$i].joburi
        # Process job query result
        $clones[$i].tries+=1
        $clones[$i].state = $response.state
        if ($clones[$i].state -eq "failure")
        {
          $clones[$i].message = $response.message
          Write-Host "FlexClone volume $($clones[$i].volume) creation failed: $($clones[$i].message)"
        }
        elseif ($clones[$i].state -eq "success")
        {
          Write-Host "FlexClone volume $($clones[$i].volume) created successfully."
        }
        elseif ($clones[$i].tries -ge $maxtries)
        {
          $clones[$i].message = "Re-try timeout exceeded, last known state = {0}" -f $clones[$i].state
          $clones[$i].state = "timeout"
          Write-Host "FlexClone volume $($clones[$i].volume) creation timed out: $($clones[$i].message)"
        }
      } catch {
        # If API call generates an exception then abort the script.
        $apierror = $_ | ConvertFrom-json
        throw "Job status request GET " + $clones[$i].uri + " error: target = " + $apierror.error.target + ", " + $apierror.error.message
      }
    }
  }
  if (-NOT $activejobs)
  {
    # Clone job processing complete
    break
  }
}

