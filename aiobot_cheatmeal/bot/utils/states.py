from aiogram.fsm.state import State, StatesGroup


# choose_location = ['Poolbar', 'Window', 'Curds']


class Location(StatesGroup):
    CHOOSE_LOCATION = State()
    SET_CASH = State()
    SET_NO_CASH = State()
    SET_WASTES = State()
    POOLBAR_CHOOSED = State()
    WINDOW_CHOOSED = State()
    TUBING_CHOOSED = State()
    any_report = State()
    CATEGORY_CHOOSED = State()
    MONEY_WASTES = State()
    MORE_WASTES = State()
    SET_DESCRIPTION = State()
    VARIANCE = State()
    VARIANCE_BAD = State()
    VARIANCE_GOOD = State()
    HALL = State()
    HALL_GOOD = State()
    HALL_BAD = State()
    BATTARY = State()
    BATTARY_GOOD = State()
    BATTARY_BAD = State()

    # States for a fill_main report
    HAVE_LOC = State()