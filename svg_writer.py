import io
import math
import typing


from settings import settings


def write_image(state, filename):
    image = Image(filename)
    write_header(image)
    write_x_axis(state, image)
    write_y_axis(state, image)
    write_boxes(state, image)
    write_footer(image)


class Image:
    def __init__(self, filename):
        self.file = io.open(filename, "w")
        self.indentation = 0

    def push(self, header: str):
        self.append(header)
        self.indentation += 1

    def pop(self, footer: str):
        assert self.indentation > 0
        self.indentation -= 1
        self.append(footer)

    def append(self, line: str):
        self.write_indent()
        print(line, file=self.file)

    def write_indent(self):
        self.file.write("  " * self.indentation)

    def __del__(self):
        self.file.close()


def write_line(x1: int, y1: int, x2: int, y2: int, image: Image):
    image.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        'style="stroke:rgb(99,99,99);stroke-width:0.5" />')


def write_color_line(x1: int, y1: int, x2: int, y2: int, color, image: Image):
    image.append(
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'style="stroke:rgb({color});stroke-width:0.5" />')


def write_text(
        x: int, y: int, rot: int,
        text: str, eid: str, align: str, image: typing.TextIO):
    image.append(
        f'<text text-anchor="{align}" x="{x}" y="{y}" '
        f'transform="rotate({rot}, {x}, {y})" '
        f'fill="rgb(0,0,0)" id="{eid}">{text}</text>')


def write_text_row(row: int, text: str, eid: str, image: typing.TextIO):
    # A fudging to make the text appear centered on the row.
    text_height_fudge = 8
    x = settings.left_gap - 1
    y = settings.grid_top_gap + (row * settings.row_height) - text_height_fudge
    write_text(x, y, 0, text, eid, "end", image)


def write_box(
        x: int, y: int, width: int, height: int, title: str,
        image: typing.TextIO,  **kwargs):
    line = f'<rect x="{x}" y="{y}" width="{width}" height="{height}"'
    opacity = kwargs.get("opacity")
    if opacity is not None:
        line += f' fill-opacity="{opacity}"'
    color = kwargs.get("color")
    if color is not None:
        line += f' fill="rgb({color})"'
    line += '>'
    image.push(line)
    image.append(f'<title>{title}</title>')
    image.pop('</rect>')


def write_box_color(
        x: int, y: int,
        width: int, height: int,
        title: str, color: str, image: typing.TextIO):

    image.push(
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
        f'title="{title}" style="fill:rgb({color})">')
    image.append(f'<title>{title}</title>')
    image.pop('</rect>')


def write_box_value(
        x: int, y: int,
        width: int, height: int,
        title: str, value: float, image: typing.TextIO):
    shade = (value / settings.color_range) * 255
    if value > 0:
        color = f"0, {shade}, 0"
    else:
        color = f"{-shade}, 0, 0"
    write_box_color(x, y, width, height, title, color, image)


def write_box_grid(
        row: int, column: int, title: str, value: float, image: typing.TextIO):
    col_width = settings.column_width
    row_height = settings.row_height

    fill_rate = 0.8
    box_width = col_width * fill_rate
    box_height = row_height * fill_rate

    width_gap = (1.0 - fill_rate) * col_width * 0.5
    height_gap = (1.0 - fill_rate) * row_height * 0.5

    x = settings.left_gap + column * col_width + width_gap
    y = settings.grid_top_gap + (row-1) * row_height + height_gap
    write_box_value(x, y, box_width, box_height, title, value, image)


def write_box_row(
        row: int, end_x: int, title: str, color, image: typing.TextIO):
    x = settings.left_gap
    y = settings.grid_top_gap + (row-1) * settings.row_height
    box_width = end_x - settings.left_gap
    box_height = settings.row_height
    write_box(
        x, y, box_width, box_height, title, image, color=color, opacity=0.5)


def write_x_axis(state, image):
    num_columns = state.gpus[-1].column + 1
    x1 = settings.left_gap
    x2 = settings.left_gap + (num_columns * settings.column_width)
    y = settings.timeline_gap
    write_line(x1, y, x2, y, image)

    text_height_fudge = 20

    for year in state.years:
        column = state.annums[year].column
        x = settings.left_gap + (column * settings.column_width)
        write_line(
            x, settings.timeline_gap,
            x, settings.timeline_gap - (0.7 * settings.row_height), image)
        write_text(
            x,
            settings.timeline_gap + text_height_fudge,
            0,
            f"{year}", f"tick-{year}", "middle", image)

    for gpu in state.gpus:
        column = gpu.column
        x = settings.left_gap + (column * settings.column_width) \
            + text_height_fudge
        y = settings.timeline_gap - settings.row_height
        write_text(x, y, -90, f"{gpu.label}", f"{gpu.label}", "start", image)
        last_row_y = \
            settings.timeline_gap + (len(state.gpus) + 1) * settings.row_height
        x -= (0.3 * text_height_fudge)
        color = gpu.id[:3] == "amd" and "100, 0, 0" or "0, 100, 0"
        write_color_line(x, y, x, last_row_y, color, image)


def write_y_axis(state, image):
    num_columns = state.gpus[-1].column + 1
    end_x = settings.left_gap + (num_columns * settings.column_width)

    for i, gpu in enumerate(state.gpus):
        write_text_row(gpu.row, gpu.label, gpu.label, image)
        color = gpu.id[:3] == "amd" and "255, 230, 230" or "230, 255, 230"
        write_box_row(gpu.row, end_x, gpu.label, color, image)


def find_exponential_growth(v_i: float, v_j: float, dt: float) -> float:
    if dt == 0:
        # Instantaneous change doesn't have a rate.
        return math.nan
    return math.log(v_j / v_i) / dt


def num_months_between(old, new):
    """Return the number of month transitions between the two dates."""
    return (new.year - old.year) * 12 + (new.month - old.month)


def write_boxes(state, image):
    for old_index, old_gpu in enumerate(state.gpus):
        row = old_gpu.row
        for new_index, new_gpu in enumerate(state.gpus[old_index + 1:]):
            column = new_gpu.column
            num_months = num_months_between(old_gpu.date, new_gpu.date)
            num_years = num_months / 12
            rate = find_exponential_growth(
                old_gpu.rating, new_gpu.rating, num_years)
            rate_percent = rate * 100
            title = (
                f"{old_gpu.name} → {new_gpu.name}\n"
                f"{old_gpu.rating} → {new_gpu.rating} = "
                f"{new_gpu.rating - old_gpu.rating} increase\n"
                f"{num_years:.1f} years\n"
                f"{rate_percent:.2f}% / year"
            )
            write_box_grid(row, column, title, rate_percent, image)


def write_header(image: Image):
    image.append('<?xml version="1.0" standalone="no" ?>')
    image.push(
        f'<svg '
        # f'width="{settings.image_width}" '
        # f'height="{settings.image_height}" '
        'version="1.1" id="svgRoot" xmlns="http://www.w3.org/2000/svg">')


def write_footer(image: Image):
    image.pop('</svg>')
