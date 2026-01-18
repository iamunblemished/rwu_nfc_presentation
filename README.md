# RWU NFC Verification Server

This project is a secure IoT Gateway built with **Django 6.0** on a **Raspberry Pi 3B+**. It serves as the central "brain" for an NFC-based access control system, using **AES-128 encryption** to verify identities from external microcontrollers before granting access to home products.

## 🚀 Features

* **Encrypted Handshake:** Uses AES-128 (ECB mode) to decrypt incoming UID payloads, preventing plain-text sniffing on the local network.
* **Live Access Dashboard:** A real-time web interface that displays scan attempts, timestamps, and authorization status.
* **Administrative Control:** Built-in management console to add/revoke authorized NFC tags and view historical access logs.
* **Secure Secrets:** Sensitive keys (Django Secret Key and AES Shared Secret) are managed via environment variables to keep them off GitHub.

## 🛠 Tech Stack

* **Framework:** Django 6.0
* **Security:** PyCryptodome (AES Encryption)
* **Database:** SQLite3
* **Frontend:** HTMX (for live log updates)

---

## 💻 Installation & Setup

Your teammate should follow these steps to get the server running on their own machine or Pi:

### 1. Clone and Prepare Environment

```bash
git clone https://github.com/iamunblemished/rwu_nfc_presentation.git
cd rwu_nfc_presentation

# Create and activate virtual environment
python3 -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

```

### 2. Configure Environment Variables

You **must** create a `.env` file in the root directory (where `manage.py` is located) for the project to start.

```bash
nano .env

```

Add the following content:

```text
DJANGO_SECRET_KEY='your-random-django-key'
SHARED_SECRET_KEY='1234567890123456'  # Must be exactly 16 characters

```

### 3. Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser  # Create your admin login

```

### 4. Run the Server

```bash
python manage.py runserver 0.0.0.0:8000

```

---

## 🔍 Usage

### Accessing the Interface

* **Admin Panel:** `http://localhost:8000/admin/` (Manage authorized UIDs here).
* **Live Dashboard:** `http://localhost:8000/dashboard/` (Monitor scans).

### Verification API

The hardware (or simulation script) sends an encrypted POST request to:
`POST /verify/`
**Payload Format:**

```json
{
    "payload": "Base64_Encrypted_String"
}

```

### Testing with Simulation

To test the server without hardware, run the `simulate_swipe.py` script included in the repo:

```bash
python simulate_swipe.py

```

---

## 🔒 Security Note

This project uses a **Shared Secret** approach for simplicity in this presentation. In a production environment, it is recommended to transition to **AES-CBC or GCM mode** with a unique Initialization Vector (IV) for every scan to prevent replay attacks.

**Author:** [Your Name / iamunblemished]
**Project:** RWU NFC Presentation Gateway
