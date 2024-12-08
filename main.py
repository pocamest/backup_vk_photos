from src.vk import VK
from src.yandexdisk import YaDisk
from environs import Env, EnvError
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[{asctime}] #{levelname:8} {filename}:'
    '{lineno} - {name} - {message}',
    style='{'
    )


def validate(value_type: str, value: str) -> None:
    data = {
        'vk_token': 'Некорректный ключ доступа VK API',
        'ya_token': 'Некорректный OAuth-токен Яндекс.Диска',
        'user_id': 'Некорректный id vk-пользователя'
    }
    if not value:
        raise ValueError(data.get(value_type, f'Неккоректный {value_type}'))


def main():
    logger.info('Начало работы')

    env = Env()
    env.read_env()

    try:
        vk_token = env('VK_TOKEN').strip()
        validate('vk_token', vk_token)
    except EnvError as e:
        logger.error(e)
        return
    except ValueError as e:
        logger.error(e)
        return

    user_id = input('Введите id vk-пользователя ').strip()
    try:
        validate('user_id', user_id)
    except ValueError as e:
        logger.error(e)
        return

    ya_token = input('Введите OAuth-токен Яндекс.Диска ').strip()
    try:
        validate('ya_token', ya_token)
    except ValueError as e:
        logger.error(e)
        return

    vk = VK(vk_token, user_id)
    logger.info('Получение фотографий с ВК...')
    photos = vk.get_photos(save_all_albums=False)
    logger.info(f'Получено {len(photos)} фотографий')

    yadisk = YaDisk(ya_token)
    path = '/vk_photos'
    logger.info(f'Загрузка фотографий на Яндекс.Диск по пути: {path}')
    yadisk.upload_photo(path, photos)

    logger.info('Завершение работы')


if __name__ == '__main__':
    main()
