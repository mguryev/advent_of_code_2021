import collections
import functools
import itertools


class Dice:
    def __init__(self):
        self.__rolls = itertools.cycle(
            range(1, 101)
        )
        self.__rolled_n = 0

    def roll(self):
        self.__rolled_n += 1
        return next(self.__rolls)

    def rolled_n(self):
        return self.__rolled_n


class Field:
    def __init__(self):
        self.__field = list(range(1, 11))

    def move(self, location, moves):
        location_idx = self.__field.index(location)
        next_location_idx = (location_idx + moves) % len(self.__field)
        return self.__field[next_location_idx]


class Player:
    def __init__(self, player_id, position, score=0):
        self.__id = player_id
        self.__position = position
        self.__score = score

    def player_id(self):
        return self.__id

    def move(self, position):
        self.__position = position
        self.__score += position

    def location(self):
        return self.__position

    def score(self):
        return self.__score

    def copy(self):
        return Player(
            self.__id,
            self.__position,
            self.__score,
        )


def part1():
    players = itertools.cycle([
        Player(player_id=1, position=4),
        Player(player_id=2, position=5),
    ])

    field = Field()
    dice = Dice()

    while True:
        current_player = next(players)

        moves = sum([dice.roll(), dice.roll(), dice.roll()])

        position = field.move(current_player.location(), moves)
        current_player.move(position)

        if current_player.score() >= 1000:
            break

    losing_player = next(players)
    print('result:', losing_player.score() * dice.rolled_n())


@functools.lru_cache()
def diracs_dice():
    dice = [1, 2, 3]

    rolls = {}

    for roll in itertools.product(dice, repeat=3):
        roll = sum(roll)
        rolls[roll] = rolls.get(roll, 0) + 1

    return rolls


PlayerDirac = collections.namedtuple(
    'PlayerDirac',
    ['position', 'score']
)


@functools.lru_cache(maxsize=None)
def play_game_diracs(
        field: Field,
        current_player: PlayerDirac, next_player: PlayerDirac,
):
    rolls = diracs_dice()

    current_player_wins = 0
    next_player_wins = 0

    for roll, roll_count in rolls.items():
        position = field.move(current_player.position, roll)

        _current_player = PlayerDirac(
            position,
            current_player.score + position
        )

        if _current_player.score >= 21:
            current_player_wins += roll_count
            continue

        (
            _next_player_wins,
            _current_player_wins,
        ) = play_game_diracs(
            field,
            next_player,
            _current_player,
        )

        current_player_wins += _current_player_wins * roll_count
        next_player_wins += _next_player_wins * roll_count

    return current_player_wins, next_player_wins


def part2():
    field = Field()

    players = [
        PlayerDirac(position=4, score=0),
        PlayerDirac(position=5, score=0),
    ]

    scores = play_game_diracs(
        field,
        players[0],
        players[1],
    )

    print(scores)


def run() -> None:
    part1()
    part2()


if __name__ == '__main__':
    run()
