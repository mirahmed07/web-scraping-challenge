# dependencies and setup
from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=True)

def scrape():
    browser = init_browser()

    # ******************************************************************************************************************************
    # Scraping Mars News
    # *****************************************************************************************************************************
    
    MarsNews_url = 'https://mars.nasa.gov/news/'

    print("Scraping Mars News...")

    # visit the Mars News website
    browser.visit(MarsNews_url)
    time.sleep(1)

    # create HTML object
    html = browser.html

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # get the first <li> item under <ul> list of headlines: this contains the latest news title and paragraph text
    first_li = soup.find('li', class_='slide')

    # save the news title under the <div> tag with a class of 'content_title'
    news_title = first_li.find('div', class_='content_title').text
    
    # save the news date under the <div> tag with a class of 'list_date'
    news_date = first_li.find('div', class_='list_date').text

    # save the paragraph text under the <div> tag with a class of 'article_teaser_body'
    news_para = first_li.find('div', class_='article_teaser_body').text

    print("Mars News: Scraping Complete!")

    # *****************************************************************************************************************************
    # Scraping JPL Featured Image URL 
    # *****************************************************************************************************************************
    
    JPLimage_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    print("Scraping JPL Featured Space Image...")

    # visit the JPL Featured Space Image website
    browser.visit(JPLimage_url)
    time.sleep(1)

    # create HTML object
    html = browser.html

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # use splinter to click on the 'full image' button to retrieve a full-size jpg url
    browser.find_by_text(' FULL IMAGE').click()
    time.sleep(1)
    
    # get the html for the full featured image
    full_img_html = browser.html

    # parse HTML with BeautifulSoup
    full_img_soup = BeautifulSoup(full_img_html, 'html.parser')

    # find the src for img tag with class 'fancybox-image'
    header_img_url_partial = full_img_soup.find('img', class_='fancybox-image')['src']
    
    # creating the final URL for JPL featured image
    JPL_base_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space'
    featured_image_url = JPL_base_url + '/' + header_img_url_partial

    # getting the title of the deatured image
    featured_img_title = soup.find('h1',class_='media_feature_title').text
    

    print("JPL Featured Space Image: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Facts
    # *****************************************************************************************************************************
    
    MarsFacts_url = 'https://space-facts.com/mars/'

    print("Scraping Mars Facts...")

    # visit the Mars Facts website
    browser.visit(MarsFacts_url)
    time.sleep(1)

    # create HTML object
    html = browser.html

    # use Pandas to scrape table of facts
    table = pd.read_html(html)

    # use indexing to slice the table to a dataframe
    facts_df = table[0]
    facts_df.columns =['Description', 'Value']
    facts_df['Description'] = facts_df['Description'].str.replace(':', '')

    # convert the dataframe to a HTML table and pass parameters for styling
    html_table = facts_df.to_html(index=False, header=True, border=1, justify = 'left',classes="table table-striped table-bordered")

    print("Mars Facts: Scraping Complete!")

    # *****************************************************************************************************************************
    #  Scraping Mars Hemisphere images
    # *****************************************************************************************************************************
    
    MarsHemImage_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    print("Scraping Mars Hemisphere Images...")
    
    # visit the Mars Hemisphere website
    browser.visit(MarsHemImage_url)
    time.sleep(1)

    # create HTML object
    html = browser.html

    # parse HTML with BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # retrieve all the parent div tags for each hemisphere
    hemisphere_divs = soup.find_all('div', class_="item")

    # create an empty list to store the python dictionary
    hemisphere_image_data = []

    # loop through each div item to get hemisphere data
    for hemisphere in range(len(hemisphere_divs)):

        # use splinter's browser to click on each hemisphere's link in order to retrieve image data
        hem_link = browser.find_by_css("a.product-item h3")
        hem_link[hemisphere].click()
        time.sleep(1)
    
        # create a beautiful soup object with the image detail page's html
        img_detail_html = browser.html
        imagesoup = BeautifulSoup(img_detail_html, 'html.parser')
    
        # create the base url for the fullsize image link
        base_url = 'https://astrogeology.usgs.gov'
    
        # retrieve the full-res image url and save into a variable
        hem_url = imagesoup.find('img', class_="wide-image")['src']
    
        # complete the featured image url by adding the base url
        img_url = base_url + hem_url

        # retrieve the image title using the title class and save into variable
        img_title = browser.find_by_css('.title').text
    
        # add the key value pairs to python dictionary and append to the list
        hemisphere_image_data.append({"title": img_title, "img_url": img_url})
    
        # go back to the main page 
        browser.back()

    # Quit the browser after scraping
    browser.quit()

    print("Mars Hemisphere Images: Scraping Complete!")
    
    # *****************************************************************************************************************************
    #  Store all values in dictionary
    # *****************************************************************************************************************************

    scraped_data = {
        "news_title": news_title,
        "news_date": news_date,
        "news_para": news_para,
        "featured_image_title": featured_img_title,
        "featured_image_url": featured_image_url,
        "mars_fact_table": html_table, 
        "hemisphere_images": hemisphere_image_data
    }

    # Return results
    return scraped_data
