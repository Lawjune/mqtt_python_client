import threading
import logging

class SafeThread(threading.Thread):
    def __init__(self, logging_level=logging.DEBUG):
        super(SafeThread, self).__init__()
        self.__flag = threading.Event() # Used to pause threading
        self.__flag.set() # Set as True
        self.__running = threading.Event() # Used to stop threading
        self.__running.set()
        _logger = logging.getLogger(self.__class__.__name__)
        _logger.setLevel(logging_level)

        _ch = logging.StreamHandler()
        _ch.setLevel(logging_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        _ch.setFormatter(formatter)
        if not _logger.handlers:
            _logger.addHandler(_ch)
        self.logger = _logger

    def run(self):
        self.logger.debug("Running...") # Do not inherit 

    def is_running(self):
        return self.__running.isSet()

    def is_waiting_for_pause(self):
        return self.__flag.wait()

    def pause(self):
        self.__flag.clear() # Set as False to pause threading

    def resume(self):
        self.__flag.set() # Set as True to resume threading

    def stop(self):
        self.__flag.set()
        self.__running.clear()
        self.logger.debug("Stopped running.")
        self.join()


if __name__ == "__main__":
    import time

    st = SafeThread()
    st.start()
    time.sleep(3)
    st.stop()