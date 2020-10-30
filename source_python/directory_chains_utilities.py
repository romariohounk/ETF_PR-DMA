import os
import errno
import json
from datetime import datetime


def validate_or_make_directory(directory_string):
    """
    Check if a directory exists. If it doesn't, then create it.

    :param directory_string: The relative directory string (ex: ../.config/secrets.json)
    :type directory_string: str
    """
    if not os.path.exists(os.path.dirname(directory_string)):
        try:
            os.makedirs(os.path.dirname(directory_string))
            print("Successfully created `{}` file directory".format(directory_string))
        except OSError as exception:  # Guard against race condition
            if exception.errno != errno.EEXIST:
                raise


def get_json_from_file(directory_string, default_json_content=None):
    """
    Get the contents of a JSON file. If it doesn't exist,
    create and populate it with specified or default JSON content.

    :param directory_string: The relative directory string (ex: ../.config/secrets.json)
    :type directory_string: str
    :param default_json_content: The content to populate a non-existing JSON file with
    :type default_json_content: dict, list
    """
    validate_or_make_directory(directory_string)
    try:
        with open(directory_string) as file:
            file_content = json.load(file)
            file.close()
            return file_content
    except (IOError, json.decoder.JSONDecodeError):
        with open(directory_string, "w") as file:
            if default_json_content is None:
                default_json_content = {}
            json.dump(default_json_content, file, indent=4)
            file.close()
            return default_json_content


def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


def write_json_to_file(directory_string, json_content):
    """
    Get the contents of a JSON file. If it doesn't exist,
    create and populate it with specified or default JSON content.

    :param directory_string: The relative directory string (ex: ../.config/secrets.json)
    :type directory_string: str
    :param json_content: The content to populate a non-existing JSON file with
    :type json_content: dict
    """
    with open(directory_string, "w") as file:
        json.dump(json_content, file, default = datetime_converter, indent=4)
        file.close()

def get_secrets():
    secrets_file_directory = os.path.expanduser('../.config/secrets_etf.json')
    secrets_template = {}
    secrets_content = get_json_from_file(secrets_file_directory, secrets_template)
    if secrets_content == secrets_template:
        print("Please completed the 'secrets_etf.json' file in your '../.config' directory")
        exit()
    return secrets_content


def make_slack_etf_chain(last_price, number, close_value, adx_value, rsi_value, stochs_value, cci_value, signal):
    slack_str = "*\n>>>\n_Last Price : *" + str(round(last_price, 2)) + \
                "*_\n_Number : *" + str(round(number, 2)) + \
                "*_\n_Closed Price : *" + str(round(close_value, 2)) + \
                "*_\n_ADX : *" + str(round(adx_value, 2)) + \
                "*_\n_RSI : *" + str(round(rsi_value, 2)) + \
                "*_\n_Stochs : *" + str(round(stochs_value, 2)) + \
                "*_\n_CCI : *" + str(round(cci_value, 2)) + \
                "*_\n_Signal : *" + signal + "*_"
    return slack_str


def make_slack_etf_chain_total(value, currency):
    slack_str = "\n_Total : *" + str(round(value, 2)) + " " + currency + \
                    "*_\n_---------------------------------_\n"
    return slack_str

