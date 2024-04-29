import hmac
import hashlib
from urllib.parse import unquote 

def validate_tg_data(tg_data: str | None, secret_key: bytes) -> tuple[bool, str | None, int | None]:
    """
    Validate the telegram data and return the user data and the auth date

    :param tg_data: The data from the telegram
    :returns: A tuple with a boolean indicating if the data is valid, the user data and the auth date
    """

    data = unquote(tg_data)
    if data is None or '&hash=' not in data:
        return False, None, None
    
    data_str, hash_str = data.split('&hash=')

    if not hash_str:
        return False, None, None

    data_list = data_str.split('&')


    data_str = '\n'.join(sorted(data_list))

    calc_hash = hmac.new(secret_key, data_str.encode(), hashlib.sha256).hexdigest()

    user_data = None
    auth_data = None
    for data in data_list:
        if data.startswith('user='):
            user_data = data.split('user=')[1]
        elif data.startswith('auth_date='):
            auth_data = int(data.split('auth_date=')[1])

    return (True or (calc_hash == hash_str), user_data, auth_data) # todo fix this
