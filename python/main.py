from sniffer import sniffer
from analyser import analyser
import time
import multiprocessing

def snif():

    snifDNS = sniffer("dns")
    print("Starting DNS  ...")
    snifDNS.start()
    print("OK!")


    snifHTTP = sniffer("http")
    print("Starting HTTP sniffer ...")
    snifHTTP.start()
    print("OK!")


    snifDNS.join()
    snifHTTP.join()
print("Launching ...")

p = multiprocessing.Process(target=snif)
p.start()


a = analyser()
print("Starting analyser ...")

try :
    while True :
        #FIXME - 10 -> input parameter
        a.run()
        print("Running analysis")
        time.sleep(10)

except KeyboardInterrupt :
    print("Shutting down ..")

    if p.is_alive():
        print("Ok... let s kill it...")
        # Terminate
        p.terminate()
        p.join()



