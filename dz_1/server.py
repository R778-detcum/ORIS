import socket
import threading
import protocol as proto

HOST = "127.0.0.1"
PORT = 5555

tasks = []
tasks_lock = threading.Lock()


def send_text(sock, text):
    proto.send_message(sock, "TEXT", text.encode("utf-8"))


def send_error(sock, text):
    proto.send_message(sock, "ERRO", text.encode("utf-8"))


def handle_client(sock, addr):
    print(f"[+] Клиент подключился: {addr}")
    try:
        while True:
            msg = proto.recv_message(sock)
            if msg is None:
                break

            command, payload = msg

            if command == "ADD":
                text = payload.decode("utf-8", errors="replace").strip()
                if not text:
                    send_error(sock, "Текст задачи не может быть пустым")
                else:
                    with tasks_lock:
                        tasks.append({"text": text, "done": False})
                    send_text(sock, "Задача добавлена")

            elif command == "LIST":
                with tasks_lock:
                    if not tasks:
                        response = "Список задач пуст"
                    else:
                        lines = []
                        for i, task in enumerate(tasks, 1):
                            mark = "x" if task["done"] else " "
                            lines.append(f"{i}. [{mark}] {task['text']}")
                        response = "\n".join(lines)
                send_text(sock, response)

            elif command == "DONE":
                num_str = payload.decode("utf-8", errors="replace").strip()
                try:
                    num = int(num_str)
                except ValueError:
                    send_error(sock, "Некорректный номер задачи")
                    continue

                result = None
                with tasks_lock:
                    if num < 1 or num > len(tasks):
                        result = ("ERRO", "Задачи с таким номером не существует")
                    else:
                        tasks[num - 1]["done"] = True
                        result = ("TEXT", "Задача отмечена как выполненная")

                if result[0] == "TEXT":
                    send_text(sock, result[1])
                else:
                    send_error(sock, result[1])

            elif command == "QUIT":
                send_text(sock, "До свидания")
                break

            else:
                send_error(sock, "Неизвестная команда")

    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        sock.close()
        print(f"[-] Клиент отключился: {addr}")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] Сервер запущен на {HOST}:{PORT}")

        while True:
            client_sock, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(client_sock, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Сервер остановлен")