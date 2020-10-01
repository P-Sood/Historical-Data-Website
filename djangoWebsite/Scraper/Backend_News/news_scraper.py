from newsplease import NewsPlease
import csv

# article_input_list = input("Please provide the path/name of media cloud article list:")
article_input_list = "data/wexit-all-story-urls-20200209163715.csv"

with open(article_input_list, mode='r', encoding='utf-8-sig') as media_cloud_input:
    reader = csv.reader(media_cloud_input)
    header = next(reader)
    media_dict = [dict(zip(header, map(str, row))) for row in reader]

# article_dump_dir = input("Please provide the name of the text dump directory:")
article_dump_dir = "data/test/"

#NewsPlease class attributes:
#            'authors': self.authors,
#            'date_download': self.date_download,
#            'date_modify': self.date_modify,
#            'date_publish': self.date_publish,
#            'description': self.description,
#            'filename': self.filename,
#            'image_url': self.image_url,
#            'language': self.language,
#            'localpath': self.localpath,
#            'maintext': self.text,
#            'source_domain': self.source_domain,
#            'text': self.text,
#            'title': self.title,
#            'title_page': self.title_page,
#            'title_rss': self.title_rss,
#            'url': self.url

error_count = 0
success_count = 0
error_list = []


for each_article in media_dict:
    # Hedayat Tabesh - 05/25/2020 - for testing
    # each_article['source_url'] = "https://www.ctvnews.ca/video?clipId=1789397"
    # each_article['source_stories_id'] = "1394136523"

    article_file_name = ""
    # Hedayat Tabesh - 05/25/2020 - run up to 10 times if "Read timed out" error.
    for Err_i in range(10):
        try:
            print(each_article)
            print ('id: ',each_article['source_stories_id'],' | url: ',each_article['source_url'])
            article = NewsPlease.from_url(each_article['source_url'],10)
            
        except Exception as err:
            print(type(err))
            if "Read timed out." in str(err):
                continue
            print('Error reading article number:',each_article['source_stories_id'], ' ||| --> Error code:',err)
            error_count += 1
            article_error = {}
            article_error['source_stories_id'] = each_article['source_stories_id']
            article_error['source_url'] = each_article['source_url']
            article_error['error_message']  = err
            error_list.append(article_error)
            break
        else:
            article_file_name = article_dump_dir+each_article['source_stories_id']+'.txt'
            break
     
    if article_file_name == "":
        continue

    # Hedayat Tabesh - 06/03/2020 - catch error when API fails to get main text
    if article.maintext is None:
        error_count += 1
        article_error = {}
        article_error['source_stories_id'] = each_article['source_stories_id']
        article_error['source_url'] = each_article['source_url']
        article_error['error_message']  = "Main text contained NONE type"
        error_list.append(article_error)
        continue

    with open(article_file_name, mode='w', newline='') as text_f:
        text_f.write("Title: %s\n" %article.title)
        # text_f.write("Title Page: %s\n" %article.title_page)
        text_f.write("Date Published: %s\n" %article.date_publish)
        text_f.write("Source domain: %s\n" %article.source_domain)
        text_f.write("URL: %s\n" %article.url)
        # Hedayat Tabesh - 05/25/2020 - adding an extra line to make more readable 
        text_f.write("Description: %s\n\n" %article.description)
        # Hedayat Tabesh - 05/25/2020 - adding an extra space at the start of each paragraph and removing "READ MORE" lines
        Main_Text = ""
        for line in article.maintext.splitlines():
            if line[:9] == "READ MORE":
                continue
            Word_count = len(line.split()) 
            if Word_count < 5:
                line = "/// "+line
            Main_Text = Main_Text + line + "\n\n"            
            
        text_f.write("Main Text: %s\n" %Main_Text)
        success_count += 1

print('---------------------------------------------------------')
print('Number of articles in error:',error_count)
print('Number of articles extracted with success:',success_count)

if error_count > 0:
    #create log file
    error_file = article_dump_dir + 'error_log.csv'

    with open(error_file, mode='w',   newline='') as   edges:
    
        writer = csv.writer(edges)
        writer.writerow(['source_stories_id','source_url'])
    
        for each_article in error_list:        
            writer.writerow([each_article['source_stories_id'],each_article['source_url'], each_article['error_message']])

        print('---------------------------------------------------------')
        print('Error log generated at:',error_file)