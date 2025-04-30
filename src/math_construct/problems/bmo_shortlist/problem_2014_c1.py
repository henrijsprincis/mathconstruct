from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bmo_shortlist/problem_2014_c1.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np
import random


FORMATTING_INSTRUCTIONS = r"""Output the sequence of the state of the seats as a comma-separated list in $\boxed{...}$, where a '1' signifies an occupied seat, and '0' signifies an empty one. Ex: $\boxed{[1,1,0,0,1,0,1]}$"""
FORMATTING_INSTRUCTIONS = "Output the sequence of the state of the seats as a python list, where a 1 signifies an occupied seat, and 0 signifies an empty one. Ex: [0,0]"

def get_solution(k: int) -> list[list[int]]:
    res = []
    for _ in range(k//10+1):
        res += [1,1,1,1,1,0,0,0,0,0] 
    return res[:k]

class ProblemBMO2014C1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="BMO 2014 Shortlist C1",
        original_parameters={"N": 56},
        original_solution=get_solution(56),
        problem_url="https://artofproblemsolving.com/community/c6h1889716p12889374",
        solution_url="https://artofproblemsolving.com/community/c6h1889716p12889374",
        tags=[Tag.COMBINATORICS, Tag.IS_SIMPLIFIED, Tag.FIND_ANY, Tag.IS_ORIGINAL]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N, m = (self.N//10)*5 + min(self.N%10, 5))

    def check(self, x: list[tuple[int]]) -> bool:
        if len(set(np.unique(x)) - set([0,1])) != 0:
            return False, "Seats should be labeled as either 0 or 1", CheckerTag.INCORRECT_FORMAT
        if len(x) != self.N:
            return False, f"There should be a total of {self.N} seats", CheckerTag.INCORRECT_LENGTH
        if sum(x) != (self.N//10)*5 + min(self.N%10, 5):
            return False, f"There should be exactly ${(self.N//10)*5 + min(self.N%10, 5)}$ occupied seats", CheckerTag.INCORRECT_FORMAT
        for i in range(5, self.N-6):
            if x[i] == 1 and (x[i-5] == 1 or x[i+5] == 1):
                return False, f"There are seats that are 4 away from each other", CheckerTag.INCORRECT_SOLUTION

        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBMO2014C1":
        k = random.randint(30, 200)
        return ProblemBMO2014C1(k)

    def get_solution(self):
        return get_solution(self.N)
