from math_construct.problems.templates import TEMPLATES
PROBLEM_TEMPLATE = TEMPLATES["bmo_shortlist/problem_2018_c1.py"]

from math_construct.problems.problem import Problem, ProblemConfig, Tag, CheckerTag
from math_construct.utils import get_latex_array
import random


FORMATTING_INSTRUCTIONS = r"""Output the match results as a matrix where the entry at indices $i,j$ is 1 if player $i$ won against player $j$. Output the answer between \verb|\begin{array}{...}| and \verb|\end{array}| inside of $\boxed{...}$. For example, $\boxed{\begin{array}{ccc}0 & 1 & 1 \\ 0 & 0 & 0 \\ 0 & 1 & 0\end{array}}$."""

def get_solution(k: int) -> list[list[int]]:
    assert (k%2 == 1)
    res = []
    for i in range(k):
        row = []
        for j in range(k):
            row.append(0 if (j - i + k) % k > (k-1)//2 or i==j else 1)
        res.append(row)
    return res


class ProblemBMO2018C1(Problem):
    config = ProblemConfig(
        name=Problem.get_name(__file__),
        statement=PROBLEM_TEMPLATE,
        formatting_instructions=FORMATTING_INSTRUCTIONS,
        parameters=["N"],
        source="BMO 2018 Shortlist C1",
        original_parameters={"N": 11},
        original_solution=get_solution(11),
        problem_url="https://artofproblemsolving.com/community/c6h1840358p12360253",
        solution_url="https://artofproblemsolving.com/community/c6h1840358p12360253",
        tags=[Tag.COMBINATORICS, Tag.FIND_ANY, Tag.IS_ORIGINAL]
    )
    N: int

    def __init__(self, N: int):
        self.N = N

    def get_problem(self):
        return PROBLEM_TEMPLATE.format(N=self.N, m=(self.N-1)*(3*self.N-1)//8)

    def check(self, x: list[list[int]]) -> bool:
        if len(x) != self.N:
            return False, f"{self.N} examples expected, received {len(x)}", CheckerTag.INCORRECT_LENGTH

        n_upsets = 0
        for i in range(self.N):
            for j in range(self.N):
                if x[i][j] not in [0, 1]:
                    return False, f"All entries should be either 0 or 1, entry ({i}, {j}) is {x[i][j]}", CheckerTag.INCORRECT_FORMAT
                if i == j and x[i][j] != 0:
                    return False, f"Players receive no points against themselves", CheckerTag.INCORRECT_FORMAT
                if i!=j and x[i][j] == 1 and x[j][i] != 0:
                    return False, f"Any loss should correspond to a win for the other (see ({i}, {j}))", CheckerTag.INCORRECT_FORMAT
                if i!=j and x[i][j] == 0 and x[j][i] != 1:
                    return False, f"Any loss should correspond to a win for the other (see ({i}, {j}))", CheckerTag.INCORRECT_FORMAT
                if i < j and x[i][j] == 1:
                    n_upsets += 1

        if n_upsets != (self.N-1)*(3*self.N-1)//8:
            return False, f"The correct number of upsets should be {(self.N-1)*(3*self.N-1)//8}", CheckerTag.INCORRECT_SOLUTION
        return True, "OK", CheckerTag.CORRECT

    @staticmethod
    def generate() -> "ProblemBMO2018C1":
        k = random.randint(4, 9)
        k = 2*k + 1
        return ProblemBMO2018C1(k)

    def get_solution(self):
        return get_solution(self.N)
