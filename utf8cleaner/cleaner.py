import logging
import os

logger = logging.getLogger(__name__)


def clean_context_bytes(data):
    cleaned = ""
    for b in data:
        try:
            # iterating over `bytes` results in `integer` which in our case
            # must then be convered back to an array of bytes with one element
            # in order for string conversion to work properly - using `chr()`
            # will "fix" any utf-8 errors so we won't see them
            # https://stackoverflow.com/questions/21017698/converting-int-to-bytes-in-python-3
            cleaned += str(bytes([b]), "utf-8")
        except UnicodeDecodeError:
            cleaned += "_"

    cleaned = cleaned.replace("\n", "")

    return cleaned

# https://stackoverflow.com/a/32661468/3441106
def get_next_character(f):
    c = f.read(1)
    width = 0
    max_width = 4
    mb = False
    starting_offset = f.tell()
    if c:
        while not mb and width < max_width:
            try:
                mb = c.decode('utf-8')
                logger.debug(f"parsed: {mb} OK")
            except UnicodeDecodeError:
                # we've encountered a multibyte character
                # read another byte and try again
                c += f.read(1)
                width += 1

        # if we're still here trying to decode bytes we got a bad bad byte
        if not mb:
            # grab surrounding bytes
            f.seek(max(0, starting_offset - 20))
            context = f.read(40)
            context_cleaned = clean_context_bytes(context)

            # we are *now* after 3 bytes past the starting position -
            # eg - (4) widening attempts. We need to grab context around this
            # bad byte to show user, then we need to seek to original position
            # and and return an empty string so that we are in the correct
            # position to read the next byte as its own entity
            f.seek(starting_offset)
            mb = ""
            logging.error(f"skipped byte {starting_offset}: {context_cleaned}")

    return mb


def clean(filename):
    output_filename = f"{filename}.clean"
    logger.info(f"Cleaning file {filename} and saving to {output_filename}")

    file_size = os.stat(filename).st_size

    with open(filename, 'rb') as fi:
        with open(output_filename, 'wb') as fo:
            while fi.tell() < file_size:
                mb = get_next_character(fi)

                if mb:
                    fo.write(bytearray(mb, "utf-8"))
