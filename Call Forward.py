import subprocess

class CallForwarding:
    def __init__(self, port):
        self.port = port

    def forward_calls(self, forward_number):
        # Command to forward calls
        command = f"adb -s emulator-{self.port} shell am start -a android.intent.action.CALL -d tel:*21*{forward_number}%23"
        subprocess.run(command, shell=True)
        print(f"Call forwarding to {forward_number} initiated on emulator-{self.port}")

if __name__ == "__main__":
    emulator_port = input("Enter the port number of the emulator: ").strip()
    forward_number = "9876543210"  # Specify the forward number here

    call_forwarding = CallForwarding(emulator_port)
    call_forwarding.forward_calls(forward_number)
