import yfinance as yf
import pandas as pd
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os

# --- CONFIGURATION ---
SENDER_EMAIL = "emwangi4777@gmail.com" 
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECEIVER_EMAIL = "emwangi4777@gmail.com" 
# ---------------------

def send_email_notification(active_alerts):
    msg = MIMEMultipart("alternative")
    msg['Subject'] = "🚨 Market Alerts Triggered"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    html_content = """
    <html>
      <body style="font-family: Arial, sans-serif; color: #333333;">
        <h2 style="color: #d9534f;">📉 Market Tracker Alerts</h2>
        <p>The following assets have dropped below their 7-day moving average:</p>
        <table style="width: 100%; border-collapse: collapse; max-width: 600px;">
          <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dddddd;">
            <th style="padding: 10px; text-align: left;">Ticker</th>
            <th style="padding: 10px; text-align: left;">Current Price</th>
            <th style="padding: 10px; text-align: left;">7-Day MA</th>
          </tr>
    """
    
    for alert in active_alerts:
        html_content += f"""
          <tr style="border-bottom: 1px solid #dddddd;">
            <td style="padding: 10px; font-weight: bold;">{alert['ticker']}</td>
            <td style="padding: 10px; color: #d9534f; font-weight: bold;">${alert['price']:.2f}</td>
            <td style="padding: 10px;">${alert['ma']:.2f}</td>
          </tr>
        """
        
    html_content += """
        </table>
        <br>
        <p style="font-size: 12px; color: #777777;">Automated message from your Python Market Tracker.</p>
      </body>
    </html>
    """
    
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print("📧 HTML Email sent successfully!")
    except Exception as e:
        print(f"⚠️ Failed to send email: {e}")

def log_alert_to_csv(ticker, price, ma):
    file_name = "alerts_log.csv"
    file_exists = os.path.isfile(file_name)
    
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Time", "Ticker", "Price", "7-Day MA"])
            
        now = datetime.now()
        writer.writerow([now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S"), ticker, f"${price:.2f}", f"${ma:.2f}"])

def check_moving_average_alert(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    history = ticker.history(period="1mo")
    
    if history.empty:
        return None

    history['7MA'] = history['Close'].rolling(window=7).mean()
    latest_day = history.iloc[-1]
    latest_price = latest_day['Close']
    latest_ma = latest_day['7MA']
    
    print(f"Checked {ticker_symbol}: ${latest_price:.2f} (7MA: ${latest_ma:.2f})")
    
    if latest_price < latest_ma:
        # Note: We removed log_alert_to_csv from here so it doesn't log every hour!
        return {"ticker": ticker_symbol, "price": latest_price, "ma": latest_ma}
    
    return None

def run_continuous_tracker(tickers_list, check_interval_seconds):
    print(f"Starting continuous tracker. Sending emails to {RECEIVER_EMAIL}...\n")
    
    # NEW: Dictionary to track the date we last alerted for each ticker
    last_alert_dates = {}
     
    while True:
        # Get today's date in YYYY-MM-DD format
        current_date = datetime.now().strftime("%Y-%m-%d")
        print(f"\n--- Check initiated at {datetime.now().strftime('%H:%M:%S')} ---")
        
        active_alerts = []
        
        for ticker in tickers_list:
            try:
                alert_data = check_moving_average_alert(ticker)
                
                if alert_data:
                    # NEW LOGIC: Check if we already sent an email for this stock today
                    if last_alert_dates.get(ticker) != current_date:
                        # We haven't alerted today! Add it to the email list.
                        active_alerts.append(alert_data)
                        
                        # Log it to the CSV just once for today
                        log_alert_to_csv(ticker, alert_data['price'], alert_data['ma'])
                        
                        # Update our memory dictionary so we don't alert again today
                        last_alert_dates[ticker] = current_date
                    else:
                        print(f"  -> Already alerted for {ticker} today. Skipping.")
                        
            except Exception as e:
                print(f"⚠️ Error checking {ticker}: {e}")
        
        if active_alerts:
            send_email_notification(active_alerts)
        else:
            print("No new alerts to send this hour.")
            
        print(f"\nWaiting {check_interval_seconds / 60} minutes...")
        time.sleep(check_interval_seconds)

if __name__ == "__main__":
    my_portfolio = ["AAPL", "TSLA", "AMZN", "GOOGL", "MSFT"]
    
    # For testing this logic quickly, you can temporarily change 3600 to 10
    run_continuous_tracker(my_portfolio, 10)