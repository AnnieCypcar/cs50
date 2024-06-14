from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledgeBase = And(
    Not(And(AKnave, AKnight)),
    Or(AKnight, AKnave),
    Not(And(BKnave, BKnight)),
    Or(BKnight, BKnave),
    Not(And(CKnave, CKnight)),
    Or(CKnight, CKnave),
)
# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledgeBase,
    Implication(And(AKnight, AKnave), AKnight),
    Implication(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeBase,
    Implication(And(AKnave, BKnave), AKnight),
    Implication(Not(And(AKnave, BKnave)), AKnave),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledgeBase,
    # A says "We are the same kind."
    Implication(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),
    Implication(Or(And(AKnave, BKnight), And(AKnight, BKnave)), AKnave),
    # B says "We are of different kinds."
    Implication(Or(And(AKnave, BKnave), And(AKnight, BKnight)), BKnave),
    Implication(Or(And(AKnave, BKnight), And(AKnight, BKnave)), BKnight)
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    knowledgeBase,
    # A says either "I am a knight." or "I am a knave.", but you don't know which.
    Implication(Or(AKnave, AKnight), AKnight),
    Implication(Not(Or(AKnave, AKnight)), AKnave),
    # B says "A said 'I am a knave'.
    Implication(AKnight, BKnave),
    Implication(AKnave, BKnight),
    # B says "C is a knave."
    Implication(CKnave, BKnight),
    Implication(CKnight, BKnave),
    # C says "A is a knight."
    Implication(CKnave, AKnave),
    Implication(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
