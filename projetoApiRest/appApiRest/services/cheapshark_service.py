import requests


class CheapSharkService:

    BASE_URL = "https://www.cheapshark.com/api/1.0"

    HEADERS = {
        "User-Agent": "BibliotecaJogos/1.0 (projeto-academico)"
    }

    @staticmethod
    def buscar_jogos_por_titulo(titulo):

        try:
            url = f"{CheapSharkService.BASE_URL}/games"

            response = requests.get(url,params={"title": titulo},headers=CheapSharkService.HEADERS,timeout=10)

            response.raise_for_status()

            jogos = response.json()

            return [
                 {
                    "id_externo": int(jogo["gameID"]),
                    "nome": jogo["external"],
                    "imagem": jogo["thumb"],
                    "metacritic_link": jogo.get("metacriticLink"),
                    "preco": float(jogo.get("salePrice")) if jogo.get("salePrice") else None,
                } 
                for jogo in jogos 
            ]
        except requests.exceptions.Timeout:
            return{
                "erro": "Erro ao buscar os jogos na API externa"
            }


    @staticmethod
    def buscar_ofertas():
        try:
            url = f"{CheapSharkService.BASE_URL}/deals"

            response = requests.get(
                url,
                headers=CheapSharkService.HEADERS,
                timeout=10
            )

            response.raise_for_status()

            ofertas = response.json()

            return [
                {
                    "nome": oferta["title"],
                    "preco_promocional": f"USD {float(oferta["salePrice"])}",
                    "preco_normal": f"USD {float(oferta["normalPrice"])}",
                    "desconto": f"{oferta.get('steamRatingPercent')}%",
                    "nota_metacritic": oferta.get("metacriticScore"),
                    "avaliacao_steam": oferta.get("steamRatingText"),
                    "imagem": oferta.get("thumb"),
                }
                for oferta in ofertas
            ]

        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro ao buscar ofertas: {str(e)}")