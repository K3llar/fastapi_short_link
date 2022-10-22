from string import ascii_letters, digits

'''Константы'''
SYMBOLS = f'{ascii_letters}{digits}'
MAX_LEN_SHORT_URL = 16
MIN_LEN_SHORT_URL = 1
LEN_SHORT_URL = 6
PATTERN = rf'^[{SYMBOLS}]+$'

'''Сообщения'''
NAME_BUSY = 'Ссылка <{}> уже занята!'
PRIVATE_URL = 'Отсутствует доступ к данной записи'
NOT_FOUND = 'Ссылка <{}> не найдена'
BAD_NAMING = 'Указано недопустимое имя для короткой ссылки'
EMPTY_FIELD = 'Поле <{}> не может быть пустым!'
EMPTY_REQUEST = 'Запрос не может быть пустым!'
