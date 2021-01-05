import numpy as np
from template import Template

test_vector = np.random.randint(1, 100, size=10)

print(sorted(test_vector))

with Template("test.cc") as template:
    template.autogen("test_vector", ", ".join(sorted(test_vector)))
    

