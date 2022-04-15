
import os
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
def etsy_product_details(product_link):
   """
   Fetch all data from a specific website
   """
   """define all variables"""
   date_time = str(datetime.now())
   stock= "X"
   author_and_title= ""
   shipping_time=""
   product_price=""
   product_desc=""
   store=""
   created=""
   country_of_origin=""
   image_link=""
   options=[]
   categories=[]
   """make the request"""
   site= requests.request('GET', product_link)
   site_soup= BeautifulSoup(site.text, "lxml")
   try:
      in_stock = site_soup.find_all("div", class_= "wt-display-flex-xs wt-align-items-center wt-justify-content-space-between")
      for items in in_stock:
         for item in items.find_all('p', class_= "wt-text-caption"):
            if item.strong is not None:
               stock=""
      author_and_title = site_soup.find("h1", class_= "wt-text-body-03").text.strip()
      shipping_time= site_soup.find("p", class_="wt-text-body-03").text.strip()
      product_price = site_soup.find("p",class_="wt-text-title-03")
      try:
         product_price.span
         product_price.span.decompose()
      except:
         pass
      product_price= product_price.text.strip()
      description= site_soup.find_all("div",id= "wt-content-toggle-product-details-read-more")
      for element in description:
         product_desc= element.p.text.strip()
      store= site_soup.find("p", class_= "wt-text-body-01 wt-mr-xs-1").a['href']
      created = site_soup.find("div",class_="wt-pr-xs-2 wt-text-caption").text.strip()
      country_of_origin = site_soup.find("div", class_="wt-grid__item-xs-12 wt-text-black wt-text-caption")\
                                          .text.strip()
      image_link = site_soup.find('img', class_= "wt-max-width-full")['src']
      """
      All options
      """
      all_options = site_soup.find('div', class_= "wt-select")
      for select_options in all_options.find_all('select', class_= "wt-select__element"):
         for option in select_options.find_all('option'):
            options.append(option.text.strip())
      """
      find all categories
      """
      all_categories = site_soup.find_all('ul', class_='wt-action-group wt-list-inline wt-mb-xs-2')
      for all_category in all_categories:
         for list_category in all_category.find_all('li',class_='wt-action-group__item-container'):
            for category in list_category.find_all('a'):
               categories.append(category.text.strip())
      print("\n",product_link, "All data fetched")
   except:
      print("\n", product_link, "This product is out of stock now")
   """
   Write in csv file 
   """
   file_name=f"etsy_output_file-{datetime.now():%Y-%m-%d %H-%m}.csv"
   with open(file_name, 'a', encoding='utf-8') as file_data:
      etsy_product_writer= csv.DictWriter(file_data,fieldnames=[
         'product_link','in_stock','author_and_title','shipping_time','product_price',
         'description','store','created','country_of_origin','image_link','options','categories'
      ])
      if os.stat(file_name).st_size == 0:
         etsy_product_writer.writeheader()
      etsy_product_writer.writerow({
         'product_link':product_link,'in_stock':stock,'author_and_title':author_and_title,'shipping_time':shipping_time,'product_price':product_price,'description':product_desc,'store':store,'created':created,'country_of_origin':country_of_origin,'image_link':image_link,'options':options,'categories':categories
      })

def main():
   """
   Fetch all the websites from the csv file
   """
   with open('etsy_input_file.csv', 'r') as data_file:
      for product_link in data_file:
         etsy_product_details(product_link)
   print("\nAll product link's data has been fetched successfully!")
main()
