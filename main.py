import time
import dns.zone
import concurrent.futures
import dns.resolver
import socket
import threading
import requests
import sys

def dns_zone(address):
    try:
        ns_answer = dns.resolver.resolve(address, 'NS')
        for server in ns_answer:
            ip_answer = dns.resolver.resolve(server.target, 'A')
            for ip in ip_answer:
                try:
                    zone = dns.zone.from_xfr(dns.query.xfr(str(ip), address))
                    for host in zone:
                        links_zn.append(str("{}.{}".format(host, alvo)))
                except Exception as e:
                    print(f"Zone transfer failed for {ip}: {e}")
        return links_zn
    except Exception as we:
        print(f"Transferencia de zona recusada ou erro: {we}")
        pass

palavrasub = []
def check_dns(palavra):
    try:
        result = socket.gethostbyname(f"{palavra}.{alvo}")
        with lock:
            results.append((palavra, result))
           # palavrasub.append(palavra)
    except socket.gaierror as e:
        if 'NXDOMAIN' in str(e):
            pass


def progress_report(count, total):
    print(f"Progresso: {count}/{total} subdominios verificados.\r")


if __name__ == '__main__':

    print("---------- AKIRA ----------".center(8))
    print(
        "---------- INFORMATION GATHERING TOOL\n---------- This script will try zone transfer and search for subdomains and directories. ----------")
    print(f"How to use: python3 {sys.argv[0]} google.com\n".center(8))

    print("".center(8))
    print("""\                                  __
                                   _.-~  )
                        _..--~~~~,'   ,-/     _
                     .-'. . . .'   ,-','    ,' )
                   ,'. . . _   ,--~,-'__..-'  ,'
                 ,'. . .  (@)' ---~~~~      ,'
                /. . . . '~~             ,-'
               /. . . . .             ,-'
              ; . . . .  - .        ,'
             : . . . .       _     /
            . . . . .          `-.:
           . . . ./  - .          )
          .  . . |  _____..---.._/ ____ @Akirasz _
    ~---~~~~----~~~~             ~~""")

    print("".center(8))
    print("".center(8))
    print("".center(8))
    time.sleep(4)
    results = []
    links_zn = []
    results_final3 = []
    stcodes = []

    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lock = threading.Lock()
    maxthreads = 50
    alvo = sys.argv[1]
    ns_servers = []

    t = True

    if t:
        links_zn = dns_zone(alvo)

    if links_zn:
        print("------------ Zone Transfer Concluido! ------------\n------------ Resultados: ".center(8))
        print(*links_zn, sep='\n')

    if not links_zn:
        try:
            with open('g.txt', 'r') as file:
                words = file.read().split()
                total_words = len(words)
                threads = [threading.Thread(target=check_dns, args=(palavra,)) for palavra in words]
                running_threads = []
                for i, thread in enumerate(threads):
                    running_threads.append(thread)
                    thread.start()
                    if len(running_threads) >= maxthreads:
                        for t in running_threads:
                            t.join()
                        running_threads = []
                    progress_report(i + 1, total_words)
                for thread in running_threads:
                    thread.join()
                print("DNS brute concluido.")

                for palavra, result in results:
                    palavrasub.append(palavra)
                    results_final3.append(f"Up: {palavra}.{alvo} | {result}")
        except FileNotFoundError:
            print("Wordlist não encontrada.")


    opt = 'S'

    if opt == "S".upper():
        print(*links_zn, sep='\n')
        print(*results_final3, sep='\n--------------------------------------\n')

        desativado = (input("\nDigite a extensão usada nas paginas do site. Ex: ( .php ou .html ) (opcional)"))
        ext = (desativado)
        try:
            sub_list = open("wordlist.txt").read()
            directories = sub_list.splitlines()


            def check_directory(dir):

                dir_enum = f"http://{alvo}/{dir}"
                r = requests.get(dir_enum)
                if r.status_code == 404:
                    pass
                else:
                    print(f"Diretório valido: {dir_enum} | Status Code: {r.status_code}")
                    results_final3.append(f"Up: http://{alvo}/{dir} | Status Code: {r.status_code} | {result}")



                if ext!="":
                        dir_enum2 = f"http://{alvo}/{dir}{ext}"

                        r2 = requests.get(dir_enum2)
                        if r2.status_code == 404:
                            time.sleep(0.5)
                            pass
                        else:
                            print(f"Diretório valido: {dir_enum2} | Status Code: {r2.status_code}")
                            results_final3.append(f"Up: http://{alvo}/{dir}{ext} | Status Code: {r2.status_code} | {result}")
                            time.sleep(0.5)
                else:
                    pass


                if links_zn == "a":
                    for i in palavrasub:

                        dir_enum3 = f"http://{i}.{alvo}/{dir}"

                        r3 = requests.get(dir_enum3)
                        if r3.status_code == 404:
                            time.sleep(0.5)
                            pass
                        else:
                            print(f"Diretório valido: {dir_enum3} | Status Code: {r3.status_code}")
                            results_final3.append(f"Up: http://{i}.{alvo}/{dir} | Status Code: {r3.status_code} | {result}")
                            time.sleep(0.5)
                else:
                    pass






            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(check_directory, directories)

        except:
            pass


    print("""\                                  __
                               _.-~  )
                    _..--~~~~,'   ,-/     _
                 .-'. . . .'   ,-','    ,' )
               ,'. . . _   ,--~,-'__..-'  ,'
             ,'. . .  (@)' ---~~~~      ,'
            /. . . . '~~             ,-'
           /. . . . .             ,-'
          ; . . . .  - .        ,'
         : . . . .       _     /
        . . . . .          `-.:
       . . . ./  - .          )
      .  . . |  _____..---.._/ ____ @Akirasz _
~---~~~~----~~~~             ~~""")

    print("---------- AKIRA  ----------".center(8))
    print("---------- RESULTS ----------\n")

    print(*links_zn, sep='\n')
    print(*results_final3, sep='\n--------------------------------------\n')
