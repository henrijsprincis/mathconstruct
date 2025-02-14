from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["jbmo_shortlist/problem_2018_a7.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
from math_construct.templates import get_list_template
from itertools import combinations


def get_solution(n: int) -> list[int]:
    seq = []
    largest_full = int(n**0.5+1e-8)
    for i in range(largest_full-1):
        seq.append((i+1)**2)
        seq.append((i+1)**2 + i + 1)
    seq.append(largest_full**2)
    if largest_full**2 + largest_full <= n:
        seq.append(largest_full**2 + largest_full)
    return seq

class ProblemJBMO2018A7(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=get_list_template(),
        parameters=['N'],
        source="2018 JBMO Shortlist A7",
        original_parameters={'N':2018},
        original_solution=get_solution(2018),
        problem_url="https://artofproblemsolving.com/community/c6h1873162p12715048",
        solution_url="https://artofproblemsolving.com/community/c6h1873162p12715048",
        tags=[Tag.ALGEBRA, Tag.FIND_ANY, Tag.IS_ORIGINAL]
    )
    N: int

    def __init__(self, N:int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N, n=int(self.N**0.5+1e-8))

    def check(self, x: list[int]) -> bool:

        largest_full = int(self.N**0.5+1e-8)
        if len(x) != 2*(largest_full):
            return False, f"Set is not of maximum cardinality", CheckerTag.INCORRECT_LENGTH

        if len(x) != len(set(x)):
            return False, f"Elements of set are non-distinct", CheckerTag.INCORRECT_FORMAT
        
        if max(x) > self.N or min(x) < 0:
            return False, f"Members should be positive integers no larger than {self.N}", CheckerTag.INCORRECT_FORMAT
        
        for comb in combinations(x, 3):
            if abs(comb[0] - comb[1]) < comb[0]**0.5 + comb[1]**0.5 and \
               abs(comb[1] - comb[2]) < comb[1]**0.5 + comb[2]**0.5 and \
               abs(comb[0] - comb[2]) < comb[0]**0.5 + comb[2]**0.5:
                return False, f"Subset {comb} does not satisfy b)", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemJBMO2018A7":
        n = random.randint(6, 15)
        return ProblemJBMO2018A7(n**2 + 2*n)

    def get_solution(self):
        return get_solution(self.N)
