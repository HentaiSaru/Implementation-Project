import path from 'path';
import { fileURLToPath } from 'url';
process.chdir(path.dirname(fileURLToPath(import.meta.url)));

import axios from 'axios';
import * as cheerio from 'cheerio';
import { File } from './!File.mjs';

(async () => {
    const Response = await axios.get("https://forum.gamer.com.tw/C.php?bsn=38898&snA=698&tnum=83");
    const $ = cheerio.load(Response.data);

    const DB = await File.Read("../DataBase/DB.json");
    const DBV = new Set(Object.values(DB['詳細資訊']).map(db=> db['IMG_URL']));

    const Data = new Set();
    for (const ID of ["3510", "3511", "3513"]) { // 抓取的帖子區域
        $(`article#cf${ID} div div div`).each((_, div) => {
            const href = $(div).find("a.photoswipe-image").attr("href");
            if (href) Data.add(href);
        })
    };

    // 排除已擁有連結
    const Result = [...Data].filter(item => !DBV.has(item));
    if (Result.length > 0) {
        File.Write("R:/Difference.json", Result);
    } else {
        console.log("無需更新");
    }
})();