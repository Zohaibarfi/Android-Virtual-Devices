import subprocess
import time

class Emulator:
    def __init__(self, port):
        self.port = port

    def open_sms_app(self):
        # Command to open the default SMS messaging app
        command = f"adb -s emulator-{self.port} shell am start -a android.intent.action.MAIN -c android.intent.category.DEFAULT -n com.google.android.apps.messaging/.ui.ConversationListActivity"
        subprocess.run(command, shell=True)
        print(f"Opened SMS Messaging app on emulator-{self.port}")

    def send_sms(self, phone_number, message):
        # Command to send SMS using adb and the default messaging app
        command = f"adb -s emulator-{self.port} shell am start -a android.intent.action.SENDTO -d sms:{phone_number} --es sms_body \"{message}\" --ez exit_on_sent true"
        subprocess.run(command, shell=True)
        time.sleep(2)  # Wait for the messaging app to open and populate the message
        
        # Press the send button
        send_command = f"adb -s emulator-{self.port} shell input keyevent 61"  # Navigate to the next focusable element (Send button)
        subprocess.run(send_command, shell=True)
        send_command = f"adb -s emulator-{self.port} shell input keyevent 60"  # Confirm the send action (Enter key)
        subprocess.run(send_command, shell=True)
        
        print(f"Sent SMS to {phone_number}: {message}")

if __name__ == "__main__":
    emulator_port = input("Enter the port number of the emulator: ").strip()
    phone_number = input("Enter the phone number to send SMS: ").strip()
    message = input("Enter the SMS message: ").strip()
    
    emulator = Emulator(emulator_port)
    
    emulator.send_sms(phone_number, message)
    time.sleep(2)  # Wait for the message to be sent
    emulator.open_sms_app()
