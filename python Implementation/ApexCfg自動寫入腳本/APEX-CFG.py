CFG = [
    # 特別按鍵設置=====================================================================================
    'bind_US_standard "F2"  "exec autoexec.cfg"											',# 重新加載 autoexec (刷新Cfg)
    'bind_US_standard "F3" "miles_reboot; miles_stop_all"								',# 聲音重製(當發生聲音Bug時 重製遊戲聲音)
    'bind_US_standard "F5"  "disconnect"												',# 段開與伺服器的連接(直接回到伺服器選擇介面)

    # 按鍵設定=======================================================================================

    'bind_US_standard "x" "+ping"                                                       ',  # 使用X ping點
    'bind_US_standard "space" "+jump; +jump; +jump;"                                    ',
    'bind_US_standard "e" "+use; +use; +use; +use_long; +use_long;"                     ',
    'bind_US_standard "MOUSE4" "+melee"                                                 ',  # 側鍵近戰
    'bind_US_standard "mouse5" "+duck; +duck;" 											',  # 側鍵蹲
    'bind_US_standard "mwheelup" "+forward; +jump; +forward; +jump;" 					',  # 滾輪 (跳+前)
    'bind_US_standard "h" "+scriptCommand5" 											',  # 短按 輔助技能
    'bind_held_US_standard "h" "+scriptCommand6"										',  # 長按 生存道具

    # 補品快速鍵設置===================================================================================

    'bind_US_standard "1" "use_consumable SHIELD_SMALL"									',  # 短按1拉小電
    'bind_held_US_standard "1" "use_consumable SHIELD_LARGE" 							',  # 長按1拉大電
    'bind_US_standard "2" "use_consumable HEALTH_SMALL"									',  # 短按2拉小補
    'bind_held_US_standard "2" "use_consumable HEALTH_LARGE" 							',  # 長按2拉大補

    # 設定靈敏度參數(我的滑鼠DPI:1450)=======================================================================
    # 平均0.48
    'm_acceleration "0"                                                                 ',  # 確保滑鼠加速關閉

    'mouse_sensitivity "0.400000" 														',  # 腰射 edpi:
    'mouse_use_per_scope_sensitivity_scalars "1"										',  # 是否開啟個別設置倍鏡 1(True) 2(False)
    'mouse_zoomed_sensitivity_scalar_0 "0.520000" 										',  # x1倍鏡 edpi:739.5
    'mouse_zoomed_sensitivity_scalar_1 "0.530000" 										',  # x2倍鏡 edpi:768.5
    'mouse_zoomed_sensitivity_scalar_2 "0.560000" 										',  # x3倍鏡 edpi:797.5
    'mouse_zoomed_sensitivity_scalar_3 "0.580000" 										',  # x4倍鏡 edpi:826.5
    'mouse_zoomed_sensitivity_scalar_4 "0.860000"										',  # x6倍鏡
    'mouse_zoomed_sensitivity_scalar_5 "0.860000"										',  # x8倍鏡
    'mouse_zoomed_sensitivity_scalar_6 "0.860000"										',  # x10倍鏡
    'mouse_zoomed_sensitivity_scalar_7 "1.0"											',  # 不知道衝三小的

    
    # 玩法優化 =======================================================================================

    'cl_showpos "1"																		',  # 顯示跑速座標等各項數據(1~4可選)
    # developer "1"																	        #開發者模式(失效)
    'mat_queue_mode "2"																    ',  # 強製遊戲使用（-1 默認，0 同步單線程，1 排隊單線程，2 多線程）
    'localClientPlayerCachedLevel "25" 													',  # 修復了當你的隊友看到你為 1 級時無法排位的問題
    'ordnanceSwapSelectCooldown "0"  													',  # 減少手榴彈交換時間
    'sidearmSwapSelectCooldown "0"														',  # 減少物品左右交換時間
    'sidearmSwapSelectDoubleTapTime "0"													',  # 減少更換武器的時間
    'mat_depthfeather_enable "0"														',  # 禁用景深
    'hud_setting_adsDof "0"																',  # 禁用向下瞄準時景深
    'cl_matchmaking_timeout "100"  														',  # NG匹配超時修復
    'cl_ranked_reconnect_timeout "100" 													',  # RK匹配超時修復
    'player_setting_damage_closes_deathbox_menu "0"                                     ',  # 關閉受到攻擊時死亡箱自動關閉
    'sprint_view_shake_style "1"                                                        ',  # Less headbob(不知道中文)
    'hud_setting_pingDoubleTapEnemy "1"                                                 ',  # 雙倍的標示敵人
    'fov_disableAbilityScaling "1"                                                      ',  # 關閉技能fov變化
    'net_netGraph2 "1"                                                                  ',  # 開啟性能展示
    'weapon_setting_autocycle_on_empty "1"                                              ',  # 武器自動循環

    # 聲音特效=======================================================================================

    'miles_max_sounds_per_server_frame "800"											',  # 服務器每偵聲音輸出上限
    'miles_channels "2"																	',  # 輸出雙聲道
    'sound_num_speakers "2"															    ',  # 喇叭雙聲道
    'snd_mixahead "0.03"																',  # 減少聲音延遲
    'snd_async_fullyasync "1"															',  # 聲音同步
    'sound_classic_music "0"															',  # 經典聲音音量
    'snd_musicvolume "0"																',  # 禁用不必要的聲音
    'sound_musicReduced "0"															    ',  # 遊戲BGM音量
    'voice_forcemicrecord "0"															',  # 錄音功能關閉
    'snd_headphone_pan_exponent "2"													    ',  # 使對的方向聲音你所面會更清晰
    'snd_setmixer PlayerFootsteps vol "0.01"											',  # 自己腳步聲音量
    'snd_setmixer GlobalFootsteps vol "3"											    ',  # 別人腳步聲音量
    'cl_footstep_event_max_dist "5000" 												    ',  # 增加敵人腳步聲傳遞範圍
    'rope_wind_dist "5000"																',  # 增大敵人使用繩索的聲音
    'player_setting_enable_heartbeat_sounds "0"                                         ',  # 禁用席爾的心跳聲
    'sound_volume_music_game "0.000000"												    ',  # 不知道
    'sound_volume_music_lobby "50.000000"												',  # 不知道
    'miles_occlusion "0"                                                                ',  # 以下為取消牆壁吸收音量(可能無效了)
    'miles_occlusion_force "0"',
    'miles_occlusion_partial "0"',
    'snd_mix_async "1"',
    'miles_nonactor_occlusion "0"',
    'miles_occlusion_server_sounds_per_frame "0"',

    # 光影效果=======================================================================================

    'mat_light_edit "1"																	',  # 地圖燈光照明
    'map_settings_override "1"															',  # 設置覆蓋 (不確定幹嘛的)
    'mat_autoexposure_min "1.9" 														',  # 光照強度最小值
    'mat_autoexposure_max "1.9" 														',  # 光照強度最大值
    'mat_autoexposure_speed "2" 														',  # 畫面曝光轉變的速度
    'mat_hide_sun_in_last_cascade "1" 													',  # 最後一個級聯中的太陽能照明
    'mat_colcorrection_disableentities "1" 												',  # 更換濾色器（稍微去除離場時“失明”的效果)
    'mat_autoexposure_max_multiplier "1.7" 												',  # 光強度最大乘數
    'mat_autoexposure_min_multiplier "1.7" 												',  # 光強度最小的乘數
    'mat_autoexposure_override_min_max "1"												',  # 曝光最大值最小值
    'mat_colorcorrection_editor "1"                                                     ',  # 顏色校正編輯
    'mat_sun_highlight_size "0"                                                         ',  # 改變來自太陽的亮點的大小
    'mat_fullbright "1"                                                                 ',  # 開啟幾何圖形的自發光功能
    'mat_colorcorrection "1"                                                            ',  # 顏色校正

    # 優化FPS=======================================================================================

    'bind_US_standard "8" "fps_max 120"',
    'bind_US_standard "9" "fps_max 144"',
    'bind_US_standard "0" "fps_max 240"',
    'fps_max 240',
    'refresh 240																		',  # 螢幕刷新 240
    'nomemorybias																	    ',  # 減少Ram消耗
    'cl_forcepreload "1"																',  # 預先載入地圖避免FPS急速掉落
    'mat_compressedtextures "1" 														',  # 壓縮遊戲裡面的畫質
    'mat_reduceparticles "0"															',  # 粒子效果關閉
    'mat_screen_blur_enabled "0"														',  # 螢幕模糊效果關閉
    'mat_disable_bloom "1"																',  # 禁用綻放特效 (不確定)
    'cl_ragdoll_collide "0" 															',  # 降低遊戲內死亡後的物理引擎
    'r_forcewaterleaf "0" 																',  # 水中植被物理引擎降低
    'r_shadowrendertotexture "0" 														',  # 降低陰影質量 (變的更亮) 0 最低
    'r_worldlights "0"																	',  # 光源減少
    'r_dxgi_max_frame_latency "0"														',  # 延遲最大幀
    'nomansky																		    ',  # 減少天空渲染
    'noforcemaccel																	    ',  # 不知道
    'noforcemspd																		',  # 不知道
    'host_writeconfig																	',  # 不知道
    'staticProp_max_scaled_dist "1500"													',  # 靜態物體渲染距離
    'r_particle_timescale "6"                                                           ',  # 加速粒子
    'nx_static_lobby_mode "2"                                                           ',  # 減少加載時間
    'noise_filter_scale "0"                                                             ',  # 去除膠片顆粒
    'cl_show_splashes "0"                                                               ',  # 減少水濺效果
    'fog_enable "0"                                                                     ',  # 禁用霧（不是到處禁用）（有效）
    'fast_fogvolume "1"                                                                 ',  # 使用優化的霧渲染
    'fog_enableskybox "1"                                                               ',  # 禁用天空上的霧（減少）（有效）
    'mat_bloom_scalefactor_scalar "0"                                                   ',  # 禁用綻放（減少）（有效）
    'r_forcecheapwater "1"                                                              ',  # 水質下降
    'r_waterdrawreflection "0"                                                          ',  # 禁用水面上的所有反射
    'r_waterforcereflectentities "0"                                                    ',  # 1 = 高（反射所有），0 = 低（減少）(有效)
    'r_cleardecals "1"                                                                  ',  # 清除所有貼花
    'r_decalstaticprops "0"                                                             ',  # 在靜態道具上禁用貼花
    'shadow_always_update "0"                                                           ',  # 禁用陰影檢查
    'r_shadows "0"                                                                      ',  # 陰影  on(1)/off(0)（不完全）（有效）
    'r_eyes "0"                                                                         ',  # 眼睛 (1)/降低質量(0)
    'r_teeth "0"                                                                        ',  # 牙齒開（1）/降低質量（0）
    'r_flex "0"                                                                         ',  # 使用面部動畫 on(1)/off(0)
    'r_maxdlights "0"                                                                   ',  # 優化屏幕上可見的動態光的最大數
    'stream_drop_unused "1"                                                             ',  # 丟棄未使用的紋理
    'glow_outline_effect_enable "0"                                                     ',  # 減少熔巖中的發光效果
    'mat_bumpmap "0"                                                                    ',  # 控制凹凸貼圖
    'mat_specular "0"                                                                   ',  # 控制鏡面效果
    'stream_cache_high_priority_static_models "1"                                       ',  # 預加載
    'stream_cache_preload_from_rpak "1"                                                 ',  # 從rpak預加載到緩存
    'viewmodel_selfshadow "0"                                                           ',  # 禁用玩家模型及其武器的陰影
    'r_drawmodeldecals "0"                                                              ',  # 在模型上渲染貼花 開(1)/關(0)
    'r_queued_post_processing "1"                                                       ',  # 將後期處理卸載到材質系統中。如果你的驅動/GPU能用的話，性能會有所提高（安慰劑）。
    'g_ragdoll_fadespeed "10000"                                                        ',  # 布娃娃的褪色率（越高的褪色率越快，所以0不會褪色並導致內存洩露） (有效)
    'g_ragdoll_lvfadespeed "10000"                                                      ',  # 低度暴力中布娃娃的褪色率 (有效)
    'mp_usehwmmodels "-1"                                                               ',  # 不要使用或加載高質量的角色
    'mp_usehwmvcds "-1"                                                                 ',  # 不要使用或加載高質量的人物面部表情 (有效)
    'cl_phys_props_enable "0"                                                           ',  # 禁用懸臂
    'cl_phys_props_max "0"                                                              ',  # 禁用懸臂
    'props_break_max_pieces "0"                                                         ',  # 禁用搖臂
    'rope_smooth "0"                                                                    ',  # 跳過對繩索的長時間平滑操作
    'rope_collide "0"                                                                   ',  # 禁用繩索抖動
    'mat_postprocess_enable "0"                                                         ',  # 移除強制HDR
    'mat_dynamic_tonemapping "0"                                                        ',  # 禁用動態HDR色調映射
    'mat_hdr_level "0"                                                                  ',  # 禁用完全HDR
    'r_shadowmaxrendered "0"                                                            ',  # 遊戲將渲染的最大陰影 (不完全)
    'r_drawtracers_firstperson "0"                                                      ',  # 子彈上沒有追蹤器
    'mat_shadowstate "0"                                                                ',  # 無陰影(0)，玩家模型為陰影(2) (減少)
    'mat_mip_linear "0"                                                                 ',  # 紋理過濾開(1)/關(0
    'ssao_blur "0"                                                                      ',  # 模糊、反射和高光
    'sssss_enable "0"                                                                   ',  # 禁用熒幕空間的次表面散射
    'mat_reducefillrate "1"                                                             ',  # 簡化材料陰影
    'cl_particle_fallback_multiplier "3"                                                ',  # 負載下回落到便宜效果的倍數
    'cl_particle_fallback_base "2"                                                      ',  # 負載下回落到更便宜的效果的基礎
    'cl_ragdoll_maxcount "0"                                                            ',  # 禁用布娃娃
    'cl_phys_maxticks "0"                                                               ',  # 允許的物理點的數量
    'r_lod_switch_scale "0.4"                                                           ',  # 低端模型的加載距離
    'cl_detailfade "0"                                                                  ',  # 細節道具淡入的距離
    'cl_detaildist "0"                                                                  ',  # 細節道具不再可見的距離
    'r_jiggle_bones "0"',
    'r_dxgi_max_frame_latency "1"',

    # 網路優化(loss丟失/choke阻塞)=======================================================================
    
    # 'host_limitlocal "1"															    ',  # 是否關閉使用本地DNS
    # 'rate "125000"																	    ',  # https//:agame01.com/article/682994/
    # 'cl_cmdrate "100"																    ',  # 每秒上傳幾組 packet 到 server (丟包loss時降低)
    # 'cl_updaterate "100"															    ',  # 每秒向 server 接收幾組 packet (阻塞choke時降低)
    # 'cl_lagcompensation "1"															    ',  # 延遲補償開啟
    # 'cl_resend "2"																	    ',  # 網路錯誤重發間隔
    # 'cl_interp "0"																	    ',  # 網路插播關閉
    # 'cl_interp_ratio "1"															    ',  # 間格比(數值加大減少丟包)
    # 'cl_pred_optimize "1"															    ',  # 預優化?
    # 'cl_predict "1"																	    ',  # 不確定
    # 'cl_predictweapons "1"															    ',  # 不確定
    # 'cl_wpn_sway_interp "0"															    ',  # wpn搖擺解釋器
    # 'cl_interpolate "0"																    ',  # 不知道
    # 'cl_interpolation_before_prediction "0"											    ',  # 不知道
    # 'cl_cmdbackup "2"																    ',  # 數據包丟失備份發送
    # 'cl_updatevisibility "1"														    ',  # 更新可見性
    # 'cl_timeout "25"																    ',  # 超時請求
    # 'cl_smooth "1"																	    ',  # 不知道
    # 'cl_smoothtime "0.01"															    ',  # 不知道
    # 'pin_opt_in "0"																	    ',  # 禁止將 PIN 遙測數據發送到 EA
    # 'pin_plat_id "0"																    ',  # 退出重生數據調查
    # 'telemetry_client_enable "0"													    ',  # 多久發送一次遙測數據
    # 'projectile_prediction " 1 "													    ',  # 啟用客戶端預測和彈丸補償
    # 'projectile_predictionErrorCorrectTime " 0.01 "									    ',  # 修正彈丸預測誤差的時間
    # 'origin_presense_updateRate " 10 "												    ',  # 在每次 Origin 存在更新之間放寬秒數
    # 'net_compresspackets " 1 "														    ',  # 壓縮發送到服務器的數據包
    # 'net_compresspackets_minsize " 64 "												    ',  # 壓縮包不低於設定值
    # 'net_maxcleartime " 0.030000 "													    ',  # 減少引擎等待發送另一個數據包的時間
    # 'host_sleep "0"																	    ',  # 強製主機每幀休眠一定的毫秒數'''
    # 'telemetry_client_sendInterval "0"',
]

