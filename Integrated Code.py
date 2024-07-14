import subprocess
import sqlite3
import os
import time
import pyperclip
import telnetlib

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
    return subprocess.Popen(f'"{adb_path}" -s {device} shell {command}', shell=True)

# Function to list installed packages
def list_installed_packages(device):
    try:
        result = subprocess.check_output(f'adb -s {device} shell pm list packages', shell=True)
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
        result = subprocess.check_output('adb devices', shell=True).decode('utf-8')
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

# Function to get the emulator port
def get_emulator_port(android_version):
    device_android_versions = map_devices_with_android_versions()
    if not device_android_versions:
        print("No connected ADB devices found.")
        return None
    
    for device, version in device_android_versions.items():
        if int(version) == android_version:
            if device.startswith('emulator-'):
                return device.split('-')[1]
    
    print(f"Emulator port not found for Android version {android_version}.")
    return None

# Function to list all installed apps
def list_all_apps(port):
    try:
        command = f'adb -s emulator-{port} shell pm list packages'
        result = subprocess.check_output(command, shell=True)
        packages = [line.strip().split(":")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        return packages
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return []

# Function to list permissions for a package
def list_permissions(package_name, port):
    try:
        command = f'adb -s emulator-{port} shell pm dump {package_name} | grep permission'
        result = subprocess.check_output(command, shell=True)
        permissions = [line.strip().split(":")[-1] for line in result.decode('utf-8').split('\n') if line.strip()]
        filtered_permissions = [permission for permission in permissions if 'android.permission.' in permission]
        return filtered_permissions
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

# Function to grant permissions
def grant_permissions(package_name, permissions, port):
    try:
        for permission in permissions:
            command = f'adb -s emulator-{port} shell pm grant {package_name} {permission}'
            subprocess.run(command, shell=True)
            print(f"Permission granted: {permission}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Function to change device location
def set_device_location(latitude, longitude, port):
    try:
        command = f'adb -s emulator-{port} emu geo fix {longitude} {latitude}'
        subprocess.run(command, shell=True)
        print("Location updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Function to send SMS
def send_sms(port):
    active_emulators = list_adb_devices()
    if not active_emulators:
        print("No active emulators found.")
        return
    
    emulator_with_port = f"emulator-{port}"
    if emulator_with_port not in active_emulators:
        print(f"No emulator found with port {port}.")
        return

    messages = [
        "Test message 1",
        "Test message 2",
        "Test message 3",
        "Test message 4",
        "Test message 5"
    ]

    from_numbers = [
        "1234567890",
        "0987654321",
        "5556667777",
        "9998887777",
        "4445556666"
    ]

    for message, from_number in zip(messages, from_numbers):
        command = f"adb -s {emulator_with_port} emu sms send {from_number} '{message}'"
        subprocess.run(command, shell=True)
        print(f"Sent SMS from {from_number}: {message}")

# Function to save file to Documents folder
def save_file_to_documents(file_path, port):
    filename = os.path.basename(file_path)
    destination_path = f"/storage/emulated/0/Documents/{filename}"
    command_push = f"adb -s emulator-{port} push {file_path} {destination_path}"
    subprocess.run(command_push, shell=True)
    print(f"File {filename} saved to Documents on emulator-{port}")

# Function to save file to Downloads folder
def save_file_to_downloads(file_path, port):
    filename = os.path.basename(file_path)
    destination_path = f"/storage/emulated/0/Download/{filename}"
    command_push = f"adb -s emulator-{port} push {file_path} {destination_path}"
    subprocess.run(command_push, shell=True)
    print(f"File {filename} saved to Downloads on emulator-{port}")

# Function to open the Documents folder
def open_documents_folder(port):
    command = f"adb -s emulator-{port} shell am start -a android.intent.action.VIEW -d content://com.android.externalstorage.documents/document/primary:Documents"
    subprocess.run(command, shell=True)
    print(f"Opened Documents folder on emulator-{port}")

class Emulator:
    def __init__(self, device_id):
        self.device_id = device_id

    def run_root(self):
        command = f"adb -s {self.device_id} root"
        subprocess.run(command, shell=True)

    def grant_permissions(self, path):
        command = f"adb -s {self.device_id} shell 'su -c \"chmod 777 {path}\"'"
        subprocess.run(command, shell=True)

    def copy_file_to_accessible_location(self, remote_path, temp_path):
        command = f"adb -s {self.device_id} shell 'su -c \"cp {remote_path} {temp_path}\"'"
        subprocess.run(command, shell=True)

    def pull_file(self, remote_path, local_path):
        command = f"adb -s {self.device_id} pull {remote_path} {local_path}"
        subprocess.run(command, shell=True)

    def push_file(self, local_path, remote_path):
        command = f"adb -s {self.device_id} push {local_path} {remote_path}"
        subprocess.run(command, shell=True)

    def retrieve_history(self):
        remote_history_path = "/data/data/com.android.chrome/app_chrome/Default/History"
        temp_history_path = "/sdcard/History"
        local_history_path = "./History"

        self.run_root()
        self.grant_permissions(remote_history_path)
        self.copy_file_to_accessible_location(remote_history_path, temp_history_path)
        self.pull_file(temp_history_path, local_history_path)

        con = sqlite3.connect(local_history_path)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT url, title, last_visit_time FROM urls")
            history = cursor.fetchall()

            for entry in history:
                print(f"URL: {entry[0]}, Title: {entry[1]}, Last Visit Time: {entry[2]}")

        except sqlite3.OperationalError as e:
            print("Error accessing history table:", e)
        finally:
            con.close()

        return local_history_path, remote_history_path

    def add_history(self, local_history_path):
        con = sqlite3.connect(local_history_path)
        cursor = con.cursor()

        # Pre-defined history entries
        histories = [
            {"url": "https://www.example.com", "title": "Example Domain"},
            {"url": "https://www.wikipedia.org", "title": "Wikipedia"},
            {"url": "https://www.github.com", "title": "GitHub"},
            {"url": "https://www.stackoverflow.com", "title": "Stack Overflow"},
            {"url": "https://www.reddit.com", "title": "Reddit"}
        ]

        for history in histories:
            url = history["url"]
            title = history["title"]
            last_visit_time = int(time.time() * 1000000)

            try:
                cursor.execute("""
                    INSERT INTO urls (url, title, visit_count, typed_count, last_visit_time, hidden)
                    VALUES (?, ?, 1, 1, ?, 0)
                """, (url, title, last_visit_time))

                print(f"Inserted history: URL={url}, Title={title}, Last Visit Time={last_visit_time}")

            except sqlite3.IntegrityError as e:
                print("Error inserting history:", e)

        con.commit()
        con.close()

        return local_history_path

    def update_history_on_device(self, local_history_path, remote_history_path):
        temp_history_path = "/sdcard/History"
        self.push_file(local_history_path, temp_history_path)
        command = f"adb -s {self.device_id} shell 'su -c \"cp {temp_history_path} {remote_history_path}\"'"
        subprocess.run(command, shell=True)
        command = f"adb -s {self.device_id} shell 'su -c \"rm {temp_history_path}\"'"
        subprocess.run(command, shell=True)

    def find_files(self, directory, extensions):
        # Command to list files in the specified directory
        command = f"adb -s {self.device_id} shell ls -R {directory}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {result.stderr}")
            return []
        
        files = result.stdout.split('\n')
        print(f"Raw output from ls command:\n{result.stdout}")  # Debugging statement
        
        # Filter files by extensions
        filtered_files = [file for file in files if file.endswith(tuple(extensions))]
        return filtered_files

    def set_clipboard_text(text):
        pyperclip.copy(text)
        print("Text has been set into the clipboard.")

    # Function to initiate a phone call
    def make_call(self, receiver_phone_number):
        # Connect to the emulator via telnet
        with telnetlib.Telnet("localhost", self.emulator_port) as tn:
            # Wait for a brief moment after connecting
            time.sleep(1)

            # Send the telnet command to initiate the call with receiver's phone number
            tn.write(b"gsm call %s\n" % receiver_phone_number.encode('ascii'))


def select_active_device():
    command = "adb devices"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:]]
    if devices:
        return devices[0]
    else:
        print("No active devices found.")
        return None

