import requests
from bs4 import BeautifulSoup
import json
import csv

# url = "https://www.calories.info/"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36 Edg/148.0.0.0"
}
# req = requests.get(url, headers=headers)
# src = req.text
# print(src)

# with open("index.html", "w", encoding="utf-8") as file:
#     file.write(src)

# with open("index.html", encoding="utf-8") as file:
#     src= file.read()

# soup = BeautifulSoup(src, "lxml")
# all_products_hrefs = soup.find_all(class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineNone MuiPaper-root MuiPaper-elevation MuiPaper-rounded MuiPaper-elevation0 MuiCard-root css-u833vp")
# all_categories_dict ={}


# for item in all_products_hrefs:
#     h3_tag = item.find("h3")
#     item_text = " ".join(h3_tag.text.split())
#     item_href = "https://www.calories.info/" + item.get("href")
#     print(f"{item_text}: {item_href}")
#     print("-" * 40)

#     all_categories_dict[item_text] = item_href

'''Save all as JSON file'''
# with open("all_categories_dict.json", "w") as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

with open("all_categories_dict.json") as file:
    all_categories = json.load(file)

iteration_count = (int(len(all_categories)))-1
print(f"Total iterations: {iteration_count}")
count  = 0

for category_name, category_href in all_categories.items():
    
    
            rep = ['.', ' ', '-', "'",'"', '&']
            for item in rep:
                if item in category_name:
                    category_name = category_name.replace(item,"_")
            
            req = requests.get(url=category_href, headers=headers)
            src = req.text

            with open(f"calorieparser/data/{count}{category_name}.html", "w", encoding="utf-8") as file:
                file.write(src)

            with open(f"calorieparser/data/{count}{category_name}.html", encoding="utf-8") as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')


            #CHECK FOR TABLE
            table = soup.find(class_="MuiTable-root css-1ryxeon")
            if table is None:
                print(f"[-] WARNING!! NO TABLE AT{category_name}! Skipping it.")
                count += 1
                continue
            tbody = table.find("tbody")
            if not tbody:
                print(f"[-] WARNING!! {category_name} NO TBODY ELEMENT <tbody>. Skipping.")
                count += 1
                continue
            products_data = tbody.find_all("tr")
            if len(products_data) == 0:
                print(f"[-] WARNING!! {category_name} IS EMPTY (NO <tr>).")
                count += 1
                continue
            print(f"[+] Cool! Найдено строк для парсинга: {len(products_data)}")




            #collecting all headers
            table_head= soup.find(class_="MuiTable-root css-1ryxeon").find("tr").find_all("th")
            product = table_head[0].text
            serving = table_head[1].text
            calories = table_head[2].text

            
            with open(f"calorieparser/data/{count}{category_name}.csv", 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        serving,
                        calories
                    )
                )


            #collecting product data
            products_data = soup.find(class_="MuiTable-root css-1ryxeon").find("tbody").find_all("tr")

            product_info = []
            
            for item in products_data:
                products_tds = item.find_all("td")

                #anti-ad
                if len(products_tds) < 3:
                    continue

                a_tag = products_tds[0].find("a")
                title = a_tag.text if a_tag else products_tds[0].text
                serving = products_tds[1].text
                calories = products_tds[2].text

                product_info.append(
                     {
                        "Title": title,
                        "Serving": serving,
                        "Calories": calories
                     }
                )

                with open(f"calorieparser/data/{count}{category_name}.csv", 'a', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            title,
                            serving,
                            calories
                        )
                    )
            with open(f"calorieparser/data/{count}{category_name}.json", "w", encoding="utf-8") as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)
            
            count+=1
            print(f"# Iteration {count}. {category_name} is done!")
            iteration_count-=1
            
            if iteration_count == 0:
                print("All iterations are done! Check the data folder for results.")
                break

            print(f"Remaining iterations: {iteration_count}")

            