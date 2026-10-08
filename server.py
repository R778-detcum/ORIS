import socket
import threading
from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 9090

clients = {}
clients_lock = threading.Lock()


def broadcast(sender_sock, command, payload):
    with clients_lock:
        targets = [(s, name) for s, name in clients.items() if s != sender_sock]

    for sock, _ in targets:
        try:
            send_message(sock, command, payload)
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass


def remove_client(sock):
    with clients_lock:
        username = clients.pop(sock, None)

    if username:
        print(f"[СЕРВЕР] {username} отключился")
        broadcast(sock, "SYSTEM", f"{username} покинул чат".encode("utf-8"))


def handle_client(sock, addr):
    username = None
    try:
        msg = recv_message(sock)
        if msg is None:
            return
        command, payload = msg
        if command != "JOIN":
            send_message(sock, "ERROR", b"First command must be JOIN")
            return

        username = payload.decode("utf-8").strip()
        if not username:
            send_message(sock, "ERROR", b"Empty username")
            return

        with clients_lock:
            clients[sock] = username

        print(f"[СЕРВЕР] {username} подключился ({addr})")
        send_message(sock, "SYSTEM", f"Добро пожаловать, {username}!".encode("utf-8"))
        broadcast(sock, "SYSTEM", f"{username} присоединился к чату".encode("utf-8"))

        while True:
            msg = recv_message(sock)
            if msg is None:
                print(f"[СЕРВЕР] {username} закрыл соединение")
                break

            command, payload = msg

            if command == "TEXT":
                text = payload.decode("utf-8")
                print(f"[СЕРВЕР] {username}: {text}")
                broadcast(sock, "TEXT", f"{username}: {text}".encode("utf-8"))

            elif command == "LIST":
                with clients_lock:
                    names = ", ".join(clients.values())
                send_message(sock, "LIST", names.encode("utf-8"))

            elif command == "QUIT":
                print(f"[СЕРВЕР] {username} вышел через QUIT")
                send_message(sock, "SYSTEM", b"Bye!")
                break

            else:
                send_message(sock, "ERROR", f"Unknown command: {command}".encode("utf-8"))

    except ConnectionResetError:
        print(f"[СЕРВЕР] {username or addr} оборвал соединение (ConnectionResetError)")
    except BrokenPipeError:
        print(f"[СЕРВЕР] {username or addr}: сломанный канал (BrokenPipeError)")
    except (ConnectionError, ValueError) as e:
        print(f"[СЕРВЕР] Ошибка у {username or addr}: {e}")
    finally:
        remove_client(sock)
        try:
            sock.close()
        except OSError:
            pass


def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    print(f"[СЕРВЕР] Запущен на {HOST}:{PORT}")

    try:
        while True:
            client_sock, addr = server_sock.accept()
            print(f"[СЕРВЕР] Новое подключение: {addr}")
            thread = threading.Thread(target=handle_client, args=(client_sock, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n[СЕРВЕР] Остановка...")
    finally:
        server_sock.close()


if __name__ == "__main__":
    main()
