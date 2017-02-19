import grequests
import json


class Retriever(object):

    def __init__(self, callback=None):
        # Provide a way to change callback so we can change if needed. The best example that comes to mind is in tests.
        self.buffer = callback or self.process_response

        # In order to give the user a way to know if the retriever is still working, we will use this attribute
        self._is_busy = False

    def fetch(self, url=''):
        """
        Main method for retriever class. It loads a file and lets the processing of response to another method
        :param url: the url that is going to be retrieved
        :return: The task (grequests.send response) to be evaluated if needed
        """
        print("Retrieving data from url: '{url}'".format(url=url))
        self._is_busy = True
        if url:
            try:
                request = grequests.get(url, hooks=dict(response=self.process_response))
                task = grequests.send(request, grequests.Pool(1))

                return task
            except Exception as err:
                self._is_busy = False
                raise err

    @property
    def is_busy(self):
        """
        Get method for _is_busy attribute, just to avoid the user will change it
        :return: Boolean. self._is_busy attribute value
        """
        return self._is_busy

    def process_response(self, response, *args, **kwargs):
        """
        It does nothing with response, but gets the text from within, converts it to dict and renders it
        :param response: The server response retrieved
        :param args: Not used but needed in requests hooks
        :param kwargs: Not used but needed in requests hooks
        :return: The response as it was
        """
        print("Preprocessing the file")
        if response.status_code == 200:
            result = response.text
            if isinstance(result, str):
                result = json.loads(result)

            self.render(result)
            self._is_busy = False
        return response

    @staticmethod
    def render(response):
        """
        Renders the response (just response.text as a dict)
        :param response: The text gotten from url (as a dict)
        :return: None. Output will be given on the screen
        """
        if isinstance(response, dict):
            data = response.get('data', list())
            print("Data provided is {len} long".format(len=len(data)))
            for item in data:
                print(item)
        else:
            print("Response not valid, please provide a valid API")
