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
        current_course = await self.__parse_html()
        if current_course is None:
            return None
        await self.redis.set_course(current_course)

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

    async def __parse_html(self) -> float | None:
        html_text = await self.__get_html_text()
        if html_text is None:
            return None
        soup = BeautifulSoup(html_text, "lxml")
        scripts = soup.find_all("script")
        for script in scripts:
            if "var round_mode = BigNumber.ROUND_HALF_UP" in script.text:
                index_bid = script.text.find("ask")
                index_course_rub = script.text.find("usdt_price", index_bid)
                text_before_bid = script.text[index_course_rub + 12 :]
                index_end = text_before_bid.find(",")
                current_course = text_before_bid[1 : index_end - 1]
                try:
                    return float(current_course) + 1
                except ValueError:
                    logger.error(f"Current course is not a float: {current_course}")
                    return None
        logger.warning("Current course not found, check parsed html garantex.org")
        return None
