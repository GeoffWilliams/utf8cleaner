import logging

logger = logging.getLogger(__name__)



def clean(filename):
    output_filename = f"{filename}.clean"
    logger.info(f"Cleaning file {filename} and saving to {output_filename}")
    i = 0
    with open(filename, 'rb') as fi:
        with open(output_filename, 'wb') as fo:
            while 1:
                byte_s = fi.read(1)
                if not byte_s:
                    break
                try:
                    # `unicode()` function is gone from python3 and should be replaced with
                    # `str()` - see https://stackoverflow.com/a/38860645/3441106
                    u = str(byte_s, "utf-8")
                    fo.write(byte_s)
                except:
                    logging.error(f"skipped bad byte at offset {i}: 0x{byte_s.hex().capitalize()}")

            i = i + 1
