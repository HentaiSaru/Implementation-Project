CFG = [
    # 特別按鍵設置 =========================================================================================
    'bind_US_standard "F2"  "exec autoexec.cfg"											',  # 重新加載 autoexec (刷新Cfg)
    'bind_US_standard "F3" "miles_reboot; miles_stop_all"								',  # 聲音重製(當發生聲音Bug時 重製遊戲聲音)
    'bind_US_standard "F5"  "disconnect"												',  # 段開與伺服器的連接(直接回到伺服器選擇介面)
    'bind_US_standard "8" "fps_max 120"                                                 ',  # 以下為動態修改 fps 上限
    'bind_US_standard "9" "fps_max 144"                                                 ',
    'bind_US_standard "0" "fps_max 240"                                                 ',

    # 設定靈敏度參數(我的滑鼠DPI:1450) =======================================================================
    # 平均0.48
    'm_acceleration "0"                                                                 ',  # 滑鼠加速關閉

    'mouse_sensitivity "0.950000" 														',  # 腰射 edpi:
    'mouse_use_per_scope_sensitivity_scalars "1"										',  # 是否開啟個別設置倍鏡 1(True) 2(False)
    'mouse_zoomed_sensitivity_scalar_0 "0.560000" 										',  # x1倍鏡 edpi:
    'mouse_zoomed_sensitivity_scalar_1 "0.580000" 										',  # x2倍鏡 edpi:
    'mouse_zoomed_sensitivity_scalar_2 "0.600000" 										',  # x3倍鏡 edpi:
    'mouse_zoomed_sensitivity_scalar_3 "0.620000" 										',  # x4倍鏡 edpi:
    'mouse_zoomed_sensitivity_scalar_4 "0.990000"										',  # x6倍鏡
    'mouse_zoomed_sensitivity_scalar_5 "0.990000"										',  # x8倍鏡
    'mouse_zoomed_sensitivity_scalar_6 "0.990000"										',  # x10倍鏡
    'mouse_zoomed_sensitivity_scalar_7 "1.0"											',  # 不知道衝三小的

    # 特別按鍵設定 ========================================================================================

    'bind_US_standard "x" "+ping"                                                       ',  # 使用X ping點
    'bind_US_standard "space" "+jump; +jump; +jump;"                                    ',
    'bind_US_standard "e" "+use; +use; +use_long; +use_long;"                           ',
    'bind_US_standard "MOUSE4" "+melee"                                                 ',  # 側鍵近戰
    'bind_US_standard "mouse5" "+duck; +duck;" 											',  # 側鍵蹲
    'bind_US_standard "mwheelup" "+forward; +jump; +forward; +jump;" 					',  # 滾輪 (跳+前)
    'bind_US_standard "h" "+scriptCommand5" 											',  # 短按 輔助技能
    'bind_held_US_standard "h" "+scriptCommand6"										',  # 長按 生存道具

    # 補品快速鍵設置 ======================================================================================

    'bind_US_standard "1" "use_consumable SHIELD_SMALL"									',  # 短按1拉小電
    'bind_held_US_standard "1" "use_consumable SHIELD_LARGE" 							',  # 長按1拉大電
    'bind_US_standard "2" "use_consumable HEALTH_SMALL"									',  # 短按2拉小補
    'bind_held_US_standard "2" "use_consumable HEALTH_LARGE" 							',  # 長按2拉大補

    # 玩法優化 ==========================================================================================

    'cl_showpos "1"																		',  # 顯示跑速座標等各項數據(1~4可選)
    'mat_queue_mode "2"																    ',  # 強製遊戲使用（-1 默認，0 同步單線程，1 排隊單線程，2 多線程）
    'ordnanceSwapSelectCooldown "0"  													',  # 減少手榴彈交換時間
    'sidearmSwapSelectCooldown "0"														',  # 減少物品左右交換時間
    'sidearmSwapSelectDoubleTapTime "0"													',  # 減少更換武器的時間
    'mat_depthfeather_enable "0"														',  # 禁用景深
    'hud_setting_adsDof "0"																',  # 禁用向下瞄準時景深
    'player_setting_damage_closes_deathbox_menu "0"                                     ',  # 關閉受到攻擊時死亡箱自動關閉
    'sprint_view_shake_style "1"                                                        ',  # Less headbob(不知道中文)
    'hud_setting_pingDoubleTapEnemy "1"                                                 ',  # 雙倍的標示敵人
    'fov_disableAbilityScaling "1"                                                      ',  # 關閉技能 fov 變化
    'net_netGraph2 "1"                                                                  ',  # 開啟性能展示
    'weapon_setting_autocycle_on_empty "1"                                              ',  # 武器自動循環
    
    # FPS優化 ========================================================================================

    'fps_max 240                                                                        ',  # 最大 fps
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
    'rope_smooth "0"                                                                    ',  # 跳過對繩索的長時間平滑操作
    'rope_collide "0"                                                                   ',  # 禁用繩索抖動
    'mat_postprocess_enable "0"                                                         ',  # 移除強制HDR
    'mat_dynamic_tonemapping "0"                                                        ',  # 禁用動態HDR色調映射
    'mat_hdr_level "0"                                                                  ',  # 禁用完全HDR
    'r_shadowmaxrendered "0"                                                            ',  # 遊戲將渲染的最大陰影 (不完全)
    'r_drawtracers_firstperson "0"                                                      ',  # 子彈上沒有追蹤器
    'mat_shadowstate "0"                                                                ',  # 無陰影(0)，玩家模型為陰影(2) (減少)
    'ssao_blur "0"                                                                      ',  # 模糊、反射和高光
    'mat_reducefillrate "1"                                                             ',  # 簡化材料陰影
    'cl_phys_maxticks "0"                                                               ',  # 允許的物理點的數量
    'cl_detailfade "0"                                                                  ',  # 細節道具淡入的距離
    'cl_detaildist "0"                                                                  ',  # 細節道具不再可見的距離
    'r_jiggle_bones "0"',
    'r_dxgi_max_frame_latency "1"',
    
    # 畫面效果設置 ====================================================================================
    
    'cl_gib_allow "0"                                                                   ',
	'cl_particle_fallback_base "0"                                                      ',
	'cl_particle_fallback_multiplier "0"                                                ',
	'cl_ragdoll_maxcount "0"                                                            ',
	'cl_ragdoll_self_collision "0"                                                      ',
	'mat_forceaniso "1"                                                                 ',
	'mat_mip_linear "0"                                                                 ',  # 紋理過濾 開(1)/關(0)
	'stream_memory "300000"                                                             ',  # 紋理記憶體
	'mat_picmip "0"                                                                     ',
	'particle_cpu_level "0"                                                             ',
	'r_createmodeldecals "0"                                                            ',
	'r_decals "0"                                                                       ',
	'r_lod_switch_scale "0.5"                                                           ',  # 模型的加載距離
	'shadow_enable "0"                                                                  ',  # 啟用陰影
	'shadow_depth_dimen_min "0"                                                         ',
	'shadow_depth_upres_factor_max "0"                                                  ',
	'shadow_maxdynamic "0"                                                              ',
	'ssao_enabled "0"                                                                   ',
	'ssao_downsample "3"                                                                ',
	'dvs_enable "0"                                                                     ',  # 啟用垂直同步
	'dvs_gpuframetime_min "0"                                                           ',
	'dvs_gpuframetime_max "0"                                                           ',
	'sound_volume "1"                                                                   ',
	'nowindowborder "1"                                                                 ',  # 無邊框窗口
	'fullscreen "0"                                                                     ',  # 全螢幕窗口
	'volumetric_lighting "0"                                                            ',
	'volumetric_fog "0"                                                                 ',
	'mat_vsync_mode "0"                                                                 ',
	'mat_backbuffer_count "1"                                                           ',
	'mat_antialias_mode "12"                                                            ',
	'csm_enabled "0"                                                                    ',  # 啟用地圖陰影
	'csm_coverage "0"                                                                   ',
	'csm_cascade_res "0"                                                                ',
	'fadeDistScale "1.000000"                                                           ',
	'dvs_supersample_enable "0"                                                         ',
	'new_shadow_settings "1"                                                            ',
	'gamma "1.000000"                                                                   ',
	'dx_version_check_timestamp "0"                                                     ',
	'set_dress_level "1"                                                                ',
    'configversion "8"                                                                  ',

    # 聲音特效=======================================================================================

    'miles_max_sounds_per_server_frame "1600"											',  # 服務器每偵聲音輸出上限
    'miles_channels "2"																	',  # 輸出雙聲道
    'sound_num_speakers "2"															    ',  # 喇叭雙聲道
    'snd_mixahead "0.03"																',  # 減少聲音延遲
    'snd_async_fullyasync "1"															',  # 聲音同步
    'sound_classic_music "0"															',  # 經典聲音音量
    'snd_musicvolume "0"																',  # 禁用不必要的聲音
    'sound_musicReduced "0"															    ',  # 遊戲BGM音量
    'voice_forcemicrecord "0"															',  # 錄音功能關閉
    'snd_headphone_pan_exponent "2"													    ',  # 使你面向的方向聲音會更清晰
    'snd_setmixer PlayerFootsteps vol "0.01"											',  # 自己腳步聲音量
    'snd_setmixer GlobalFootsteps vol "3"											    ',  # 別人腳步聲音量
    'cl_footstep_event_max_dist "5000" 												    ',  # 增加敵人腳步聲傳遞範圍
    'rope_wind_dist "5000"																',  # 增大敵人使用繩索的聲音
    'sound_volume_music_game "0.000000"												    ',  # 不知道
    'sound_volume_music_lobby "50.000000"												',  # 不知道
    'miles_occlusion "0"                                                                ',  # 以下為取消牆壁吸收音量(可能無效了)
    'miles_occlusion_force "0"',
    'miles_occlusion_partial "0"',
    'snd_mix_async "1"',
    'miles_nonactor_occlusion "0"',
    'miles_occlusion_server_sounds_per_frame "0"',

    # 光影效果=======================================================================================

    'mat_light_edit "0"																	',  # 地圖燈光照明
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
]

