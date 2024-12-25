import os
from DrissionPage import ChromiumPage, ChromiumOptions


def set_driver(headless=False, browser_path=None):
    # 常见的Linux Chrome/Chromium浏览器路径
    default_paths = [
        '/usr/bin/google-chrome',  # Chrome默认路径
        '/usr/bin/chromium',  # Chromium默认路径
        '/usr/bin/chromium-browser',  # Ubuntu Chromium默认路径
        '/usr/bin/microsoft-edge'  # Edge默认路径
    ]

    # 如果未指定路径，则自动检测
    if not browser_path:
        for path in default_paths:
            if os.path.exists(path):
                browser_path = path
                break
        if not browser_path:
            raise FileNotFoundError("未找到可用的浏览器，请手动指定browser_path参数")

    co = ChromiumOptions().set_paths(browser_path=browser_path)

    # 检测是否为root用户
    is_root = os.geteuid() == 0
    if is_root:
        # root环境下启用沙盒模式
        co.set_argument('--no-sandbox')
        co.set_argument('--disable-dev-shm-usage')
    # 禁止所有弹出窗口
    co.set_pref(arg='profile.default_content_settings.popups', value='0')
    # 隐藏是否保存密码的提示
    co.set_pref('credentials_enable_service', False)
    # 阻止“要恢复页面吗？Chrome未正确关闭”的提示气泡
    co.set_argument('--hide-crash-restore-bubble')
    # co.set_proxy('127.0.0.1:10809')        #设置代理
    co.headless(headless)
    co.set_user_agent(
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.92 Safari/537.36')
    co.new_env()
    plugin_path = r"cf/turnstilePatch"  # 插件文件夹路径
    co.add_extension(f"{plugin_path}")
    co.add_extension(r"zhiwen")
    driver = ChromiumPage(co)
    return driver

def deletecookie(driver):
    try:
        privacy_url = "chrome://settings/clearBrowserData"
        driver.get(privacy_url)
        driver.wait.eles_loaded('css:body > settings-ui')
        try:
            outer = driver.ele('css:body > settings-ui')
            sr = outer.shadow_root
            outer_2 = sr.ele('css:#main')
            sr_2 = outer_2.shadow_root
            outer_3 = sr_2.ele('css:settings-basic-page')
            sr_3 = outer_3.shadow_root
            outer_4 = sr_3.ele('x://*[@id="basicPage"]/settings-section[5]/settings-privacy-page')
            sr_4 = outer_4.shadow_root
            outer_5 = sr_4.ele('css:settings-clear-browsing-data-dialog')
            sr_5 = outer_5.shadow_root
            time_2 = sr_5.ele('css:#clearFromBasic')
            tsr_2 = time_2.shadow_root
            time_option = tsr_2.ele('css:#dropdownMenu')
        except Exception as e:
            return False, f"元素定位失败: {str(e)}"

        try:
            time_option.select.by_value(value=4)
            print("已选择时间不限")
        except Exception as e:
            return False, f"选择时间范围失败: {str(e)}"

        time.sleep(1)

        try:
            delete_bnt = sr_5.ele('x://*[@id="clearButton"]')
            delete_bnt.click()
            print("已清除cookie")
        except Exception as e:
            return False, f"点击清除按钮失败: {str(e)}"

        return True, "成功清除cookie"

    except Exception as e:
        error_msg = f"清除cookie时发生错误: {str(e)}"
        print(error_msg)
        return False

driver = set_driver()
deletecookie(driver)
driver.get('https://nc.me')
