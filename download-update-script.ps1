# Get the current script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Current directory: {$scriptDir}"
$response = Invoke-WebRequest -Headers @{"Accept"="application/json"; "Authorization"="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"} -Uri "https://api.github.com/repos/xplod24/wot-app/releases/" 
$json = $response | ConvertFrom-Json
$target_version = $json[0].tag_name
$current_version = Get-Content -path './current-version'
Write-Host "Current version: {$($current_version)}"
Write-Host "Target version: {$($target_version)}"

# Ask user to choose between full release and update
while ($true) {
    $choice = Read-Host "Do you want to download a full release or an update? (full/update)"
    if ( $choice -eq "update") {
        if ($current_version -eq  $target_version) {
            Write-Host "You are already up to date"
            exit $LASTEXITCODE
        } else {
            break
        }
    } elseif ($choice -eq "full") {
        break
    }{
        Write-Host "Incorrect option chosen. Please enter 'full' or 'update'."
    }
}

# Download update from GitHub releases page
if ($choice -eq "update") {

    $githubReleaseUrl = "https://github.com/xplod24/wot-app/releases/latest/download/update.zip"
    $downloadPath = Join-Path -Path $scriptDir -ChildPath "update.zip"
    Write-Host "Downloading update..."
    Invoke-WebRequest -Uri $githubReleaseUrl -OutFile $downloadPath -PassThru
    Write-Host "Download complete!"
    Write-Host $downloadPath

    # Create './update' folder if it doesn't exist
    $extractPath = Join-Path -Path $scriptDir -ChildPath "update"
    if (!(Test-Path -Path $extractPath)) {
        New-Item -ItemType Directory -Path $extractPath
    }

    # Unpack the update to './update' folder
    $zipPath = $downloadPath
    Write-Host "Unpacking update..."
    Expand-Archive -Path $zipPath -DestinationPath $extractPath -Force -PassThru
    Write-Host "Unpacking complete!"
    Write-Host $extractPath

    # Delete the './update' folder after update is finished
    Remove-Item -Path $extractPath -Recurse -Force
    Write-Host "Update folder deleted."
} elseif ($choice -eq "full") {
    $githubReleaseUrl = "https://github.com/xplod24/wot-app/releases/latest/download/full-release.zip"
    $downloadPath = Join-Path -Path $scriptDir -ChildPath "full-release.zip"
    Write-Host "Downloading full release..."
    Invoke-WebRequest -Uri $githubReleaseUrl -OutFile $downloadPath -PassThru
    Write-Host "Download complete!"
    Write-Host $downloadPath
}

# Create './app' folder if it doesn't exist
$appPath = Join-Path -Path $scriptDir -ChildPath "app"
if (!(Test-Path -Path $appPath)) {
    New-Item -ItemType Directory -Path $appPath
}

# Copy contents of './update' folder (if update was chosen) or './full-release' folder (if full release was chosen) to './app' folder, overwriting if file already exists
if ($choice -eq "update") {
    $filesToUpdate = Get-ChildItem -Path $extractPath -Recurse
    foreach ($file in $filesToUpdate) {
        $targetPath = Join-Path -Path $appPath -ChildPath $file.Name
        Copy-Item -Path $file.FullName -Destination $targetPath -Force
    }
} elseif ($choice -eq "full") {
    $zipPath = $downloadPath
    Write-Host "Unpacking full release..."
    Expand-Archive -Path $zipPath -DestinationPath $appPath -Force -PassThru
    Write-Host "Unpacking complete!"
}

Read-Host "Script finished executing. Press Enter to exit..."