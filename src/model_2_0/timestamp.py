class Timestamp:
    def __init__(self, day, step):
        if day < 0:
            raise ValueError(f'Expected `day` to be >= 0. Got {day}')
        if step < 0:
            raise ValueError(f'Expected `step` to be >= 0. Got {step}')
        self.day = day
        self.step = step
