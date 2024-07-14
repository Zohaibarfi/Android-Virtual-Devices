import subprocess

def get_android_version(device):
    try:
        result = subprocess.check_output(f'adb -s {device} shell getprop ro.build.version.release', shell=True)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting Android version for device {device}: {e}")
        return None

def get_emulator_port(android_version):
    # Map connected ADB devices with their Android versions
    device_android_versions = map_devices_with_android_versions()
    if not device_android_versions:
        print("No connected ADB devices found.")
        return None
    
    # Iterate over devices to find the one with the matching Android version
    for device, version in device_android_versions.items():
        if int(version) == android_version:
            # Extract the port number from the device ID (e.g., emulator-5554)
            if device.startswith('emulator-'):
                return device.split('-')[1]
    return None

def list_all_apps(port):
    try:
        # Run adb shell pm list packages command to get all installed package names
        command = f'adb -s emulator-{port} shell pm list packages'
        result = subprocess.check_output(command, shell=True)
        # Extract package names from the result
        packages = [line.strip().split(":")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def list_packages(apk_name, port):
    try:
        # Run adb shell pm list packages command and filter by apk_name
        command = f'adb -s emulator-{port} shell pm list packages -f | grep {apk_name}'
        result = subprocess.check_output(command, shell=True)
        # Extract package names from the result (after "/base.apk=")
        packages = [line.strip().split("/base.apk=")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def list_permissions(package_name, port):
    try:
        # Run adb shell pm dump command to get permissions
        command = f'adb -s emulator-{port} shell pm dump {package_name} | grep permission'
        result = subprocess.check_output(command, shell=True)
        # Extract permissions from the result
        permissions = [line.strip().split(":")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        # Filter permissions with "android.permission."
        filtered_permissions = [permission for permission in permissions if 'android.permission.' in permission]
        return filtered_permissions
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def grant_permissions(package_name, permissions, port):
    try:
        # Run adb shell pm grant command to grant permissions
        for permission in permissions:
            command = f'adb -s emulator-{port} shell pm grant {package_name} {permission}'
            subprocess.run(command, shell=True)
            print(f"Permission granted: {permission}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Function to map connected ADB devices with their Android versions
def map_devices_with_android_versions():
    try:
        # Run 'adb devices' command to list connected devices
        result = subprocess.check_output('adb devices', shell=True).decode('utf-8')
        # Extract device IDs and Android versions from the result
        devices_info = [line.split('\t') for line in result.split('\n')[1:] if line.strip()]
        device_android_versions = {}
        for device_info in devices_info:
            device = device_info[0]
            android_version = get_android_version(device)
            if android_version:
                device_android_versions[device] = android_version
        return device_android_versions
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {}

# Main function
def main():
    # Step 1: Ask for the Android version
    while True:
        android_version_input = input("Enter the Android version (e.g., 14, 13, 12, 11, 10, 9, 8): ")
        try:
            android_version = int(android_version_input)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Selected Android Version: {android_version}")

        # Step 2: Select the emulator port based on the Android version
    emulator_port = get_emulator_port(android_version)
    if emulator_port is None:
        print("No emulator found for the specified Android version.")
        return

    print(f"Emulator Port: {emulator_port}")

    # Step 3: List all installed apps
    installed_apps = list_all_apps(emulator_port)

    if installed_apps:
        print("Installed Apps:")
        for app in installed_apps:
            print(f"\nPackage Name: {app}")

            # Step 4: List permissions for each app
            permissions = list_permissions(app, emulator_port)
            if permissions:
                print("\nPermissions:")
                for permission in permissions:
                    print(permission)

                # Step 5: Grant permissions
                grant_permissions(app, permissions, emulator_port)
            else:
                print("No permissions found.")
    else:
        print("No installed apps found.")

if __name__ == "__main__":
    main()
