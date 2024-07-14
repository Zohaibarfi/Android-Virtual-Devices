import subprocess
import os

class Emulator:
    def __init__(self, port):
        self.port = port

    def open_downloads_folder(self):
        # Command to open the Downloads folder in internal storage
        command = f"adb -s emulator-{self.port} shell am start -a android.intent.action.VIEW -d content://com.android.externalstorage.documents/document/primary:Download"
        subprocess.run(command, shell=True)
        print(f"Opened Downloads folder on emulator-{self.port}")

    def save_file_to_downloads(self, file_path):
        # Extract the filename from the given path
        filename = os.path.basename(file_path)
        # Define the destination path on the emulator
        destination_path = f"/storage/emulated/0/Download/{filename}"
        # Push the file to the emulator's Downloads directory
        command_push = f"adb -s emulator-{self.port} push {file_path} {destination_path}"
        subprocess.run(command_push, shell=True)
        print(f"File {filename} saved to Downloads on emulator-{self.port}")

if __name__ == "__main__":
    emulator_port = input("Enter the port number of the emulator: ").strip()
    file_path = input("Enter the full path of the file to save in Downloads: ").strip()

    emulator = Emulator(emulator_port)
    emulator.save_file_to_downloads(file_path)
    emulator.open_downloads_folder()
