import subprocess
import os

class Emulator:
    def __init__(self, port):
        self.port = port

    def open_documents_folder(self):
        # Command to open the Documents folder in internal storage
        command = f"adb -s emulator-{self.port} shell am start -a android.intent.action.VIEW -d content://com.android.externalstorage.documents/document/primary:Documents"
        subprocess.run(command, shell=True)
        print(f"Opened Documents folder on emulator-{self.port}")

    def save_file_to_documents(self, file_path):
        # Extract the filename from the given path
        filename = os.path.basename(file_path)
        # Define the destination path on the emulator
        destination_path = f"/storage/emulated/0/Documents/{filename}"
        # Push the file to the emulator's Documents directory
        command_push = f"adb -s emulator-{self.port} push {file_path} {destination_path}"
        subprocess.run(command_push, shell=True)
        print(f"File {filename} saved to Documents on emulator-{self.port}")

if __name__ == "__main__":
    emulator_port = input("Enter the port number of the emulator: ").strip()
    file_path = input("Enter the full path of the file to save in Documents:/Users/macos/Documents/Sample_ios/b9c2e48973ee720fa513157015ef1da7/Dynamic_Analysis_Results/Screenshots/17_ios_image.png").strip()

    emulator = Emulator(emulator_port)
    emulator.save_file_to_documents(file_path)
    emulator.open_documents_folder()
