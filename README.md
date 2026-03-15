# RetrexOS

RetrexOS is a futuristic-looking dashboard application built with Python and Tkinter. It provides real-time system monitoring, market data, and local incident alerts (earthquakes) in a sleek, hacker-style interface.

## 🚀 Features

- **Secure Access**: Password-protected login screen.
- **System Monitoring**: Live CPU and RAM usage graphs using `psutil`.
- **Market Data**: Real-time USD/TRY and EUR/TRY exchange rates.
- **Incident Alerts**: Latest earthquake information via Kandilli Observatory API.
- **Quick Actions**: Integrated shortcuts for Terminal and Web Browser.
- **Futuristic HUD**: Interactive dashboard with a premium aesthetic and assets support.

## 🛠 Installation

1. Clone the repository.
2. Ensure you have the required dependencies installed:

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

The system is configured via a `.env` file for better security and flexibility. Create a `.env` file in the root directory:

```env
PROFILE_IMG_PATH=assets/profile.png
BG_PATH=assets/background.jpg
SIFRE=1234
KULLANICI=Retrex User
RUTBE=Admin
```

## 📂 Project Structure

- `main.py`: Core application logic.
- `assets/`: Directory for images and icons (default location for `profile.png` and `background.jpg`).
- `.env`: Environment variables and configuration.
- `requirements.txt`: Python package dependencies.

## 🖥 Usage

To start the dashboard, run:

```bash
python main.py
```

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
