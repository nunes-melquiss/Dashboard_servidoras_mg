def format_number(value,prefix=''):
    for unit in ['mil','milhões']:
        if value < 1000000:
            return f'{prefix} {value/1000:.1f} {unit}'
        value /= 1000
    return f'{prefix} {value/1000:.1f} bilhões'

