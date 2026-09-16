import struct
MAX_MESSAGE_SIZE = 10 * 1024 * 1024
HEADER_FORMAT = "!II"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)


def recv_exact(sock, size):

    data = b""
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if chunk == b"":
            raise ConnectionError("Соединение закрыто до получения всех данных")
        data += chunk
    return data


def send_message(sock, command: str, payload: bytes = b""):
    command_bytes = command.encode("utf-8")
    header = struct.pack(HEADER_FORMAT, len(command_bytes), len(payload))
    sock.sendall(header + command_bytes + payload)


def recv_message(sock):
    try:
        header = recv_exact(sock, HEADER_SIZE)
    except ConnectionError:
        return None

    cmd_len, payload_len = struct.unpack(HEADER_FORMAT, header)

    if payload_len > MAX_MESSAGE_SIZE:
        raise ValueError(f"Слишком большое сообщение: {payload_len} байт")

    command_bytes = recv_exact(sock, cmd_len) if cmd_len > 0 else b""
    payload = recv_exact(sock, payload_len) if payload_len > 0 else b""

    command = command_bytes.decode("utf-8")
    return command, payload
