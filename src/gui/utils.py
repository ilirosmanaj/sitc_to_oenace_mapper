def _format_sitc_item(key, value):
    return f'{key} - {value}'


def _get_code_from_text(text: str):
    if not text:
        return None

    return text.split('-')[0].strip()
