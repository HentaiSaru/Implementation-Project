import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
process.chdir(path.dirname(fileURLToPath(import.meta.url)));

import axios from 'axios';
import * as cheerio from 'cheerio';

function ReadDB() {
    return new Promise((resolve, reject) => {
        fs.readFile("DB.json", "utf-8", (err, data) => {
            const Read = err ? false : data ?? false;
            if (Read) resolve(JSON.parse(Read));
            else {
                console.log(err);
                resolve({});
            }
        })
    })
};

(async () => {
    const DB = await ReadDB();
    const DBV = new Set(Object.values(DB['詳細資訊']).map(db=> db['IMG_URL']));

    const Response = await axios.get("https://forum.gamer.com.tw/C.php?bsn=38898&snA=698&tnum=83");
    const $ = cheerio.load(Response.data);

    const Data = new Set();
    for (const ID of ["3510", "3511", "3513"]) { // 抓取的帖子區域
        $(`article#cf${ID} div div div`).each((_, div) => {
            const href = $(div).find("a.photoswipe-image").attr("href");
            if (href) Data.add(href);
        })
    };

    fs.writeFile( // 輸出不同的連結
        "R:/Difference.json",
        JSON.stringify(
            [...Data].filter(item => !DBV.has(item)),
            null,
            4
        ),
    err => {
        err ? console.log("輸出失敗") : console.log("輸出成功");
    });
})();