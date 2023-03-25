/*
 * Versions 1.2.3
 * [+] 將驗證部份改寫為Class
 * [+] 刪掉了多執行序,添加程式運行時間計數
 * [*] 預計添加輸出URL計數器
 * [*] 預計整合可修改網址類型接口
~~~~~~~~~~~~~~~~~~~~~~~*/
import java.io.*;
import java.net.*;
import java.util.*;
import java.util.concurrent.*;
public class RandomURL implements ShortenURL {
    static boolean jud; // 判斷輸出成敗的變數
    public static synchronized void main(String[] argv) {
        try (Scanner scanner = new Scanner(System.in)) {
            FileWriter clear = new FileWriter("可用網址.bat", false); // 開始程式時先將該bat內容清空
            clear.close();
            Random random = new Random();
            boolean cycleState = true; // 迴圈循環狀態
            boolean outStatus = false; // 判斷是否有驗證成功的網址
            long UrlSum = 0;           // URL計數器(未使用)

            while (cycleState) {

                System.out.print("輸入數量: ");
                int enter = scanner.nextInt();
                long timing1 = System.currentTimeMillis();      // 開始計算執行時間

                Generation_Quantity(enter);                     // 先採用懶人輸入量,後面的值是ShortenURL含有的總量
                System.out.println("\n網址可用性驗證中請稍後(數量越多時間越長)...");
                if (enter >= 1) {
                    jud = false;

                    for (int i = 0; i < enter; i++) {           // 根據輸入數量去生成縮網址
                        randomURL(random, SixrRandom);
                    }
 
                    if (jud) {outStatus = true;}                // 直接用方法判斷是否成功輸出
                    long timing2 = System.currentTimeMillis();
                    timeconversion((timing2 - timing1));        // 輸出所用時間
                    successOrFailureJudgment(outStatus);        // 判斷是否有成功輸出
                    cycleState = false;                         // 關閉迴圈

                } else {
                    throw new Exception();
                }
            }
        } catch (Exception e) {
            System.out.println("異常中止,錯誤代碼:" + e);
            return;
        }
    }

    // 輸出bat
    public static void batoutput(String url) throws IOException {
        FileWriter bat = new FileWriter("可用網址.bat", true);
        jud = true;
        bat.write("start " + url + "+\ntimeout /t 5 >nul\n");
        bat.close();
    }// ----------方法結尾----------
    // 隨機數生成器
    private static char get(Random random) {
        int i = random.nextInt(3);
        switch (i) {
            case 0:
                return (char) (random.nextInt(26) + 'A');
            case 1:
                return (char) (random.nextInt(26) + 'a');
            case 2:
                return (char) (random.nextInt(10) + '0');
        }
        return ' ';
    }// ----------方法結尾----------
    // 取用隨機數方法並且合併到輸出字串
    public static Callable<String> randomURL(Random random, String[] url) throws MalformedURLException {
        Network_Connection_Verification Network = new Network_Connection_Verification();

        String URL = url[0];
        for (int j = 0; j < 6; j++) {
            URL += get(random);
        }
        Network.DNS_resolution(URL);
        return null;
    }// ----------方法結尾----------

    /* ---以下為額外功能性Function--- */
    //  判斷需輸出網址數量
    public static void Generation_Quantity(int Enterthequantity) {
        System.out.printf("\n你將生成 %d 個網址\n", Enterthequantity);
    }
    // 輸出狀態
    private static void successOrFailureJudgment(boolean outStatus) throws IOException {
        if (outStatus) {
            System.out.println("成功輸出網址");
            //System.out.print("開啟網址");
            //Ran();
        } else {
            System.out.print("無可使用網址");
        }
    }
    // 輸出成功自動開啟
    public static void Ran() throws IOException {
        String path = System.getProperty("user.dir");
        String command = path + "\\可用網址.bat";
        ProcessBuilder builder = new ProcessBuilder(command);
        builder.directory(new File(path));
        builder.redirectOutput(ProcessBuilder.Redirect.INHERIT);
        Process process = builder.start();
        try {
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                System.err.println("開啟失敗，錯誤碼：" + exitCode);
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
    // 最後運行完的時間轉換
    public static void timeconversion(long Milliseconds) {
        long hours = 0,minutes = 0,seconds = 0,millisecond = 0;

        if(Milliseconds >= 1000){
            seconds = ((Milliseconds % 3600000) % 60000) / 1000;
            if(seconds >= 60){
                minutes = (Milliseconds % 3600000) / 60000;
                if(minutes >= 60){
                    hours = (Milliseconds / 3600000);
                }
            }
        }else{millisecond = Milliseconds;}  
        System.out.println("程式大約用時:"+ hours + "時" + minutes + "分" + seconds + "秒" + millisecond + "毫秒");
    }
}

/* 網址格式 */
interface ShortenURL {
    String[] SixrRandom = { "https://reurl.cc/" };
}

/* 網路驗證類別 */
class Network_Connection_Verification{

    // 網址第一重驗證(DNS解析)
    public String DNS_resolution(String url) throws MalformedURLException {
        try {
            URL parsedUrl = new URL(url);
            String hostname = parsedUrl.getHost();
            Response_validation(url);
        } catch (Exception e) {
        }
        return "";
    }// ----------方法結尾----------

    // 網址第二重驗證(響應驗證)
    private String Response_validation(String url) {
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setRequestMethod("HEAD");
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                URL finalUrl = connection.getURL();
                connection.disconnect();
                connection = (HttpURLConnection) finalUrl.openConnection();
                connection.setRequestMethod("HEAD");
                responseCode = connection.getResponseCode();
                Page_content_analysis(url);
            }
        } catch (IOException e) {
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
        return url;
    }// ----------方法結尾----------

    // 網址第三重驗證(網站內容驗證)
    private void Page_content_analysis(String url) throws IOException {
        URLConnection connection = new URL(url).openConnection();
        String contentType = connection.getContentType();

        try { // 驗證網站內容(以下為可通過驗證的類型)

            if (contentType.startsWith("text/") || contentType.startsWith("audio/") || contentType.startsWith("video/")
                    || contentType.startsWith("image/") || contentType.startsWith("application/zip")
                    || contentType.startsWith("application/x-rar-compressed")) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                if ((reader.readLine()) != null) {
                    RandomURL.batoutput(url); // 經過多重驗證後,再去呼叫輸出方法,將其寫
                } else {
                    throw new Exception();
                }
                reader.close();
            } else {
                throw new Exception();
            }
        } catch (Exception e) {
        }
    }// ----------方法結尾----------
}