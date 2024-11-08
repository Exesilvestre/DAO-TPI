import requests

class CountryAPI:
    def __init__(self, base_url="https://restcountries.com/v3.1"):
        self.base_url = base_url
    # Obtiene la lista de países desde la API y la retorna.
    def obtener_paises(self):
        endpoint = f"{self.base_url}/all"
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
            paises = response.json()
            return sorted([pais.get('name', {}).get('common') for pais in paises if 'name' in pais])
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return []
