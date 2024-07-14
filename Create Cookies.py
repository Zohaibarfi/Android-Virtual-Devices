import subprocess
import sqlite3
import os
import time

class Emulator:
    def __init__(self, port):
        self.port = port
        self.device_id = f"emulator-{self.port}"

    def run_root(self):
        command = f"adb -s {self.device_id} root"
        subprocess.run(command, shell=True)

    def grant_permissions(self):
        command = f"adb -s {self.device_id} shell 'su -c \"chmod 777 /data/data/com.android.chrome/app_chrome/Default/Cookies\"'"
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

    def retrieve_cookies(self):
        remote_cookie_path = "/data/data/com.android.chrome/app_chrome/Default/Cookies"
        temp_cookie_path = "/sdcard/Cookies"
        local_cookie_path = "./Cookies"

        # Ensure root access
        self.run_root()

        # Copy the cookie file to a more accessible location
        self.copy_file_to_accessible_location(remote_cookie_path, temp_cookie_path)

        # Pull the copied file from the accessible location
        self.pull_file(temp_cookie_path, local_cookie_path)

        # Read the cookies from the SQLite database
        con = sqlite3.connect(local_cookie_path)
        cursor = con.cursor()
        try:
            cursor.execute("SELECT host_key, name, value, path, expires_utc, creation_utc FROM cookies")
            cookies = cursor.fetchall()

            # Print cookies
            for cookie in cookies:
                print(f"Host: {cookie[0]}, Name: {cookie[1]}, Value: {cookie[2]}, Path: {cookie[3]}, Expires: {cookie[4]}, Creation: {cookie[5]}")

        except sqlite3.OperationalError as e:
            print("Error accessing cookies table:", e)
        finally:
            con.close()

        return local_cookie_path, remote_cookie_path

    def add_cookie(self, local_cookie_path):
        con = sqlite3.connect(local_cookie_path)
        cursor = con.cursor()

        # Get user input for new cookie details
        host_key = input("Enter host key: ").strip()
        name = input("Enter cookie name: ").strip()
        value = input("Enter cookie value: ").strip()
        path = input("Enter path: ").strip()
        expires_utc = int(input("Enter expiry time in seconds since epoch (0 for session cookie): ").strip())

        # Get the current time in microseconds since the epoch for creation_utc
        creation_utc = int(time.time() * 1000000)

        try:
            cursor.execute("""
                INSERT INTO cookies (host_key, name, value, path, expires_utc, creation_utc)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (host_key, name, value, path, expires_utc, creation_utc))

            con.commit()

            print(f"Inserted cookie: Host={host_key}, Name={name}, Value={value}, Path={path}, Expires={expires_utc}, Creation={creation_utc}")

        except sqlite3.IntegrityError as e:
            print("Error inserting cookie:", e)
        finally:
            con.close()

        return local_cookie_path

    def update_cookies_on_device(self, local_cookie_path, remote_cookie_path):
        temp_cookie_path = "/sdcard/Cookies"

        # Push the updated cookie file back to the accessible location
        self.push_file(local_cookie_path, temp_cookie_path)

        # Copy the updated cookie file back to the original location
        command = f"adb -s {self.device_id} shell 'su -c \"cp {temp_cookie_path} {remote_cookie_path}\"'"
        subprocess.run(command, shell=True)

        # Remove the temporary cookie file from the device
        command = f"adb -s {self.device_id} shell 'su -c \"rm {temp_cookie_path}\"'"
        subprocess.run(command, shell=True)

def main():
    emulator_port = input("Enter the port number of the emulator: ").strip()

    emulator = Emulator(emulator_port)
    local_cookie_path, remote_cookie_path = emulator.retrieve_cookies()
    local_cookie_path = emulator.add_cookie(local_cookie_path)
    emulator.update_cookies_on_device(local_cookie_path, remote_cookie_path)

if __name__ == "__main__":
    main()
