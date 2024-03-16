from itertools import chain


class Node:
    def __init__(self, id):
        self.questions = None
        self.children = None
        self.id = id
        self.parent = None
        self.children_subset = None
        self.options = None
        self.question_explanation = None
        self.option_explanations = None

    def build_node(
        self,
        questions,
        children,
        children_subset,
        options,
        option_explanations,
        question_explanations,
    ):
        self.set_questions(questions)
        self.set_children(children)
        self.current_subset = list(chain(*children_subset))
        self.options = options
        self.option_explanation = option_explanations
        self.question_explanation = question_explanations

    def set_current_subset(self, subset):
        self.current_subset = [license for license in subset]

    def set_left_child(self, left_node):
        self.left_child = left_node

    def set_middle_child(self, middle_node):
        self.middle_child = middle_node

    def set_right_child(self, right_node):
        self.right_child = right_node

    def set_children(self, children):
        self.children = [child for child in children]

    def set_parent(self, parent):
        self.parent = parent

    def set_questions(self, questions):
        self.questions = [question for question in questions]

    def print_info(self):
        print("-----------------------------------------------------------------")
        print("Current Node info: \n")
        if self.parent is not None:
            print("Parent:", self.parent.id)
        # print("Questions:", self.questions)
        if self.left_child is not None:
            print("Left child:", self.left_child.id)
        if self.middle_child is not None:
            print("Middle child:", self.middle_child.id)
        if self.right_child is not None:
            print("Right child:", self.right_child.id)

        print("Positive Subset:", self.positive_subset)
        print("Negative Subset:", self.negative_subset)
        print("----------------------------------------------------------------\n")
