
import pandas as pd

import time

from webdriver import Browser
import util

KEYWORD = "explore"
NUM_OF_POSTS = 100000

'''
Website Notes:
 - The search query is the keyword
 - 20 posts are loaded per scroll
 - Thumbnails provide:
    - Title
    - views
    - date posted
    - channel name
    - channel url
    - video url
    - video duration
    - video description 
    - video tags

- Videos provide:
    - video tags
    - video title
    - video views
    - date posted
    - video description
    - # of likes
    - channel name
    - channel url
    - # of subscribers
    - # of comments
    - Comments:
        - channel name
        - channel url
        - time posted ago
        - comment text
        - number of likes  
        - number of replies
        - replies --> comments of comment
    - Related video thumbnails:
        - Video title
        - video url
        - Channel name
        - video views
        - time posted ago
# '''

def parse_thumbnails(thumbnail_text):
    thumbnail_text = thumbnail_text.split('\n')

    if KEYWORD == 'explore':
        base = 0

        if thumbnail_text[2] == '•':
            base = 1

        thumbnail_data = {
            'title': thumbnail_text[0],
            'views': 0 if thumbnail_text[base + 2] == "No views" else util.format_big_num(thumbnail_text[base + 2].split(' ')[0]),
            'date_posted': thumbnail_text[base + 3],
            'channel_name': thumbnail_text[1]
        }
    else:
        thumbnail_data= {
            'title': thumbnail_text[0],
            'views': 0 if thumbnail_text[1] == "No views" else util.format_big_num(thumbnail_text[1].split(' ')[0]),
            'date_posted': thumbnail_text[2],
            'channel_name': thumbnail_text[3]
        }

    if len(thumbnail_text) > 4:
        thumbnail_data['description'] = thumbnail_text[4]
    else:
        thumbnail_data['description'] = ''

    return thumbnail_data

def export_post_data(post_data):
    pd.DataFrame(post_data).to_csv(f'output/youtube/top_viewed/{KEYWORD}.csv', index=False)


if __name__ == '__main__':

    browser = Browser()
    # url =f'https://www.youtube.com/results?search_query={KEYWORD}&sp=CAM%253D'
    # url = 'https://www.youtube.com/feed/explore'
    url = 'https://www.youtube.com/'

    current_section = 0
    posts = []

    browser.load_page(url)

    while len(posts) < NUM_OF_POSTS:

        try:

            print(f'Section: {current_section}')
            # section = browser.get_elements_by_css(f'ytd-item-section-renderer.ytd-section-list-renderer')[current_section]
            videos = browser.get_elements_by_css('div.text-wrapper.ytd-video-renderer')
            
            # for i in range(min(len(videos), NUM_OF_POSTS - len(posts))):
            for i in range(len(posts), len(videos)):
                video = videos[i]
                posts.append(parse_thumbnails(video.text))
                print(len(posts))
                time.sleep(0.05)

            if len(posts) < NUM_OF_POSTS:
                browser.scroll_down(10)
                current_section += 1
                time.sleep(2)

        except:
            break
    
    export_post_data(posts)
    browser.quit()


