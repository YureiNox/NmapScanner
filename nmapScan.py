import subprocess
import re
import socket

def get_local_ip():
    # Utilise une connexion temporaire à un serveur pour récupérer l'adresse IP locale
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.1)
    try:
        # L'adresse IP de destination n'a pas d'importance ici
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
    # Formate les résultats pour une meilleure lisibilité
    formatted_results = re.findall(r'Nmap scan report for (.+?)\nHost is up.*?MAC Address: (.*?)\((.*?)\)\n', results, re.DOTALL)
    return formatted_results

def main():
    local_ip = get_local_ip()
    print(f"\n\033[1mIP LOCAL:\033[0m {local_ip}\n")

    results = scan_network(local_ip)
    formatted_results = format_results(results)

    for entry in formatted_results:
        host_name = entry[0].split(' ')[0]  # Pour obtenir le nom d'hôte sans l'adresse IP
        ip_match = re.search(r'\((.*?)\)', entry[0])
        ip_address = ip_match.group(1) if ip_match else "N/A"
        mac_address = entry[1]
        device_brand = entry[2] if entry[2] else "N/A"

        print(f"\033[1m{host_name}\033[0m")
        print(f"\033[1mIP:\033[0m {ip_address}")
        print(f"\033[1mMAC:\033[0m {mac_address}")
        print(f"\033[1mBRAND:\033[0m {device_brand}\n")

if __name__ == "__main__":
    main()
