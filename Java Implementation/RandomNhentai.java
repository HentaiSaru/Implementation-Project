
/*
 * Versions 1.2
 * [+] 重構部份代碼
 * [+] 功能重寫
 * [+] 增加隨機範圍
~~~~~~~~~~~~~~~~~~~~~~~*/
import java.util.*;
import java.util.List;
import java.io.*;
import java.net.*;
import java.awt.*;
public class RandomNhentai {
    public static void main(String[] argv) {

        try (Scanner NHentai = new Scanner(System.in)) {
            ArrayList<String> UrlBox = new ArrayList<String>();
            System.out.println("輸入任意數字給予指定數量本本(-1結束程式)\n");
            String description = "請輸入數量 : ";
            boolean Cycle_State = true;

            while (Cycle_State) {
                System.out.print(description);
                int enter = NHentai.nextInt();
                if (enter >= 1) {
                    for (int i = 1; i <= enter; i++) {
                        String hentai = "https://nhentai.net/g/" + (int) (Math.random() * 447000 + 1);
                        UrlBox.add(hentai);
                    }
                    System.out.print("等待開啟...\n");
                    ran(UrlBox);
                    UrlBox.clear();
                    description = "請繼續輸入 : ";
                } else if (enter == -1) {
                    Cycle_State = false;
                } else {
                    throw new InputMismatchException();
                }

            }
        } catch (Exception InputMismatchException) {
            System.out.println("請輸入數字\n程式已終止...");
        }
    }

    public static void ran(List<String> Box) throws URISyntaxException {
        for (String url : Box) {
            try {
                Desktop.getDesktop().browse(new URI(url));
                Thread.sleep(1500);
            } catch (IOException e) {
                System.out.println("無效的網址: " + url);
            } catch (InterruptedException e) {
                System.out.println("運行被中斷");
            }
        }
        System.out.println("開啟完畢...");
    }
}