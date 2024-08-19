// 這是用於名稱, 即時搜尋對象的算法 回傳 -> {Length: ?, Data_n: obj...}
function NameSearchCore(original) {
    const searchDict = {};
    const originalTable = original;

    const addEntry = (node, key, value) => {
        let currentNode = node;
        for (const char of key) {
            if (!currentNode[char]) currentNode[char] = {};
            currentNode = currentNode[char];
        }
        currentNode.data = value;
    };

    // 將最終數據解析為對應物件回傳
    const finalObject = (results) => {
        const resultsLen = Object.keys(results).length;

        if (resultsLen == 0) return;

        if (resultsLen == 1) { // 長度為 1, 回傳為一物件, 和長度資訊
            const data = results[0];

            if (typeof data === "string") { // 是單個字串, 從原始表找出對應
                return {Length: resultsLen, Data_0: originalTable[data]}
            } else { // 是其他物件類型, 直接回傳
                return {Length: resultsLen, Data_0: data}
            }
        }

        // 存在多個對應
        const merge = {Length: resultsLen}; // 將多對應合併
        for (const [index, data] of results.entries()) {
            merge[`Data_${index}`] = originalTable[data] ?? {};
        }

        return merge;
    };

    // 遞迴找到最終所有符合的 .data 數據
    const collectAllNames = (node) => {
        const results = [];
        if (node.data) results.push(node.data);

        for (const key in node) {
            const nodeKey = node[key];

            if (typeof nodeKey === "object") {
                results.push(...collectAllNames(nodeKey));
            }
        }

        return results;
    };

    // 觸發遞歸搜尋, 找對最終數據
    const searchRecursively = (node, str, index) => {
        if (index >= str.length) return [];

        const nextNode = node[str[index]];

        if (!nextNode) return [];

        if (index === str.length - 1) {
            return finalObject(collectAllNames(nextNode));
        }

        return searchRecursively(nextNode, str, index + 1);
    };

    return {
        showData: () => { // 展示添加結果
            console.log(JSON.stringify(searchDict, null, 4));
        },
        addData: (dataObj) => { // 創建實例後, 先將數據物件添加
            for (const [key, value] of Object.entries(dataObj)) {
                addEntry(searchDict, key, value);
            }
        },
        searchData: (str) => { // 輸入任意字串進行搜索
            return searchRecursively(searchDict, str, 0);
        }
    };
}

// 創建實例要先傳遞初始表 (未被轉換)
const SC = NameSearchCore(
    {}
);

// 添加需轉換的表
SC.addData();