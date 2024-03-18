import asyncio

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger

from src.storage.redis.db_redis import RedisDatabase


class CurrentCoursesGetter:
    URL = "https://garantex.org/"

    def __init__(self, redis: RedisDatabase):
        self.redis = redis
        self.ua = UserAgent()

    async def run(self) -> None:
        logger.info("start course getter")
        while True:
            await self.__save_current_course_to_db()
            await asyncio.sleep(60)

    async def __save_current_course_to_db(self):
        current_course_ask, current_course_bid, current_course_btc_ask = await self.__parse_html()
        if current_course_ask is None or current_course_bid is None or current_course_btc_ask is None:
            return None
        await self.redis.set_course_ask(current_course_ask)
        await self.redis.set_course_bid(current_course_bid)
        await self.redis.set_course_btc_ask(current_course_btc_ask)

    async def __headers(self):
        return {"User-Agent": self.ua.random}

    async def __get_html_text(self) -> str | None:
        async with ClientSession() as session:
            async with session.get(self.URL, headers=await self.__headers()) as resp:
                try:
                    return await resp.text()
                except Exception as e:
                    logger.error(f"error while getting html text: {e}")
                    return None

    async def __parse_html(self) -> tuple[float, float, float] | tuple[None, None, None]:
        html_text = await self.__get_html_text()
        if html_text is None:
            return None, None, None
        soup = BeautifulSoup(html_text, "lxml")
        scripts = soup.find_all("script")
        for script in scripts:
            if "var round_mode = BigNumber.ROUND_HALF_UP" in script.text:
                current_course_ask = self.__get_course(script.text, "ask", "usdt_price")
                current_course_bid = self.__get_course(script.text, "bid", "usdt_price")
                current_course_btc_ask = self.__get_course(script.text, "ask", "price")
                if current_course_ask is not None:
                    current_course_ask += 1
                if current_course_bid is not None:
                    current_course_bid -= 1
                if current_course_btc_ask is not None:
                    current_course_btc_ask += 1
                return current_course_ask, current_course_bid, current_course_btc_ask
        logger.warning("Current course not found, check parsed html garantex.org")
        return None, None, None

    @staticmethod
    def __get_course(find_text: str, find_key: str, find_value: str):
        index = find_text.find(find_key)
        index_course = find_text.find(find_value, index)
        text_before = find_text[index_course + len(find_value) + 2:]
        index_end = text_before.find(",")
        current_course = text_before[1 : index_end - 1]
        try:
            return float(current_course)
        except ValueError:
            logger.error(f"Current course {find_key} - {find_value} is not a float: {current_course}")
            return None
