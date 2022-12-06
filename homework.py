class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance_covered = self.action * self.LEN_STEP / self.M_IN_KM
        return distance_covered

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        movement_speed = self.get_distance() / self.duration
        return movement_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        workout_message = InfoMessage(self.__class__.__name__,
                                      self.duration,
                                      self.get_distance(),
                                      self.get_mean_speed(),
                                      self.get_spent_calories())
        return workout_message


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить дистанцию в км."""
        calorie_consumption = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                               * self.get_mean_speed()
                               + self.CALORIES_MEAN_SPEED_SHIFT)
                               * self.weight / self.M_IN_KM
                               * self.duration * self.MIN_IN_H)
        return calorie_consumption


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTI = 0.035
    CALORIES_MEAN_SPEED_SH = 0.029
    KMH_IN_MSEС = 0.278
    CM_IN_M = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_in_sec = self.get_mean_speed() * self.KMH_IN_MSEС
        height_in_m = self.height / self.CM_IN_M
        calorie_consumption = ((self.CALORIES_MEAN_SPEED_MULTI
                               * self.weight
                               + (speed_in_sec ** 2 / height_in_m)
                               * self.CALORIES_MEAN_SPEED_SH
                               * self.weight)
                               * self.duration * self.MIN_IN_H)
        return calorie_consumption


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_SW_1 = 1.1
    LEN_SW_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.LEN_STEP = 1.38
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        mean_speed_swimming = (self.length_pool
                               * self.count_pool
                               / self.M_IN_KM
                               / self.duration)
        return mean_speed_swimming

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calorie_consumption = ((self.get_mean_speed() + self.LEN_SW_1)
                               * self.LEN_SW_2
                               * self.weight
                               * self.duration)
        return calorie_consumption


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    return type_of_training[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
