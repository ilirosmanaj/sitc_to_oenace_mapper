def format_sitc_item(key, value):
    return f'{key} - {value}'


def get_code_from_text(text: str):
    if not text:
        return None

    return text.split('-')[0].strip()


def get_sitc_code_from_mapping_text(text: str):
    if not text:
        return None

    return text.split('->')[0].split('-')[0].strip()
