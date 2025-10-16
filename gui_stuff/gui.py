import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from ssh_stuff.ssh_keygen import generate_ssh_key
from ssh_stuff.ssh_connect import connect_ssh

def launch_app():
    root = tk.Tk()
    root.title("SSH Key Generator & Connector")
    notebook = ttk.Notebook(root)
    frame_gen = tk.Frame(notebook)
    frame_conn = tk.Frame(notebook)
    notebook.add(frame_gen, text="Generate SSH Key")
    notebook.add(frame_conn, text="SSH Connect")
    notebook.pack(expand=1, fill="both")

    # --- Key Generation Tab ---
    tk.Label(frame_gen, text="Key Type:").pack()
    key_type_var = tk.StringVar(value="rsa")
    tk.OptionMenu(frame_gen, key_type_var, "rsa", "ed25519").pack()

    tk.Label(frame_gen, text="Passphrase (optional):").pack()
    passphrase_var = tk.StringVar()
    tk.Entry(frame_gen, textvariable=passphrase_var, show="*").pack()

    tk.Label(frame_gen, text="Comment (optional):").pack()
    comment_var = tk.StringVar()
    tk.Entry(frame_gen, textvariable=comment_var).pack()

    def save_keys(private_key, public_key):
        priv_path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("PEM files", "*.pem"), ("All files", "*.*")])
        if priv_path:
            with open(priv_path, "w") as f:
                f.write(private_key)
            with open(priv_path + ".pub", "w") as f:
                f.write(public_key)
            messagebox.showinfo("Success", f"Keys saved:\n{priv_path}\n{priv_path}.pub")

    def on_generate():
        try:
            priv, pub = generate_ssh_key(
                key_type=key_type_var.get(),
                passphrase=passphrase_var.get() or None,
                comment=comment_var.get()
            )
            save_keys(priv, pub)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(frame_gen, text="Generate SSH Key", command=on_generate).pack(pady=10)

    # --- SSH Connect Tab ---
    tk.Label(frame_conn, text="Hostname:").pack()
    hostname_var = tk.StringVar()
    tk.Entry(frame_conn, textvariable=hostname_var).pack()

    tk.Label(frame_conn, text="Username:").pack()
    username_var = tk.StringVar()
    tk.Entry(frame_conn, textvariable=username_var).pack()

    tk.Label(frame_conn, text="Private Key File:").pack()
    keyfile_var = tk.StringVar()
    tk.Entry(frame_conn, textvariable=keyfile_var).pack()
    tk.Button(frame_conn, text="Browse", command=lambda: keyfile_var.set(filedialog.askopenfilename())).pack()

    tk.Label(frame_conn, text="Passphrase (if any):").pack()
    conn_passphrase_var = tk.StringVar()
    tk.Entry(frame_conn, textvariable=conn_passphrase_var, show="*").pack()

    tk.Label(frame_conn, text="Command:").pack()
    command_var = tk.StringVar(value="whoami")
    tk.Entry(frame_conn, textvariable=command_var).pack()

    def on_connect():
        try:
            output = connect_ssh(
                hostname=hostname_var.get(),
                username=username_var.get(),
                key_path=keyfile_var.get(),
                passphrase=conn_passphrase_var.get() or None,
                command=command_var.get() or "whoami"
            )
            messagebox.showinfo("SSH Output", output)
        except Exception as e:
            messagebox.showerror("SSH Error", str(e))

    tk.Button(frame_conn, text="Connect & Run", command=on_connect).pack(pady=10)

    root.mainloop()