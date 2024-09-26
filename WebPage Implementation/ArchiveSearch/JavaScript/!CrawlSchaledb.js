// ==UserScript==
// @name         __Crawl Schaledb__
// @version      0.0.1
// @author       Canaan HS
// @description  手動爬取數據

// @match        *://schaledb.com/*

// @license      MIT
// @namespace    https://greasyfork.org/users/989635
// @icon         https://schaledb.com/favicon.svg?v=1

// @noframes
// @run-at       document-start
// @grant        GM_setClipboard
// @grant        GM_getResourceText
// @grant        GM_registerMenuCommand
// @require      https://update.greasyfork.org/scripts/495339/1413531/ObjectSyntax_min.js
// @resource     Reference https://raw.githubusercontent.com/Canaan-HS/Implementation-Project/refs/heads/Main/WebPage%20Implementation/ArchiveSearch/DataBase/DB.json
// ==/UserScript==

// https://schaledb.com/student

(async () => {

    /* 將參考數據添加 */
    const Reference = JSON.parse(GM_getResourceText("Reference"));

    /* 對應列表 */
    const Correspond = {
        0: ['戰略定位', 'STRIKER'],
        1: ['戰略定位', 'SPECIAL'],
        2: ['戰術類別', '坦克'],
        3: ['戰術類別', '輸出'],
        4: ['戰術類別', '補師'],
        5: ['戰術類別', '輔助'],
        6: ['戰術類別', '支援'],
        7: ['角色稀有', '1星'],
        8: ['角色稀有', '2星'],
        9: ['角色稀有', '3星'],
        10: ['獲取管道', '常駐'],
        11: ['獲取管道', '限定'],
        12: ['獲取管道', '活動'],
        13: ['獲取管道', '慶典'],
        14: ['攻擊屬性', '爆炸'],
        15: ['攻擊屬性', '貫通'],
        16: ['攻擊屬性', '神秘'],
        17: ['攻擊屬性', '振動'],
        18: ['防禦裝甲', '輕裝'],
        19: ['防禦裝甲', '重裝'],
        20: ['防禦裝甲', '特殊'],
        21: ['防禦裝甲', '彈力'],
        22: ['戰鬥站位', '前方'],
        23: ['戰鬥站位', '中間'],
        24: ['戰鬥站位', '後方'],
        25: ['角色學園', '阿拜多斯'],
        26: ['角色學園', '奧利斯'],
        27: ['角色學園', '格黑娜'],
        28: ['角色學園', '百鬼夜行'],
        29: ['角色學園', '千年'],
        30: ['角色學園', '赤冬'],
        31: ['角色學園', '山海經'],
        32: ['角色學園', '三一'],
        33: ['角色學園', '女武神'],
        34: ['角色學園', 'SRT'],
        35: ['角色學園', '其他'],
        36: ['角色武器', 'SG霞彈槍'],
        37: ['角色武器', 'SMG衝鋒槍'],
        38: ['角色武器', 'AR突擊槍'],
        39: ['角色武器', 'GL榴彈發射器'],
        40: ['角色武器', 'HG手槍'],
        41: ['角色武器', 'SR狙擊槍'],
        42: ['角色武器', 'RG磁軌炮'],
        43: ['角色武器', 'MG機槍'],
        44: ['角色武器', 'RL火箭發射器'],
        45: ['角色武器', 'MT迫擊炮'],
        46: ['角色武器', 'FT噴火槍']
    };

    const Crawl = CrawlCore();
    const Display = { // 顯示菜單
        "一鍵自動操作": {
            func: () => Crawl.Auto("一鍵自動操作")
        },
        "➖➖➖ 戰略定位 ➖➖➖": {func: () => {}, close: false},
        "STRIKER": {
            func: () => Crawl.Monitor("STRIKER", Reference['戰略定位']['STRIKER']), close: false
        },
        "SPECIAL": {
            func: () => Crawl.Monitor("SPECIAL", Reference['戰略定位']['SPECIAL']), close: false
        },
        "➖➖➖ 戰術類別 ➖➖➖": {func: () => {}, close: false},
        "坦克": {
            func: () => Crawl.Monitor("坦克", Reference['戰術類別']['坦克']), close: false
        },
        "輸出": {
            func: () => Crawl.Monitor("輸出", Reference['戰術類別']['輸出']), close: false
        },
        "補師": {
            func: () => Crawl.Monitor("補師", Reference['戰術類別']['補師']), close: false
        },
        "輔助": {
            func: () => Crawl.Monitor("輔助", Reference['戰術類別']['輔助']), close: false
        },
        "支援": {
            func: () => Crawl.Monitor("支援", Reference['戰術類別']['支援']), close: false
        },
        "➖➖➖ 角色稀有度 & 獲取管道 ➖➖➖": {func: () => {}, close: false},
        "1星": {
            func: () => Crawl.Monitor("1星", Reference['角色稀有']['1星']), close: false
        },
        "2星": {
            func: () => Crawl.Monitor("2星", Reference['角色稀有']['2星']), close: false
        },
        "3星": {
            func: () => Crawl.Monitor("3星", Reference['角色稀有']['3星']), close: false
        },
        "慶典": {
            func: () => Crawl.Monitor("慶典", Reference['獲取管道']['慶典']), close: false
        },
        "限定": {
            func: () => Crawl.Monitor("限定", Reference['獲取管道']['限定']), close: false
        },
        "活動": {
            func: () => Crawl.Monitor("活動", Reference['獲取管道']['活動']), close: false
        },
        "常駐": {
            func: () => Crawl.Monitor("常駐", Reference['獲取管道']['常駐']), close: false
        },
        "➖➖➖ 攻擊屬性 ➖➖➖": {func: () => {}, close: false},
        "爆炸": {
            func: () => Crawl.Monitor("爆炸", Reference['攻擊屬性']['爆炸']), close: false
        },
        "貫通": {
            func: () => Crawl.Monitor("貫通", Reference['攻擊屬性']['貫通']), close: false
        },
        "神秘": {
            func: () => Crawl.Monitor("神秘", Reference['攻擊屬性']['神秘']), close: false
        },
        "振動": {
            func: () => Crawl.Monitor("振動", Reference['攻擊屬性']['振動']), close: false
        },
        "➖➖➖ 防禦裝甲 ➖➖➖": {func: () => {}, close: false},
        "輕裝": {
            func: () => Crawl.Monitor("輕裝", Reference['防禦裝甲']['輕裝']), close: false
        },
        "重裝": {
            func: () => Crawl.Monitor("重裝", Reference['防禦裝甲']['重裝']), close: false
        },
        "特殊": {
            func: () => Crawl.Monitor("特殊", Reference['防禦裝甲']['特殊']), close: false
        },
        "彈力": {
            func: () => Crawl.Monitor("彈力", Reference['防禦裝甲']['彈力']), close: false
        },
        "➖➖➖ 戰鬥站位 ➖➖➖": {func: () => {}, close: false},
        "前方": {
            func: () => Crawl.Monitor("前方", Reference['戰鬥站位']['前方']), close: false
        },
        "中間": {
            func: () => Crawl.Monitor("中間", Reference['戰鬥站位']['中間']), close: false
        },
        "後方": {
            func: () => Crawl.Monitor("後方", Reference['戰鬥站位']['後方']), close: false
        },
        "➖➖➖ 角色學園 ➖➖➖": {func: () => {}, close: false},
        "阿拜多斯": {
            func: () => Crawl.Monitor("阿拜多斯", Reference['角色學園']['阿拜多斯']), close: false
        },
        "奧利斯": {
            func: () => Crawl.Monitor("奧利斯", Reference['角色學園']['奧利斯']), close: false
        },
        "格黑娜": {
            func: () => Crawl.Monitor("格黑娜", Reference['角色學園']['格黑娜']), close: false
        },
        "百鬼夜行": {
            func: () => Crawl.Monitor("百鬼夜行", Reference['角色學園']['百鬼夜行']), close: false
        },
        "千年": {
            func: () => Crawl.Monitor("千年", Reference['角色學園']['千年']), close: false
        },
        "赤冬": {
            func: () => Crawl.Monitor("赤冬", Reference['角色學園']['赤冬']), close: false
        },
        "山海經": {
            func: () => Crawl.Monitor("山海經", Reference['角色學園']['山海經']), close: false
        },
        "三一": {
            func: () => Crawl.Monitor("三一", Reference['角色學園']['三一']), close: false
        },
        "女武神": {
            func: () => Crawl.Monitor("女武神", Reference['角色學園']['女武神']), close: false
        },
        "SRT": {
            func: () => Crawl.Monitor("SRT", Reference['角色學園']['SRT']), close: false
        },
        "其他": {
            func: () => Crawl.Monitor("其他", Reference['角色學園']['其他']), close: false
        },
        "➖➖➖ 角色武器 ➖➖➖": {func: () => {}, close: false},
        "SG": {
            func: () => Crawl.Monitor("SG", Reference['角色武器']['SG霞彈槍']), close: false
        },
        "SMG": {
            func: () => Crawl.Monitor("SMG", Reference['角色武器']['SMG衝鋒槍']), close: false
        },
        "AR": {
            func: () => Crawl.Monitor("AR", Reference['角色武器']['AR突擊槍']), close: false
        },
        "GL": {
            func: () => Crawl.Monitor("GL", Reference['角色武器']['GL榴彈發射器']), close: false
        },
        "HG": {
            func: () => Crawl.Monitor("HG", Reference['角色武器']['HG手槍']), close: false
        },
        "SR": {
            func: () => Crawl.Monitor("SR", Reference['角色武器']['SR狙擊槍']), close: false
        },
        "RG": {
            func: () => Crawl.Monitor("RG", Reference['角色武器']['RG磁軌炮']), close: false
        },
        "MG": {
            func: () => Crawl.Monitor("MG", Reference['角色武器']['MG機槍']), close: false
        },
        "RL": {
            func: () => Crawl.Monitor("RL", Reference['角色武器']['RL火箭發射器']), close: false
        },
        "MT": {
            func: () => Crawl.Monitor("MT", Reference['角色武器']['MT迫擊炮']), close: false
        },
        "FT": {
            func: () => Crawl.Monitor("FT", Reference['角色武器']['FT噴火槍']), close: false
        }
    };
    Syn.Menu(Display); // 首次創建菜單

    /* 抓取核心 */
    function CrawlCore() {
        const Record = new Set(); // 用於紀錄當前的操作對象

        // 抓取網頁數據
        let SaveRecord = []; // 紀錄保存資料
        function GetDB() {
            document
                .querySelector("div.vue-recycle-scroller__item-wrapper")
                .querySelectorAll("span.label-text")
                .forEach((item) => {
                    SaveRecord.push(item.textContent.replace("（", "(").replace("）", ")"));
                });
        };

        // 更新菜單名稱 (ID 就是原始的名稱)
        function RefreshMenu(ID, Name) {
            const NewDisplay = Object.keys(Display).reduce((acc, key) => {
                if (key === ID) acc[Name] = Display[key]; // 修改指定的鍵
                else acc[key] = Display[key]; // 保留原有鍵
                return acc;
            }, {});
            Syn.Menu(NewDisplay); // 為了保有順序全部重新創建
        };

        return {
            Auto: (Name)=> { // 菜單名

                if (Record.size > 0 && !Record.has(Name)) return; // 有運行中的紀錄
                let Stop = false; //! 無效重新修正 (再次呼叫時, 會被重新宣告, 因此其無法真正的停止)

                if (Record.has(Name)) { // 臨時取消操作
                    Stop = true;

                    //! 等待開發
                    Record.clear();
                    SaveRecord = [];
                    return;
                };
                Record.add(Name); // 紀錄運行

                const FinalResult = {};
                const MenuList = [...Syn.$$("div.search-filter-group-list button.btn-pill", { all: true })].slice(3);
                const Deselect = Syn.$$(".d-flex.gap-2.flex-wrap button");
                const Loop = (index, callback) => { // 循環處理
                    if (Stop) return;

                    const Box = Correspond[index];
                    if (!Box) {
                        callback?.();
                        return;
                    };

                    if (!Deselect.classList.contains("disabled")) { // 取消其他選取
                        Deselect.click();
                    };

                    setTimeout(() => {
                        if (Stop) return;

                        MenuList[index]?.click(); // 點擊操作對象
                        window.scroll(0, 0); // 回到最上方

                        const scrollRun = setInterval(()=> {
                            if (Stop) {
                                clearInterval(scrollRun);
                                return;
                            };

                            GetDB(); // 循環抓取數據
                            if (window.scrollY + window.innerHeight >= Syn.$$(".vue-recycle-scroller__item-wrapper").scrollHeight) {
                                clearInterval(scrollRun);

                                const refer = new Set(Reference[Box[0]][Box[1]]); // 利用對應列表數據找到 參照列表
                                const clearRepeat = [...new Set(SaveRecord)].filter(item => !refer.has(item));

                                if (clearRepeat.length > 0) { // 有重複的才顯示
                                    const Label = FinalResult[Box[0]] ?? (FinalResult[Box[0]] = {});
                                    Label[Box[1]] = clearRepeat; // 將重複數據保存到最終結果

                                    const json = JSON.stringify(clearRepeat, null, 4);
                                    console.log(`${Box[1]} : `, json);
                                };

                                SaveRecord = []; // 清空緩存
                                Loop(++index, callback); // 下一輪操作
                            };

                            // 開始循環滾動
                            window.scrollBy(0, window.innerHeight);
                        }, 1.3e3);
                    }, 500);
                };

                //! 等待開發
                Loop(0, ()=> {
                    console.log("操作完成");
                    console.log(JSON.stringify(FinalResult, null, 4));      
                });
            },
            /**
             * 監聽滑鼠滾動, 抓取數據 (個別操作)
             * @param {string} Name - 菜單名
             * @param {object} Refer - 參考數據
             */
            Monitor: (Name, Refer)=> {

                if (Record.size > 0 && !Record.has(Name)) return;

                if (Record.has(Name)) { // 取消監聽並輸出
                    Record.clear();
                    RefreshMenu(Name, Name);
                    Syn.RemovListener(window, "wheel");

                    const refer = new Set(Refer); // 根據參照物排除重複, 輸出剩下的
                    const clearRepeat = [...new Set(SaveRecord)].filter(item => !refer.has(item));

                    const json = JSON.stringify(clearRepeat, null, 1);
                    GM_setClipboard(json.slice(1, -1).trim());
                    console.log(`${Name} : `, json);

                    SaveRecord = [];
                    return;
                }

                Record.add(Name); // 紀錄運行
                RefreshMenu(Name, `${Name} (監聽中)`);

                GetDB(); // 先抓取一次數據
                Syn.AddListener(window, "wheel", Syn.Throttle(GetDB, 100)); // 監聽滑鼠滾動, 持續抓數據
            }
        }
    };
})();