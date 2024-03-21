class Node:
    def __init__(self, id):
        self.questions = None
        self.left_child = None
        self.middle_child = None
        self.right_child = None
        self.id = id
        self.parent = None
        self.positive_subset = None
        self.negative_subset = None
        self.current_subset = None
        self.options = None
        self.question_explanation = None

    def build_node(
        self,
        left_child,
        middle_child,
        right_child,
        questions,
        positive_subset,
        negative_subset,
        options,
        question_explanation,
    ):
        self.set_questions(questions)
        self.set_left_child(left_child)
        self.set_middle_child(middle_child)
        self.set_right_child(right_child)
        self.positive_subset = [license for license in positive_subset]
        self.negative_subset = [license for license in negative_subset]
        self.current_subset = list(set(positive_subset).union(set(negative_subset)))
        self.neutral_subset = self.current_subset
        self.options = options
        self.question_explanation = question_explanation

    def set_current_subset(self, subset):
        self.current_subset = [license for license in subset]

    def set_left_child(self, left_node):
        self.left_child = left_node

    def set_middle_child(self, middle_node):
        self.middle_child = middle_node

    def set_right_child(self, right_node):
        self.right_child = right_node

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
