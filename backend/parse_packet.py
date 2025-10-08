from typing import List, Tuple

def parse(packet: bytes) -> Tuple[str, int, List[int]]:
    """
    Parse a hex-encoded 32-byte ASCII frame produced by generate() into
    (name, sequence_id, data_array).

    READ CUSTOM UART PROTOCOL FROM NOTION:
    """

    # Convert hex-encoded ASCII back to raw bytes
    try:
        raw_packet = bytes.fromhex(packet.decode('ascii'))
    except ValueError:
        raise ValueError("Invalid hex-encoded packet")

    # Split up the packet into its components
    # Format: !(start bit) + sequence_id(4) + sensor_id(2) + timestamp(4) + payload(17) + CRC(2) + \r\n(2)
    if len(raw_packet) != 32:
        raise ValueError(f"Invalid packet length: expected 32 bytes, got {len(raw_packet)}")
    
    # Extract each components of the packet: slicing!
    #   reminder: start index is inclusive, end index is exclusive
    start_byte = raw_packet[0:1]
    sequence_bytes = raw_packet[1:5]
    sensor_id_bytes = raw_packet[5:7]
    timestamp_bytes = raw_packet[7:11]
    payload_bytes = raw_packet[11:28]
    crc_bytes = raw_packet[28:30]
    end_bytes = raw_packet[30:32]

    # Validate the packet start stop and crc
    if start_byte != b'!':
        raise ValueError(f"Invalid start byte: expected '!', got {start_byte}")
    
    if end_bytes != b'\r\n':
        raise ValueError(f"Invalid end bytes: expected '\\r\\n', got {end_bytes}")
    
    # CRC validation (simplified - in real implementation you'd calculate and verify)
    if crc_bytes != b'XX':
        raise ValueError(f"Invalid CRC: expected 'XX', got {crc_bytes}")

    # Decode sensor name - hardcoded for now
    sensor_id = sensor_id_bytes.decode('ascii')
    if sensor_id == 'ah':
        name = 'HIGH_G_ACCEL'
    else:
        name = f'UNKNOWN_SENSOR_{sensor_id}'

    # Decode sequence id
    seq = int(sequence_bytes.decode('ascii'))

    # Decode timestamp (for fun)
    timestamp = int(timestamp_bytes.decode('ascii'))

    # Parse payload (hint: mm Xdddd Ydddd Zdddd)
    # Example: b"00X0123Y0456Z7890"
    payload_str = payload_bytes.decode('ascii')
    
    # 1. extract X, Y, Z values from payload format: mmXddddYddddZdddd
    if len(payload_str) != 17:
        raise ValueError(f"Invalid payload length - should be 17 chars, got {len(payload_str)}")
    
    # 2. find X, Y, Z markers
    x_pos = payload_str.find('X') #position of X
    y_pos = payload_str.find('Y') #position of Y
    z_pos = payload_str.find('Z') #position of Z
    
    # make sure all markers were found
    if x_pos == -1 or y_pos == -1 or z_pos == -1:
        raise ValueError("Invalid payload format: missing X, Y, or Z markers")
    
    # 3. extract values (4 digits each)
    x_val = int(payload_str[x_pos+1:x_pos+5])  
    y_val = int(payload_str[y_pos+1:y_pos+5])
    z_val = int(payload_str[z_pos+1:z_pos+5])

    # Create data array
    data_array = [x_val, y_val, z_val]

    return name, seq, data_array