def main():
    avd_name = "Pixel 7 Pro"
    android_version = int(input("Enter the Android version: ").strip())

    device_android_versions = map_devices_with_android_versions()
    if not device_android_versions:
        print("No connected ADB devices found.")
        return

    device = None
    for dev, version in device_android_versions.items():
        if int(version) == android_version:
            device = dev
            break

    if not device:
        print(f"No device found with Android version {android_version}.")
        return

    x_coordinate, y_coordinate = load_coordinates(avd_name, android_version)
    if not (x_coordinate and y_coordinate):
        print(f"No coordinates found for AVD '{avd_name}' and Android version '{android_version}'.")
        return

    text_file_path = "/Users/macos/zohaib/script_app/packages.txt"
    package_not_found_file = "/Users/macos/zohaib/script_app/package_not_found.txt"
    package_names = read_package_names_from_text_file(text_file_path)

    if not package_names:
        print("No package names found in the text file.")
        return

    missing_packages = []

    for package_name in package_names:
        if is_package_installed(device, package_name):
            print(f"{package_name} is already installed.")
        else:
            print(f"{package_name} is not installed.")
            missing_packages.append(package_name)
            open_play_store(package_name, device, package_not_found_file)
            wait_for_play_store_load(5)

            for _ in range(3):
                adb_shell(f"input keyevent 20", device)
                time.sleep(1)

            tap_install_button(x_coordinate, y_coordinate, device)
            wait_for_installation_complete(15)

    if missing_packages:
        write_to_text_file(missing_packages)

    installed_apps = list_all_apps(device.split('-')[1])
    print("Installed Apps:", installed_apps)

    set_device_location(48.8584, 2.2945, device.split('-')[1])
    send_sms(device.split('-')[1])


    for app in installed_apps:
        permissions = list_permissions(app, device.split('-')[1])
        if permissions:
            grant_permissions(app, permissions, device.split('-')[1])

    

    file_path_documents = "/Users/macos/Documents/Sample_ios/b9c2e48973ee720fa513157015ef1da7/Dynamic_Analysis_Results/Screenshots/17_ios_image.png"
    save_file_to_documents(file_path_documents, device.split('-')[1])
    open_documents_folder(device.split('-')[1])

    file_path_downloads = "/Users/macos/Documents/Sample_ios/b9c2e48973ee720fa513157015ef1da7/Dynamic_Analysis_Results/Screenshots/12_ios_image.png"
    save_file_to_downloads(file_path_downloads, device.split('-')[1])

    device_id = select_active_device()
    if not device_id:
        return

    emulator = Emulator(device_id)
    local_history_path, remote_history_path = emulator.retrieve_history()
    local_history_path = emulator.add_history(local_history_path)
    emulator.update_history_on_device(local_history_path, remote_history_path)


    # Make a phone call
    emulator_port = get_emulator_port(android_version)
    if emulator_port:
        emulator.emulator_port = emulator_port
        receiver_phone_number = "9876543210"  # Replace with the desired receiver phone number
        emulator.make_call(receiver_phone_number)

    # Select the active device based on the provided Android version
    device_id = select_active_device()
    if not device_id:
        return
    
    # Specify file extensions to look for
    extensions = (".mp3", ".mp4", ".wav", ".amr", ".3gp", ".ogg", ".aac", ".m4a", ".flac")

    # Define the directory to search for files
    directory = "/storage/emulated/0"

    emulator = Emulator(device_id)

    # Search for files with the specified extensions
    files_found = emulator.find_files(directory, extensions)

    if files_found:
        print("Files found:")
        for file in files_found:
            print(file)
    else:
        print("No files found in the specified directory.")

def set_clipboard_text(text):
    pyperclip.copy(text)
    print("Text has been set into the clipboard.")
text_to_set = "Your desired text here"
set_clipboard_text(text_to_set)

if __name__ == "__main__":
    main()


