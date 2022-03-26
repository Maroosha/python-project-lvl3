"Auxilary in-out functions for page_loader.py."

import logging


def write_to_file(filepath: str, data: str, flag='w'):
    """Write webpage content to file.

    Parameters:
        filepath: path to file,
        data: data to be written to file.
    """
    try:
        with open(filepath, flag) as file_:
            file_.write(data)
    except PermissionError as error1:
        print(f'Access denied to file {filepath}.')
        logging.error('Access denied to file %s.', filepath)
        raise error1
    except OSError as error2:
        print(f'Unable to write to file {filepath}.')
        logging.error('Unable to write to file %s.', filepath)
        raise error2
