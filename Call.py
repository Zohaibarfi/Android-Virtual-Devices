import telnetlib
import time
import subprocess

def change_phone_number(emulator_port, new_phone_number):
    # Connect to the emulator via telnet
    with telnetlib.Telnet("localhost", emulator_port) as tn:
        # Wait for a brief moment after connecting
        time.sleep(1)

        # Send the telnet command to change the phone number
        tn.write(b"gsm change %s\n" % new_phone_number.encode('ascii'))

def make_call(caller_emulator_port, receiver_emulator_port, caller_phone_number, receiver_phone_number):
    # Connect to the caller emulator via telnet and change the phone number
    change_phone_number(caller_emulator_port, caller_phone_number)

    # Connect to the caller emulator via telnet
    with telnetlib.Telnet("localhost", caller_emulator_port) as caller_tn:
        # Wait for a brief moment after connecting
        time.sleep(1)

        # Display caller and receiver phone numbers in the console
        print(f"Caller Phone Number: {caller_phone_number}")
        print(f"Receiver Phone Number: {receiver_phone_number}")

        # Send the telnet command to initiate the call with caller's phone number
        caller_tn.write(b"gsm call %s\n" % receiver_phone_number.encode('ascii'))

        # Wait for the call to connect (adjust the time as needed)
        time.sleep(5)

        # Hang up the call (optional)
        caller_tn.write(b"gsm cancel\n")

    # Connect to the receiver emulator via telnet and change the phone number
    change_phone_number(receiver_emulator_port, receiver_phone_number)

    # Connect to the receiver emulator via telnet
    with telnetlib.Telnet("localhost", receiver_emulator_port) as receiver_tn:
        # Wait for a brief moment after connecting
        time.sleep(1)

        # Simulate answering the call by pressing the green call button
        receiver_tn.write(b"gsm accept\n")

def map_devices_with_android_versions():
    try:
        result = subprocess.check_output('adb devices', shell=True).decode('utf-8')
        devices = [line.split('\t')[0] for line in result.split('\n')[1:] if line.strip()]
        device_android_versions = {}
        for device in devices:
            android_version = get_android_version(device)
            if android_version:
                device_android_versions[device] = android_version
        return device_android_versions
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return {}

def get_android_version(device):
    try:
        result = subprocess.check_output(f'adb -s {device} shell getprop ro.build.version.release', shell=True)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        print(f"Error getting Android version for device {device}: {e}")
        return None

if __name__ == "__main__":
    # Get the Android version from the user
    android_version = int(input("Enter the Android version: ").strip())

    # Get the active devices and their Android versions
    device_android_versions = map_devices_with_android_versions()

    # Find a device with the entered Android version to set as the receiver
    receiver_device = None
    for device, version in device_android_versions.items():
        if int(version) == android_version:
            receiver_device = device
            break

    if not receiver_device:
        print(f"No device found with Android version {android_version}.")
    else:
        receiver_emulator_port = receiver_device.split('-')[1]
        print(f"Receiver emulator port set to: {receiver_emulator_port}")

        # Find another active device to set as the caller
        caller_device = None
        for device in device_android_versions:
            if device != receiver_device:
                caller_device = device
                break

        if not caller_device:
            print("No other active device found.")
        else:
            caller_emulator_port = caller_device.split('-')[1]
            print(f"Caller emulator port set to: {caller_emulator_port}")

            # Phone numbers for testing
            caller_phone_number = "1234567890"
            receiver_phone_number = "9876543210"

            # Make the call
            make_call(caller_emulator_port, receiver_emulator_port, caller_phone_number, receiver_phone_number)
