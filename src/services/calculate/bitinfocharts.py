from aiohttp import ClientSession
from bs4 import BeautifulSoup
from loguru import logger

from src.storage.db.connect import DBConnect


class BitinfochartsProfitability:
    URL = "https://bitinfocharts.com/"

    def __init__(self, db_connect: DBConnect) -> None:
        self.db_connect = db_connect

    async def parse_mining_profitability_usdt(self) -> float | None:
        mining_info_text = await self.__get_mining_info()
        soup = BeautifulSoup(mining_info_text, "lxml")
        try:
            td_mining_profitability_title = soup.find("td", text="Mining Profitability")
            if td_mining_profitability_title:
                td_mining_profitability_text = (
                    td_mining_profitability_title.find_next_sibling("td")
                )
                if td_mining_profitability_text:
                    return float(
                        td_mining_profitability_text.text.strip().split(" ")[0]
                    )

            logger.error("Error while parsing mining profitability")
        except Exception as e:
            logger.error(f"Error while parsing mining profitability: {e}")
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
