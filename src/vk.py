import requests


class VK:
    access_token: str
    user_id: str
    version: str
    count_photos: int
    url: str
    params: dict[str, str]
    all_photos: dict[str, dict[str, str]]

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
        self.all_photos = {}

    def get_photos(
            self,
            save_all_albums: bool = False,
    ) -> dict[str, dict[str, str]]:
        # Переделать чтобы возвращала до 5 фотографий наибольшего размера
        self._get_photos_album('profile')
        if save_all_albums and len(self.all_photos) < self.count_photos:
            album_ids = self._get_album_ids()
            for album_id in album_ids:
                self._get_photos_album(album_id)
                if len(self.all_photos) == self.count_photos:
                    break
        return self.all_photos

    def _get_photos_album(self, album_id: str) -> None:
        # Разделить на несколько методов
        url = f'{self.url}/photos.get'
        params = {
            'owner_id': self.user_id,
            'album_id': album_id,
            'extended': '1',
        }
        response = requests.get(url, params={**self.params, **params})
        for item in response.json()['response']['items']:
            if len(self.all_photos) == self.count_photos:
                break
            photo = sorted(
                item['sizes'],
                key=lambda x: x['height'] + x['width'])[-1]
            dict_photo = {
                    'url': photo['url'],
                    'size': photo['type'],
                }
            likes = str(item['likes']['count'])
            if likes in self.all_photos:
                photo_name = f'{likes}_{item["date"]}'
                self.all_photos[photo_name] = dict_photo
            else:
                self.all_photos[likes] = dict_photo

    def _get_album_ids(self) -> list[str]:
        url = f'{self.url}/photos.getAlbums'
        params = {'owner_id': self.user_id}
        response = requests.get(url, params={**self.params, **params})
        return [item['id']for item in response.json()['response']['items']]
