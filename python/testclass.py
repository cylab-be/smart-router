from sniffer import sniffer
from database import database
import datetime
snif = sniffer()

snif.dnsQuerry("10.0.2.15")

# db = database()
# db.connect()
# now = datetime.datetime.now()
# values = [str("10.0.2.15"), str("test"), now]
# sql = "INSERT INTO DNSQueries (ip_iot, ip_dst, datetime) VALUES (%s, %s, %s)"
# print (db.execquery(sql, values))
# sql = "select * from  DNSQueries"
# print (db.execquery(sql))
# db.close()