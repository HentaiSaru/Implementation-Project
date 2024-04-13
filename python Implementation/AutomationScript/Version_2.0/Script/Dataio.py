import pickle
import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# 使用絕對路徑 , 創建 user-data-dir 時 , 會創建完整的數據
def data_location():
    return "WebsiteData"

def import_json(Json_name):
    with open(Json_name , "r") as file:
        return json.loads(file.read())

def output_json(Json_name, Json_data):
    with open(Json_name , "w") as file:
        file.write(json.dumps(Json_data, indent=4, separators=(",", ":"), ensure_ascii=False))

# 數據輸入
class DataImport:
    def __init__(self):
        self.path = data_location()

    def get_website_data(self, web: str):
        data_path = os.path.join(self.path, f"{web}_default")

        if os.path.exists(data_path):
            return data_path
        else:
            self.create_folder(data_path)
            return data_path

    def get_website_cookie(self, web: str):
        data_path = os.path.join(self.path, f"{web}_default\\{web}_cookies.json")

        if os.path.exists(data_path):
            return import_json(data_path)
        else:
            return None

    def get_acc(self):
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Account.json")

        if os.path.exists(data_path):
            Account = import_json(data_path)
            return Account
        else:
            Format = {
                "Genshin_account": "",
                "Genshin_password": "",
                "StarRail_account": "",
                "StarRail_password": ""
            }
            output_json(data_path, Format)
            return None
        
    def create_folder(self, name):
        os.mkdir(name)

# 數據輸出
class DataOutput:
    def __init__(self):
        self.path = data_location()
        self.cookie_save = []
        
    def json_record(self, path, name, record):
        output_json(f"{path}\\{name}.json", record)

    def json_cookie(self, cookies: dict, web: str):
        self.cookie_save.clear()
        data_path = os.path.join(self.path, f"{web}_default")

        for cookie in cookies:
            cookie_dict = {}
            cookie_dict["name"] = cookie["name"]
            cookie_dict["value"] = cookie["value"]
            self.cookie_save.append(cookie_dict)

        output_json(f"{data_path}\\{web}_cookies.json", self.cookie_save)

    def pkl_cookie(self, cookies: dict, web: str):
        data_path = os.path.join(self.path, f"{web}_default")
        pickle.dump(cookies, open(f"{data_path}\\{web}_cookies.pkl","wb"))

DI = DataImport()
DO = DataOutput()