class Regex:
    def __init__(self, regex):
        self.infix = regex
        self.checkNumParenthesis()
        self.check_parenthesesOrder()
        self.verifyParenthesesSyntax()
        # self.operatorsExist()
        self.postfix = self.to_postfix()

    def to_postfix(self):
        regex = self.infix
        # precedence dictionary for each operator
        precedence = {"+": 2, "*": 3, "$": 1}
        postfix = []
        operator_stack = []
        # iterate through the characters of the regex
        for char in regex:
            if char.isalpha():
                # if character is a letter, add it to the postfix expression
                postfix.append(char)
            elif char == '(':
                # if character is an opening parenthesis, push onto operator stack
                operator_stack.append(char)
            elif char == ')':
                # if character is a closing parenthesis, pop operators from stack and add them to postfix until
                # opening parenthesis is reached
                while operator_stack and operator_stack[-1] != '(':
                    postfix.append(operator_stack.pop())
                operator_stack.pop() # remove the opening parenthesis
            else:
                # if character is an operator, pop operators from stack and add them to postfix in order of
                # greatest to least precedence
                while operator_stack and operator_stack[-1] != '(' and precedence.get(char, 0) <= precedence.get(operator_stack[-1], 0):
                    postfix.append(operator_stack.pop())
                operator_stack.append(char) # push the operator onto the stack
        # once all characters have been iterated through, add any remaining operators to postfix
        while operator_stack:
            postfix.append(operator_stack.pop())

        # combine postfix expression into a string and return it
        return ''.join(postfix)


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


    def check_parenthesesOrder(self):
        must_be_closed = 0
        for i in range(len(self.infix)):
            if self.infix[i] == '(':
                must_be_closed += 1
            elif self.infix[i] == ')':
                must_be_closed -= 1
        
        if must_be_closed == 0:
            pass
        else:
            raise ValueError("Error: The parentheses are not in order")
            
            
            

    # def operatorsExist(self):
    #     operators = ['+', '*', '|', '$', '?']
    #     for i in self.infix:
    #         if i in operators:
    #             return True
    #         else:
    #             raise ValueError("Error: There are no operators in the expression or the operators are not in syntax.")