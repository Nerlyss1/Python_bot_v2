class TreeNode:
    def __init__(self, question, yes_node=None, no_node=None, other_node=None, answer=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.other_node = other_node
        self.answer = answer


class DiscussionSystem:
    def __init__(self):
        # Création de l'arbre de discussion
        self.root = TreeNode("Aimez-vous les jeux vidéo ? (répondez à l'aide de !answer et oui ou non)",
                             yes_node=TreeNode("Quel est votre jeu préféré (répondez à l'aide de !answer et oui ou non)",
                                               other_node=TreeNode("C'est un excellent choix de jeu ! (répondez à l'aide de !answer et par grave ou bof)",
                                                                 other_node=TreeNode("Cool, à plus tard."))),
                             no_node=TreeNode("Quel est votre activité préféré ? (répondez à l'aide de !answer)",
                                                                                  other_node=TreeNode("Cool, à plus tard.")))

        self.current_node = self.root
        self.topics = set(["jeux", "activité"])


    def reset_discussion(self):
        self.current_node = self.root
        self.topics = set()

    def process_answer(self, answer):
        if self.current_node.yes_node and answer.lower() in ["yes", "oui"]:
            self.current_node = self.current_node.yes_node
        elif self.current_node.no_node and answer.lower() in ["no", "non"]:
            self.current_node = self.current_node.no_node
        else:
            if self.current_node.other_node:
                self.current_node = self.current_node.other_node
        return self.current_node.question

    def get_response(self):
        if self.current_node.answer:
            return self.current_node.answer
        elif self.current_node.question:
            return self.current_node.question
        else:
            return "Cool, à plus tard."

    def speak_about(self, topic):
        if topic.lower() in self.topics:
            return f"Oui, je parle de {topic}."
        else:
            return f"Non, je ne parle pas de {topic}."
