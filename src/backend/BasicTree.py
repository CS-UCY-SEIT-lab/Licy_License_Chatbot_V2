class BasicTree:
    def __init__(self, nodes, parent, initial_subset):
        self.nodes = nodes
        self.parent = parent
        self.initial_subset = [license for license in list(initial_subset)]
        self.current_node = parent
        self.current_subset = [license for license in list(initial_subset)]

    def empty_subset(self):
        list_positive = list(
            set(self.current_subset).intersection(
                set(self.current_node.positive_subset)
            )
        )
        list_negative = list(
            set(self.current_subset).intersection(
                set(self.current_node.negative_subset)
            )
        )

        if not list_positive or not list_negative:
            return 1

        return 0

    def positive_answer(self):
        self.current_subset = list(
            set(self.current_subset).intersection(
                set(self.current_node.positive_subset)
            )
        )
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.left_child is None:
            return 1

        # TODO: when i move back there is an issue
        elif self.current_node.left_child.id < self.current_node.id:
            self.current_subset = [
                license for license in self.current_node.left_child.current_subset
            ]
            return 1

        self.current_node = self.current_node.left_child

        if self.empty_subset():
            return 1

        return 0

    def negative_answer(self):
        self.current_subset = list(
            set(self.current_subset).intersection(
                set(self.current_node.negative_subset)
            )
        )
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.right_child is None:
            return 1

        elif self.current_node.right_child.id < self.current_node.id:
            self.current_subset = [
                license for license in self.current_node.right_child.current_subset
            ]
            return 1

        self.current_node = self.current_node.right_child

        if self.empty_subset():
            return 1

        return 0

    def neutral_answer(self):
        self.current_node.set_current_subset(self.current_subset)

        if self.current_node.middle_child is None:
            return 1

        self.current_node = self.current_node.middle_child

        if self.empty_subset():
            return 1
        return 0

    # def start_questionnaire(self):
    #     self.current_node = self.parent
    #     questions = 1
    #     answer = None
    #     while questions:
    #         print(
    #             "\n ------------------------------------------------------------------------------------------ \n"
    #         )
    #         print("     " + self.current_node.questions[0])
    #         print(
    #             "\n ------------------------------------------------------------------------------------------ \n"
    #         )
    #         answer = input("Answer: ")

    #         if answer == "yes" or answer == "Yes" or answer == "y":
    #             questions = self.positive_answer()
    #         elif answer == "no" or answer == "No" or answer == "n":
    #             questions = self.negative_answer()
    #         else:
    #             questions = self.neutral_answer()

    #         self.current_node.print_info()
    #         print("Current Subset: ", self.current_subset)

    async def start_questionnaire2(self, request):
        finished = 0
        if request == "yes" or request == "Yes" or request == "y":
            finished = self.positive_answer()
        elif request == "no" or request == "No" or request == "n":
            finished = self.negative_answer()
        elif request == "Don't Care" or request == "dm":
            finished = self.neutral_answer()

        question = self.current_node.questions[0]
        current_subset = self.current_subset
        return {
            "question": question,
            "current_subset": current_subset,
            "options": self.current_node.options,
            "finished": finished,
            "question_explanation": self.current_node.question_explanation,
        }

    def refresh(self):
        self.current_node = self.parent
        self.current_subset = self.initial_subset
