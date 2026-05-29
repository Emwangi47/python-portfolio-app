# 📈 Emmanuel's Python Portfolio & Market Tracker

Welcome to my interactive software engineering portfolio. This repository contains a multi-page web application built with pure Python, designed to showcase my capabilities in API integration, front-end data visualization, and back-end automation.

## 🏗️ Architecture Overview
This project is split into two distinct components:
1. **Front-End Dashboard (`app.py`):** A Streamlit-powered UI featuring an interactive layout, dynamic data rendering, and a secure login gateway demonstration.
2. **Back-End Daemon (`market_alert_daemon.py`):** A headless background process that continuously polls financial APIs, manages state memory to prevent alert spam, and routes automated HTML emails via SMTP.


## 🚀 Server Deployment Guide

If you are pulling this codebase to host on a server, follow these steps to get the environment running.

**1. Clone the Repository**
```bash
git clone [https://github.com/Emwangi47/python-portfolio-app.git](https://github.com/Emwangi47/python-portfolio-app.git)
cd python-portfolio-app

**2. Setup Enviroment**
'''bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
'''

**3. Config secrets (.env)**

WEATHER_API_KEY=your_weather_api_key
SENDER_PASSWORD=your_email_app_password

**4. Launch Web app**

streamlit run app.py

**5. Launch Market Daemon**

python market_alert_daemon.py


## ALTERNATIVE DOWNLOAD METHOD##

**YOU MAY DOWNLOAD THIS REPOSITORY FROM THE GITHUB WEBSITE BY DOWLOADING ZIP**