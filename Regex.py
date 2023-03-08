class Regex:
    def __init__(self, regex):
        self.infix = regex
        self.checkNumParenthesis()
        self.verifyParenthesesSyntax()

        self.postfix = self.infixToPostfix()

    def infixToPostfix(self):
        expression = self.infix

        Operators = set(['+', '-', '*', '/', '(', ')', '^', '$', '?'])

        Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '$': 3, '?': 3}

        stack = []

        output = ''

        for character in expression:

            if character not in Operators:

                output += character

            elif character == '(':

                stack.append('(')

            elif character == ')':

                while stack and stack[-1] != '(':

                    output += stack.pop()

                stack.pop()

            else:

                while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:

                    output += stack.pop()

                stack.append(character)

        while stack:

            output += stack.pop()

        return output

    def checkNumParenthesis(self):

        openParenthesis = 0
        closeParenthesis = 0
        infix = self.infix

        for i in infix:
            if i == '(':
                openParenthesis += 1
            elif i == ')':
                closeParenthesis += 1

        if openParenthesis == closeParenthesis:

            return True
        else:
            raise ValueError("Error: The number of parenthesis is not equal")

    def verifyParenthesesSyntax(self):
        infix = self.infix
        for i in range(len(infix)):
            if infix[i] == '(' and infix[i + 1] == ')':
                raise ValueError("Error: Empty parentheses")
        for i in range(len(infix)):
            try:
                if not infix[i].isalpha() and not infix[i + 1].isalpha():
                    raise ValueError("Error: There are two symbols together")
            except:
                pass
