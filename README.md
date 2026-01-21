# RWU NFC Verification Server & Appliance Controller

This project is a secure IoT Gateway built with **Django 6.0** and designed to run on a **Raspberry Pi 3B+**. It acts as the central "brain" for an NFC access control system, using **AES-128 encryption** to communicate with hardware nodes and control external appliances.

## 🚀 System Architecture

The system is split into three main parts:

1. **The Gateway (This Server):** Manages the database of authorized cards, processes encrypted scans, and provides a web dashboard.
2. **The Bridge (`bridge_sensor.py`):** A script that interface with the physical NFC reader, encrypts the data, and sends it to this server.
3. **The Appliance Node:** A remote CLI or hardware device (like lights or a coffee machine) that polls this server to see if it should "unlock" or perform an action based on a successful scan.

## 📁 Detailed Code Breakdown

### 1. The Security Layer (`core/views.py` & `core/crypto_utils.py`)

The system uses a **Shared Secret** approach for security.

* **AES-128 Encryption:** Incoming data is not sent in plain text. The hardware node must encrypt the NFC UID using the `SHARED_SECRET_KEY` before sending it to the `/verify/` endpoint.
* **Decryption:** The server uses `PyCryptodome` to decrypt the payload, ensuring that even if a bad actor sniffs your network traffic, they cannot see the actual ID of your keycards.

### 2. The Database (`core/models.py`)

* **Keycards:** This table stores the unique IDs of allowed tags and their owners. Access is only granted if a scanned UID exists here and is marked as `is_active`.
* **Access Logs:** Every single scan attempt—whether granted or denied—is recorded with a timestamp for security auditing.

### 3. The API Endpoints (`core/urls.py`)

* **`/verify/`**: The hardware bridge posts encrypted payloads here to request access.
* **`/appliance-msg/`**: Used by the remote "Appliance Node" (CLI). It polls this endpoint to check if the system is currently `authorized` and to receive custom messages sent from the server.
* **`/dashboard/`**: A web UI for the user to monitor all activity in real-time.
* **`/remote/`**: A "Terminal Input" page where you can type a message to be displayed on the remote appliance's CLI.

### 4. Automation & Webhooks

When a valid card is swiped, the server doesn't just unlock itself; it can trigger external devices. The `fire_webhooks` function is configured to send POST requests to other IP addresses on your network (e.g., smart lights or coffee machines) the moment access is granted.

## 🛠 Setup & Installation

### 1. Clone and Prepare

```bash
git clone https://github.com/iamunblemished/rwu_nfc_presentation.git
cd rwu_nfc_presentation
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

```

### 2. Configuration (`.env`)

Create a `.env` file in the root directory. You must define your keys here to keep them secure:

```text
DJANGO_SECRET_KEY='your-private-key'
SHARED_SECRET_KEY='1234567890123456'  # 16-character key for AES

```

### 3. Execution

You can use the provided shell script to launch the bridge and the server simultaneously:

```bash
chmod +x start_demo.sh
./start_demo.sh

```

## 🧠 Logical Workflow

1. **NFC Tag Swiped** → `bridge_sensor.py` reads the UID.
2. **Encryption** → The bridge encrypts the UID and POSTs it to the server.
3. **Verification** → Server decrypts the UID and checks the `Keycard` database.
4. **Action** → If valid, the global `is_authorized_state` becomes `True`, webhooks are fired, and the `AccessLog` is updated.
5. **Remote Feedback** → The Appliance CLI (polling `/appliance-msg/`) sees the authorized state and unlocks.

---

**Project:** RWU NFC Presentation Gateway

**Developed by:** iamunblemished
