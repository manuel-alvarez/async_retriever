import grequests
import json


class Retriever(object):

    def __init__(self, callback=None):
        # Provide a way to change callback so we can change if needed. The best example that comes to mind is in tests.
        self.buffer = callback or self.process_response

        self.pool = grequests.Pool(1)

    def fetch(self, url=''):
        """
        Main method for retriever class. It loads a file and lets the processing of response to another method
        :param url: the url that is going to be retrieved
        :return: The task (grequests.send response) to be evaluated if needed
        """
        self.print("Retrieving data from url: '{url}'".format(url=url))
        if url:
            request = grequests.get(url, hooks=dict(response=self.process_response))
            task = grequests.send(request, self.pool)

            return task

    @staticmethod
    def print(content):
        """
        This method is used only for testing purposes. This way we can capture what's being printed
        :param content: the content that is going to be printed
        :return: None
        """
        print(content)

    def process_response(self, response, *args, **kwargs):
        """
        It does nothing with response, but gets the text from within, converts it to dict and renders it
        :param response: The server response retrieved
        :param args: Not used but needed in requests hooks
        :param kwargs: Not used but needed in requests hooks
        :return: The response as it was
        """
        self.print("Preprocessing the file")
        if response.status_code == 200:
            result = response.text
            if isinstance(result, str):
                result = json.loads(result)

            self.render(result)
        else:
            self.print("Response not valid. Status Code {code}".format(code=response.status_code))
        return response

    def render(self, response):
        """
        Renders the response (just response.text as a dict)
        :param response: The text gotten from url (as a dict)
        :return: None. Output will be given on the screen
        """
        if isinstance(response, dict):
            data = response.get('data', list())
            self.print("Data provided is {len} long".format(len=len(data)))
            for item in data:
                self.print(item)
        else:
            self.print("Response not valid, please provide a valid API")
