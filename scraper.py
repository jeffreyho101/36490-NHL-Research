# Import your newly installed selenium package
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import json
import numpy as np
import csv
import time

# -*- coding: utf-8 -*-

# Now create an 'instance' of your driver
# This path should be to wherever you downloaded the driver
driver = webdriver.Chrome(executable_path="/Users/Jeffrey/Desktop/chromedriver")
# A new Chrome (or other browser) window should open up

# Now just tell it wherever you want it to go

teams_links = ['boston-bruins', 'buffalo-sabres', 'detroit-red-wings', 'florida-panthers', 'montreal-canadiens', 'ottawa-senators', 'tampa-bay-lightning', 'toronto-maple-leafs', 'carolina-hurricanes', 'columbus-blue-jackets', 'new-jersey-devils','new-york-rangers','new-york-islanders','philadelphia-flyers','pittsburgh-penguins','washington-capitals','chicago-blackhawks', 'colorado-avalanche', 'dallas-stars','minnesota-wild','nashville-predators', 'st-louis-blues', 'winnipeg-jets','anaheim-ducks','arizona-coyotes', 'calgary-flames','edmonton-oilers','los-angeles-kings','san-jose-sharks','vancouver-canucks','vegas-golden-knights']

file_names = ['Bruins-Data', 'Sabres-Data','RedWings-Data', 'Panthers-Data','Canadiens-Data','Senators-Data', 'Lightning-Data','MapleLeafs-Data',	'Hurricanes-Data',		'BlueJackets-Data','Devils-Data',	'Rangers-Data',	'Islanders-Data',		'Flyers-Data','Penguins-Data', 'Capitals-Data','Blackhawks-Data', 'Avalanche-Data',					'Stars-Data','Wild-Data',		'Predators-Data', 'Blues-Data',
  'Jets-Data',		'Ducks-Data',		'Coyotes-Data',				'Flames-Data',
  		'Oilers-Data',	      'Kings-Data',		'Sharks-Data',  'Canucks-Data',	'GoldenKnights-Data']

# for count in range(0, len(teams_links)):
# missing 5,link
# for count in range(5, len(teams_links)):
for link in range(0, len(teams_links)):
    url = "https://www.tsn.ca/nhl/team/" + teams_links[link] + "/roster"
    driver.get(url)

    language_element = driver.find_elements(By.CLASS_NAME, 'stick')

    languages = [x.text for x in language_element]
    names = languages[1:len(languages)]
    names_regex = []
    # get everythinb before second comma
    regex = '^(.+?),'
    for i in range(0,len(names)):
    # for i in range(0,6):
        names_regex.append(names[i].split(",")[0])
    # print("names:")
    # print(names_regex,'\n')
    for player_name in range(0, len(names_regex)):
        if(driver.find_element_by_link_text(names_regex[player_name]).is_enabled()):
            driver.find_element_by_link_text(names_regex[player_name]).click()
            time.sleep(2)
        else:
            continue
        if(driver.find_element_by_xpath("(//a[contains(@href,'player-bio')])[2]").is_enabled()):
            driver.find_element_by_xpath("(//a[contains(@href,'player-bio')])[2]").click()
            time.sleep(2)
        else:
            driver.back()
            continue

        pre = driver.find_element_by_class_name("transactions").text

        data = json.dumps(pre)
        data = data[1:len(data) - 1]
        entries = data.split('\\n')
        arr = []

        for a in range(0, len(entries)):
            arr.append(entries[a][0:12])
            arr.append(entries[a][13:len(entries[a])])

        arr2 = np.asarray(arr)
        arr2 = np.reshape(arr2, (len(arr2) / 2, 2))

        firstname = driver.find_element_by_class_name("first-name").text
        lastname = driver.find_element_by_class_name("last-name").text
        firstname = firstname.encode('ascii', 'ignore')
        lastname = lastname.encode('ascii', 'ignore')
        cityname = teams_links[link].split("-")[0].upper()
        teamname = teams_links[link].split("-")[1:]
        teamname = ''.join(teamname).upper()

        arr_edit = arr2.tolist()

        arr_edit = [x + [firstname, lastname, cityname, teamname] for x in arr_edit]

        arr_edit.insert(0, ["Date", "Injury", "Firstname", "Lastname", "City", "TeamName"])
        filepath = "Player-Data/" + file_names[link] + "/"+ lastname.lower() + ".csv"
        with open(filepath, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(arr_edit)
        driver.back()
        driver.back()
        time.sleep(3)
    driver.back()
# print firstname, lastname
# print arr_edit_last

# print(L)

# print (arr2.tolist())

# close driver
driver.close()
