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

class TemplateGeneration(ImageDataImport):
    def __init__(self):
        super().__init__()
        self.create_path = None
        self.create_name = None
        self.data_box = None
        self.template = None

    def Get_data(self):
        try:self.create_path, self.create_name, self.data_box = self.Read_folder()
        except:pass

    def Create_Template(self):
        template = """
        <!DOCTYPE html>
        <html>
            <head>
                <title>{{ title }}</title>
                <style>
                    body {
                        margin: 0;
                        padding: 0;
                        background: {{ bg }};
                    }
                    img {
                        width: 100%;
                        height: 100%;
                        max-width: 50%;
                        display: block;
                        margin: 0 auto;
                    }
                </style>
                <script>
                    async function ErrorRemove(Img) {
                        Img.remove();
                    }
                    async function WidthModify() {
                        const Rules = document.querySelector("style").sheet.cssRules[1];
                        document.addEventListener("keydown", event=> {
                            const key = event.key;
                            if (key == "+" || key == "-") {
                                const current = parseInt(Rules.style.maxWidth);
                                requestAnimationFrame(()=> {
                                    Rules.style.maxWidth =
                                    key == "+"
                                    ? `${Math.min(current + 1, 100)}%`
                                    : `${Math.max(current - 1, 1)}%`;
                                })
                            }
                        })
                    }
                    WidthModify();
                </script>
            </head>
            <body>
                <div id = "picture_box">
                    {% for src in data %}
                    <img src="{{ src|safe }}" onerror="ErrorRemove(this)">
                    {% endfor %}
                </div>
            </body>
        </html>
        """
        self.template = Template(template)

    def Generate_Save_HTML(self):
        self.Get_data()

        if self.create_path != None:
            # 創建模板
            self.Create_Template()

            # 傳遞創建模板參數
            html = self.template.render({
                "title": self.create_name,
                "bg": "rgb(110, 110, 110)",
                "data": self.data_box,
            })

            # 文件名稱
            name = os.path.join(self.create_path, f"{self.create_name}.html")
            # 輸出文件
            with open(name, "w", encoding="utf-8") as f:
                f.write(html)

            print("輸出完成")
            os.startfile(name)

if __name__ == "__main__":
    TG = TemplateGeneration()
    TG.Generate_Save_HTML()