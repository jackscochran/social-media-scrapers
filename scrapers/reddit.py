from webdriver import Browser
import util

import pandas as pd

import time

KEYWORD = "personal%20training"
NUM_OF_POSTS = 100000

PAGE = 'search_page'
SORT = 'new'

ELEMENT_SELECTOR = {
    'forum_page':{
        'url': f'https://www.reddit.com/r/{KEYWORD}/{SORT}/?t=all',
        'upvotes': 'div[id*=vote-arrows]',
        'date': 'span[data-testid=post_timestamp]',
        'author': 'a[data-testid=post_author_link]',
        'comments': 'a[data-test-id=comments-page-link-num-comments]',
    },
    'search_page':{
        'url': f'https://www.reddit.com/search/?q={KEYWORD}&sort={SORT}&t=all',
        'upvotes': 'span._vaFo96phV6L5Hltvwcox',
        'date': 'span[data-testid=post_timestamp]',
        'author': 'a[data-testid=post_author_link]',
        'comments': 'span._vaFo96phV6L5Hltvwcox',
    },
    'home_page':{
        'url': f'https://www.reddit.com/{SORT}/?t=all',
        'upvotes': 'div[id*=vote-arrows]',
        'date': 'span[data-testid=post_timestamp]',
        'author': 'a[data-testid=post_author_link]',
        'comments': 'a[data-test-id=comments-page-link-num-comments]',

    }
}

def parse_post(browser, post_element):

    title = "N/A"
    author = browser.get_element_text(browser.get_sub_element_by_css(post_element, ELEMENT_SELECTOR[PAGE]['author']))
    date = browser.get_element_text(browser.get_sub_element_by_css(post_element, ELEMENT_SELECTOR[PAGE]['date']))

    if PAGE == 'forum_page' or PAGE == 'home_page':
        upvotes = browser.get_element_text(browser.get_sub_element_by_css(post_element, ELEMENT_SELECTOR[PAGE]['upvotes']))
        comments = browser.get_element_text(browser.get_sub_element_by_css(post_element, ELEMENT_SELECTOR[PAGE]['comments']))
    elif PAGE == 'search_page':
        upvotes = browser.get_element_text(browser.get_sub_elements_by_css(post_element, ELEMENT_SELECTOR[PAGE]['upvotes'])[0])
        comments = browser.get_element_text(browser.get_sub_elements_by_css(post_element, ELEMENT_SELECTOR[PAGE]['comments'])[1])

    is_promtion = date == 'N/A'
    if is_promtion:
        upvotes = "N/A"

    return {
        'title': title,
        'upvotes': upvotes,
        'author': author,
        'date': date,
        'comments': comments,
        'promotion': is_promtion,
    }

if __name__ == '__main__':

    browser = Browser(headless=False)
    posts = []

    browser.load_page(ELEMENT_SELECTOR[PAGE]['url'])
    time.sleep(2)

    while(len(posts) < NUM_OF_POSTS):

        try:

            while True:        

                time.sleep(0.5)
                post_elements = browser.get_elements_by_css('div[data-testid=post-container]')

                if len(posts) >= len(post_elements):
                    browser.scroll_down(1)
                    continue

                if post_elements[len(posts)].text != '':
                    post_data = parse_post(browser, post_elements[len(posts)] )
                
                    # if len(posts) % 6 == 0:
                    #     browser.scroll_down(1)

                    break

                else:
                    browser.scroll_down(1)
                    continue
            
                
            posts.append(post_data)

            print(f'index: {len(posts)}, ele: {len(post_elements)}')

        except:
            break

    pd.DataFrame(posts).to_csv(f'output/reddit/{PAGE}/{SORT}/{KEYWORD}.csv', index=False)
    browser.quit()