from types import SimpleNamespace

def make_settings():
    settings = dict(
        scale=1,
        row_height=30,
        column_width=30,
        timeline_gap=120,
        grid_top_gap=150,
        left_gap=100,
        color_range=100)

    return SimpleNamespace(**settings)


settings = make_settings()
