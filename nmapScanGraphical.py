import subprocess
import re
import socket
import tkinter as tk
from tkinter import scrolledtext

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def scan_network(ip):
    try:
        command = f'nmap -sn {ip}/24'
        result = subprocess.check_output(command, shell=True, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution de la commande : {e.output}"

def format_results(results):
    formatted_results = re.findall(r'Nmap scan report for (.+?)\nHost is up.*?MAC Address: (.*?)\((.*?)\)\n', results, re.DOTALL)
    return formatted_results

def main():
    local_ip = get_local_ip()

    # Création de l'interface graphique
    root = tk.Tk()
    root.title("Scanner de réseau")

    # Label pour afficher l'IP locale en haut à gauche
    ip_label = tk.Label(root, text=f"IP LOCAL : {local_ip}")
    ip_label.grid(row=0, column=0, pady=10, sticky=tk.NW)

    # Frame pour contenir la liste des dispositifs
    device_frame = scrolledtext.ScrolledText(root, width=80, height=20, wrap=tk.WORD)
    device_frame.grid(row=1, column=0, columnspan=2, pady=10)

    def scan_and_display():
        results = scan_network(local_ip)
        formatted_results = format_results(results)

        device_frame.delete(1.0, tk.END)  # Efface le contenu actuel du widget Text

        for entry in formatted_results:
            host_name = entry[0].split(' ')[0]
            ip_match = re.search(r'\((.*?)\)', entry[0])
            ip_address = ip_match.group(1) if ip_match else "N/A"
            mac_address = entry[1]
            device_brand = entry[2] if entry[2] else "N/A"

            device_frame.insert(tk.END, f"\n\n{host_name}\n")
            device_frame.insert(tk.END, f"IP: {ip_address}\n")
            device_frame.insert(tk.END, f"MAC: {mac_address}\n")
            device_frame.insert(tk.END, f"BRAND: {device_brand}\n")

    # Bouton pour lancer le scan
    scan_button = tk.Button(root, text="Scanner le réseau", command=scan_and_display)
    scan_button.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
