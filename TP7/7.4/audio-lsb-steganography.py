import struct
import wave


def payload(msg: bytes) -> bytes:
    message_length = len(msg)
    message_length_bytes = struct.pack(">I", message_length)
    return message_length_bytes + msg


def extract_bit(byte: int, n: int) -> int:
    return (byte >> n) & 1


def lsb_to_byte(sequence: bytes) -> int:
    byte = 0
    for i in range(8):
        byte |= (sequence[i] & 1) << i
    return byte


def encode(msg: bytes, input_file: str, output_file: str):
    with wave.open(input_file, "rb") as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    msg_with_length = payload(msg)
    message_bin = "".join(format(byte, "08b") for byte in msg_with_length)

    if len(message_bin) > len(frames):
        raise ValueError("The input file is not large enough to hold the message.")

    for i in range(len(message_bin)):
        frames[i] = (frames[i] & 0xFE) | int(message_bin[i])

    with wave.open(output_file, "wb") as audio_result:
        audio_result.setparams(audio.getparams())
        audio_result.writeframes(bytes(frames))


def decode(input_file: str) -> bytes:
    with wave.open(input_file, "rb") as audio:
        frames = bytearray(list(audio.readframes(audio.getnframes())))

    length_bits = [frames[i] & 1 for i in range(32)]
    length_bytes = bytearray()
    for i in range(0, 32, 8):
        length_bytes.append(lsb_to_byte(length_bits[i : i + 8]))
    message_length = struct.unpack(">I", length_bytes)[0]

    message_bits = [frames[i] & 1 for i in range(32, 32 + message_length * 8)]
    message_bytes = bytearray()
    for i in range(0, len(message_bits), 8):
        message_bytes.append(lsb_to_byte(message_bits[i : i + 8]))

    return bytes(message_bytes)


message = b"Hi"
input_file = "input.wav"
output_file = "output.wav"
encode(message, input_file, output_file)

decoded_message = decode(output_file)
print(decoded_message.decode())
