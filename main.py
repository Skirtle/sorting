from dataclasses import dataclass, field
from TrackedList import tlist
from collections.abc import Iterator
from random import randint
import tkinter

DELAY = 1
BG_COLOR = "#131313"
DEFAULT_FILL = "#C0C0C0"
MAIN_INDEX = "#50FF50"
INDEX_TO_CHECK = "#FF5050"
AUX_INDEX = "#6060FD"
AUX_INDEX_2 = "#47A5A8"

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
        self.canvas.create_rectangle(x1, y1, x2, y2, fill = fill, outline = fill)

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
        
    def start_sort(self, arr: tlist, generator) -> None:
        self.arr = arr
        self.sort = generator(arr)
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
            yield {j: INDEX_TO_CHECK, j_min: MAIN_INDEX}
            if arr.is_lt(j, j_min):
                j_min = j
        
        yield {i: INDEX_TO_CHECK, j_min: MAIN_INDEX}
        arr.swap(i, j_min)
    yield {}

def bubble_sort(arr: tlist):
    length = len(arr)
    for i in range(length):
        swapped = False
        
        for j in range(0, length - i - 1):
            yield {i: MAIN_INDEX, j: INDEX_TO_CHECK}
            if arr.is_gt(j, j + 1):
                arr.swap(j, j + 1)
                swapped = True
                yield {j: INDEX_TO_CHECK, j + 1: INDEX_TO_CHECK, i: MAIN_INDEX}
                
        if (not swapped):
            break
    yield {}

def bidrectional_selection_sort(arr: tlist):
    length = len(arr)

    for i in range(length // 2):
        j_min = i
        j_max = i
        last = length - 1 - i

        for j in range(i + 1, last + 1):
            yield { j: INDEX_TO_CHECK, j_min: MAIN_INDEX, j_max: "#5050FF" }
            if arr.is_lt(j, j_min): j_min = j
            if arr.is_gt(j, j_max): j_max = j

        if (j_max != last):
            arr.swap(j_max, last)
            if (j_min == last): j_min = j_max

        if (j_min != i):
            arr.swap(i, j_min)
        yield {}
    yield {}

def cycle_sort(arr: tlist):
    length = len(arr)
    
    for cycle_start in range(0, length - 1):
        item = arr[cycle_start]

        pos = cycle_start
        for i in range(cycle_start + 1, length):
            yield { i: INDEX_TO_CHECK, cycle_start: MAIN_INDEX }
            if (arr[i] < item): pos += 1
        if (pos == cycle_start): continue

        while (item == arr[pos]): pos += 1

        if (pos != cycle_start):
            yield { cycle_start: MAIN_INDEX, pos: INDEX_TO_CHECK, pos: AUX_INDEX}
            arr[pos], item = item, arr[pos]

        while (pos != cycle_start):
            pos = cycle_start

            for i in range(cycle_start + 1, length):
                yield { i: INDEX_TO_CHECK, cycle_start: MAIN_INDEX, pos: AUX_INDEX}
                if (arr[i] < item): pos += 1

            while (item == arr[pos]): pos += 1

            if (item != arr[pos]):
                yield { cycle_start: MAIN_INDEX, pos: INDEX_TO_CHECK }
                arr[pos], item = item, arr[pos]

        yield {}
    yield {}

def quick_sort(arr: tlist):
    def partition(arr: tlist, low: int, high: int):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if (arr[j] < pivot):
                i += 1
                arr.swap(i, j)
                yield {i: MAIN_INDEX, j: INDEX_TO_CHECK}

        arr.swap(i + 1, high)
        yield {i + 1: MAIN_INDEX, high: INDEX_TO_CHECK}

        return i + 1


    def quick_sort_main(arr: tlist, low: int, high: int):
        if (low < high):
            partition_gen = partition(arr, low, high)

            while True:
                try: yield next(partition_gen)
                except StopIteration as e:
                    pi = e.value
                    break

            yield from quick_sort_main(arr, low, pi - 1)
            yield from quick_sort_main(arr, pi + 1, high)

    
    yield from quick_sort_main(arr, 0, len(arr) - 1)
    yield {}

def bogo_sort(arr: tlist):
    sorted = False
    while (not sorted):
        length = len(arr)
        for i in range(length - 1):
            yield {i: MAIN_INDEX, i + 1: INDEX_TO_CHECK}
            if (arr.is_gt(i, i + 1)):
                sorted = False
                break
        else:
            sorted = True
        if (sorted): break
        arr.shuffle()

def insertion_sort(arr: tlist):
    length = len(arr)
    for i in range(1, length):
        key = arr[i]
        j = i - 1
        
        while (j >= 0 and key < arr[j]):
            yield {i: MAIN_INDEX, j: INDEX_TO_CHECK}
            arr[j+1] =arr[j]
            j -= 1
        arr[j + 1] = key
    yield {}

def merge_sort(arr: tlist):
    def merge(arr: tlist, left: int, mid: int, right: int):
        n1 = mid - left + 1
        n2 = right - mid
        
        L = tlist([0] * n1)
        R = tlist([0] * n2)
        
        for i in range(n1):
            L[i] = arr[left + i]
        for i in range(n2):
            R[i] = arr[mid + 1 + i]
            
        i = 0
        j = 0
        k = left
        
        while (i < n1 and j < n2):
            colors = {}
            for x in range(n1): colors[left + x] = AUX_INDEX
            for x in range(n2): colors[mid + 1 + x] = AUX_INDEX_2
            yield colors
            
            if L[i] <= R[j]:
                arr.comparisons += 1
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
            
        while i < n1:
            arr[k] = L[i]
            i += 1
            k += 1
            
        while j < n2:
            arr[k] = R[j]
            j += 1
            k += 1
            
        tlist.reads += L.reads + R.reads
        tlist.writes += L.writes + R.writes
        tlist.comparisons += L.comparisons + R.comparisons
        tlist.swaps += L.swaps + R.swaps
        
    def merge_sort_main(arr, left, right):
        if (left < right):
            mid = (left + right) // 2

            reds = {}
            for i in range(left, mid + 1): reds[i] = INDEX_TO_CHECK
            yield from merge_sort_main(arr, left, mid)
            # yield reds
            
            reds = {}
            for i in range(mid + 1, right + 1): reds[i] = INDEX_TO_CHECK
            yield from merge_sort_main(arr, mid + 1, right)
            # yield reds
            
            yield from merge(arr, left, mid, right)
    
    yield from merge_sort_main(arr, 0, len(arr) - 1)
    yield {}

n = 100
arr = tlist(list(range(1, n + 1)))
arr.shuffle()
engine = Engine(2000, 1000)
engine.start_sort(arr, merge_sort)
engine.start()
print(arr.info())