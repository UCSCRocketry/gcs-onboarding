from random import randint 
import struct
import sys
import time

'''
SENSOR ID:
HIGH_G_ACCEL:  ac  0x6163
'''

START_BYTE = b'!'  
END_BYTES = b'\r\n'  #CR (0x0D) and LF (0x0A)
CRC = b'XX'  ##verifies message content
SENSOR_ID = b'ah' #sensorID

def generate(sequence_id) -> bytes: 
    """
    Generates a 32-byte hex encoded High-G Accelerometer dummy packet based on the custom UART ASCII protocol.

    Args:
        sequence_id: the sequence id of the packet (use an incrimenter to incriment each packet) 

    Returns:
        bytes: 32-byte ASCII hex packet
    """
    # 4 bytes
    sequence_id_str = f'{sequence_id:04d}' 
    sequence_id_bytes = sequence_id_str.encode('ascii')
    
    # 4 byte
    cur_ms = int(time.time() * 1000) % 10000  #take last 4 dig of current ms as int
    timestamp_bytes = f'{cur_ms:04d}'.encode('ascii')

    # ---- 17 byte payload ----
    # low acceleration on X and Y (moving side to side)
    X = randint(0, 500)
    Y = randint(0, 500)

    # vertical direction (moving up and down -- thrust vector)
    Z = randint(5000, 9999)

    payload_str = f'{0:02d}X{X:04d}Y{Y:04d}Z{Z:04d}'
    payload_bytes = payload_str.encode('ascii')
    # --------


    # 32 byte per frame
    packet = (START_BYTE + sequence_id_bytes + SENSOR_ID + timestamp_bytes + payload_bytes + CRC + END_BYTES)

    if len(packet) != 32:
        raise ValueError(f"Packet length is worng. Needs to be 32 bytes, got {len(packet)}.")

    return packet.hex().encode('ascii')  #hex encoded packet