# ===================================================上面才是設定值,下面不用觀看=============================================================
"""~~~~~~~~~~~~~~~~~~~~
Versions 1.3
[+] 功能代碼重構
[+] 多線程輸出加速

預計增加
[+] UI介面
~~~~~~~~~~~~~~~~~~~~"""

from tkinter import filedialog
import configparser as config
import tkinter as tk
import threading
import os

os.system('color A')
os.system('@echo off')
os.system('cls')
os.system('@ ECHO.')
os.system('@ ECHO.~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ APEX-CFG設置程序 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
os.system('@ ECHO.')
os.system('@ ECHO                                                  測試17賽季適用')
os.system('@ ECHO.')
os.system('@ ECHO                                                     使用說明')
os.system('@ ECHO.')
os.system('@ ECHO                               最多可設置兩個路徑 , 第一次設置完成後 , 就不會再跳出設置了')
os.system('@ ECHO.')
os.system('@ ECHO                          需要重新設置的 , 就將生成的[CFG_Set.ini]刪除掉 , 再次運行程式進行設置')
os.system('@ ECHO.')
os.system('@ ECHO -----------------------------------------------------------------------------------------------------------------------')
os.system('@ ECHO                                                按任意鍵開始運行程式')
os.system('@ ECHO -----------------------------------------------------------------------------------------------------------------------')
os.system('@ ECHO.')
os.system('pause')
os.system('cls')
class Automatic:
    def __init__(self):
        self.set = None     # 保存設定設置
        self.file = None    # 保存檔案開啟
        self.path1 = None   # 設置路徑1
        self.path2 = None   # 設置路徑2
        self.filename = "/autoexec.cfg" #檔名格式宣告

        # ============= 讀取設置檔 =============
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        try:
            # 環境不同有解析失敗的問題,改成直接讀取
            with open('CFG_Set.ini', 'r') as c:
                contents = c.read()

            InSet = config.ConfigParser()
            InSet.read_string(contents)

            # 設置讀取
            self.path1 = InSet.get('set', 'path1')
            self.path2 = InSet.get('set', 'path2')

            # 輸出第一設置路徑
            threading.Thread(target=self.output,args=(self.path1,)).start()

        # ======== 判斷設置檔是否存在第二項位置 ========
            if self.path2.lower() != "null":
                # 輸出第二設置路徑
                threading.Thread(target=self.output,args=(self.path2,)).start()
            elif self.path2.lower() == "null":pass

            # 用於已有設置ini檔,運行成功的提示
            print('運行成功')
            input('\n按任意鍵結束運行...')
        
        # 當出現讀取錯誤時創建
        except:self.file_creation()

    # ========== 創建一個設置檔 ==========
    def file_creation(self):
        # 創建
        self.file = open("CFG_Set.ini", "w")

        # 讀取並使用config設置
        self.set = config.ConfigParser()
        self.set.read("CFG_Set.ini" , "UTF-8")

        """也可使用 file.write("[set]\n") 去進行寫入,這方法較為簡單"""
        # 添加寫入 set
        self.set.add_section('set')

        # 呼叫設置方法
        self.settings()

    # ========== 開始設置 ==========
    def settings(self):
        #! 選擇文件 -> askopenfilename()  選擇資料夾 -> askdirectory()

        # 調用選取窗口
        root = tk.Tk()
        root.withdraw()

        print('請選擇您的APEX資料夾,內的CFG資料夾的')
        self.path1 = filedialog.askdirectory()
        Cfg_File = os.path.join(self.path1,'autoexec.cfg')

        with open(Cfg_File, 'w') as cfg_file:
           cfg_file.write('\n')

        # 創建完後再將字串加入,方便寫入至設定ini檔保存
        self.path1 += self.filename
        self.set.set('set','path1', self.path1)

        # ========== 第二項設置詢問 ==========
        try:
            while True:
                self.path2 = input('是否需要設置第二個位置(Y/N):')

                if self.path2.lower() == 'y':

                    self.path2 = filedialog.askdirectory()
                    Cfg_File = os.path.join(self.path2,'autoexec.cfg')

                    with open(Cfg_File, 'w') as cfg_file:
                        cfg_file.write('\n')

                    self.path2 += self.filename
                    self.set.set('set','path2', self.path2)
                    break

                elif self.path2.lower() == 'n':
                    self.path2 = "NULL"
                    break

                else:
                    print("輸入錯誤 , 請輸入 Y 或 N\n")
                    continue

            # 全部設置完就輸出第一路徑和第二路徑
            threading.Thread(target=self.output,args=(self.path1,)).start()
            threading.Thread(target=self.output,args=(self.path2,)).start()
            # 保存設置
            threading.Thread(target=self.save_settings).start()

            print('運行成功')
            input('\n按任意鍵結束運行...')
            # os._exit(0)
        except:
            os.system('cls')
            print('運行錯誤,請重新運行\n')
            # 基本上不會有出錯的時候
            os.system("del /f /s /q CFG_Set.ini >nul 2>&1") #採用靜默刪除指令
            input('\n按任意鍵結束運行...')

    def output(self,path):
        with open(path, 'w') as Auto:
            for out in CFG:Auto.write(out + '\n')
    
    def save_settings(self):
        with open("CFG_Set.ini", "w") as f:
            self.set.write(f,delimiter='')
        self.file.close()

if __name__ == "__main__":
    Automatic()