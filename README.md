# RWU NFC Verification Server & IoT Gateway

This repository contains the full source code for a secure, end-to-end NFC access control system. Built with **Django 6.0**, this project serves as a centralized gateway that manages encrypted authentication from hardware sensors and orchestrates responses across an IoT ecosystem.

---

## 🏗️ System Architecture

The project is designed as a distributed system with three primary layers:

1. **The Gateway (Raspberry Pi/Central Server):** A Django-based hub that manages authorized credentials, logs access attempts, and hosts a live monitoring dashboard.
2. **The Sensor Bridge:** A Python script (e.g., `nano_to_pi_bridge.py`) that interfaces with physical hardware (like an Arduino/Nano) to read NFC tags. It encrypts the raw UID and transmits it to the Gateway.
3. **The Appliance Ecosystem:** Simulated or physical IoT devices that poll the server for authorization status or listen for webhooks to trigger real-world actions (e.g., unlocking a door or activating a coffee machine).

---

## 🚀 Key Features

* **AES-128 Encryption:** All communication between hardware sensors and the server is secured using AES-128 (ECB mode) with a shared secret, preventing plain-text "sniffing" of NFC UIDs on the network.
* **Live Admin Dashboard:** A web-based interface that provides real-time visibility into access logs, authorization status, and system activity.
* **Dynamic Webhooks:** Automatically dispatches POST requests to external IP addresses upon successful authorization, enabling integration with third-party IoT devices.
* **Remote Appliance Terminal:** Includes a dedicated UI (`/remote/`) to send custom text commands directly to authenticated appliance nodes.
* **Robust Logging:** Every scan attempt—authorized or denied—is stored in a SQLite3 database for security auditing.

---

## 📁 Repository Breakdown

### **Core Gateway (Django App)**

* **`core/crypto_utils.py`**: Contains the logic for AES encryption and decryption, ensuring secure payload handling.
* **`core/models.py`**: Defines `Keycard` (authorized users) and `AccessLog` (historical scans) database tables.
* **`core/views.py`**: The "brain" of the server. It handles the `/verify/` API, manages global system states, and fires webhooks.
* **`core/templates/`**: HTML dashboards for system monitoring (`dashboard.html`) and remote command input (`remote.html`).

### **Hardware & Simulation (Laptop/Bridge)**

* **`nano_to_pi_bridge.py`**: A high-speed bridge that reads NFC data from a Serial port (Arduino), encrypts it, and posts it to the Pi.
* **`appliance_cli.py`**: A terminal-based "Locked/Unlocked" interface that mimics a secure appliance responding to the server's state.
* **`appliances.py`**: A Flask-based simulator that acts as multiple IoT nodes (Alpha & Beta) to demonstrate webhook reception.
* **`simulate_swipe.py`**: A utility to test the server's verification logic without requiring physical hardware.

---

## 🛠️ Setup & Installation

### 1. Environment Configuration

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/iamunblemished/rwu_nfc_presentation.git
cd rwu_nfc_presentation
python3 -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate
pip install -r requirements.txt

```

### 2. Secure Secrets (`.env`)

You **must** create a `.env` file in the root directory to store sensitive keys:

```text
DJANGO_SECRET_KEY='your-random-django-key'
SHARED_SECRET_KEY='1234567890123456'  # Must be exactly 16 characters

```

### 3. Database Initialization

```bash
python manage.py migrate
python manage.py createsuperuser  # Create your admin credentials

```

### 4. Running the System

To launch the server and the bridge sensor simultaneously on the Raspberry Pi:

```bash
chmod +x start_demo.sh
./start_demo.sh

```

---

## 🧠 Logical Workflow

1. **Detection:** A physical NFC tag is tapped against the reader.
2. **Bridge Processing:** The `nano_to_pi_bridge.py` script captures the UID, encrypts it using the `SHARED_SECRET_KEY`, and sends a POST request to `/verify/`.
3. **Authentication:** The Gateway decrypts the payload. It checks the `Keycard` database for a matching, active UID.
4. **Action:**
* If **Valid**: `is_authorized_state` is set to `True`, a success log is created, and webhooks are fired to external nodes.
* If **Invalid**: A denial log is created, and the system remains locked.


5. **Feedback:** The `appliance_cli.py` (polling the server) detects the authorization change and updates its UI from "LOCKED" to "UNLOCKED."

---

## 🔒 Security Note

This implementation uses **AES-ECB** for simplicity during this presentation. For production environments, it is recommended to upgrade to **AES-GCM** with a unique Initialization Vector (IV) for every scan to prevent replay attacks.

**Author:** [iamunblemished]

**Project:** RWU NFC Presentation Gateway
