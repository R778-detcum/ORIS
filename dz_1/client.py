import socket
import protocol as proto

HOST = "127.0.0.1"
PORT = 5555


def receive_response(sock):
    msg = proto.recv_message(sock)
    if msg is None:
        print("[!] Соединение с сервером потеряно")
        return False

    command, payload = msg
    text = payload.decode("utf-8", errors="replace")

    if command == "ERRO":
        print(f"[ошибка] {text}")
    else:
        print(text)

    return True


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((HOST, PORT))
    except (ConnectionRefusedError, OSError) as e:
        print(f"Не удалось подключиться: {e}")
        return

    print("Доступные команды:")
    print("  /add <текст>  - добавить задачу")
    print("  /list         - показать задачи")
    print("  /done <номер> - отметить выполненной")
    print("  /quit         - выйти")

    try:
        while True:
            line = input("> ").strip()

            if not line:
                continue

            if line == "/quit":
                proto.send_message(sock, "QUIT")
                receive_response(sock)
                break

            elif line == "/list":
                proto.send_message(sock, "LIST")
                if not receive_response(sock):
                    break

            elif line.startswith("/add "):
                text = line[5:].strip()
                proto.send_message(sock, "ADD", text.encode("utf-8"))
                if not receive_response(sock):
                    break

            elif line == "/add":
                proto.send_message(sock, "ADD", b"")
                if not receive_response(sock):
                    break

            elif line.startswith("/done "):
                num = line[6:].strip()
                proto.send_message(sock, "DONE", num.encode("utf-8"))
                if not receive_response(sock):
                    break

            elif line == "/done":
                proto.send_message(sock, "DONE", b"")
                if not receive_response(sock):
                    break

            else:
                print("Неизвестная команда. Используйте /add, /list, /done, /quit")

    except (EOFError, KeyboardInterrupt, BrokenPipeError, OSError):
        print("\n[!] Завершение работы")
    finally:
        sock.close()


if __name__ == "__main__":
    main()