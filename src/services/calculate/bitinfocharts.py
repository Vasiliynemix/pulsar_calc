from aiohttp import ClientSession
from bs4 import BeautifulSoup, NavigableString, Tag
from loguru import logger

from src.storage.db.connect import DBConnect


class BitinfochartsProfitability:
    URL = "https://bitinfocharts.com/"

    def __init__(self, db_connect: DBConnect) -> None:
        self.db_connect = db_connect

    async def parse_mining_profitability_usdt(self, coin: str) -> float | None:
        mining_info_text = await self.__get_mining_info()
        soup = BeautifulSoup(mining_info_text, "lxml")
        try:
            td_mining_profitability_title = soup.find("td", text="Mining Profitability")
            if td_mining_profitability_title:
                tr_containing_td = td_mining_profitability_title.parent
                td_with_specific_class = tr_containing_td.find("td", class_=f'c_{coin}')
                if td_with_specific_class:
                    return float(td_with_specific_class.text.strip().split(" ")[0])

                # td_mining_profitability_text = (
                #     td_mining_profitability_title.find_next_sibling("td")
                # )
                # if td_mining_profitability_text:
                #     return float(
                #         td_mining_profitability_text.text.strip().split(" ")[0]
                #     )

            logger.error("Error while parsing mining profitability")
        except Exception as e:
            logger.error(f"Error while parsing mining profitability: {e}")
        return None

    async def parse_btc_on_usdt(self) -> float | None:
        btc_on_usdt_info_text = await self.__get_mining_info()
        soup = BeautifulSoup(btc_on_usdt_info_text, "lxml")
        try:
            tr_price_btc = soup.find("tr", {"id": "t_price"})

            if tr_price_btc:
                td_price_btc_title = tr_price_btc.find("td", text="Price")

                if td_price_btc_title:
                    td_price_btc_on_usdt = td_price_btc_title.find_next_sibling("td")
                    btc_on_usdt = await self.__get_btc_on_usdt_by_span(td_price_btc_on_usdt)

                    if btc_on_usdt:
                        return btc_on_usdt

            logger.error("Error while parsing btc on usdt")
        except Exception as e:
            logger.error(f"Error while parsing btc on usdt: {e}")
        return None

    async def __get_mining_info(self) -> str | None:
        try:
            async with ClientSession() as session:
                async with session.get(self.URL) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    else:
                        logger.error(f"Error while getting mining info: {resp.status}")
        except Exception as e:
            logger.error(f"Error while getting mining info: {e}, {resp.status}")
        return None

    @staticmethod
    async def __get_btc_on_usdt_by_span(
        td_price_btc_on_usdt: Tag | NavigableString | None,
    ) -> None | float:
        first_span = td_price_btc_on_usdt.find("span")
        if first_span:
            btc_on_usdt = first_span.find("span").text.replace(",", "")
            return float(btc_on_usdt)

        return None
