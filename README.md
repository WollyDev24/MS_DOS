# **DOS-E Emulator**
A lightweight Python-based **simulated DOS environment**

## ⭐ Overview
DOS-E is **not** a real DOS emulator. Instead, it **simulates** classic DOS behavior using Python while keeping everything inside a folder called `VIRTUAL_DRIVE`. 

## 🎯 Features
- 📁 **Virtual File System** inside `VIRTUAL_DRIVE`
- 📂 Classic file commands: `DIR`, `CD`, `MD`, `RD`, `COPY`, `DEL`, `REN`
- 📄 `TYPE` command for reading text files
- 🧮 Built-in **calculator** (`CALC`)
- 📝 Real Windows **Notepad integration**
- 🎮 Mini-game: **Guess the Number**
- 💻 System info commands: `VER`, `SYSINFO`, `DATE`, `TIME`
- 🎨 Customizable **command prompt**
- 🔒 Reserved DOS filenames protected

---

## 🧰 Installation

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/wollydev24/MS_DOS
cd MS_DOS
```

### **2️⃣ Run the emulator**
```bash
py(thon(3)) dos.py
```

> ✔ Requires **Python 3.8+**  
> ✔ Works on Windows, Linux, and macOS

---

## 🖥️ Commands

| Command | Description |
|--------|-------------|
| `DIR [path]` | List directory contents |
| `CD [path]` | Change directory |
| `MD`, `MKDIR` | Create folder |
| `RD`, `RMDIR` | Remove *empty* folder |
| `TYPE file` | Display a text file |
| `COPY src dst` | Copy a file |
| `DEL`, `ERASE` | Moves file to `VIRTUAL_DRIVE/$TRASH` |
| `REN old new` | Rename file or folder |
| `CLS` | Clear the screen |
| `DATE` | Show simulated date |
| `TIME` | Show simulated time |
| `VER` | Show DOS-E version |
| `PROMPT text` | Set command prompt |
| `SYSINFO` | Show system info |
| `TRASH` | Show trash content |
| `CLEARTRASH` | Empty the trash |
| `CALC` | Mini calculator mode |
| `NOTEPAD file` | Open file in system Notepad |
| `GAME` | Number guessing game |
| `EXIT` | Quit the emulator |

---

## 📂 Virtual Drive Layout

```
VIRTUAL_DRIVE/
│
├── FILES/
│   └── README.TXT
│
└── $TRASH/
```

---

## 🔧 Configuration Constants

| Variable | Purpose |
|---------|---------|
| `VERSION` | Emulator version string |
| `COMPUTERNAME` | Fake system computer name |
| `OSNAME` | Fake OS name |
| `OWNER` | Copyright owner |
| `PROMPT` | Default command prompt |

---
