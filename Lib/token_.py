"""
@package token_
This is the Token class its self explanitory
"""
class Token:
    """
    @brief This represents a token.  It has a type, lexeme, and line number
    """
    def __init__(self, token_type, lexeme):
        """
        @brief The Constructor
        
        @param[in] token_type A string representing the token's type
        @param[in] lexeme The lexeme for the token
        """
        self.token_type = token_type
        self.lexeme = lexeme
        self.line_number = None

    def __eq__(self, y):
        """
        @brief Overloading == operator because I'm lazy
        
        Overloaded == operator so I didn't have to keep typing "var_name.lexeme" everywhere
        @param[in] y A string to compare against the lexeme
        @retval True self.lexeme is the same as the incoming string
        @retval False self.lexeme is different than the incoming string
        """
        return self.lexeme == y

    def __ne__(self, y):
        """
        @brief Overloading != operator because I'm lazy
        
        Overloaded == operator so I didn't have to keep typing "var_name.lexeme" everywhere
        @param[in] y A string to compare against the lexeme
        @retval True self.lexeme is the same as the incoming string
        @retval False self.lexeme is the same as the incoming string
        """
        return self.lexeme != y
