from dataclasses import dataclass


@dataclass
class Price:
    amount_dog_treat: float
    amount_belly_rub: float

    def __post_init__(self) -> None:
        self.amount_dog_treat = 0 if self.amount_dog_treat < 0 else self.amount_dog_treat
        self.amount_belly_rub = 0 if self.amount_belly_rub < 0 else self.amount_belly_rub

    def __mul__(self, o: "float | Price") -> "Price":
        if isinstance(o, Price):
            return Price(
                amount_dog_treat=self.amount_dog_treat * o.amount_dog_treat,
                amount_belly_rub=self.amount_belly_rub * o.amount_belly_rub,
            )
        return Price(
            amount_dog_treat=self.amount_dog_treat * o,
            amount_belly_rub=self.amount_belly_rub * o,
        )

    def __truediv__(self, o: "float | Price") -> "Price":
        if isinstance(o, Price):
            return Price(
                amount_dog_treat=self.amount_dog_treat / o.amount_dog_treat,
                amount_belly_rub=self.amount_belly_rub / o.amount_belly_rub,
            )
        return Price(
            amount_dog_treat=self.amount_dog_treat / o,
            amount_belly_rub=self.amount_belly_rub / o,
        )

    def __add__(self, o: "float | Price") -> "Price":
        if isinstance(o, Price):
            return Price(
                amount_dog_treat=self.amount_dog_treat + o.amount_dog_treat,
                amount_belly_rub=self.amount_belly_rub + o.amount_belly_rub,
            )
        return Price(
            amount_dog_treat=self.amount_dog_treat + o,
            amount_belly_rub=self.amount_belly_rub + o,
        )

    def __sub__(self, o: "float | Price") -> "Price":
        if isinstance(o, Price):
            return Price(
                amount_dog_treat=self.amount_dog_treat - o.amount_dog_treat,
                amount_belly_rub=self.amount_belly_rub - o.amount_belly_rub,
            )
        return Price(
            amount_dog_treat=self.amount_dog_treat - o,
            amount_belly_rub=self.amount_belly_rub - o,
        )
