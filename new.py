import shelve
import time
import socket
def dnsShelf(hostname):
    i = 0
    dnsName = 'dns.shelve'
    IPaddress = shelve.open(dnsName)
    while i <= 0:
        i += 1

        if hostname == '':
            break

        if hostname not in IPaddress:
            elaplseTime = time.time()
            IPaddress[hostname] = socket.gethostbyname(hostname)
            elaplseTime = time.time() - elaplseTime
            print('-=-=- Got '+ hostname + ' from DNS search in ' +
                str(elaplseTime) + 'seconds')

        print(hostname + ' is at ' + IPaddress[hostname])

    #pprint.pprint(list(IPaddress.items()))
    IPaddress.close()
if __name__ == "__main__":
    dnsShelf("github.com")