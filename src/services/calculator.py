from datetime import datetime, timezone, timedelta
from typing import Any

from src.bot.lexicon.lexicon import Lexicon
from src.config import Config
from src.storage.db.models import Product


class Calculator:
    ALGORITHMS = ["sha256"]

    def __init__(self, lexicon: Lexicon, cfg: Config) -> None:
        self.algorithms: list = self.ALGORITHMS
        self.lexicon = lexicon
        self.cfg = cfg

    async def start_calculate_by_algorithm_and_get_text(
        self,
        algorithm: str,
        mining_profitability_usdt: float,
        product: Product,
        course: float,
        price_for_electricity: float,
    ) -> str | None:
        result = None
        if len(self.algorithms) == 0 or algorithm not in self.algorithms:
            result = await self.default_calculate(
                mining_profitability_usdt=mining_profitability_usdt,
                product=product,
                course=course,
                price_for_electricity=price_for_electricity,
            )
        else:
            if algorithm == self.algorithms[0]:
                result = await self.default_calculate(
                    mining_profitability_usdt=mining_profitability_usdt,
                    product=product,
                    course=course,
                    price_for_electricity=price_for_electricity,
                )
            elif algorithm == self.algorithms[1]:
                pass

        if result is None:
            return None
        return await self.__create_text(algorithm, result, product)

    @staticmethod
    async def default_calculate(
        mining_profitability_usdt: float,
        product: Product,
        course: float,
        price_for_electricity: float,
    ) -> dict[str, float]:
        profit_black_day = mining_profitability_usdt * product.terahesh * course
        cost_day = product.consumption / 1000 * 24 * price_for_electricity
        profit_white_day = profit_black_day - cost_day
        term = (product.price * course) / (profit_white_day * 30.5)
        return {
            "profit_black_day": profit_black_day,
            "cost_day": cost_day,
            "profit_white_day": profit_white_day,
            "term": term,
            "course": course,
            "price_for_electricity": price_for_electricity,
            "mining_profitability_usdt": mining_profitability_usdt,
        }

    async def __create_text(
        self,
        algorithm: str,
        result: dict[str, float],
        product: Product,
    ) -> str | tuple[Any]:
        profit_black_day = result["profit_black_day"]
        cost_day = result["cost_day"]
        profit_white_day = result["profit_white_day"]
        term = result["term"]
        course = result["course"]
        price_for_electricity = result["price_for_electricity"]
        mining_profitability_usdt = result["mining_profitability_usdt"]
        format_round = 2
        time_now = datetime.now(tz=timezone.utc) + timedelta(hours=3)
        if algorithm == "":
            return self.__default_text(
                mining_profitability_usdt=mining_profitability_usdt,
                product=product,
                course=course,
                price_for_electricity=price_for_electricity,
                profit_black_day=profit_black_day,
                cost_day=cost_day,
                profit_white_day=profit_white_day,
                term=term,
                time_now=time_now,
                format_round=format_round,
            )
        elif algorithm == self.algorithms[0]:
            return self.__algorithm_text(
                mining_profitability_usdt=mining_profitability_usdt,
                product=product,
                course=course,
                price_for_electricity=price_for_electricity,
                profit_black_day=profit_black_day,
                cost_day=cost_day,
                profit_white_day=profit_white_day,
                term=term,
                time_now=time_now,
                format_round=format_round,
            )
        elif algorithm == self.algorithms[1]:
            pass

    def __default_text(
        self,
        mining_profitability_usdt: float,
        product: Product,
        course: float,
        price_for_electricity: float,
        profit_black_day: float,
        cost_day: float,
        profit_white_day: float,
        term: float,
        time_now: datetime,
        format_round: int = 2,
    ) -> str | tuple[Any]:
        text = (
            self.lexicon.send.on_product_click.format(
                name=product.name,
                terahesh=product.terahesh,
                consumption=product.consumption / 1000,
                price_usdt=product.price,
                price_rub=round(product.price * (course + 1), format_round),
                mining_profitability_usdt=round(
                    mining_profitability_usdt, format_round
                ),
                price_for_electricity=price_for_electricity,
                profit_black_day=round(profit_black_day, format_round),
                cost_day=round(cost_day, format_round),
                profit_white_day=round(profit_white_day, format_round),
                profit_black_moth=round(profit_black_day * 30.5, format_round),
                cost_moth=round(cost_day * 30.5, format_round),
                profit_white_moth=round(profit_white_day * 30.5, format_round),
                term=round(term, 1),
                time_now=time_now.strftime(self.cfg.time_format),
                course=course,
            ),
        )
        if isinstance(text, tuple):
            return text[0]
        return text

    def __algorithm_text(
        self,
        mining_profitability_usdt: float,
        product: Product,
        course: float,
        price_for_electricity: float,
        profit_black_day: float,
        cost_day: float,
        profit_white_day: float,
        term: float,
        time_now: datetime,
        format_round: int = 2,
    ) -> str | tuple[Any]:
        text = (
            self.lexicon.send.algorithm_calculate.format(
                name=product.name,
                terahesh=product.terahesh,
                consumption=product.consumption / 1000,
                price_usdt=product.price,
                price_rub=round(product.price * (course + 1), format_round),
                mining_profitability_usdt=round(
                    mining_profitability_usdt, format_round
                ),
                price_for_electricity=price_for_electricity,
                profit_black_day=round(profit_black_day, format_round),
                cost_day=round(cost_day, format_round),
                profit_white_day=round(profit_white_day, format_round),
                profit_black_moth=round(profit_black_day * 30.5, format_round),
                cost_moth=round(cost_day * 30.5, format_round),
                profit_white_moth=round(profit_white_day * 30.5, format_round),
                term=round(term, 1),
                time_now=time_now.strftime(self.cfg.time_format),
                course=course,
            ),
        )
        if isinstance(text, tuple):
            return text[0]
        return text
