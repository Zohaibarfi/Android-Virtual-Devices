import subprocess
import time
import os

# Function to execute adb shell commands
def adb_shell(command, device):
    adb_path = None
    # Find adb executable
    for path in os.getenv("PATH").split(os.pathsep):
        adb_candidate = os.path.join(path, "adb")
        if os.path.exists(adb_candidate) and os.access(adb_candidate, os.X_OK):
            adb_path = adb_candidate
            break
    if not adb_path:
        print("ADB executable not found.")
        return

    subprocess.Popen(f'"{adb_path}" -s {device} shell {command}', shell=True)

# Function to list installed packages
def list_installed_packages(device):
    try:
        # Run adb shell pm list packages command to list all installed packages on the selected device
        result = subprocess.check_output(f'adb -s {device} shell pm list packages', shell=True)
        # Extract package names from the result
        packages = [line.strip().split(":")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Function to check if package is installed
def is_package_installed(device, package_name):
    installed_packages = list_installed_packages(device)
    if installed_packages is not None:
        return package_name in installed_packages
    else:
        return False

# Function to write missing package names to a text file
def write_to_text_file(missing_packages):
    with open("/Users/macos/zohaib/script_app/missing_packages.txt", "a") as file:
        for package in missing_packages:
            file.write(package + "\n")

# Function to load coordinates based on the selected AVD name and Android version
def load_coordinates(avd_name, android_version):
    coordinates = {
        "Pixel 7 Pro": {
            13: (700, 1000),
            14: (700, 1000),
            12: (700, 1000),
            11: (700, 1000),
            10: (700, 1000),
            9: (700, 700),
            8: (700, 700)
        }
    }
    if avd_name in coordinates and android_version in coordinates[avd_name]:
        return coordinates[avd_name][android_version]
    else:
        return None

# Function to launch the AVD
def launch_avd(avd_name):
    subprocess.Popen(f"emulator -avd {avd_name}", shell=True)

# Function to wait for the AVD to boot
def wait_for_avd_boot(wait_time):
    time.sleep(wait_time)

# Function to open Google Chrome and navigate to the Play Store URL
def open_play_store(package_name, device, package_not_found_file):
    url = f"https://play.google.com/store/apps/details?id="
    full_url = url + package_name
    process = subprocess.Popen(f"adb -s {device} shell am start -a android.intent.action.VIEW -d '{full_url}' com.android.chrome", shell=True)
    time.sleep(5)  # Adjust this sleep time as needed
    if process.poll() is not None:
        with open(package_not_found_file, "a") as file:
            file.write(package_name + "\n")

# Function to wait for the Play Store page to load
def wait_for_play_store_load(wait_time):
    time.sleep(wait_time)

# Function to tap on the install button
def tap_install_button(x_coordinate, y_coordinate, device):
    adb_shell(f"input tap {x_coordinate} {y_coordinate}", device)

# Function to wait for the installation to complete
def wait_for_installation_complete(wait_time):
    time.sleep(wait_time)

# Function to list connected ADB devices
def list_adb_devices():
    try:
        # Run 'adb devices' command to list connected devices
        result = subprocess.check_output('adb devices', shell=True).decode('utf-8')
        # Extract device IDs from the result
        devices = [line.split('\t')[0] for line in result.split('\n')[1:] if line.strip()]
        return devices
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

# Function to get Android version of a device using ADB
def get_android_version(device):
    try:
        result = subprocess.check_output(f'adb -s {device} shell getprop ro.build.version.release', shell=True)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting Android version for device {device}: {e}")
        return None

# Function to map connected ADB devices with their Android versions
def map_devices_with_android_versions():
    adb_devices = list_adb_devices()
    device_android_versions = {}
    for device in adb_devices:
        android_version = get_android_version(device)
        if android_version:
            device_android_versions[device] = android_version
    return device_android_versions

# Function to read package names from a text file
def read_package_names_from_text_file(text_file_path):
    try:
        with open(text_file_path, 'r') as file:
            package_names = [line.strip() for line in file if line.strip()]
        return package_names
    except Exception as e:
        print(f"Error reading text file: {e}")
        return []

# Main function to install the packages
def install_packages(start_index, num_packages):
    # Map connected ADB devices with their Android versions
    device_android_versions = map_devices_with_android_versions()
    if not device_android_versions:
        print("No connected ADB devices found.")
        return
    
    # Print mapped devices and Android versions
    print("Connected ADB devices and their Android versions:")
    for device, android_version in device_android_versions.items():
        print(f"Device: {device}, Android Version: {android_version}")

    # Choose an ADB device based on the selected Android version
    selected_device = None
    android_version = None
    while True:
        android_version_input = input("Enter the Android version (e.g., 14, 13, 12, 11, 10, 9, 8): ")
        try:
            android_version = int(android_version_input)
            for device, version in device_android_versions.items():
                if int(version) == android_version:
                    selected_device = device
                    break
            if selected_device:
                break
            else:
                print("No device found with the specified Android version.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Selected ADB device: {selected_device}, Android Version: {android_version}")

    # Load coordinates based on the selected AVD name and Android version
    avd_name = "Pixel 7 Pro"  # Fixed AVD name
    coordinates = load_coordinates(avd_name, android_version)
    if coordinates is None:
        print("Coordinates not found for the selected AVD and Android version.")
        exit()

    x_coordinate, y_coordinate = coordinates

    # Use the provided text file path
    text_file_path = "/Users/macos/zohaib/script_app/packages.txt"
    package_not_found_file = "/Users/macos/zohaib/script_app/package_not_found_file.txt"

    # Read package names from the text file
    package_names = read_package_names_from_text_file(text_file_path)
    if not package_names:
        print("No package names found in the text file.")
        exit()

    # Launch the AVD
    launch_avd(selected_device)
    # Wait for the AVD to boot
    wait_for_avd_boot(5)

    installed_packages_count = 0
    missing_packages = []
    installed_packages = []
    for i in range(start_index, min(start_index + num_packages, len(package_names))):
        package_name = package_names[i]
        # Open Google Chrome and navigate to the Play Store URL for each package
        open_play_store(package_name, selected_device, package_not_found_file)
        # Wait for the Play Store page to load
        wait_for_play_store_load(5)
        # Tap on the install button
        tap_install_button(x_coordinate, y_coordinate, selected_device)
        # Wait for the installation to complete
        wait_for_installation_complete(10)

        # Check if the package is installed
        if is_package_installed(selected_device, package_name):
            installed_packages.append(package_name)
        else:
            missing_packages.append(package_name)
        installed_packages_count += 1

    # Write missing package names to a text file
    write_to_text_file(missing_packages)

    # Print installed and missing packages
    print("Installed Packages:")
    for package in installed_packages:
        print(package)
    print("\nMissing Packages:")
    for package in missing_packages:
        print(package)



start_index = int(input("Enter the index from which you want to start installing: "))
num_packages = int(input("Enter the number of packages to install: "))
install_packages(start_index, num_packages)



