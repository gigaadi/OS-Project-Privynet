import socket
import tkinter as tk
from tkinter import messagebox, scrolledtext

HOST = 'YOUR IPV4 address' #same as in the server.py file
PORT = 5001 #same as in the server.py file

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
user_role = None

def send_data(data):
    client.send(data.encode())
    response = client.recv(4096).decode()
    return response

def authenticate():
    global user_role
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Username and Password are required")
        return

    message = f"{username}::{password}"
    client.send(message.encode())
    response = client.recv(1024).decode()

    if "Authentication successful" in response:
        _, role = response.split("::")
        user_role = role
        messagebox.showinfo("Success", f"Authenticated as {role}")
        show_commands(role)
    else:
        messagebox.showerror("Error", "Authentication failed")
        root.destroy()

def show_commands(role):
    auth_frame.pack_forget()
    command_frame.pack()

    list_button.config(state=tk.NORMAL)
    read_button.config(state=tk.NORMAL)

    if role == "admin":
        create_button.config(state=tk.NORMAL)
        delete_button.config(state=tk.NORMAL)

def list_files():
    response = send_data("LIST::")
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Files:\n{response}")

def create_file():
    filename = filename_entry.get()
    content = content_entry.get()
    if not filename or not content:
        messagebox.showerror("Error", "Filename and Content required")
        return
    response = send_data(f"CREATE::{filename}::{content}")
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, response)

def read_file():
    filename = filename_entry.get()
    if not filename:
        messagebox.showerror("Error", "Filename required")
        return
    response = send_data(f"READ::{filename}")
    output_text.delete('1.0', tk.END)
    output_text.insert(tk.END, f"Content of {filename}:\n\n{response}")

def delete_file():
    filename = filename_entry.get()
    if not filename:
        messagebox.showerror("Error", "Filename required")
        return
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{filename}'?")
    if confirm:
        response = send_data(f"DELETE::{filename}")
        output_text.delete('1.0', tk.END)
        output_text.insert(tk.END, response)

# GUI
root = tk.Tk()
root.title("PrivyNet File Client")

auth_frame = tk.Frame(root)
tk.Label(auth_frame, text="Username:").pack()
username_entry = tk.Entry(auth_frame)
username_entry.pack()

tk.Label(auth_frame, text="Password:").pack()
password_entry = tk.Entry(auth_frame, show="*")
password_entry.pack()

tk.Button(auth_frame, text="Authenticate", command=authenticate).pack(pady=5)
auth_frame.pack(pady=10)

command_frame = tk.Frame(root)

tk.Label(command_frame, text="Filename:").pack()
filename_entry = tk.Entry(command_frame)
filename_entry.pack()

tk.Label(command_frame, text="Content (for create):").pack()
content_entry = tk.Entry(command_frame)
content_entry.pack()

list_button = tk.Button(command_frame, text="List Files", command=list_files, state=tk.DISABLED)
list_button.pack(pady=2)

create_button = tk.Button(command_frame, text="Create File", command=create_file, state=tk.DISABLED)
create_button.pack(pady=2)

read_button = tk.Button(command_frame, text="Read File", command=read_file, state=tk.DISABLED)
read_button.pack(pady=2)

delete_button = tk.Button(command_frame, text="Delete File", command=delete_file, state=tk.DISABLED)
delete_button.pack(pady=2)

output_text = scrolledtext.ScrolledText(command_frame, width=60, height=15)
output_text.pack(pady=10)

root.mainloop()
