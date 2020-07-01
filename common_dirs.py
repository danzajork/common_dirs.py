#!/usr/bin/python3
import concurrent.futures
import requests
from tqdm import tqdm
from argparse import ArgumentParser

def check_site(subdomain, path):
    try:
        host = subdomain.rstrip()
        response = requests.get(f"https://{host}{path}", timeout=5, allow_redirects=False)
        if response.status_code == 200:
            length = len(response.content)
            return str(f"{response.status_code} : {length} : https://{host}{path}")
        return None
    except:
        return None

def check_url(hosts, path, num_threads = 40):
    print(f"checking {path}")
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        future_to_url = {executor.submit(check_site, host, path): host for host in hosts}
        for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(hosts), unit='urls'):
            sub_ns_sc = future_to_url[future]
            try:
                if future.result() is not None:
                    results.append(future.result())
            except Exception as e:
                print(f"{e}")
                raise
    return results

def main():
    parser = ArgumentParser()
    parser.add_argument("-d", "--domains", dest="domains", help="Domain to target")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Wordlist")
    args = parser.parse_args()

    with open(args.domains, "r") as file:
        hosts = file.readlines()

    with open(args.wordlist, "r") as file:
        paths = file.readlines()

    final = []
    for path in paths:
        results = check_url(hosts, str(f"{path.rstrip()}"))
        for response in results:
            final.append(response)

    for final_resp in final:
        print(f"{final_resp}")

if __name__ == "__main__": main()

