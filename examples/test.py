import numpy as np
from sourcegen import SourceGenerator

test_vector = np.random.randint(1, 100, size=10)
test_vector = list(map(str, sorted(test_vector)))

with SourceGenerator("test.cc") as source:
    source.generate("test_vector", ", ".join(test_vector))
    

