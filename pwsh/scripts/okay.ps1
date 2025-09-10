while ($true) {
Write-Host "Starting pwsh script"
$pfxpath = "/certs/teams.pfx"
$pfxpass = $env:PW

try {
    $modules = Get-Module -ListAvailable MicrosoftTeams 
    if (-not $modules) {
        Write-Host "Insalling Module"
        Install-Module MicrosoftTeams -Force
        Write-Host "Installed MicrosoftTeams"
    }
    else {
        Write-Host "Module installed, skipping module install."
    }

    Import-Module MicrosoftTeams
    Write-Host "Imported module"
    $flags = [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::MachineKeyset `
        -bor [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::Exportable `
        -bor [System.Security.Cryptography.X509Certificates.X509KeyStorageFlags]::EphemeralKeySet
    write-host "Got certificate flags"
    $cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new($pfxpath, $pfxpass, $flags)
    write-host "Unpacked .pfx"
    $connect = @{
        ApplicationID = $env:APP
        TenantID = $env:TENANT
        Certificate = $cert
        }
    Connect-MicrosoftTeams @connect
    Write-Host "Succefully connected to MicrosoftTeams module"

    try {
        $greeting = Get-Content -Path "/message/greeting.txt" -Raw
        if (-not $greeting) {
            Write-Host "Attempting to remove greeting message"

            $aa = Get-CsAutoAttendant -Identity 299f08d3-f8b1-4f2f-b575-e58a9228cdfa
            $aa.DefaultCallFlow.Greetings = @()
            Set-CsAutoAttendant -Instance $aa

            Write-Host "Greeting message removed"
        }
        else {
            Write-Host "Attempting to upload greeting message: $greeting"

            $aa = Get-CsAutoAttendant -Identity $env:AA
            $aa.DefaultCallFlow.Greetings = @(New-CsAutoAttendantPrompt -TextToSpeechPrompt $greeting)
            Set-CsAutoAttendant -Instance $aa

            write-host "Greeting uploaded"
        }
    }
    catch {
        Write-Host "An error occured with fetching or adding greeting"
    }

}
catch {
    Write-Warning "An error occured on the overall script."
}

Write-Host "Sleeping for 60 seconds"
Start-Sleep -Seconds 60
}

