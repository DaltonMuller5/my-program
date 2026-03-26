# DataPortal — Login Analytics Web App

A Flask web application with user authentication, Google OAuth, and a live login analytics dashboard.

---

## Requirements

- Python 3.8 or higher
- pip
- Internet connection (for Google Fonts and Google OAuth)

---

## Project Structure

```
my-program/
├── app.py
├── .env.example
├── .env              ← you create this (see step 3)
├── users.json        ← auto-created on first register
├── login_log.json    ← auto-created on first login
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    └── dashboard.html
```

---

## Setup & Run

### 1. Clone or download the project

```bash
git clone https://github.com/your-username/my-program.git
cd my-program
```

### 2. Install dependencies

```bash
pip install flask python-dotenv google-auth requests
```

### 3. Create your `.env` file

Copy the example file:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your values:

```
SECRET_KEY=any-long-random-string-you-choose
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

> If you don't need Google login, you can leave `GOOGLE_CLIENT_ID` empty. Email/password login will still work.

### 4. Run the app

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## Mock Credentials (for testing)

A default admin account is included out of the box:

| Field    | Value   |
|----------|---------|
| Username | `admin` |
| Password | `admin` |

You can also register a new account at `/register`.

---

## Google OAuth Setup (optional)

To enable "Continue with Google":

1. Go to [https://console.cloud.google.com](https://console.cloud.google.com)
2. Create a project (or select an existing one)
3. Navigate to **APIs & Services → Credentials**
4. Click **Create Credentials → OAuth 2.0 Client ID**
5. Set application type to **Web application**
6. Under **Authorized JavaScript origins**, add:
   ```
   http://localhost:5000
   ```
7. Copy the **Client ID** and paste it into your `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   ```
8. Restart the app

---

## Pages

| URL          | Description                              |
|--------------|------------------------------------------|
| `/`          | Home page                                |
| `/login`     | Login with email/password or Google      |
| `/register`  | Create a new account                     |
| `/dashboard` | Live analytics dashboard (requires login)|
| `/logout`    | Sign out                                 |
| `/api/analytics` | JSON analytics data (REST endpoint)  |

---

## Notes

- User data is stored locally in `users.json`
- Login history is stored in `login_log.json`
- Never commit your `.env` file to version control
- This app uses Flask's built-in development server — do not use in production without a WSGI server (e.g. gunicorn)
