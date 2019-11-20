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

#    cleaned += cleaned + " original: "
#     try:
#         cleaned += str(data, "utf-8")
#     except UnicodeDecodeError:
#         cleaned += "unavailable"

    cleaned = cleaned.replace("\n", "")

    return cleaned

# https://stackoverflow.com/a/32661468/3441106
def get_next_character(f):
    # note: assumes valid utf-8
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
                # try:
                mb = get_next_character(fi)

                if mb:
                    fo.write(bytearray(mb, "utf-8"))

                # except UnicodeDecodeError:
                #     # grab surrounding bytes
                #     offset = fi.tell()
                #     fi.seek(max(0, offset - 20))
                #     context = fi.read(40)
                #     context_cleaned = clean_context_bytes(context)
                #
                #     # back to original position
                #     fi.seek(offset)
                #
                #     logging.error(f"skipped byte {offset}: 0x{byte_s.hex().capitalize()} - {context_cleaned}")
                #
                # byte_s = fi.read(1)
                # if not byte_s:
                #     # EOF
                #     break
                # try:
                #     # `unicode()` function is gone from python3 and should be replaced with
                #     # `str()` - see https://stackoverflow.com/a/38860645/3441106
                #     u = str(byte_s, "utf-8")
                #     fo.write(byte_s)
                # except UnicodeDecodeError:
                #     # not a valid utf8 *byte*
                #     #
                #     # This *might* (or might not!) be a multibyte character so
                #     # read another byte and try again
                #     u += fi.read(1)
                #
                #
                #     offset = fi.tell()
                #
                #     # grab surrounding bytes
                #     fi.seek(max(0, offset - 20))
                #     context = fi.read(40)
                #     context_cleaned = clean_context_bytes(context)
                #
                #     # back to original position
                #     fi.seek(offset)
                #
                #     logging.error(f"skipped byte {offset}: 0x{byte_s.hex().capitalize()} - {context_cleaned}")
                #
                # i = i + 1
