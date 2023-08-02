"""
This package is for appending the pickled object with a metadata with a fixed length (16).
We can prepend the pickele with some bytes (encoded string) so we can know what is the received bytes are for
It can be benificial to identify the byte and to know if we can unpickle it
"""
META_WIDTH = 16
def make_packet(meta_data: str, data: bytes = None) -> bytearray:
    packet = bytearray(f"{meta_data:-<{META_WIDTH}}".encode())
    if data:
        packet.extend(data)

    return packet
