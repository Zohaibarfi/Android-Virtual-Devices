import subprocess

class Emulator:
    def __init__(self, device_id):
        self.device_id = device_id

    def find_files(self, directory, extensions):
        # Command to list files in the specified directory
        command = f"adb -s {self.device_id} shell ls -R {directory}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        files = result.stdout.split('\n')
        # Filter files by extensions
        filtered_files = [file for file in files if file.endswith(tuple(extensions))]
        return filtered_files

def select_active_device():
    # Command to list connected devices
    command = "adb devices"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    # Parse the output to extract device IDs
    devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:]]
    # Select the first device from the list as the active device
    if devices:
        return devices[0]
    else:
        print("No active devices found.")
        return None

def main():
    # Select the active device
    device_id = select_active_device()
    if not device_id:
        return
    
    # Specify file extensions to look for
    extensions = (".mp3", ".mp4", ".wav", ".amr", ".3gp", ".ogg", ".aac", ".m4a", ".flac")

    # Define the directory to search for files (Downloads folder)
    directory = "/storage/emulated/0"

    emulator = Emulator(device_id)

    # Search for files with the specified extensions in the Downloads folder
    files_found = emulator.find_files(directory, extensions)

    if files_found:
        print("Files found:")
        for file in files_found:
            print(file)
    else:
        print("No files found in the Downloads folder.")

if __name__ == "__main__":
    main()
