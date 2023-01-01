from webdriver import Browser
import util

import pandas as pd

import time

KEYWORD = "explore"
NUM_OF_POSTS = 100000
PAGE = 'explore'

USERNAME = 'webresearch18@gmail.com'
PASSWORD = 'w3bR3s3arch567!'

ELEMENT_SELECTOR = {
    'tags': {
        'url': f'https://www.instagram.com/explore/tags/{KEYWORD}/',
        'post': 'div._aabd',
    },
    'search': {
        'url': f'https://www.instagram.com/explore/search/keyword/?q={KEYWORD}',
        'post': 'div._ab70',
    },
    'explore': {
        'url': f'https://www.instagram.com/explore/q={KEYWORD}',
        'post': 'div._ab70',
    },
}

def login(browser):
    browser.load_page('https://www.instagram.com/')
    browser.get_element_by_css('input[name="username"]').send_keys(USERNAME)
    browser.get_element_by_css('input[name="password"]').send_keys(PASSWORD)
    time.sleep(1)
    browser.get_element_by_css('button[type="submit"]').click()
    time.sleep(1)

def pull_post_data(browser):
    account = browser.get_element_text(browser.get_element_by_css('header._aaqw')).split('\n')[0]
    num_of_interactions = browser.get_element_text(browser.get_element_by_css('section._ae5m._ae5n._ae5o'))
    date_posted = browser.get_element_text(browser.get_element_by_css('time._aaqe'))
    description = browser.get_element_text(browser.get_element_by_css('span._aacl._aaco._aacu._aacx._aad7._aade'))
    is_video = num_of_interactions != 'N/A' and num_of_interactions.split(' ')[1] == 'views'

    return {
        'account': account,
        'num_of_interactions': util.format_instagram_interactions(num_of_interactions),
        'date_posted': util.format_instagram_date(date_posted),
        'description': description,
        'is_video': is_video
    }

if __name__ == '__main__':

    browser = Browser(headless=False)

    # url = ELEMENT_SELECTOR[PAGE]['url']
    url = 'https://www.instagram.com/explore/'

    posts = []

    login(browser)
    browser.load_page(url)
    time.sleep(2)
    
    selected_post = browser.get_elements_by_css(ELEMENT_SELECTOR[PAGE]['post'])[0]
    selected_post.click()

    for i in range(NUM_OF_POSTS):

        try:
            print(f'Post: {i}')
            time.sleep(0.5)
            posts.append(pull_post_data(browser))
            
            try:
                next_post_button = browser.get_element_by_css('div._aaqg._aaqh')
                next_post_button.click()

                # if i % 7*3 == 0:
                #     raise Exception('Scrolling')

            except:
                print('Scrolling')
                close_post_button = browser.get_element_by_css('div.s8sjc6am.mczi3sny.pxtik7zl.b0ur3jhr')
                close_post_button.click()
                browser.scroll_down(10)
                time.sleep(2)
                all_posts = browser.get_elements_by_css(ELEMENT_SELECTOR[PAGE]['post'])
                selected_post = all_posts[8*3]
                selected_post.click()
        except:
            break

    pd.DataFrame(posts).to_csv(f'output/instagram/{PAGE}/{KEYWORD}.csv', index=False)
    browser.quit()
