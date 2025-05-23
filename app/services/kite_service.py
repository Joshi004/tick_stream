import json
import logging
from kiteconnect import KiteTicker

from app.core.config import settings

class KiteTickerService:
    def __init__(self):
        self.api_key = settings.KITE_API_KEY
        self.access_token = settings.KITE_ACCESS_TOKEN
        self.ticker = None
        self.active_instruments = set()
        
    def initialize(self):
        if not self.api_key or not self.access_token:
            logging.error("Kite API credentials not found in settings")
            raise ValueError("Missing Kite API credentials. Please set KITE_API_KEY and KITE_ACCESS_TOKEN in environment variables.")
            
        self.ticker = KiteTicker(self.api_key, self.access_token)
        self.ticker.on_ticks = self.on_ticks
        self.ticker.on_connect = self.on_connect
        self.ticker.on_close = self.on_close
        self.ticker.on_error = self.on_error
        
    def start(self):
        if not self.ticker:
            self.initialize()
        self.ticker.connect()
        
    def subscribe_instrument(self, instrument_code):
        """Subscribe to instrument ticks"""
        try:
            instrument_token = int(instrument_code)  # Ensure it's an integer
            self.active_instruments.add(instrument_token)
            
            # If already connected, subscribe to the new instrument
            if self.ticker and self.ticker.is_connected():
                self.ticker.subscribe([instrument_token])
                logging.info(f"Subscribed to instrument: {instrument_token}")
            return True
        except Exception as e:
            logging.error(f"Failed to subscribe to instrument {instrument_code}: {e}")
            return False
    
    # WebSocket event callbacks
    def on_ticks(self, ws, ticks):
        for tick in ticks:
            # Log tick data to console
            print(f"Received tick: {json.dumps(tick)}")
    
    def on_connect(self, ws, response):
        logging.info("Connected to Kite WebSocket")
        # Subscribe to all active instruments
        if self.active_instruments:
            self.ticker.subscribe(list(self.active_instruments))
            
    def on_close(self, ws, code, reason):
        logging.info(f"Connection closed: {reason} (Code: {code})")
        
    def on_error(self, ws, code, reason):
        logging.error(f"Error in WebSocket connection: {reason} (Code: {code})")
