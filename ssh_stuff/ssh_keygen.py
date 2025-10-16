import paramiko
import io

def generate_ssh_key(key_type="rsa", bits=2048, passphrase=None, comment=""):
    if key_type == "rsa":
        key = paramiko.RSAKey.generate(bits)
    elif key_type == "ed25519":
        key = paramiko.Ed25519Key.generate()
    else:
        raise ValueError("Unsupported key type")
    private_key = io.StringIO()
    key.write_private_key(private_key, password=passphrase)
    public_key = f"{key.get_name()} {key.get_base64()} {comment}".strip()
    return private_key.getvalue(), public_key