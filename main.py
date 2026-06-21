import os
import requests
import time

from dotenv import load_dotenv
from lightstreamer.client import LightstreamerClient, Subscription, SubscriptionListener

load_dotenv()

# --- 1. Your StoneX Account Configuration ---
# Note: Substitute these with actual StoneX endpoints given in your API documentation
STONEX_REST_URL = os.getenv("STONEX_REST_URL")
STONEX_LS_URL   = os.getenv("STONEX_LS_URL")
ADAPTER_SET     = "DEMO"
DATA_ADAPTER    = "PRICES"

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
APP_KEY  = os.getenv("APP_KEY")

# --- 2. Authenticate to get the Token ---
def get_session_token():
    
    payload = {
        "UserName": USERNAME,
        "Password": PASSWORD,
        "AppKey": APP_KEY
    }
    response = requests.post(STONEX_REST_URL + '/v2/Session', json=payload)
    response.raise_for_status()
    
    # Typically returns a session token or JWT used for the Lightstreamer session
    return response.json().get("session")

def delete_session(session_token: str):
    
    payload = {
        "UserName": USERNAME,
        "Session": session_token
    }
    response = requests.post(
        STONEX_REST_URL + f"/TradingAPI/session/deleteSession?UserName={USERNAME}&Session={session_token}", 
        json=payload
    )
    response.raise_for_status()

# --- 3. Define the Subscription Listener ---
class PriceStreamListener(SubscriptionListener):
    def onItemUpdate(self, update):
        item_name = update.getItemName()
        # Extract specific market fields
        bid = update.getValue("Bid")
        ask = update.getValue("Ask")
        market_time = update.getValue("Time")
        
        print(f"[{market_time}] {item_name} -> Bid: {bid} | Ask: {ask}")

    def onSubscription(self):
        print("Successfully subscribed to price stream.")

    def onSubscriptionError(self, code, message):
        print(f"Subscription failed: {message} (Code: {code})")

# --- 4. Main Streaming Logic ---
def main():
    try:
        print("Authenticating with StoneX...")
        session_token = get_session_token()
        print(f"Authentication successful: {session_token}")
        
        # Initialize Lightstreamer Client
        client = LightstreamerClient(STONEX_LS_URL, ADAPTER_SET)
        
        # Pass credentials (Passing token into setPassword)
        client.connectionDetails.setUser(USERNAME)
        client.connectionDetails.setPassword(session_token)
        
        # Define items (e.g., AUD/USD) and fields you want to stream
        # (Refer to StoneX documentation for exact item naming conventions)
        items_to_stream = ["ID.404702486"]
        fields_to_stream = ["Bid", "Ask", "Time", "High", "Low"]
        
        # Create a subscription in MERGE mode (best for market prices)
        subscription = Subscription(
            mode="MERGE",
            items=items_to_stream,
            fields=fields_to_stream
        )
        subscription.setDataAdapter(DATA_ADAPTER)
        subscription.setRequestedSnapshot("yes") # Asks for the current price immediately
        
        # Attach the listener and subscribe
        subscription.addListener(PriceStreamListener())
        client.subscribe(subscription)
        
        # # Connect to the stream
        print("Connecting to Lightstreamer stream...")
        client.connect()
        print("Connected to Lightstreamer stream")
        
        # Keep the main thread alive to listen to incoming data
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nDisconnecting...")
        client.disconnect()
        
        if session_token:
            print("Deleting session...")
            delete_session(session_token)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
