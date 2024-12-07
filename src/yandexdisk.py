import requests
import json
import logging


class YaDisk:
    ya_token: str
    URL: str = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def __init__(self, ya_token: str) -> None:
        self.ya_token = ya_token
        self.headers = {
            'Authorization': ya_token,
        }
        self.logger = logging.getLogger(__name__)

    def upload_photo(
            self,
            path: str,
            photos: dict[str, dict[str, str]],
    ) -> None:
        '''Загрузка фотографий на Я.Диск'''
        url = f'{self.URL}upload'
        info_photos = []
        for key, value in photos.items():
            self._create_folder(path)
            params = {
                'path': f'{path}/{key}',
                'url': value['url']
            }
            try:
                res = requests.post(
                    url,
                    headers=self.headers,
                    params=params,
                ).json()
                info_photos.append({'file_name': key, 'size': value['size']})
            except Exception:
                self.logger.exception(
                    f'Ошибка при загрузге фотографии {params["path"]}'
                )
            if 'message' in res:
                self.logger.error(res['message'])
            else:
                self.logger.info(f'Загружена фотография {params["path"]}')
        self._write_json(info_photos)

    def _write_json(self, info_photos: list[dict[str, str]]) -> None:
        '''Запись в json файл информации о заруженных фотографиях'''
        try:
            with open('info_photos.json', 'w') as f:
                json.dump(info_photos, f, indent=4)
        except Exception:
            self.logger.exception('Ошибка при записи в json')

    def _create_folder(self, path: str) -> None:
        '''Создание директории в Я.Диске'''
        params = {'path': path}
        try:
            res = requests.put(
                self.URL,
                headers=self.headers,
                params=params
            )
        except Exception:
            self.logger.exception(
                f'Ошибка при создании директории {params["path"]}'
            )
        if res.status_code == 201:
            self.logger.info(f'Создана директория {params["path"]}')
        elif res.status_code == 409:
            self.logger.debug(res.json().get('message'))
        else:
            self.logger.error(res.json()['message'])
