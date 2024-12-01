from src.vk import VK
from src.yandexdisk import YaDisk
from environs import Env
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='[{asctime}] #{levelname:8} {filename}:'
    '{lineno} - {name} - {message}',
    style='{'
    )


def main():
    logger.info('Начало работы')

    env = Env()
    env.read_env()
    vk_token = env('VK_TOKEN')

    user_id = input('Введите id vk-пользователя ')
    ya_token = input('Введите OAuth-токен Яндекс.Диска ')

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
