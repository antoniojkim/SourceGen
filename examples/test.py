import numpy as np
from sourcegen import SourceGenerator

test_vector = np.random.randint(1, 100, size=25)
test_vector = list(map(str, sorted(test_vector)))

with SourceGenerator("test.cc") as source:
    source["test_vector"].set_text(test_vector, delimiter=", ", wrap_width=80)
    

