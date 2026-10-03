from dataclasses import dataclass as _dataclass, field as _field
from random import shuffle as _shuffle, seed as _seed

@_dataclass
class tlist():
    values: list[int] = _field(default_factory = list[int])
    reads: int = 0
    writes: int = 0
    swaps: int = 0
    comparisons: int = 0
    
    def __len__(self) -> int:
        return len(self.values)
    
    def __getitem__(self, index: int) -> int: 
        self.reads += 1
        return self.values[index]
    
    def __setitem__(self, index: int, value: int) -> None:
        self.writes += 1
        self.values[index] = value
        
    def __iter__(self):
        return iter(self.values)
        
    def shuffle(self, seed: int | None = None) -> None: 
        _seed(seed)
        _shuffle(self.values)
    
    def reset(self, shuffle_values: bool = True) -> None: 
        self.reads = 0
        self.writes = 0
        self.swaps = 0
        self.comparisons = 0
        if (shuffle_values): self.shuffle()
        
    def is_gt(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] > self[index_2]
    
    def is_gte(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] >= self[index_2]
    
    def is_lt(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] < self[index_2]
    
    def is_lte(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] <= self[index_2]
    
    def is_eq(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] == self[index_2]
    
    def is_neq(self, index_1: int, index_2: int) -> bool:
        self.comparisons += 1
        return self[index_1] != self[index_2]
        
    def swap(self, index_1: int, index_2: int) -> None:
        self.swaps += 1
        temp = self[index_1]
        self[index_1] = self[index_2]
        self[index_2] = temp
    
    def get(self, index: int) -> int: return self.values[index]
    
    def info(self) -> str:
        return f"Writes: {self.writes}\nReads: {self.reads}\nSwaps: {self.swaps}\nComparisons: {self.comparisons}"