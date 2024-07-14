import subprocess
import time

class Emulator:
    def __init__(self, port):
        self.port = port

    def send_sms(self, message, from_number):
        # Command to send SMS using adb with a specified sender number
        command = f"adb -s emulator-{self.port} emu sms send {from_number} \"{message}\""
        subprocess.run(command, shell=True)
        print(f"Sent SMS from {from_number}: {message}")

    @staticmethod
    def get_active_emulators():
        # Command to list active devices
        command = "adb devices"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        devices = result.stdout.split('\n')[1:-2]  # Extract device IDs
        active_emulators = [device.split('\t')[0] for device in devices if "emulator" in device]
        return active_emulators

def main():
    # Get list of active emulators
    active_emulators = Emulator.get_active_emulators()
    if not active_emulators:
        print("No active emulators found.")
        return
    
    # Choose the first active emulator
    emulator_port = active_emulators[0].split("-")[-1]

    emulator = Emulator(emulator_port)

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
        "1112223333",
        "4445556666"
    ]

    for message, from_number in zip(messages, from_numbers):
        emulator.send_sms(message, from_number)
        time.sleep(5)  # Wait for 5 seconds before sending the next message

if __name__ == "__main__":
    main()
