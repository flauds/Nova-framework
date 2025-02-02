N.O.V.A _Framework
from cryptography.fernet import Fernet
import json
import os
from getpass import getpass
import base64
import hashlib

class NovaFramework:
    def __init__(self, storage_file="nova_knowledge.json", key_file="nova_sea_keys.enc"):
        self.storage_file = storage_file
        self.encrypted_key_file = key_file
        self.keys = self.load_or_create_keys()
        self.knowledge = self.load_knowledge()

    def derive_master_key(self, password):
        """Derive a key from the master password."""
        return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    def encrypt_keys(self, keys, master_password):
        """Encrypt sea keys using the master password."""
        master_key = self.derive_master_key(master_password)
        fernet = Fernet(master_key)
        encrypted_data = fernet.encrypt(json.dumps(keys).encode())
        with open(self.encrypted_key_file, "wb") as f:
            f.write(encrypted_data)
        print("Keys encrypted and saved securely.")

    def decrypt_keys(self, master_password):
        """Decrypt sea keys using the master password."""
        master_key = self.derive_master_key(master_password)
        fernet = Fernet(master_key)
        try:
            with open(self.encrypted_key_file, "rb") as f:
                encrypted_data = f.read()
            return json.loads(fernet.decrypt(encrypted_data).decode())
        except Exception as e:
            print("Failed to decrypt keys. Check your password.")
            raise e

    def load_or_create_keys(self):
        """Load keys from the encrypted file or create new ones."""
        if os.path.exists(self.encrypted_key_file):
            print("Encrypted key file found.")
            password = getpass("Enter master password to decrypt keys: ")
            try:
                return self.decrypt_keys(password)
            except Exception:
                print("Incorrect password or corrupted file.")
                exit(1)
        else:
            print("No encrypted key file found. Generating new keys.")
            keys = {sea: Fernet.generate_key().decode() for sea in ["Atlantic", "Pacific", "Indian", "Arctic", "Southern"]}
            password = getpass("Set a master password to encrypt keys: ")
            self.encrypt_keys(keys, password)
            return keys

    def load_knowledge(self):
        """Load encrypted knowledge from storage."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                return json.load(f)
        return {}

    def save_knowledge(self):
        """Save encrypted knowledge to storage."""
        with open(self.storage_file, "w") as f:
            json.dump(self.knowledge, f)

    def encrypt_knowledge(self, sea, data):
        """Encrypt data using the key for the given sea."""
        if sea not in self.keys:
            print(f"Sea '{sea}' not found in keys.")
            return None
        fernet = Fernet(self.keys[sea].encode())
        return fernet.encrypt(data.encode()).decode()

    def decrypt_knowledge(self, sea, encrypted_data):
        """Decrypt data using the key for the given sea."""
        if sea not in self.keys:
            print(f"Sea '{sea}' not found in keys.")
            return None
        fernet = Fernet(self.keys[sea].encode())
        return fernet.decrypt(encrypted_data.encode()).decode()

    def add_knowledge(self, sea, topic, content):
        """Add new knowledge to the framework."""
        if sea not in self.keys:
            print(f"Invalid sea: {sea}")
            return
        encrypted_content = self.encrypt_knowledge(sea, content)
        self.knowledge[topic] = {"sea": sea, "content": encrypted_content}
        self.save_knowledge()
        print(f"Knowledge about '{topic}' added under {sea} sea.")

    def retrieve_knowledge(self, topic):
        """Retrieve knowledge by topic."""
        if topic not in self.knowledge:
            print(f"No knowledge found about '{topic}'.")
            return
        sea = self.knowledge[topic]["sea"]
        encrypted_content = self.knowledge[topic]["content"]
        content = self.decrypt_knowledge(sea, encrypted_content)
        print(f"Knowledge about '{topic}': {content}")

# Example Usage
if __name__ == "__main__":
    nova = NovaFramework()

    # Teach Nova something new
    nova.add_knowledge("Atlantic", "Python", "Python is a versatile programming language.")
    nova.add_knowledge("Pacific", "Encryption", "Encryption secures data by converting it into a coded format.")

    # Retrieve knowledge
    nova.retrieve_knowledge("Python")
    nova.retrieve_knowledge("Encryption")