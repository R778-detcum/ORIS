import socket
import threading
import sys
from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 9090


def listen_server(sock):
    try:
        while True:
            msg = recv_message(sock)
            if msg is None:
                print("\n[КЛИЕНТ] Сервер закрыл соединение")
                break
            command, payload = msg
            text = payload.decode("utf-8", errors="replace")
            if command == "TEXT":
                print(f"\n{text}")
            elif command == "SYSTEM":
                print(f"\n[СИСТЕМА] {text}")
            elif command == "LIST":
                print(f"\n[СПИСОК] {text}")
            elif command == "ERROR":
                print(f"\n[ОШИБКА] {text}")
            else:
                print(f"\n[{command}] {text}")
    except (ConnectionResetError, ConnectionError, OSError):
        print("\n[КЛИЕНТ] Соединение потеряно")
    finally:
        try:
            sock.close()
        except OSError:
            pass
        sys.exit(0)


def main():
    if len(sys.argv) < 2:
        print("Использование: python client.py <username>")
        return

    username = sys.argv[1]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("[КЛИЕНТ] Не удалось подключиться к серверу")
        return

    # Отпр JOIN
    send_message(sock, "JOIN", username.encode("utf-8"))

    listener = threading.Thread(target=listen_server, args=(sock,), daemon=True)
    listener.start()

    print(f"[КЛИЕНТ] Вы вошли как {username}. Команды: текст, /list, /quit")
    print("Введите сообщение и нажмите Enter:")

    try:
        while True:
            line = input()
            if not line:
                continue

            if line.strip() == "/quit":
                send_message(sock, "QUIT")
                print("[КЛИЕНТ] Выход...")
                break
            elif line.strip() == "/list":
                send_message(sock, "LIST")
            else:
                send_message(sock, "TEXT", line.encode("utf-8"))

    except (KeyboardInterrupt, EOFError):
        print("\n[КЛИЕНТ] Прервано пользователем")
    except (BrokenPipeError, ConnectionResetError):
        print("\n[КЛИЕНТ] Соединение потеряно при отправке")
    finally:
        try:
            sock.close()
        except OSError:
            pass


if __name__ == "__main__":
    main()
