import subprocess

class Emulator:
    def __init__(self, port):
        self.port = port

    def simulate_keyboard_input(self, key):
        # Command to simulate keyboard input
        command = f"adb -s emulator-{self.port} shell input text '{key}'"
        subprocess.run(command, shell=True)
        print(f"Simulated typing '{key}' on emulator-{self.port}")

if __name__ == "__main__":
    emulator_port = input("Enter the port number of the emulator: ").strip()

    emulator = Emulator(emulator_port)
    
    # Prompt the user to enter the key they want to type
    key = input("Enter the key you want to type on the emulator keyboard: ")

    # Simulate typing the specified key
    emulator.simulate_keyboard_input(key)
