from dataclasses import dataclass, field
from TrackedList import tlist
from collections.abc import Iterator
import tkinter

DELAY = 20
BG_COLOR = "#131313"
DEFAULT_FILL = "#C0C0C0"
CHECKING_INDEX = "#50FF50"
CURR_INDEX = "#FF5050"

@dataclass
class Engine():
    width: int
    height: int
    
    root: tkinter.Tk = field(init = False)
    canvas: tkinter.Canvas = field(init = False)
    
    arr: tlist = field(init = False)
    sort: Iterator[dict[int, str]] = field(init = False)
    
    def __post_init__(self) -> None:        
        self.root = tkinter.Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.canvas = tkinter.Canvas(self.root, height = self.height, width = self.width, bg = BG_COLOR)
        self.canvas.pack()
        
    def start(self) -> None:
        self.root.mainloop()
        
    def draw_rect(self, x1: int, y1: int, x2: int, y2: int, fill: str = "") -> None:
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = fill)

    def draw_array(self, arr: list[int] | tlist, colors: dict[int, str] = {}) -> None:
        self.canvas.delete("all")
        if (isinstance(arr, tlist)): self.canvas.create_text(10, 10, text = arr.info(), fill = DEFAULT_FILL, anchor = tkinter.NW)
        side_spacing = 5
        bar_spacing = 3
        bottom_spacing = 5

        count = len(arr)

        # Space available for the bars themselves
        available_width = (self.width - (2 * side_spacing) - (bar_spacing * (count - 1)))

        bar_width = available_width / count
        vertical_multiplier = 0.8
        max_bar_height_multiplier = ((self.height - bottom_spacing) / max(arr)) * vertical_multiplier
        
        for index, value in enumerate(arr):
            x1 = side_spacing + index * (bar_width + bar_spacing)
            x2 = x1 + bar_width
            y1 = self.height - bottom_spacing
            y2 = self.height - (max_bar_height_multiplier * value)
            self.draw_rect(round(x1), round(y2), round(x2), round(y1), colors.get(index, DEFAULT_FILL))
        
    def start_sort(self, arr: tlist, function) -> None:
        self.arr = arr
        self.sort = function(arr)
        self.next_step()
        
    def next_step(self) -> None:
        try:
            colors = next(self.sort)
            self.draw_array(self.arr, colors)
            self.root.after(int(DELAY), self.next_step)
        except StopIteration:
            ...
        
def selection_sort(arr: tlist):
    length = len(arr)
    for i in range(length - 1):
        j_min = i
        for j in range(i + 1, length):
            yield {j: CURR_INDEX, j_min: CHECKING_INDEX}
            if arr.is_lt(j, j_min):
                j_min = j
        
        arr.swap(i, j_min)
        yield {}

def bubble_sort(arr: tlist):
    length = len(arr)
    for i in range(length):
        swapped = False
        
        for j in range(0, length - i - 1):
            yield {i: CHECKING_INDEX, j: CURR_INDEX}
            if arr.is_gt(j, j + 1):
                arr.swap(j, j + 1)
                swapped = True
                yield {j: CURR_INDEX, j + 1: CURR_INDEX, i: CHECKING_INDEX}
                
        if (not swapped):
            break

def bidrectional_selection_sort(arr: tlist):
    length = len(arr)

    for i in range(length // 2):
        j_min = i
        j_max = i
        last = length - 1 - i

        for j in range(i + 1, last + 1):
            yield { j: CURR_INDEX, j_min: CHECKING_INDEX, j_max: "#5050FF" }
            if arr.is_lt(j, j_min): j_min = j
            if arr.is_gt(j, j_max): j_max = j

        if (j_max != last):
            arr.swap(j_max, last)
            if (j_min == last): j_min = j_max

        if (j_min != i):
            arr.swap(i, j_min)
        yield {}
    yield {}


n = 50
arr = tlist(list(range(1, n + 1)))
arr.shuffle()
engine = Engine(2000, 1000)
engine.start_sort(arr, bidrectional_selection_sort)
engine.start()
print(arr)