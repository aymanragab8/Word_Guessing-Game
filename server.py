import socket
import tkinter as tk
import tkinter.messagebox as messagebox
import random
import threading

class ServerGUI:
    def __init__(self, top):
        self.master = top
        self.master.title("Server")
        self.master.configure(bg="lightblue")  # Set background color of the window

        self.label = tk.Label(top, text="Enter words (separated by commas)", bg="lightblue", fg="black")
        self.label.pack()

        self.label_message = tk.Label(top, text="You Must Enter Capital Words :)", bg="lightblue", fg="black")
        self.label_message.pack()

        self.words_entry = tk.Entry(top, width=50, bg="white", fg="black")
        self.words_entry.pack()

        self.start_button = tk.Button(top, text="Start Server", command=self.start_server, bg="lightgray", fg="black")
        self.start_button.pack()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = '127.0.0.1'
        self.PORT = 5050
        self.client_threads = []  # List to store client threads

    def start_server(self):
        words = self.words_entry.get().split(',')
        if not words[0]:  # Check if no words are entered
            messagebox.showerror("Error", "You must enter at least one word.")
            return

        # Check if all words are capitalized
        if not all(word.strip().isupper() for word in words):
            messagebox.showerror("Error", "Enter Capital Words Only")
            return

        self.server_socket.bind((self.HOST, self.PORT))
        self.server_socket.listen()

        while True:
            client_socket, _ = self.server_socket.accept()
            # Create a new thread to handle the client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, words))
            client_thread.start()
            self.client_threads.append(client_thread)

    def handle_client(self, client_socket, words):
        chosen_word = random.choice(words).strip()
        print("Chosen word:", chosen_word)
        client_socket.sendall(chosen_word.encode())
        client_socket.close()

def main():
    root = tk.Tk()
    server_gui = ServerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
