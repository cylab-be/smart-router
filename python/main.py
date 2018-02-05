from python.sniffer import sniffer
# from database import database
# import datetime
snifDNS = sniffer("dns")
snifDNS.setHost("")
snifDNS.start()


snifHTTP = sniffer("http")
snifHTTP.setHost("")
snifHTTP.start()
snifDNS.join()
snifHTTP.join()