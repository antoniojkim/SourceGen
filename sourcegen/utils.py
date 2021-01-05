import os
import textwrap


def wrap(text, width=88, indent="\t", delimiter=", "):
    if not isinstance(text, str):
        text = delimiter.join(text)
    return (os.linesep + indent).join(textwrap.wrap(text, width))


def map_quote(text_list, quote='"'):
    return map(f"{quote}{{}}{quote}".format, text_list)
