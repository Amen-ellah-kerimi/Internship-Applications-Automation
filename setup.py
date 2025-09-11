import os
from cryptography.fernet import Fernet

def main():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print(".env file already exists. Aborting setup.")
        return
    key = Fernet.generate_key().decode()
    print(f"Generated Fernet Key: {key}")
    with open(env_path, 'w') as f:
        f.write(f"FERNET_KEY={key}\n")
    print(".env file created with Fernet key.")

if __name__ == "__main__":
    main()
