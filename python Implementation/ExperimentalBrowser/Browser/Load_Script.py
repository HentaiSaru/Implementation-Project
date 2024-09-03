import time
import threading

class LoadScript:
    def __init__(self, driver):
        self.driver = driver
        self.current_url = driver.current_url

        self.DarkModeState = False
        
        threading.Thread(target=self.__ListenChange).start()

    def __ListenChange(self):
        while True:
            try:
                current_url = self.driver.current_url
                if current_url != self.current_url:
                    if self.DarkModeState: self.DarkMode()
                time.sleep(1)
            except:
                break

    def DarkMode(self, simple=True):
        SimpleScript = r"""
            function Debounce(func, delay=500) {
                let timer = null;
                return (...args) => {
                    clearTimeout(timer);
                    timer = setTimeout(function() {
                        func(...args);
                    }, delay);
                }
            };

            function filter() {
                if (!document.body.getAttribute("DarkMode")) {
                    const Dark = document.createElement("DarkMode");
                    Dark.style.cssText = `
                        background: rgba(0,0,0,0.3);
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        display: flex;
                        z-index: 9999;
                        overflow: auto;
                        position: fixed;
                        pointer-events: none;
                    `;

                    document.body.appendChild(Dark);
                    document.body.setAttribute("DarkMode", "true");
                };
            };
            filter();

            const Option = {
                subtree: true,
                childList: true
            }, Observer = new MutationObserver(Debounce(() => filter()));
            Observer.observe(document, Option);
        """

        #! 進階板目前沒有很好的展示效果
        AdvancedScript = r"""
            function Debounce(func, delay=100) {
                let timer = null;
                return (...args) => {
                    clearTimeout(timer);
                    timer = setTimeout(function() {
                        func(...args);
                    }, delay);
                }
            };

            function rgbToGrayValue(rgb) {
                const [r, g, b] = rgb.match(/\d+/g).map(Number);
                return (r + g + b) / 3;
            };

            function conversion() {
                for (const element of document.querySelectorAll("body *:not(script):not(style):not(svg):not(img):not(br):not(hr)")) {

                    if (element.getAttribute("DarkMode")) continue;

                    const elementColor = window.getComputedStyle(element);
 
                    const colorRGB = rgbToGrayValue(elementColor.color);
                    const backgroundRGB = rgbToGrayValue(elementColor.background);

                    if (backgroundRGB > 150) {
                        element.style.background = "#272727";
                    }

                    if (colorRGB < 150) {
                        element.style.color = "#FFFFFF";
                    }

                    element.setAttribute("DarkMode", true);
                }
            };
            conversion();

            const Option = {
                subtree: true,
                childList: true,
                attributes: true,
                characterData: true
            }, Observer = new MutationObserver(Debounce(() => conversion()));
            Observer.observe(document.head, Option);
        """
        self.DarkModeState = True
        Script = SimpleScript if simple else AdvancedScript
        self.driver.execute_script(Script)