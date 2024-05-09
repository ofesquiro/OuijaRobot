import os
import subprocess
def is_windows_SO():
    return os.name == 'nt'
def gatherInputDeviceInfo():
    if is_windows_SO():
        response = device_info_in_windows()
        if response is not None:
            print(getIdFromResponse(response))
            return getIdFromResponse(response)
def device_info_in_windows():
    command = "wmic sounddev get DeviceID,Name"
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("no response")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def getIdFromResponse(response):
    usb_input_ids = []
    lines = response.split('\n')
    for line in lines[1:]:
        if "USB" in line:  # Check if the line contains "USB"
            parts = line.split('  ')
            for part in parts:
                if part.startswith("USB"):
                    usb_input_ids.append(part.strip())
    return usb_input_ids

def device_info_in_linux():
    print()
def main():
    return gatherInputDeviceInfo()[0]

main()