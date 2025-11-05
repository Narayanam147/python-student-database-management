"""
Database configuration and connection module for Supabase
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Database:
    """Database connection class using Supabase"""
    
    _instance = None
    _client: Client = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self.connect()
    
    def connect(self):
        """Initialize Supabase client"""
        try:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            
            if not url or not key:
                raise ValueError(
                    "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in .env file"
                )
            
            self._client = create_client(url, key)
            print("✅ Successfully connected to Supabase database")
            return True
        except Exception as e:
            print(f"❌ Error connecting to database: {e}")
            return False
    
    @property
    def client(self) -> Client:
        """Get Supabase client instance"""
        if self._client is None:
            self.connect()
        return self._client
    
    def is_connected(self):
        """Check if database is connected"""
        return self._client is not None


# Global database instance
db = Database()
