import subprocess

class EmulatorContacts:
    def __init__(self, port):
        self.port = port

    def push_contacts(self, vcf_file_path):
        # Push contacts file to emulator's storage
        command = f"adb -s emulator-{self.port} push {vcf_file_path} /sdcard/contacts.vcf"
        subprocess.run(command, shell=True)
        print(f"Pushed {vcf_file_path} to /sdcard/contacts.vcf on emulator-{self.port}")

    def import_contacts(self):
        # Use ADB to start the activity that can handle the VCF file
        command = f"adb -s emulator-{self.port} shell am start -t text/x-vcard -d file:///sdcard/contacts.vcf -a android.intent.action.VIEW com.android.contacts"
        subprocess.run(command, shell=True)
        print(f"Imported contacts from /sdcard/contacts.vcf on emulator-{self.port}")

def create_vcf_file(file_path, contacts):
    with open(file_path, "w") as file:
        for contact in contacts:
            vcf_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact['name']}
TEL;TYPE=CELL:{contact['phone']}
END:VCARD
"""
            file.write(vcf_content)
    print(f"{file_path} created successfully.")

if __name__ == "__main__":
    contacts = []
    
    while True:
        name = input("Enter contact name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        phone = input("Enter contact phone number: ").strip()
        
        contacts.append({"name": name, "phone": phone})
    
    vcf_file_path = "contacts.vcf"
    create_vcf_file(vcf_file_path, contacts)

    emulator_port = input("Enter the port number of the emulator: ").strip()
    
    emulator_contacts = EmulatorContacts(emulator_port)
    emulator_contacts.push_contacts(vcf_file_path)
    emulator_contacts.import_contacts()
