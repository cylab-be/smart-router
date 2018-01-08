from sniffer import sniffer
# from database import database
# import datetime
snifDNS = sniffer("dns")
snifDNS.setHost("10.0.2.15")
snifDNS.start()


snifHTTP = sniffer("http")
snifHTTP.setHost("10.0.2.15")
snifHTTP.start()
snifDNS.join()
snifHTTP.join()