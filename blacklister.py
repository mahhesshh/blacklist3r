import requests
import socket
import argparse

def display_banner():
    ascii_banner = """
______  _               _     _      _       _    _____ ______ 
| ___ \| |             | |   | |    (_)     | |  |____ || ___ \
| |_/ /| |  __ _   ___ | | __| |     _  ___ | |_     / /| |_/ /
| ___ \| | / _` | / __|| |/ /| |    | |/ __|| __|    \ \|    / 
| |_/ /| || (_| || (__ |   < | |____| |\__ \| |_ .___/ /| |\ \ 
\____/ |_| \__,_| \___||_|\_\\_____/|_||___/ \__|\____/ \_| \_|
                                                               
Made By @Mahhesshh 🇮🇳                                                         

 """
    print(ascii_banner)

def get_common_names(domain):
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            common_names = set()
            for entry in data:
                name = entry.get("name_value", "")
                # Split by newlines for entries with multiple names and remove duplicates
                common_names.update(name.split("\n"))
            return sorted(common_names)
    except Exception as e:
        print(f"Error fetching data from crt.sh: {e}")
    return []

def is_active(subdomain):
    try:
        socket.gethostbyname(subdomain)
        return True
    except:
        return False

def save_to_file(active_subdomains, filename):
    with open(filename, "w") as file:
        for sub in active_subdomains:
            file.write(sub + "\n")
    print(f"Saved active subdomains to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Subdomain enumeration tool using crt.sh")
    parser.add_argument("domain", help="The target domain to search subdomains for")
    parser.add_argument("-o", "--output", required=True, help="Output file for active subdomains")
    args = parser.parse_args()
    
    print(f"Fetching subdomains for {args.domain}...")
    common_names = get_common_names(args.domain)
    print(f"Found {len(common_names)} subdomains. Checking activity...")
    
    active_subdomains = [sub for sub in common_names if is_active(sub)]
    print(f"Found {len(active_subdomains)} active subdomains.")
    
    save_to_file(active_subdomains, args.output)

if __name__ == "__main__":
    main()
