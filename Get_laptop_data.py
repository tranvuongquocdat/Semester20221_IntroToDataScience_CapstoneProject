from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import csv

class laptop:
    def __init__(self, name, cpu, ram, monitor, gpu, memory, battery, connection, weight, price):
        self.name = name
        self.cpu = cpu
        self.ram = ram
        self.monitor = monitor
        self.gpu = gpu
        self.memory = memory
        self.battery = battery
        self.connection = connection
        self.weight = weight
        self.price = price

class replace_option:
    def __init__(self):
        self.text = "0"

class replace_battery:
    def __init__(self):
        self.text = "10WHr"


def get_laptop_link():
    #Find path with class name = "col-span-3" and 'col-span-2
    laptop_link_3 = browser.find_elements(By.CLASS_NAME, "col-span-3")
    laptop_link_2 = browser.find_elements(By.CLASS_NAME, "col-span-2")
    laptop_links = laptop_link_2 + laptop_link_3
    return laptop_links


def next_page():
    Trang_tiep = browser.find_element(By.CLASS_NAME, "t-pagination__left")
    Trang_tiep.click()

def get_laptop_infor():
    name = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > aside > div > div > div.t-scroll-bar.flex-1.overflow-auto.p-4 > div > div.flex.flex-col.space-y-3 > div.flex.flex-col > h2")
    cpu = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(1) > div:nth-child(1) > div > div:nth-child(2)")
    ram = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(2)")
    monitor = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(2) > div:nth-child(1) > div > div:nth-child(2)")
    gpu = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(2) > div:nth-child(2) > div > div:nth-child(2)")
    memory = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(3) > div:nth-child(1) > div > div:nth-child(2)")
    try:
        battery = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div.container.pt-4 > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(3) > div:nth-child(2) > div > div:nth-child(2)")
    except:
        battery = replace_battery()
    connection = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(4) > div:nth-child(1) > div > div:nth-child(2)")
    try:
        weight = browser.find_element(By.CSS_SELECTOR, "#__layout > div > main > div > section > div > section > section.section-characteristic > div.mt-8 > div.flex.flex-col.space-y-3 > div:nth-child(4) > div:nth-child(2) > div > div:nth-child(2)")
    except:
        weight = replace_option()

    price = browser.find_element(By.CSS_SELECTOR,"#__layout > div > main > div.container.pt-4 > section > aside > div > div > div.t-scroll-bar.flex-1.overflow-auto.p-4 > div > div.flex.flex-col.space-y-3 > div.flex.flex-col > div.mt-1.flex.items-center > span")
    return name.text, cpu.text, ram.text, monitor.text, gpu.text, memory.text, battery.text, connection.text, weight.text, price.text

if __name__ == "__main__":
    #open file to write laptop infor
    f = open("laptop_infor.csv", "w", newline= "", encoding= "utf-8")
    writer = csv.writer(f)
    name_column = ["name", "cpu", "ram", "monitor", "gpu", "memory", "battery", "connection", "weight", "price"]
    writer.writerow(name_column)

    #Declare browser variable
    browser = webdriver.Chrome(executable_path = "chromedriver.exe")

    #Open the website
    browser.get("https://thinkpro.vn/laptop/?f_price=7000000_null&p_sort=1")

    #Stop the program 3 seconds
    sleep(3)

    count = 0
    laptop_list = []
    #Get laptop links
    for i in range(1, 26):
        j = 0
        print("Page: ", i)
        #Get laptop data
        while True:
            count += 1
            laptop_links = get_laptop_link()
            laptop_links[j].click()
            sleep(3)
            browser.get(browser.current_url)
            sleep(3)

            name, cpu, ram, monitor, gpu, memory, battery, connection, weight, price = get_laptop_infor()
            print("laptop ", count)
            print("name: ", name,
            "\ncpu: ", cpu,
            "\nram: ", ram,
            "\nmonitor: ", monitor,
            "\ngpu: ", gpu,
            "\nmemory: ", memory,
            "\nbattery: ", battery,
            "\nweight: ", weight,
            "\nprice: ", price)
            laptop_tmp = laptop(name, cpu, ram, monitor, gpu, memory, battery, connection, weight, price)
            laptop_list.append(laptop_tmp)
            in4 = [name, cpu, ram, monitor, gpu, memory, battery, connection, weight, price]
            writer.writerow(in4)

            #back to previous page
            #browser.back()
            browser.execute_script("window.history.go(-1)")
            sleep(3)
            browser.get(browser.current_url)
            sleep(3)
            j += 1
            if j == len(laptop_links):
                break



        #Load to next page
        if i != 25:
            next_page()
            sleep(2)
            browser.get(browser.current_url)
            sleep(2)

    print("Done")
    print(laptop_list)
    f.close()

    #Close the browser
    exit()