# ===================================================上面才是設定值,下面不用觀看=============================================================

from tkinter import filedialog
import configparser as config
import tkinter as tk
import threading
import os

""" Versions 1.3

[+] 功能代碼重構
[+] 多線程輸出加速

Todo - APEX-CFG設置程序 -

16 賽季適用

使用說明:

設置路徑到 Apex 資料夾下的 Cfg 資料夾
最多可設置兩個路徑 , 第一次設置完成後 , 就不會再跳出設置了
需要重新設置的 , 就將生成的[CFG_Set.ini]刪除掉 , 再次運行程式進行設置
"""

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
            threading.Thread(target=self.output, args=(self.path1,)).start()

            # ======== 判斷設置檔是否存在第二項位置 ========
            if self.path2.lower() != "null":
                # 輸出第二設置路徑
                threading.Thread(target=self.output, args=(self.path2,)).start()

            # 用於已有設置ini檔,運行成功的提示
            print('運行完畢')

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

        print('請選擇您的APEX資料夾, 內的CFG資料夾')
        self.path1 = filedialog.askdirectory()
        Cfg_File = os.path.join(self.path1,'autoexec.cfg')

        with open(Cfg_File, 'w') as cfg_file:
           cfg_file.write('\n')

        # 創建完後再將字串加入,方便寫入至設定ini檔保存
        self.path1 += self.filename
        self.set.set('set', 'path1', self.path1)

        # ========== 第二項設置詢問 ==========
        try:
            while True:
                self.path2 = input('是否需要設置第二個位置(Y/N):')

                if self.path2.lower() == 'y':

                    self.path2 = filedialog.askdirectory()
                    Cfg_File = os.path.join(self.path2, 'autoexec.cfg')

                    with open(Cfg_File, 'w') as cfg_file:
                        cfg_file.write('\n')

                    self.path2 += self.filename
                    self.set.set('set', 'path2', self.path2)
                    break

                elif self.path2.lower() == 'n':
                    self.path2 = "NULL"
                    break

                else:
                    print("輸入錯誤 , 請輸入 Y 或 N\n")
                    continue

            # 全部設置完就輸出第一路徑和第二路徑
            threading.Thread(target=self.output, args=(self.path1,)).start()
            threading.Thread(target=self.output, args=(self.path2,)).start()
            # 保存設置
            threading.Thread(target=self.save_settings).start()

            print('運行完畢')
        except:
            os.system('cls')
            print('運行錯誤,請重新運行\n')
            # 基本上不會有出錯的時候
            os.system("del /f /s /q CFG_Set.ini >nul 2>&1") #採用靜默刪除指令
            input('\n按任意鍵結束運行...')

    def output(self, path):
        # 讀取設置並輸出
        with open(path, 'w') as Auto:
            for out in CFG:Auto.write(f'{out.strip()}\n')

    def save_settings(self):
        with open("CFG_Set.ini", "w") as f:
            self.set.write(f, delimiter='')
        self.file.close()

if __name__ == "__main__":
    Automatic()