from tkinter import filedialog
from jinja2 import Template
import tkinter as tk
import os

class ImageDataImport:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.root = tk.Tk()
        
    def Read_folder(self):
        self.root.withdraw()
        folder_path = filedialog.askdirectory(title="選取文件夾")
        self.root.destroy()
        
        if folder_path:
            data_box = []
            create_path = os.path.dirname(folder_path)
            create_name = os.path.basename(folder_path)
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                data_box.append(os.path.relpath(file_path, create_path).replace("\\","/"))
            return create_path, create_name, data_box
                
class TemplateGeneration:
    def __init__(self):
        self.InData = ImageDataImport()
        self.create_path = None
        self.create_name = None
        self.data_box = None
        self.template = None
        
    def Get_data(self):
        try:self.create_path, self.create_name, self.data_box = self.InData.Read_folder()
        except:pass
        
    def Create_Template(self):
        template = """
            <!DOCTYPE html>
            <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title></title>
                    <style>
                        body {
                            background: rgb(110, 110, 110);
                            margin: 0;
                            padding: 0;
                        }
                        .image-style {
                            width: 100%;
                            height: 100%;
                            display: block;
                            margin: 0 auto;
                            max-width: 50%;
                        }
                    </style>
                </head>
                <body>
                    <div id = "picture_box">
                        {% for src in data %}
                        <div>
                            <img src="{{ src|safe }}" class="image-style">
                        </div>
                        {% endfor %}
                    </div>
                </body>
            </html>
        """
        self.template = Template(template)
        
    def Generate_Save_HTML(self):
        self.Get_data()
        
        if self.create_path != None:
            self.Create_Template()
            html = self.template.render(data = self.data_box)
            name = os.path.join(self.create_path, f"{self.create_name}.html")
            with open(name, "w", encoding="utf-8") as f:
                f.write(html)
                
            print("創建完成")
            os.startfile(name)

if __name__ == "__main__":
    TG = TemplateGeneration()
    TG.Generate_Save_HTML()