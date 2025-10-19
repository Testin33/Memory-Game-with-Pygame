from game.core import GameLogic, GameConfig, GameState


def test_logic_sequence_and_win():
    logic = GameLogic(GameConfig(rows=2, cols=2, total_seconds=40), seed=123)
    # consume showing until playing
    while logic.state == GameState.SHOWING:
        logic.update_showing()
    assert logic.state == GameState.PLAYING
    for coord in logic.pattern:
        logic.input_click(coord)
    assert logic.state == GameState.WON


def test_logic_wrong_click_loses_after_five():
    logic = GameLogic(GameConfig(rows=2, cols=2, total_seconds=40, max_wrong=5), seed=1)
    while logic.state == GameState.SHOWING:
        logic.update_showing()
    assert logic.state == GameState.PLAYING
    wrong = (9, 9)
    # 4 wrong attempts: still playing
    for _ in range(4):
        logic.input_click(wrong)
        assert logic.state == GameState.PLAYING
    # 5th wrong: lose
    logic.input_click(wrong)
    assert logic.state == GameState.LOST


def test_timer_loss():
    logic = GameLogic(GameConfig(rows=2, cols=2, total_seconds=0), seed=1)
    logic.tick()
    assert logic.state == GameState.LOST


