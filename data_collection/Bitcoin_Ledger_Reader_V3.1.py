import json
import os
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import threading
import tkinter as tk
from tkinter import *
from tkinter import messagebox


page_express = True
loop_express = True
show_num = 20
read_page_info = False


def check_web(string, sub_str):
    if string.find(sub_str) == -1:
        return False
    else:
        return True


def loop_start():
    global loop_express
    loop_express = True
    global page_express
    page_express = True


def loop_stop():
    global loop_express
    loop_express = False


def clear_frame():
    for widgets in toolbar.winfo_children():
        widgets.destroy()

def print_current_time():
    timenow = Label(window, text="Time : " + str(time.asctime(time.localtime(time.time()))) + "   ")
    timenow.place(x=500, y=80)


def print_recent(height_num_now, page_num_now):
    height = Label(window, text="Height : " + str(height_num_now) + "   ")
    height.place(x=500, y=40)
    page = Label(window, text="Page : " + str(page_num_now) + "   ")
    page.place(x=500, y=60)


def print_something(condition, flag=1):
    if flag == 1:
        label = Label(toolbar, text=condition, bg='green')
        label.pack()
    elif flag == 2:
        label = Label(toolbar, text=condition, bg='yellow')
        label.pack()
    else:
        label = Label(toolbar, text=condition, bg='red')
        label.pack()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()


def thread_it(func, *args):
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def visit_url(url_value, min_value, max_value, chrome_location, chromedriver_location):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.binary_location = chrome_location
    url_visit = webdriver.Chrome(executable_path=chromedriver_location, options=options)
    # time out
    url_visit.set_page_load_timeout(30)
    url_visit.set_script_timeout(30)

    url_visit.implicitly_wait(random.uniform(min_value, max_value))
    url_visit.minimize_window()

    global show_num
    flag_run = True
    i = 0
    while i < 5000:
        try:
            url_visit.get(url_value)
            break
        except:
            print_something("TRY TO VISIT WEB-----" + "TIME " + str(i+1) + "/5000", 2)
            print_current_time()
            show_num = show_num - 1
            if show_num == 0:
                clear_frame()
                show_num = 20
            time.sleep(10)
            i = i + 1
            if i == 10:
                flag_run = False

    if flag_run is True:
        html_info = url_visit.page_source
        time.sleep(random.uniform(min_value, max_value))  # 1, 2/  0.1 0.2/ 0.01 0.02
        url_visit.close()
        url_visit.quit() # need to be placed behind .close() otherwise ERROR
        return html_info
    else:
        url_visit.execute_script('window.stop()')
        return 0


