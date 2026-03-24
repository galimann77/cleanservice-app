import bcrypt
import yaml
from pathlib import Path

def generate_hash(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

if __name__ == "__main__":
    passwords = {"admin": "abc", "demo": "123"}
    print("="*70)
    print("CLEANSERVICE Password Hash Generator")
    print("="*70)
    hashes = {}
    for username, password in passwords.items():
        hash_value = generate_hash(password)
        hashes[username] = hash_value
        print(f"\nUser: {username} | Passwort: {password}\nHash: {hash_value}")
    
    config_path = Path(__file__).parent / "auth_config.yaml"
    if config_path.exists():
        # Auto-update without prompt for automation
        print("\nUpdating auth_config.yaml automatically...")
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Ensure structure exists
        if 'credentials' not in config: config['credentials'] = {}
        if 'usernames' not in config['credentials']: config['credentials']['usernames'] = {}
        
        # Admin
        if 'admin' not in config['credentials']['usernames']:
            config['credentials']['usernames']['admin'] = {'email': 'admin@cleanservice.app', 'name': 'Admin User'}
        config['credentials']['usernames']['admin']['password'] = hashes['admin']
        
        # Demo
        if 'demo' not in config['credentials']['usernames']:
            config['credentials']['usernames']['demo'] = {'email': 'demo@cleanservice.app', 'name': 'Demo User'}
        config['credentials']['usernames']['demo']['password'] = hashes['demo']
            
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print("✅ Aktualisiert!")
    else:
        print(f"❌ Config not found at {config_path}")
