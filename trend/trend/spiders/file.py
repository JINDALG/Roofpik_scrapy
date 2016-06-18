import csv
with open('query_data.csv','wb') as csvfile:
    fieldnames = ['url','p','a','span','h1','h2','h3','h4','h5','h6','title','meta','li','img','th','td']
    writer = csv.DictWriter(csvfile, fieldnames)
    writer.writeheader()