import subprocess

def get_emulator_port():
    while True:
        try:
            port = int(input("Enter the port number of the emulator device: "))
            return port
        except ValueError:
            print("Invalid input. Please enter a valid port number.")

def get_latitude_longitude():
    #return 25.2048, 55.2708
    while True:
        try:
            latitude = float(input("Enter the latitude: "))
            longitude = float(input("Enter the longitude: "))
            return latitude, longitude
        except ValueError:
            print("Invalid input. Please enter valid latitude and longitude.")

def set_location(latitude, longitude, port):
    try:
        # Run adb shell geo fix command to set the location
        command = f'adb -s emulator-{port} emu geo fix {longitude} {latitude}'
        subprocess.run(command, shell=True)
        print("Location updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Step 1: Ask for emulator port number
emulator_port = get_emulator_port()

# Step 2: Ask for latitude and longitude
latitude, longitude = get_latitude_longitude()

# Step 3: Set the location
set_location(latitude, longitude, emulator_port)
