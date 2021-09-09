import os
import requests  # conda or pip install requests #to sent GET requests on google
from bs4 import BeautifulSoup # conda or pip install bs4 #to parse html(getting data out from html, xml or other markup languages)

"""
user can input a search keyword and the count of images required
download images from google search image
"""

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

"""
The User-Agent request header contains a characteristic string
that allows the network protocol peers to identify the application type,
operating system, and software version of the requesting software user agent.
needed for google search
it is found by typing 'my user agent' in a google browser's search box to get your browser user agent details
and replace it in the code below. Leave the rest of code intact/unchanged.
"""
u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

Image_Folder = 'bears'  # creating the main folder and name it appropriately


def main():
    if not os.path.exists(Image_Folder):
        os.mkdir(Image_Folder)
    download_images()

def download_images():
    # Creating a list of our search keywords
    datas = []
    while True:
        data = input('Enter your search keyword and q to quite: ')
        if data == 'q':
            break
        datas.append(data)

    # Capture the number of images for each keyword search
    num_images = int(input('Enter the number of images you are searching for each keyword search: '))

    print(f'Searching Images for . . . {datas} \n')  # prints a list of all keyword search

    for data in datas:
        search_url = Google_Image + 'q=' + data  # adding 'q=' to url because its a query

        # request url, without u_agnt the permission gets denied
        response = requests.get(search_url, headers=u_agnt)
        html = response.text  # To get actual result i.e. to read the html data in text mode

        # find all img where class='rg_i Q4LuWd'
        b_soup = BeautifulSoup(html, 'html.parser')  # html.parser is used to parse/extract features from HTML files
        results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})

        # extract the links of requested number of images with 'data-src' attribute and appended those links to a list 'imagelinks'
        # allow to continue the loop in case query fails for non-data-src attributes

        count = 0
        imagelinks = []
        for res in results:
            try:
                link = res['data-src']
                imagelinks.append(link)
                count = count + 1
                if (count >= num_images):
                    break

            except KeyError:
                continue

        print(f'Found {len(imagelinks)} images of ' + data)

        # Downloading images
        print(f'Start downloading images of ' + data + ' ...')

        # Creating a subfolder in the main folder
        Image_Subfolder = data
        if not os.path.exists(os.path.join(Image_Folder, Image_Subfolder)):
            os.mkdir(os.path.join(Image_Folder, Image_Subfolder))

        for i, imagelink in enumerate(imagelinks):
            # open each image link and save the file
            response = requests.get(imagelink)
            imagename = Image_Folder + '/' + Image_Subfolder + '/' + data + str(i + 1) + '.jpg'
            with open(imagename, 'wb') as file:
                file.write(response.content)

        print(f'Downloading ' + data + ' is completed!\n')


if __name__ == '__main__':
    main()
