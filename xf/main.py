import re
import time
import pyperclip
from PIL import Image, ImageGrab
import os
from WebITRTeach import get_result
import ctypes
 
def start():
    window_handle = ctypes.windll.kernel32.GetConsoleWindow()
    # 0：隐藏；6：最小化
    # 1：显示；3：最大化
    ctypes.windll.user32.ShowWindow(window_handle, 0)
    time.sleep(0.5)
    os.system('RUNDLL32.EXE PrScrn.dll PrScrn')
    ctypes.windll.user32.ShowWindow(window_handle, 1)
    img = ImageGrab.grabclipboard()
    if not isinstance(img, Image.Image):
        return
    print('>> 识别中...')
    image_path = "1.png"
    img.save(image_path)
    recognition = get_result()
    res = recognition.call_url(image_path)
    os.remove(image_path)
    if res['code'] != 0:
        return
    content = res['data']['region'][0]['recog']['content']
    content = re.sub(r'ifly-latex-begin', '', content)
    content = re.sub(r'ifly-latex-end', '', content)
    # 将结果复制到剪切板
    pyperclip.copy(content)
    print(content)
 
if __name__ == '__main__':
    while True:
        if input('>> 按回车启动，按q退出: ').strip().lower() == 'q':
            break
        print('>> 启动中...')
        try:
            start()
        except Exception as e:
            print(e)