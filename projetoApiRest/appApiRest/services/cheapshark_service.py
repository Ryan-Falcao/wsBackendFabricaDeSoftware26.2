import requests


class CheapSharkService:

    BASE_URL = "https://www.cheapshark.com/api/1.0"

    HEADERS = {
        "User-Agent": "BibliotecaJogos/1.0 (projeto-academico)"
    }

    @staticmethod
    def buscar_jogos_por_titulo(titulo):

        url = f"{CheapSharkService.BASE_URL}/games"

        response = requests.get(url,params={"title": titulo},headers=CheapSharkService.HEADERS,timeout=10)

        response.raise_for_status()

        jogos = response.json()

        return [
            {
                "id_externo": int(jogo["gameID"]),
                "nome": jogo["external"]
            }
            for jogo in jogos
        ]