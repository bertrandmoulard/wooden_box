import board
import busio
from digitalio import DigitalInOut
from adafruit_pn532.i2c import PN532_I2C
import time

# Set up I2C connection
i2c = busio.I2C(board.SCL, board.SDA)
pn532 = PN532_I2C(i2c, debug=False)

# Get firmware version to verify the connection
ic, ver, rev, support = pn532.firmware_version
print(f"Found PN532 with firmware version {ver}.{rev}")

# Configure the PN532 to read MiFare cards
pn532.SAM_configuration()

def write_tag(content):
    # Convert content to bytes
    content_bytes = content.encode('utf-8')
    
    # Create an NDEF-like TLV structure
    tlv = b'\x03' + bytes([len(content_bytes)]) + content_bytes + b'\xFE'  # NDEF TLV + terminator
    
    # Write the TLV to the NFC tag (block 4 onward for NTAG2xx)
    print("Writing to tag...")
    block = 4
    for i in range(0, len(tlv), 4):
        block_data = tlv[i:i+4]
        if len(block_data) < 4:
            block_data = block_data.ljust(4, b'\x00')  # Pad to 4 bytes if necessary
        pn532.ntag2xx_write_block(block, block_data)
        block += 1

    print("Content written successfully!")

def main():
    while True:
        # Prompt the user to input content
        content = input("Enter the content you want to write to the NFC tag: ")
        if not content:
            print("No content entered. Exiting...")
            break

        print("Waiting for an NFC tag...")
        while True:
            uid = pn532.read_passive_target(timeout=1)
            if uid is not None:
                print(f"Tag detected! UID: {uid.hex()}")
                write_tag(content)
                break
            else:
                print("No tag detected. Hold a tag near the reader...")

        # Ask if the user wants to write more content
        again = input("Do you want to write more content? (y/n): ").strip().lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()
