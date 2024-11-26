import requests
from typing import Any


class VK:
    access_token: str
    user_id: str
    version: str
    count_photos: int
    url: str
    params: dict[str, str]

    def __init__(
            self, access_token: str, user_id: str,
            version: str = '5.199', count_photos: int = 5
    ) -> None:
        self.access_token = access_token
        self.user_id = user_id
        self.version = version
        self.count_photos = count_photos
        self.url = 'https://api.vk.com/method'
        self.params = {
            'access_token': self.access_token,
            'v': self.version,
        }

    def _choose_photos(
            self,
            photos: list[dict[str, str | int]],
            count=1,
    ) -> list[dict[str, str | int]]:
        '''Выбирает фотографии максимального разрешения'''
        return sorted(
            photos,
            key=lambda x: x['height'] * x['width'],
        )[-count:]

    def _processing_photo(self, item: dict[str, Any]):
        '''
        Формирует словарь с ключами:
            'likes', 'date', 'height', 'type', 'width', 'type'
        '''
        return {
            'likes': str(item['likes']['count']),
            'date': item['date'],
            **self._choose_photos(item['sizes'])[0],
        }

    def _combine_photos(self, responses: list[list[dict]]) -> list[dict]:
        '''Объединяет сформированные словари фотографий в один список'''
        return [self._processing_photo(item)
                for items in responses
                for item in items]

    def _format_photos(self, photos: list) -> list[dict[str, dict[str, str]]]:
        '''Форматирует для фотографий уникальные имена'''
        result = {}
        for photo in photos:
            if photo['likes'] in result:
                photo_name = f'{photo["likes"]}_{photo["date"]}'
            else:
                photo_name = photo['likes']
            result[photo_name] = {
                'url': photo['url'],
                'size': photo['type'],
            }
        return result

    def _make_request(
            self,
            url: str,
            params: dict[str, str],
    ) -> dict[str, Any]:
        # Надо добавить обработку ошибок и логгер
        response = requests.get(url, params)
        return response.json()

    def _get_items(self, album_id: str) -> list[dict[str, Any]]:
        '''Возвращает фографии из альбома'''
        url = f'{self.url}/photos.get'
        params = {
            'owner_id': self.user_id,
            'album_id': album_id,
            'extended': '1',
        }
        data = self._make_request(url, params={**self.params, **params})
        return data.get('response', {}).get('items', [])

    def _get_album_ids(self) -> list[str]:
        """Возвращает id всех альбомов пользователя"""
        url = f'{self.url}/photos.getAlbums'
        params = {'owner_id': self.user_id}
        response = requests.get(url, params={**self.params, **params})
        return [item['id']for item in response.json()['response']['items']]

    def get_photos(
            self,
            save_all_albums=False,
    ) -> list[dict[str, dict[str, str]]]:
        '''Возвращает  фотографии в виде словаря:
            ключи: уникальные имена фотографий
            значения: словари с служебной информацией'''
        albums = ['profile']
        if save_all_albums:
            albums.extend(self._get_album_ids())
        responses = [self._get_items(album) for album in albums]
        raw_photos = self._choose_photos(
            self._combine_photos(responses),
            count=self.count_photos,
        )
        return self._format_photos(raw_photos)
