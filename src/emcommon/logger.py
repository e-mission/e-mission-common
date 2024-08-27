"""
A unified logging interface that will work for both JS and Python.

The logging module is used for Python only, and window.Logger is used for JS only (with a fallback
  to console.log if window.Logger is not available).

Note: Transcrypt actually does have the capability to translate the Python logging module to JS,
  but it would add about 100kb to the JS bundle size, so we're not using it.
"""

# The special comments in this file (e.g. <#__: skip> and <'''?>) allow code to be executed only in JS or only in Python.
# see https://www.transcrypt.org/docs/html/special_facilities.html#skipping-transcrypt-code-fragments-when-running-with-cpython-pragma-ecom-and-pragma-noecom


# only executed in Python environment
import logging  # __: skip
logging.basicConfig(level=logging.DEBUG)  # __: skip


def debug(*args):
    # only executed in JS environment
    '''?
    if window["Logger"]:
        window["Logger"].log(window["Logger"].LEVEL_DEBUG, *args)
    else:
        console.log(*args)
    ?'''

    # only executed in Python environment
    logging.debug(*args)  # __: skip


def info(*args):
    # only executed in JS environment
    '''?
    if window["Logger"]:
        window["Logger"].log(window["Logger"].LEVEL_INFO, *args)
    else:
        console.info(*args)
    ?'''

    # only executed in Python environment
    logging.info(*args)  # __: skip


def warn(*args):
    # only executed in JS environment
    '''?
    if window["Logger"]:
        window["Logger"].log(window["Logger"].LEVEL_WARN, *args)
    else:
        console.warn(*args)
    ?'''

    # only executed in Python environment
    logging.warning(*args)  # __: skip


def error(*args):
    # only executed in JS environment
    '''?
    if window["Logger"]:
        window["Logger"].log(window["Logger"].LEVEL_ERROR, *args)
    else:
        console.error(*args)
    ?'''

    # only executed in Python environment
    logging.error(*args)  # __: skip
