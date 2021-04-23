class InvalidSelection(BaseException):
    def __init__(self, selection_value=None):
        super().__init__()
        self.__selection_value = selection_value

    def __str__(self):
        if self.__selection_value is not None:
            return 'The selection {} is not valid'.format(self.__selection_value)
        return 'The selection you made is not valid.'