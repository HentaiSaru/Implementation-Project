class calculate:
    def __init__(self):
        self.result = None

    def count(self,a,b,c):
        self.result = eval((a+b+c))

    def get_result(self):
        return self.result