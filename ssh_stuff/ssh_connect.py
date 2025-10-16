import paramiko

def connect_ssh(hostname, username, key_path, passphrase=None, command="whoami"):
    # Detect key type from file extension
    if key_path.endswith("id_ed25519"):
        key = paramiko.Ed25519Key.from_private_key_file(key_path, password=passphrase)
    else:
        key = paramiko.RSAKey.from_private_key_file(key_path, password=passphrase)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=hostname, username=username, pkey=key)
    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode()
    client.close()
    return output