from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["jbmo_shortlist/problem_2023_c2.py"]

import random
from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
import numpy as np


EXTRA_FORMATTING_INSTRUCTIONS = r"""Output the answer as two comma-separated sequences of the same length inside $\boxed{...}$, i.e. $\boxed{((1, 2, 3, 4), (5, 6, 7, 8))}$"""

def get_solution(N:int) -> list[list[int]]:
    seq1 = []
    seq2 = []
    for i in range(1, N+1):
        if i != N:
            seq1.append(2**i)
        else:
            seq1.append(2**(i-1) + 1)
        if i == 1:
            seq2.append(-2**(N-1) - 1)
        else:
            seq2.append(-2**(N+1-i))
    return seq1, seq2

class ProblemJBMO2023C5(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=EXTRA_FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="2023 JBMO Shortlist C5",
        original_parameters={"N": 25},
        original_solution=get_solution(25),
        problem_url="https://artofproblemsolving.com/community/c6h3347819p31039710",
        solution_url="https://artofproblemsolving.com/community/c6h3347819p31039710",
        tags=[Tag.ALGEBRA, Tag.FIND_MAX_MIN, Tag.IS_SIMPLIFIED]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(
            N=self.N,
            Mmax=self.N*(self.N-1)//2-2*(self.N-3)-1, 
            Mmin=2*(self.N-3), 
            Nminusone=self.N-1
        )

    def check(self, x: list[list[int]]) -> bool:
        if len(x) != 2:
            return False, "2 sequences should be presented", CheckerTag.INCORRECT_FORMAT

        for seq in x:
            if len(seq) != self.N:
                return False, f"Each sequence should be of length {self.N}", CheckerTag.INCORRECT_LENGTH
            for i in range(len(seq) - 1):
                if seq[i] >= seq[i+1]:
                    return False, f"Sequences are not sorted", CheckerTag.INCORRECT_SOLUTION
        
        seq1 = x[0]
        seq2 = x[1]

        sum_1 = seq1[1] + seq1[-2]
        sum_2 = seq2[1] + seq2[-2]
        count_1 = 0
        count_2 = 0

        pairwise_sums_1 = np.add.outer(seq1, seq1)
        pairwise_sums_1 = pairwise_sums_1[np.tril_indices(len(pairwise_sums_1), k=-1)]
        pairwise_sums_2 = np.add.outer(seq2, seq2)
        pairwise_sums_2 = pairwise_sums_2[np.tril_indices(len(pairwise_sums_2), k=-1)]

        count_1 = np.sum(pairwise_sums_1 < sum_1)
        count_2 = np.sum(pairwise_sums_2 < sum_2)

        if len(pairwise_sums_2) != len(set(list(pairwise_sums_2))) or len(pairwise_sums_1) != len(set(list(pairwise_sums_1))):
            return False, "Pairwise sums should be distinct", CheckerTag.INCORRECT_SOLUTION
        
        true_count_1 = self.N*(self.N-1)//2-2*(self.N-3)-1
        true_count_2 = 2*(self.N-3)

        if count_1 != true_count_1 or count_2 != true_count_2:
            return False, "Optimal number was not reach for one of the sequences.", CheckerTag.INCORRECT_SOLUTION

        return True

    @staticmethod
    def generate() -> "ProblemJBMO2023C5":
        N = random.randint(20, 60)
        return ProblemJBMO2023C5(N)

    def get_solution(self):
        return get_solution(self.N)
