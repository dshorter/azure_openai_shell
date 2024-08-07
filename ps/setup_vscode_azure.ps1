# Function to check if a command exists
function Test-Command($cmdname) {
    return [bool](Get-Command -Name $cmdname -ErrorAction SilentlyContinue)
}

# Function to check if a VS Code extension is installed
function Test-VSCodeExtension($extension) {
    $result = code --list-extensions | Where-Object { $_ -eq $extension }
    return [bool]$result
}

# Check required VS Code extensions
$extensions = @(
    "ms-python.python",
    "ms-azuretools.vscode-azureresourcegroups",
    "ms-azuretools.vscode-azurefunctions",
    "ms-vscode.azurecli",
    "ms-azuretools.vscode-docker"
)

$missingExtensions = @()
foreach ($extension in $extensions) {
    if (-not (Test-VSCodeExtension $extension)) {
        $missingExtensions += $extension
    }
}

if ($missingExtensions.Count -gt 0) {
    Write-Host "The following VS Code extensions are not installed:"
    $missingExtensions | ForEach-Object { Write-Host "- $_" }
    Write-Host "Please install these extensions manually from the VS Code marketplace."
    Write-Host "Press any key to continue with the rest of the setup..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
} else {
    Write-Host "All required VS Code extensions are installed."
}

# Check and install Python if not present
if (-not (Test-Command "python")) {
    Write-Host "Python is not installed. Installing Python..."
    $installerUrl = "https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe"
    $installerPath = "$env:TEMP\python_installer.exe"
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath
    Start-Process -FilePath $installerPath -Args "/quiet InstallAllUsers=1 PrependPath=1" -Wait
    Remove-Item $installerPath
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    Write-Host "Python installed successfully."
} else {
    Write-Host "Python is already installed."
}

# Create a new Python virtual environment
python -m venv .venv

# Ask user if they want to activate the virtual environment
$activateVenv = Read-Host "Do you want to activate the virtual environment? (y/n)"

if ($activateVenv -eq 'y') {
    # Activate the virtual environment
    .\.venv\Scripts\Activate.ps1

    # Upgrade pip
    python -m pip install --upgrade pip

    # Install required Python packages
    pip install azure-identity openai python-dotenv

    Write-Host "Virtual environment activated and packages installed."
    Write-Host "To deactivate the virtual environment later, type 'deactivate'."
} else {
    Write-Host "Virtual environment created but not activated."
    Write-Host "To activate later, run: .\.venv\Scripts\Activate.ps1"
}

# Create a .env file for Azure credentials
@"
AZURE_TENANT_ID=your_tenant_id
AZURE_CLIENT_ID=your_client_id
AZURE_CLIENT_SECRET=your_client_secret
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
"@ | Out-File -FilePath .env

Write-Host "Setup complete. Remember to update the .env file with your actual Azure credentials."