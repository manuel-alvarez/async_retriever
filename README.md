# async_retriever

Python 3 script to fetch and render a remote json file asynchronously.

## Installation

In order to be able to execute this script, you will need to have installed virtualenv. You can learn how to do it at: https://virtualenv.pypa.io/en/stable/installation/

Once installed, create a new virtualenv writing:

```
virtualenv my_env
```

And then
```
source my_env/bin/activate
```

to activate it.

You have all required libraries in requirements.txt file. To install them, please write:
```
pip install -r requirements.txt
```

## Execution

To execute main.py, type this in your console
```python main.py```

Test have been made using unittest and mock. In order to run tests, type:
```python tests.py```
