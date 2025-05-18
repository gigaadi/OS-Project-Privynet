# OS-Project-Privynet: A Role-Centric Client-Server File Access System with Two-Factor Authentication

## 🔐 Project Overview

This project implements a **client-server architecture** for secure file access based on **user roles** with an added layer of **Two-Factor Authentication (2FA)**. The system ensures that only authorized users can connect to the server, authenticate themselves, and access permitted files or services.

## 📌 Key Features

- 🔑 **User Authentication** using JSON-stored credentials
- 🛂 **Role-Based Access Control (RBAC)** for fine-grained permissions
- 🔐 **Two-Factor Authentication (2FA)** using One-Time Password (OTP)
- 🔒 **Password Hashing** for secure credential storage *(in progress)*
- 📁 **File Access Management** based on user role
- 🌐 **Socket-based Client-Server Communication**
- ⚠️ **Basic Error Handling and Input Validation**
- 🧪 **Tested for various user roles and login flows**

## 🗂️ Project Structure

─ client.py # Client-side code with CLI for login and file access
─ server.py # Server-side logic for authentication and role enforcement
─ users.json # JSON file storing user credentials and roles
─ README.md # Project overview and instructions


## 🔧 How It Works

1. The client connects to the server using sockets.
2. The user logs in by providing a username and password.
3. The server checks the credentials and identifies the user's role.
4. Upon successful authentication, the user is prompted for an OTP (2FA).
5. Access is granted only if both password and OTP are valid.
6. Role-specific actions and file access permissions are enforced.

## 🧪 Current Progress

- ✅ Basic client-server communication
- ✅ User authentication and role recognition
- 🚧 2FA (OTP) module in development
- 🚧 Role-based file access in progress
- ⏳ Secure TLS communication (planned)
- ⏳ Password hashing (planned)

## 📋 Future Enhancements

- 🔐 Integration with email/SMS services for OTP delivery
- 🔒 TLS/SSL encryption for socket communication
- 🗄️ Switch from JSON to database (e.g., SQLite or MongoDB)
- 🧠 Logging and user activity auditing
- 🖥️ GUI client interface

## 👨‍💻 Team Members

- **Vijay Singh** – Secure communication & error handling
- **Yash Khati** – Role access and CLI interface
- **Kavya Mittal** – 2FA logic and authentication
- **Aaditya Kumar** – Password hashing & testing

## 📃 License

This project is licensed under the Graphic Era institutions License.
