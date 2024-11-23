import requests
import json


class YaDisk:
    def __init__(self, ya_token: str) -> None:
        self.ya_token = ya_token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'
        self.headers = {
            'Authorization': ya_token,
        }

    def upload_photo(
            self,
            path: str,
            photos: dict[str, dict[str, str]],
    ) -> None:
        url = f'{self.url}upload'
        info_photos = []
        for key, value in photos.items():
            self._create_folder(path)
            params = {
                'path': f'{path}/{key}',
                'url': value['url']
            }
            requests.post(url, headers=self.headers, params=params)
            info_photos.append({'file_name': key, 'size': value['size']})
        self._write_json(info_photos)

    def _write_json(self, info_photos: list[dict[str, str]]) -> None:
        with open('info_photos.json', 'w') as f:
            json.dump(info_photos, f)

    def _create_folder(self, path: str) -> None:
        params = {'path': path}
        response = requests.put(self.url, headers=self.headers, params=params)
        if response.status_code == 201:
            print(f'Создана папка {path}')  # Потом переделать на логгер
        elif response.status_code != 409:
            print(response.json().get('message'))  # Потом переделать на логгер

    def _is_exist(self, path: str) -> bool:
        params = {'path': path}
        response = requests.get(self.url, headers=self.headers, params=params)
        return response.status_code == 200
