import json
import unittest

from requests import Response
from retriever import Retriever
from unittest.mock import MagicMock, Mock


class TestRetrieverMethods(unittest.TestCase):

    def setUp(self):
        self.retriever = Retriever()
        self.output = []

        def fake_print(content):
            self.output.append(content)

        self.retriever.print = fake_print

        self.text_response = '{"success": true, "data": [209], "length": 1, "type": "uint8"}'
        self.json_response = {'type': 'uint8', 'data': [209], 'length': 1, 'success': True}

    def tearDown(self):
        self.output = None
        self.retriever = None

    def test_fetch(self):
        self.retriever.render = MagicMock()

        # Check empty url
        response = self.retriever.fetch("")
        self.assertIsNone(response)
        self.retriever.render.assert_not_called()

        # Check invalid url
        response = self.retriever.fetch("Invalidurl")
        self.assertIsNone(response.value)  # Still None, still loading
        response.join()  # Force the response to be retrieved
        self.assertIsInstance(response.value.exception, Exception)
        self.retriever.render.assert_not_called()

        # Check valid url
        response = self.retriever.fetch("https://gist.githubusercontent.com/manuel-alvarez/aa2834634700489d68aa579faf0e133f/raw/8fcc0620f2b619cd37b18a53a8bb15b04e8b30e3/simple_file.json")
        self.assertIsNone(response.value)  # Still None, still loading
        response.join()  # Force the response to be retrieved
        self.assertIsInstance(response.value.response, Response)
        self.retriever.render.assert_called_once_with(self.json_response)

    def test_process_response(self):
        response = Mock()
        response.status_code = 200
        response.text = self.text_response

        processed_response = self.retriever.process_response(response)
        self.assertEqual(response, processed_response)
        self.assertEqual(len(self.output), 3)
        self.assertEqual(self.output[2], 209)  # The single value we have in our data

        self.output = []  # Reset output

        empty_response = Mock()
        empty_response.status_code = 400
        processed_response = self.retriever.process_response(empty_response)
        self.assertEqual(len(self.output), 2)
        self.assertEqual(self.output[1], "Response not valid. Status Code 400")

    def test_render(self):
        self.retriever.render(self.json_response)
        self.assertEqual(len(self.output), 2)
        self.assertEqual(self.output[1], 209)  # The single value we have in our data

        self.output = []

        self.retriever.render(self.text_response)  # Bad response. Still a text
        self.assertEqual(len(self.output), 1)
        self.assertEqual(self.output[0], "Response not valid, please provide a valid API")

if __name__ == '__main__':
    unittest.main()
