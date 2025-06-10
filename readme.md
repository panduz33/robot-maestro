# 📡 Robot Framework Wi-Fi Testing (Raspberry Pi / Linux / macOS)

This project performs automation testing using **Robot Framework** on Linux-based systems such as **Raspberry Pi** 

---

## 🛠️ Setup Instructions

### 1. **Clone the Repository**

```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

---

### 2. **Create & Activate a Python Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# OR (for Windows)
venv\Scripts\activate
```

---

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

---

### 4. **Create the `.env` File**

Create a `.env` file in the project root:

```
SSID=Your_Wifi_SSID
WIFI_PASSWORD=Your_Wifi_Password
EXPECTED_SSID=Expected_Wifi_SSID
```

> ⚠️ This file is ignored by Git (`.gitignore`) for security reasons.

---

### 5. **Install Required System Packages**

For Raspberry Pi or Linux systems:
```bash
sudo apt update
sudo apt install wireless-tools network-manager
```

---

### 6. **Run the Robot Framework Tests**

```bash
robot tests/
```

Or to run a specific file:

```bash
robot tests/your_test.robot
```

---

## 📂 Project Structure

```
.
├── .env               # Environment variables (not committed)
├── .gitignore
├── requirements.txt
├── README.md
├── load_env.py        # Python helper to load .env
├── tests/
│   └── wifi_test.robot
├── resources/
│   └── wifi_keywords.robot
```

---

## ❗ Notes

- Ensure **Python 3.8+** is installed.
- **Do not push the `.env` file** — it's excluded via `.gitignore`.
- This test suite is designed for **Linux (Raspberry Pi)** only.

---

## 🤝 Contribution Guide

1. Fork the repo.
2. Create feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes.
4. Push to the branch.
5. Open a pull request.
