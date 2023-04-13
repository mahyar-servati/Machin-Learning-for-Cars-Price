import numpy as np
import re
# import requests
import selenium.webdriver as webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from unidecode import unidecode
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import tree

# city = input("please insert your city: ").lower()
city = "tehran"
# carname = input("please insert Car name: ")
carname = "پارس سال"
url = f"https://divar.ir/s/{city}/car"

def get_selenium():                           
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('headless')                        
    driver = webdriver.Chrome(chrome_options=options)
    return (driver)
browser = get_selenium()
browser.get(url)
search_box = browser.find_element(By.TAG_NAME, 'input')
search_box.send_keys(carname)
search_box.send_keys(Keys.ENTER)
browser.refresh()
htmlelement= browser.find_element(By.TAG_NAME,'html')
data=[]
for i in range(5):
    temp = browser.find_elements(By.CSS_SELECTOR, "div.kt-post-card__body")
    for d in temp:
        data.append((d.text).split("\n"))
    htmlelement.send_keys(Keys.END)
    time.sleep(10)
    htmlelement.send_keys(Keys.END)
    time.sleep(10)
browser.close()


data_en = np.zeros((len(data), 3))
for i in range(len(data)):
    try:
        mdl = re.findall("mdl\s+(\d+)", unidecode(data[i][0]))[0]
        if len(mdl) == 2 and mdl[0] == '0':
            data_en[i,0] = int('14' + mdl)
        elif len(mdl) == 3 and mdl[0] == '4':
            data_en[i,0] = int('1' + mdl)
        elif len(mdl) == 2 and mdl[0] != '0':
            data_en[i,0] = int('13' + mdl)
        # elif re.findall("(درحد)", data[i][0].replace(" ", "")) != [] :
            # data_en[i,0] = 1401
        else:
            data_en[i,0] = int(mdl)
    except:
        data_en[i,0] = float('nan')
    try:
        data_en[i,1] = int(re.findall("\d+", unidecode(data[i][1]).replace(',', ''))[0])
    except:
        data_en[i,1] = float('nan')
    try:
        data_en[i,2] = int(re.findall("\d+", unidecode(data[i][2]).replace(',', ''))[0])
    except:
        data_en[i,2] = float('nan')
    # data_en[i,4] = data[i][3]

df = pd.DataFrame(data_en, columns = ['Model','Km','Price'])
df.to_csv(path_or_buf=f"cars_{carname}.csv", sep=';', encoding='utf-8', index=False)

fig,ax = plt.subplots(1, figsize=(10,10))
ax = sns.pairplot(df[['Model', 'Km', 'Price']], kind='reg')
plt.show()
ax.figure.savefig(f"Cars_correlation_{carname}.png", bbox_inches = 'tight', dpi=300)

df2=df.dropna()
df2 = np.array(df2)
x = df2[:,0:2]
y = df2[:,2]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
new_model = int(input("inter your Car's Model in range 1380 to 1401: "))
new_km = int(input("inter your Car's km-age: "))

new_data = [[new_model, new_km]]
new_price = clf.predict(new_data)

print("your Car price is", int(new_price[0]), 'Tooman')