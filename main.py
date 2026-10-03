from dataclasses import dataclass, field
from TrackedList import tlist
import tkinter

DELAY = 0.005
BG_COLOR = "#131313"
DEFAULT_FILL = "#C0C0C0"

@dataclass
class Engine():
    width: int
    height: int
    
    root: tkinter.Tk = field(init = False)
    canvas: tkinter.Canvas = field(init = False)
    
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
        if (isinstance(arr, tlist)): 
            self.canvas.create_text(10, 10, text = arr.info(), fill = DEFAULT_FILL, anchor = tkinter.NW)
        side_spacing = 10
        bar_spacing = 5
        bottom_spacing = 10

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
        
        
def selectionsort(arr: tlist, engine: Engine | None = None) -> None:
    length = len(arr)
    
    def step(i: int, j: int, j_min: int) -> None:
        if (i >= length - 1 or engine == None): return
        
        if (j >= length):
            if j_min != i:
                arr.swap(i, j_min)
            
            engine.draw_array(arr, {i: "#50FF50"})
            engine.root.after(int(DELAY * 1000), step, i + 1, i + 2, i + 1)
            return
        
        colors = {
            i: "#50FF50",
            j: "#FF0000",
            j_min: "#FFFF00"
        }
        engine.draw_array(arr, colors)
        if (arr.is_lt(j, j_min)):
            j_min = j
            
        engine.root.after(int(DELAY * 1000), step, i, j + 1, j_min)
    
    if (engine == None):
        # do normal here
        ...
    else:
        step(0, 1, 0)


arr = tlist(list(range(1, 50)))
arr.shuffle()
print(arr)

engine = Engine(1000, 800)

selectionsort(arr, engine)
engine.start()
print(arr)