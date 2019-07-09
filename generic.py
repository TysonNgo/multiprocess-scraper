from multiprocessing import Process, Lock
from time import time, strftime, gmtime

class Scraper(object):
    def __init__(self):
        self.start_time = time()
        self.lock = Lock()
        self.processes = 10

    def run(self, cb):
        """Get pages and executes cb function on each

        Parameters
        ----------
        cb : callable
            A callback function that takes self and the
            result of self.get_page and processes it
            (e.g. saves the page to disk)
        """
        def r():
            while self.has_next():
                page = self.get_page()
                cb(self, page)
                self.log(page)

        procs = [Process(target=r) for i in range(self.processes)]

        for p in procs: p.start()
        for p in procs: p.join()

    def get_page(self):
        """override this method

        may return anything
        """
        with self.lock:
            v = 'self.v.value'
            self.next()
        return {
            'name': v,
            'response': None
        }

    def next(self):
        """override this method

        sets a class field to
        """
        pass

    def has_next(self):
        """override this method
        """
        return True

    def page_to_log_str(self, page):
        """override this method

        takes page and returns a string
        to use for printing progress
        """
        pass

    def log(self, page):
        """Prints the progress of the scraper
        """
        t = time()-self.start_time
        t = strftime('%Hh %Mm %Ss', gmtime(t))
        print (self.page_to_log_str(page), t, 'elapsed')


if __name__ == '__main__':
    from multiprocessing import Value
    import requests

    class Example(Scraper):
        def __init__(self):
            Scraper.__init__(self)

            self.v = Value('i', 0)
            self.url = 'https://www.google.ca/search?q='

        def get_page(self):
            with self.lock:
                v = str(self.v.value)
                self.next()
            return {
                'name': v,
                'response': requests.get(self.url + v)
            }

        def next(self):
            self.v.value += 1

        def has_next(self):
            return self.v.value < 10

        def page_to_log_str(self, page):
            return str(page['name'])+' '+str(page['response'])

    example = Example()
    def cb(self, page):
        # save the page...
        pass
    example.run(cb)
