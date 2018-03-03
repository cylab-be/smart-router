#!/usr/bin/python3
from sniffer import sniffer
from analyser import analyser
from os.path import join, dirname
from dotenv import load_dotenv
import time
import multiprocessing
import logging
import os

class main:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.logfile = os.environ.get("LOGFILE")
        logging.basicConfig(filename=self.logfile, level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s - %(message)s')
        try :
            self.minutes_between_analysis=int(os.environ.get("MINUTES_BETWEEN_ANALYSIS"))
        except ValueError :
            logging.error("MINUTES_BETWEEN_ANALYSIS in .env has to be INT value !!!")
            exit(-1)



    def snif(self):

        snifDNS = sniffer("dns")
        # logging.info("Starting DNS  ...")
        snifDNS.start()
        logging.info("OK!")

        snifHTTP = sniffer("http")
        # logging.info("Starting HTTP sniffer ...")
        snifHTTP.start()
        logging.info("OK!")

        snifHTTPS = sniffer("https")
        # logging.info("Starting HTTPS sniffer ...")
        snifHTTPS.start()
        logging.info("OK!")

        snifDNS.join()
        snifHTTP.join()
        snifHTTPS.join()

    def run(self):
        logging.info("Launching ...")

        p = multiprocessing.Process(target=self.snif)
        p.start()

        a = analyser()
        logging.info("Starting analyser ...")

        try:
            while True:
                logging.info("Running analysis ... ")
                a.run()
                logging.info("Analysis ended .. sleeping for " + str(self.minutes_between_analysis)+ " minutes")
                time.sleep(self.minutes_between_analysis*60)



        except KeyboardInterrupt:
            logging.info("Shutting down ..")

            if p.is_alive():
                logging.info("Ok... let s kill it...")
                # Terminate
                p.terminate()
                p.join()


if __name__ == "__main__":
    main().run()
