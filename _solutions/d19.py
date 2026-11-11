"""День 19. Деньги: стоимость запроса, бюджет, выбор модели."""


class BudgetExceeded(Exception):
    """Лимит расходов исчерпан."""


def cost_usd(usage, prices):
    """Стоимость одного запроса в долларах.
    usage: {"input_tokens", "output_tokens", "cache_read_tokens"}; чего нет, то 0.
    prices: цена за 1 000 000 токенов: {"input", "output", "cache_read"};
    если цены cache_read нет, считать кэш по цене input.
    """
    cache_price = prices.get("cache_read", prices["input"])
    total = (
        usage.get("input_tokens", 0) * prices["input"]
        + usage.get("output_tokens", 0) * prices["output"]
        + usage.get("cache_read_tokens", 0) * cache_price
    )
    return total / 1_000_000


class Budget:
    """Ограничитель расходов: агент не должен сжечь деньги в цикле."""

    def __init__(self, limit_usd):
        """Запомнить лимит, потрачено 0."""
        self.limit_usd = limit_usd
        self.spent = 0.0

    @property
    def left(self):
        """Остаток."""
        return self.limit_usd - self.spent

    def add(self, cost):
        """Учесть расход. Отрицательный -> ValueError.
        Если после него траты превысят лимит -> BudgetExceeded, расход не учитывать.
        """
        if cost < 0:
            raise ValueError("отрицательный расход")
        if self.spent + cost > self.limit_usd:
            raise BudgetExceeded(f"лимит {self.limit_usd} превышен")
        self.spent += cost


def cheapest_model(prices_by_model, usage):
    """prices_by_model: {модель: prices}. Вернуть имя модели, на которой этот usage дешевле всего.
    Пустой словарь -> ValueError.
    """
    if not prices_by_model:
        raise ValueError("нет моделей")
    return min(prices_by_model, key=lambda m: cost_usd(usage, prices_by_model[m]))