def process_data():
    clear_frame()
    global show_num
    global page_express
    global read_page_info
    read_page_info = True

    total_block = int(entry1_total_block.get())
    final_block = int(entry2_final_block.get())

    chrome = entry4_chrome.get()
    chromedriver = entry5_chromedriver.get()
    route = entry6_route.get()

    minspeed = float(entry7_minspeed.get())
    maxspeed = float(entry8_maxspeed.get())
    sleep_time = int(entry9_sleeptime.get())

    for m in range(total_block, final_block - 1, -1):
        if loop_express is True:
            url_info = "https://chain.api.btc.com/v3/block/" + str(m) + "/tx?pagesize=50"
            html_content = visit_url(url_info, minspeed, maxspeed, chrome, chromedriver)
            if html_content == 0:
                print_something("WEB CONNECTION ERROR", 3)
                read_page_info = False
                break
            else:
                flag_visit_info = 0
                while flag_visit_info < 10:
                    if check_web(html_content, "Access denied") is True:
                        show_num = show_num - 1
                        print_something("WEB INFO BANNED WAITING " + str(sleep_time) + "s-----" + "Round " + str(
                            flag_visit_info + 1) + "/10", 2)
                        time.sleep(sleep_time)
                        flag_visit_info = flag_visit_info + 1
                        html_content = visit_url(url_info, minspeed, maxspeed, chrome, chromedriver)  # 2.5, 3.5/ 1, 2/ 0.1 0.2/ 0.01 0.02
                    else:
                        first_step = html_content.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '')
                        final_step = first_step.replace('</pre></body></html>', '')
                        try:
                            json_info_dict = json.loads(final_step)
                        except:
                            print_something("READ ERROR", 3)
                            break
                        page_num = json_info_dict["data"]["page_total"]

                        directory = route + str(m) + "/"
                        folder_create = os.path.exists(directory)
                        if folder_create is True:
                            print_something("The folder " + str(m) + " has existed, continue the process")
                            show_num = show_num - 1
                            if show_num == 0:
                                clear_frame()
                                show_num = 20
                            break
                        else:
                            os.makedirs(directory)
                            show_num = show_num - 1
                            if show_num == 0:
                                clear_frame()
                                show_num = 20
                            print_something(str(m) + " has been built")
                            break
        else:
            # print_something("LOOP ENDS", 3)
            break

        if page_express is True:
            page_now = int(entry3_page_now.get())
        else:
            page_now = 1

        if read_page_info is False:
            break
        else:
            for n in range(page_now, page_num + 1):
                if loop_express is True:
                    show_num = show_num - 1
                    if show_num == 0:
                        clear_frame()
                        show_num = 20
                    print_something("BLOCK HEIGHT: " + str(m) + "-----PAGE: " + str(n) + "/" + str(page_num))
                    print_current_time()

                    url = "https://chain.api.btc.com/v3/block/" + str(m) + "/tx?page=" + str(n) + "&pagesize=50"

                    url_content_ori = visit_url(url, minspeed, maxspeed, chrome,
                                                chromedriver)  # 2.5, 3.5/ 1, 2/ 0.1 0.2/ 0.01 0.02
                    if url_content_ori == 0:
                        print_something("WEB CONNECTION ERROR", 3)
                        break
                    else:
                        flag_visit = 0
                        while flag_visit < 10:
                            if check_web(url_content_ori, "Access denied") is True:
                                show_num = show_num - 1
                                print_something("WEB BANNED WAITING " + str(sleep_time) + "s-----" + "Round " + str(
                                    flag_visit + 1) + "/10", 2)
                                time.sleep(sleep_time)
                                flag_visit = flag_visit + 1
                                url_content_ori = visit_url(url, minspeed, maxspeed, chrome, chromedriver)  # 2.5, 3.5/ 1, 2/ 0.1 0.2/ 0.01 0.02
                            else:
                                first_step = url_content_ori.replace('<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">', '')
                                final_step = first_step.replace('</pre></body></html>', '')
                                try:
                                    json_dict = json.loads(final_step)
                                except:
                                    print_something("READ ERROR", 3)
                                    break
                                file = open(directory + str(page_num) + '_' + str(n) + '.json', 'w')
                                json.dump(json_dict, file)
                                file.close()
                                print_recent(m, n)
                                if page_num == n:
                                    page_express = False
                                break
                    sys.stdout.flush()
                else:
                    print_something("STOP", 3)
                    break


if __name__ == '__main__':
    window = tk.Tk()
    window.title('Bitcoin Transaction Reader V3.1')
    window.geometry('700x750')
    defaultbg = window.cget('bg')

    entry1_total_block = tk.Entry(window, width=40)
    entry2_final_block = tk.Entry(window, width=40)
    entry3_page_now = tk.Entry(window, width=40)
    entry4_chrome = tk.Entry(window, width=40)
    entry5_chromedriver = tk.Entry(window, width=40)
    entry6_route = tk.Entry(window, width=40)
    entry7_minspeed = tk.Entry(window, width=40)
    entry8_maxspeed = tk.Entry(window, width=40)
    entry9_sleeptime = tk.Entry(window, width=40)

    window_sign_up = window

    tk.Label(window_sign_up, text='Block Start: ').place(x=10, y=0)
    tk.Label(window_sign_up, text='Block End: ').place(x=10, y=21)
    tk.Label(window_sign_up, text='Page Now: ').place(x=10, y=42)
    tk.Label(window_sign_up, text='Chrome Location: ').place(x=10, y=63)
    tk.Label(window_sign_up, text='Chrome Driver Location: ').place(x=10, y=84)
    tk.Label(window_sign_up, text='Save Route: ').place(x=10, y=105)

    tk.Label(window_sign_up, text='Min Speed: ').place(x=10, y=126)
    tk.Label(window_sign_up, text='Max Speed: ').place(x=10, y=147)
    tk.Label(window_sign_up, text='Time Waiting (10 Rounds): ').place(x=10, y=168)

    frequency = tk.Button(window, text='Run', command=lambda: [loop_start(), thread_it(process_data)])  
    frequency.place(x=500, y=0)

    stop = Button(window, text="Stop", command=lambda: loop_stop())
    stop.place(x=550, y=0)

    entry1_total_block.pack()
    entry2_final_block.pack()
    entry3_page_now.pack()
    entry4_chrome.pack()
    entry5_chromedriver.pack()
    entry6_route.pack()
    entry7_minspeed.pack()
    entry8_maxspeed.pack()
    entry9_sleeptime.pack()

    toolbar = tk.Frame(bg=defaultbg, height=500, width=300)
    toolbar.place(x=200, y=200)

    window.protocol('WM_DELETE_WINDOW', on_closing)
    window.mainloop()
