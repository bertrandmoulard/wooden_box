import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import subprocess
import time

# Set up I2C connection
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Get firmware version to verify the connection
ic, ver, rev, support = pn532.firmware_version
#  print(f"Found PN532 with firmware version {ver}.{rev}")

# Configure the PN532 to read MiFare cards
pn532.SAM_configuration()

#  print("Listening for NFC tags...")
decoded_text = None

while True:
    try:
        # Wait for an NFC card
        uid = pn532.read_passive_target(timeout=1)
        if uid is not None:
            #  print(f"Tag detected! UID: {uid.hex()}")

            # Read raw data from memory blocks
            raw_data = b""
            for block in range(4, 16):  # Adjust range based on tag size
                block_data = pn532.ntag2xx_read_block(block)
                if block_data:
                    raw_data += block_data
                else:
                    break

            # Debug: Print raw data
            #  print(f"Raw Data (Hex): {raw_data.hex()}")

            # Manually decode the custom-written content
            try:
                # Locate NDEF TLV (starts with 0x03)
                ndef_start = raw_data.find(b'\x03')
                if ndef_start == -1:
                    print("No NDEF TLV found in the tag.")
                    continue

                # Extract the payload length
                ndef_length = raw_data[ndef_start + 1]
                ndef_payload = raw_data[ndef_start + 2:ndef_start + 2 + ndef_length]

                #  print(f"NDEF Payload (Hex): {ndef_payload.hex()}")

                # Decode the payload as a string
                try:
                    new_decoded_text = ndef_payload.decode('utf-8')
                    if decoded_text != new_decoded_text:
                        decoded_text = new_decoded_text
                        #  print(f"New Tag Content: {decoded_text}")

                        # Command to run
                        command = ["python3", "wooden_box.py", "play", decoded_text]

                        # Run the command
                        try:
                            result = subprocess.run(command, check=True, text=True, capture_output=True)
                            print(f"Playing album {decoded_text}")
                            print(f"Command Output:\n{result.stdout}")
                        except subprocess.CalledProcessError as e:
                            print(f"Command failed with error:\n{e.stderr}")

                except UnicodeDecodeError:
                    print("Payload is not valid UTF-8.")
                    print(f"Raw Payload: {ndef_payload.hex()}")

            except Exception as e:
                print(f"Error manually decoding the tag content: {e}")

        else:
            #  print("No tag detected.")
            if decoded_text != None:
                # Command to run
                command = ["python3", "wooden_box.py", "pause", decoded_text]

                # Run the command
                try:
                    result = subprocess.run(command, check=True, text=True, capture_output=True)
                    print(f"Pausing")
                    print(f"Command Output:\n{result.stdout}")
                except subprocess.CalledProcessError as e:
                    print(f"Command failed with error:\n{e.stderr}")
            decoded_text = None

        # Delay before the next scan
        time.sleep(1)

    except Exception as e:
        print(f"Error reading tag: {e}")
