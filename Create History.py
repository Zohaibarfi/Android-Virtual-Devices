import subprocess
import sqlite3
import os
import time

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
    device_id = select_active_device()
    if not device_id:
        return

    emulator = Emulator(device_id)
    local_history_path, remote_history_path = emulator.retrieve_history()
    local_history_path = emulator.add_history(local_history_path)
    emulator.update_history_on_device(local_history_path, remote_history_path)

if __name__ == "__main__":
    main()
