class BeginnerTree:
    def __init__(
        self,
        questions,
        question_explanations,
        options,
        option_explanations,
        option_license_subsets,
        option_paths,
    ):
        self.questions = questions
        self.question_explanations = question_explanations
        self.options = options
        self.option_explanations = option_explanations
        self.option_license_subsets = option_license_subsets
        self.option_paths = option_paths
        self.current_question_id = 0

    async def start_questionnaire(self, request):
        finished = 0

        if request is not None:
            option_license_subsets = self.option_license_subsets[request]

            if self.options_paths[request] == "end":
                finished = 1
            else:
                self.current_question_id = int(self.options_paths[request])

        question = self.questions[self.current_question_id]
        question_explanation = self.question_explanations[self.current_question_id]
        options = self.options[self.current_question_id]
        option_explanations = self.option_explanations[self.current_question_id]

        return {
            "question": question,
            "question_explanation": question_explanation,
            "options": options,
            "option_explanations": option_explanations,
            "option_license_subsets": option_license_subsets,
            "finished": finished,
        }

    # def refresh(self):
    #     self.current_node = self.parent
    #     self.current_subset = self.initial_subset
