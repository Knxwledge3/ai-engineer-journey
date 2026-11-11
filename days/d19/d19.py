"""День 19. Деньги: стоимость запроса, бюджет, выбор модели."""

class BudgetExceeded(Exception):
    """Лимит расходов исчерпан."""

def cost_usd(usage, prices):
    """Стоимость одного запроса в долларах.
    usage: {"input_tokens", "output_tokens", "cache_read_tokens"}; чего нет, то 0.
    prices: цена за 1 000 000 токенов: {"input", "output", "cache_read"};
    если цены cache_read нет, считать кэш по цене input.
    """
    raise NotImplementedError('напиши меня')

class Budget:
    """Ограничитель расходов: агент не должен сжечь деньги в цикле."""

    def __init__(self, limit_usd):
        """Запомнить лимит, потрачено 0."""
        raise NotImplementedError('напиши меня')

    @property
    def left(self):
        """Остаток."""
        raise NotImplementedError('напиши меня')

    def add(self, cost):
        """Учесть расход. Отрицательный -> ValueError.
        Если после него траты превысят лимит -> BudgetExceeded, расход не учитывать.
        """
        raise NotImplementedError('напиши меня')

def cheapest_model(prices_by_model, usage):
    """prices_by_model: {модель: prices}. Вернуть имя модели, на которой этот usage дешевле всего.
    Пустой словарь -> ValueError.
    """
    raise NotImplementedError('напиши меня')
