from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bmo_shortlist/problem_2019_c2.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.templates import MATRIX_FORMATTING_TEMPLATE
import random
import numpy as np


def get_solution(k: int) -> list[list[int]]:
    res = [[23, 13, 19, 12, 24],
           [7,2,9,4,5],
           [18, 16, 17, 15, 21],
           [8, 1, 10, 3, 6],
           [22, 14, 20, 11, 25]]
    
    return res

class ProblemBMO2019C2(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=MATRIX_FORMATTING_TEMPLATE,
        parameters=["N"],
        source="BMO 2019 Shortlist C2",
        original_parameters={"N": 45},
        original_solution=get_solution(45),
        problem_url="https://artofproblemsolving.com/community/c6h1924920p13206326",
        solution_url="https://artofproblemsolving.com/community/c6h1924920p13206326",
        tags=[Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_ORIGINAL]
    )
    k: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N)

    def check(self, x: list[list[int]]) -> bool:
        # Check dimensions
        if len(x) != 5:
            return False, f"Example should be have 5 rows.", CheckerTag.INCORRECT_LENGTH
        
        for row in x:
            if len(row) != 5:
               return False, f"Each table row should have 5 entries.", CheckerTag.INCORRECT_FORMAT 
        
        all_nums = np.arange(1, 26)
        x = np.array(x)
        entries = np.sort(x.flatten())
        # Check all numbers are used
        if not (all_nums == entries).all():
            return False, "Every number from 1 to 25 should be used", CheckerTag.INCORRECT_FORMAT
        
        # Check sums
        for i in range(4):
            for j in range(4):
                if np.sum(x[i:i+2, j:j+2]) > self.N:
                    return False, f"Group {x[i:i+2, j:j+2]} should have a sum of no more than {self.N}, got {np.sum(x[i:i+2, j:j+2])}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBMO2019C2":
        k = random.randint(45, 55)
        return ProblemBMO2019C2(k)

    def get_solution(self):
        return get_solution(self.N)
