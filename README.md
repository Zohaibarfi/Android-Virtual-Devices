# Android-Virtual-Devices
This repository contains a project developed on an Android Virtual Device (AVD), focusing on automation of different tasks using pyhthon scripts and network traffic analysis using Python scripts and Mitmproxy.

# Environment
This project was developed and tested on macOS.

# Project Overview
The project includes Python automation scripts designed for various tasks on AVDs, enhancing testing and simulation capabilities:
Python Automation Scripts:

# 1. Auto-Installing Apps
This Python script automates app installations from the Google Play Store onto an Android emulator. It reads package names from a text file, installs apps using ADB commands, handles errors gracefully, and automates permission granting, saving time and ensuring consistent installations.

# 2. Granting Permissions:
This Python script automates the process of granting permissions to all apps on an Android device. It asks for the Android version, connects via ADB, and grants permissions uniformly, saving time and ensuring consistency during app testing and development.

# 3. Telephony Operations:
Python script for Android devices that automates various telephony operations. The script can make outgoing calls using ADB commands, forward incoming calls to alternative numbers for enhanced accessibility, and automatically record calls for compliance and record-keeping purposes. This comprehensive solution streamlines telephony management by integrating call making, forwarding, and recording into one automated process, saving time and reducing the risk of errors. Each function operates seamlessly, ensuring consistent execution and facilitating easy access to recorded call files stored on the device.

# 4. Messaging:
Python script for Android devices that automates sending and receiving SMS messages. The script efficiently sends SMS messages to specified phone numbers using ADB commands and monitors incoming SMS messages for real-time processing and automated responses. This solution streamlines SMS communication for testing and development, offering automation that saves time, ensures reliability in message handling, and enables real-time interaction with incoming messages.

# 5. Accessibility Functions:
Python script for Android devices that simulates accessibility functions, focusing on touch events. Using ADB commands, the script simulates various touch interactions such as taps, swipes, and long presses by specifying coordinates and durations. It automates user interactions for tasks like navigating app menus and filling out forms, facilitating accessibility feature testing and UI development. This automation saves time, ensures consistent execution of touch interactions, and supports comprehensive testing of app accessibility features.

# 6. File Operations:
Python script for Android Virtual Devices (AVDs) that automates file saving tasks. Using ADB commands, the script transfers files from the host machine to specified directories within the AVD, such as Documents or Downloads folders. It facilitates automated file management tasks like organizing directories, moving, and deleting files, optimizing testing scenarios requiring specific files for app testing. This automation improves efficiency by saving time, ensuring consistent file operations, and enhancing testing processes.

# 7. Location Spoofing:
For my project, I implemented a method to spoof the geolocation of the Android emulator using command line tools. This involved enabling location administration and executing ADB commands to simulate various geographic coordinates directly within the emulator environment. This flexibility allowed for rapid iteration and validation of location-aware features, minimizing potential inaccuracies in test results and enhancing efficiency during iterative testing cycles.

# 8. Contact Management:
Python script for Android Virtual Devices (AVDs) that automates the creation of contacts. Using ADB commands, the script interacts with the AVD's contact database, allowing users to specify details such as names, phone numbers, and email addresses for each contact. It supports bulk contact creation by reading details from files like CSV or JSON, efficiently populating the contact list for testing purposes. This automation saves time, ensures consistent creation of contacts, and enhances efficiency in scenarios requiring specific contact data for testing.

# 9. Browser Data:
Python scripts for Android Virtual Devices (AVDs) to automate the creation of cookies and browser history. The cookie script prompts users to input details like name, value, domain, path, and expiration date, injecting these into the AVD's browser via ADB commands for precise testing of web apps requiring specific cookies. Similarly, the browser history script manages predefined entries such as URLs, titles, and timestamps in a structured format, updating the AVD's history database to ensure consistent and accurate browsing histories for efficient testing. These automations streamline testing workflows by saving time, maintaining reliability, and enhancing accuracy in setting up essential testing environments for web applications.

# 10. Clipboard Operations:
Python script for Android Virtual Devices (AVDs) that automates clipboard operations by copying specified text programmatically. The script prompts users to input text for copying, utilizing ADB commands to interact with the AVD and ensure accurate placement into the clipboard. This functionality is invaluable for testing applications dependent on clipboard operations, offering customization for diverse testing scenarios and streamlining testing workflows by saving time through automation. This capability enhances testing efficiency by facilitating precise and efficient testing of clipboard-dependent functionalities in AVDs.

# 11. Integration:
Integrates all above processes into cohesive scripts.


