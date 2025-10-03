from typing import List, Tuple

def parse(packet: bytes) -> Tuple[str, int, List[int]]:
    """
    Parse a hex-encoded 32-byte ASCII frame produced by generate() into
    (name, sequence_id, data_array).

    READ CUSTOM UART PROTOCOL FROM NOTION:
    """

    # Convert hex-encoded ASCII back to raw bytes

    # Split up the packet into its components

    # Validate the packet start stop and crc

    # Decode sensor name
    name = 

    # Decode sequence id
    seq =

    # Decode timestamp (for fun)

    # Parse payload (hint: mm Xdddd Ydddd Zdddd)
    # Example: b"00X0123Y0456Z7890"
    x_val =
    y_val =
    z_val =

    # Create data array
    data_array = [x_val, y_val, z_val]

    return name, seq, data_array