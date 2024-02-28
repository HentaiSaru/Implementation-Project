import re

# 打印計算結果
def Result(result):
    print(result)

class Binary:

    def Binary_Classifier(self, value):
        if value[1] == "(8)": 
            self.Binary_To_Octal(value[0].split("."))
        elif value[1] == "(10)":
            self.Binary_To_Decimal(value[0].split("."))
        elif value[1] == "(16)":
            self.Binary_To_HexaDecimal(value[0].split("."))
            
    def Binary_Verify(self, value):
        return value > 1 or value < 0

    def Binary_To_Octal(self, value):
        pass

    def Binary_To_Decimal(self, value):
        result = 0
        initial = 0

        try:
            if len(value) > 1:
                initial = f"{value[0]}.{value[1]}"
                for i, v in enumerate(value[1]):
                    number = int(v)
                    
                    if self.Binary_Verify(number):
                        raise Exception("錯誤的二進制值")

                    #? 公式: n * 2^-1 + n * 2^-2 + n * 2^-n
                    result += number * 2 ** (-1 * (i + 1))
            else:
                initial = value[0]

            for i, v in enumerate(value[0][::-1]):
                number = int(v)

                if self.Binary_Verify(number):
                    raise Exception("錯誤的二進制值")

                #? 公式: n * 2^0 + n * 2^1 + n * 2^n
                result += number * 2 ** i

            Result(f"{initial}(2) => {result}(10)")

        except Exception as e:
            print(f"{e}: {initial}")

    def Binary_To_HexaDecimal(self, value):
        pass

class Octal:

    def Octal_Classifier(self, value):
        pass

    def Octal_To_Binary(self):
        pass

    def Octal_To_Decimal(self):
        pass

    def Octal_To_HexaDecimal(self):
        pass

class Decimal:

    def Decimal_Classifier(self, value):
        pass

    def Decimal_To_Binary(self):
        pass

    def Decimal_To_Octal(self):
        pass

    def Decimal_To_HexaDecimal(self):
        pass

class HexaDecimal:

    def HexaDecimal_Classifier(self, value):
        pass

    def HexaDecimal_To_Binary(self):
        pass

    def HexaDecimal_To_Octal(self):
        pass

    def HexaDecimal_To_Decimal(self):
        pass

class CalculationInput(Binary, Octal, Decimal, HexaDecimal):
    def __init__(self) -> None:
        super().__init__()
        self.CalculationFormat_1 = re.compile(r'\d+(\.\d+)?\((2|8|10|16)\)')
        self.CalculationFormat_2 = re.compile(r'\((2|8|10|16)\)')
        self.DataFormat = re.compile(r'(\d+(?:\.\d+)?)(\(2\))?')
        self.ComputeString = None
        self.Separate = None

    def Trigger(self, Data):
        for key, value in Data.items():
            if key == "(2)":
                self.Binary_Classifier(value)
            elif key == "(8)":
                self.Octal_Classifier(value)
            elif key == "(10)":
                self.Decimal_Classifier(value)
            elif key == "(16)":
                self.HexaDecimal_Classifier(value)

    def Input(self):
        """ 
        * 輸入計算值進行進制轉換
        
        >>> 計算值 A(進制) (進制), 請確保使用空格, 將所需的參數隔開
        範例 12(10) (2) = 將數字 12 的十進制 轉換 為 二進制
        """
        try:
            self.ComputeString = "10101101.10110(2) (10)" #input("輸入計算值: ")
            self.Separate = self.ComputeString.split(" ")

            if len(self.Separate) != 2:
                raise Exception("[輸入格式錯誤] 需要使用空格, 分別輸入兩個值")

            ArithmeticBox = {}
            if self.CalculationFormat_1.match(self.Separate[0]) and self.CalculationFormat_2.match(self.Separate[1]):
                for Data in self.DataFormat.findall(self.Separate[0]):
                    ArithmeticBox[Data[1]] = [Data[0], self.Separate[1]]
            else:
                raise Exception("[計算值格式錯誤] 第一個值為: 數字(進制), 第二個值為: (進制), 進制只有 2|8|10|16")

            self.Trigger(ArithmeticBox)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    Calculation = CalculationInput()
    Calculation.Input()