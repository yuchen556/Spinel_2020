import logging

EEE = "23423"+".log"
logging.basicConfig(filename=r'C:\Users\Zhen Wang\Desktop\{:s}'.format(EEE), filemode='a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%d, %H:%M:%S', level=logging.DEBUG)


logging.debug(':Debug info')
logging.info(":Running Urban Planning")


logging.critical(':critical message')

# TT = open(r'C:\Users\Zhen Wang\Desktop\SN_1stMAC_.log')

# logger = logging.getLogger('urbanGUI')
