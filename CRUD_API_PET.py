import unittest
import requests


class TestPetStoreAPI(unittest.TestCase):
    base_url = 'https://petstore.swagger.io/v2/store'
    api_key = 'special-key'  # API ключ для авторизации

    def setUp(self):
        # Для каждого теста создаем заголовки с API ключом
        self.headers = {
            'accept': 'application/json',
            'api_key': self.api_key
        }

    def test_create_order_positive(self):
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "id": 1,
            "petId": 12,
            "quantity": 1,
            "shipDate": "2023-07-31T06:58:00.718Z",
            "status": "placed",
            "complete": True
        }
        response = requests.post(f'{self.base_url}/order', headers=self.headers, json=data)
        self.assertEqual(response.status_code, 200)

    def test_create_order_negative_invalid_data(self):
        headers = {
            'Content-Type': 'application/json'
        }
        invalid_data = {

            "id": -1.5,  # id должен быть целым числом
            "petId": 12,
            "quantity": 1,
            "shipDate": "2023-07-31T06:58:00.718Z",
            "status": "placed",
            "complete": True
        }

        response = requests.post(f'{self.base_url}/order', headers=self.headers, json=invalid_data)
        self.assertEqual(response.status_code, 400)

    def test_get_order_valid_order_id(self):
        valid_order_id = 12
        url = f'{self.base_url}/order/{valid_order_id}'
        headers = {
            'accept': 'application/json'
        }
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_get_order_invalid_order_id(self):
        invalid_order_id = -1  # Пример некорректного orderId (значение меньше 1)
        url = f'{self.base_url}/order/{invalid_order_id}'
        headers = {
            'accept': 'application/json'
        }

        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_order_positive(self):
        order_id = 1
        url = f'{self.base_url}/order/{order_id}'
        headers = {
            'accept': 'application/json'
        }

        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_order_negative_invalid_id(self):
        invalid_order_id = -1  # Пример некорректного orderId (значение меньше 1)
        url = f'{self.base_url}/order/{invalid_order_id}'
        headers = {
            'accept': 'application/json'
        }

        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get_inventory(self):
        url = f'{self.base_url}/inventory'
        headers = {
            'accept': 'application/json'
        }
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
