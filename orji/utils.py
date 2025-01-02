import orgmunge
from enum import Enum


class Insertion(Enum):
    ABOVE = 0
    BELOW = 1
    UNDER = 2
    REPLACE = 3


def _insert(
    document: str, to_insert: str, indexes: list[int], insertion_type: Insertion
):
    parsed_document = orgmunge.Org(document, from_file=False)

    parent_to_attach_to = parsed_document.root

    for previous_index in indexes[:-1]:
        parent_to_attach_to = parent_to_attach_to.children[previous_index]

    second = orgmunge.Org(to_insert, from_file=False)

    last_index = (
        indexes[-1] + 1
        if insertion_type in (Insertion.BELOW, Insertion.UNDER, Insertion.REPLACE)
        else indexes[-1]
    )

    before = parent_to_attach_to.children[:last_index]
    after = parent_to_attach_to.children[last_index:]
    parent_to_attach_to.children = before + second.root.children + after

    how_many_elements_to_insert = len(second.root.children)

    reread = orgmunge.Org(str(parsed_document), from_file=False)

    if insertion_type == Insertion.UNDER:
        for element in reread.root.children[
            last_index : last_index + how_many_elements_to_insert
        ]:
            for _ in range(len(indexes)):
                element.demote()

    if insertion_type == Insertion.REPLACE:
        del reread.root.children[last_index - 1]
    return reread


def below(document: str, to_insert: str, indexes: list[int]):
    """
    >>> str(below("* O1\\n* O2\\n", "* IN1\\n", [0]))
    \'* O1\\n* IN1\\n* O2\\n\'

    >>> str(below("* O1\\n* O2\\n", "* IN1\\n", [1]))
    \'* O1\\n* O2\\n* IN1\\n\'
    """
    return _insert(document, to_insert, indexes, Insertion.BELOW)


def under(document: str, to_insert: str, indexes: list[int]):
    """
    >>> str(under("* O1\\n* O2\\n", "* IN1\\n* IN2\\n", [0]))
    \'* O1\\n** IN1\\n** IN2\\n* O2\\n\'

    >>> str(under("* O1\\n** O1.1\\n* O2\\n", "* IN1\\n* IN2\\n", [0, 0]))
    \'* O1\\n** O1.1\\n*** IN1\\n*** IN2\\n* O2\\n\'
    """
    return _insert(document, to_insert, indexes, Insertion.UNDER)


def above(document: str, to_insert: str, indexes: list[int]):
    """
    >>> str(above("* O1\\n* O2\\n", "* IN1\\n", [0]))
    \'* IN1\\n* O1\\n* O2\\n\'
    """
    return _insert(document, to_insert, indexes, Insertion.ABOVE)


def replace(document: str, to_insert: str, indexes: list[int]):
    """
    >>> str(replace("* O1\\n* O2\\n", "* IN1\\n", [0]))
    \'* IN1\\n* O2\\n\'
    """
    return _insert(document, to_insert, indexes, Insertion.REPLACE)
