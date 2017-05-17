from selenium import webdriver
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def chromePNG(url,tmpf):
    padding_right = 0
    padding_bottom = 0
    options = webdriver.ChromeOptions()
    
    options.add_argument('headless')
    options.add_argument('window-size=2000x2000')
    options.add_argument("start-maximized")
    options.add_argument("no-sandbox")
    
    driver = webdriver.Chrome(executable_path='/src/chromedriver_linux64/chromedriver',chrome_options=options)
    driver.get(url)

    element = driver.find_element_by_css_selector('svg')
    driver.save_screenshot(tmpf)
    location = element.location
    size = element.size
    
    im = Image.open(tmpf) # uses PIL library to open image in memory
    width, height = im.size
    
    left = int(location['x'])
    top = int(location['y'])
    right = int(location['x']) + min(int(size['width']),width) + padding_right
    bottom = int(location['y']) + min(int(size['height']),height) + padding_bottom
    
    
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(tmpf) # saves new cropped image
    
    driver.close()
    
    return True

def chromeSVG(url):
    options = webdriver.ChromeOptions()
    
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1200x1200')
    options.add_argument("no-sandbox")
    
    driver = webdriver.Chrome(executable_path='/src/chromedriver_linux64/chromedriver',chrome_options=options)
    driver.get(url)
    element = driver.find_element_by_css_selector('svg')
    source_code = element.get_attribute("outerHTML")
    
    driver.close()
    
    return source_code
    

