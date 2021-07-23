# Import modules
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import csv
from datetime import datetime

now = datetime.now()
csv_file_name = "freelance_register_" + now.strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
website_url = ""

# Main function
def parse_freelance_register():
    with open(csv_file_name, mode = 'w') as freelancer_file:
        header = ["index","last_name","first_name","description"]
        freelancer_writer = csv.writer(freelancer_file, delimiter = ';', quotechar = '"')
        freelancer_writer.writerow(header)

        index = 0
        print("index,last_name,first_name,description")
        for site in range(1,84): # Current number of pages on website
            # URL for website that will be scraped
            register_url = website_url + str(site) + "/"

            # Load website into variable
            try:
                uClient = uReq(register_url)
            except HTTPError:
                continue

            page_raw_html = uClient.read()
            uClient.close()

            # Html parsing
            page_soup = soup(page_raw_html, "html.parser")

            containers = page_soup.tbody

            tr_tags = containers.findAll("tr")

            for i in range(0,len(tr_tags)):
                freelancers = tr_tags[i]
                full_name = freelancers.find("td").find_next_sibling("td").text.strip()
                last_name = freelancers.find("td").find_next_sibling("td").find_next_sibling("td").text.strip()
                first_name = full_name.replace(last_name, "").strip()

                if not first_name:
                    first_name = last_name

                mylink = tr_tags[i].find("a")

                description_url = mylink.attrs['href']


                try:
                    udescClient = uReq(description_url)
                except HTTPError:
                    continue

                desc_raw_html = udescClient.read()
                udescClient.close()

                desc_page_soup = soup(desc_raw_html, "html.parser")

                try:
                    desc_page_soup.p.text
                    desc_containers = desc_page_soup.findAll("p")

                    paragraphs = []
                    for i in desc_containers:
                        paragraphs.append(i.text)

                    description = ' '.join(paragraphs).replace("\n", "")
                except AttributeError:
                    description = "NA"

                print(f"{index},{last_name},{first_name},{description}")

                freelancer_writer.writerow([index, last_name, first_name, description])
                index += 1

    freelancer_file.close()

parse_freelance_register()
