from src.vk import VK
from src.yandexdisk import YaDisk
from environs import Env


def main():
    env = Env()
    env.read_env()
    vk_token = env('VK_TOKEN')

    # ya_token = env('YA_TOKEN')
    # user_id = env('VK_ID')

    user_id = input('Введите id vk-пользователя ')
    ya_token = input('Введите OAuth-токен Яндекс.Диска ')

    vk = VK(vk_token, user_id)
    photos = vk.get_photos(save_all_albums=True)

    yadisk = YaDisk(ya_token)
    yadisk.upload_photo('/vk_photos', photos)


if __name__ == '__main__':
    main()
