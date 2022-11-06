import sys, time
from shodan import Shodan
from termcolor import colored, cprint

# Coloring
def print_paid(x): return cprint(x, 'green')
def print_unpaid(x): return cprint(x, 'blue')
def print_fail(x): return cprint(x, 'red')

def check(key, oF):
    try:
        shodan_api = Shodan(key)
        if shodan_api.info()['query_credits'] >= qc_limit:
            print_paid("[+] Valid key (paid):  " + key)
            with open(oF, "a+") as f:
                f.write("{0} | Query Credits: {1} | Scan Credits: {2}\n".format(key, str(shodan_api.info()['query_credits']), str(shodan_api.info()['scan_credits'])))
        else:
            print_unpaid("[!] Valid key (limit): " + key)
    except KeyboardInterrupt:
        raise Exception("Exit via keyboard")
        exit()
    except:
        print_fail("[-] Invalid key:       " + key)

def load(iF):
    try:
        keys = []
        
        with open(iF, "r") as f:
            for line in f.readlines():
                currKey = line.split(" ")[0]
                if currKey not in keys:
                    keys.append(str(currKey).strip())

        return keys
    except:
        raise Exception("Failed to load keys!")
        exit()

try:
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: checkshodkey.py <keysToCheck.txt> <keys.out> <query credit limit>")
        print("If query limit not set, defaulting to 100")
        exit()

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    try: 
        qc_limit = int(sys.argv[3])
    except:
        qc_limit = 100

    # Load key file
    loadedKeys = load(inputFile)
   
    # Start checking the keys
    print("Checking your keys (Query limit = {0})".format(qc_limit))
    print()
    for i in loadedKeys:
        check(str(i), outputFile)
    print()
    print("Done, have fun! ;)")
except Exception as e:
    print_fail("Program stopped - " + str(e))
    exit()
