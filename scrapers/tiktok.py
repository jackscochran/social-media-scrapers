from webdriver import Browser
import util

import pandas as pd

import time

KEYWORD = "explore"
NUM_OF_POSTS = 1000

def select_post(i):
    all_posts = browser.get_elements_by_css('div.tiktok-1soki6-DivItemContainerForSearch')
    all_posts = browser.get_elements_by_css('div.tiktok-3g8031-DivVideoPlayerContainer')
    selected_post = all_posts[i]
    selected_post.click()

def scroll_and_load(browser):
    browser.scroll_down(8)
    load_more_buttom = browser.get_element_by_css('button.tiktok-1mwtjmv-ButtonMore')
    load_more_buttom.click()
    time.sleep(2)

def pull_post_data(browser, i):
    return {
        'account': browser.get_element_text(browser.get_element_by_css('span.tiktok-1r8gltq-SpanUniqueId')),
        'date': util.format_tiktok_date(browser.get_element_text(browser.get_element_by_css('span.tiktok-6hn0mp-SpanOtherInfos'))),
        'description': browser.get_element_text(browser.get_element_by_css('div.tiktok-5dmltr-DivContainer')),
        'num_of_likes': util.format_big_num(browser.get_element_text(browser.get_elements_by_css('strong.tiktok-1y2yo26-StrongText')[(i-1)*3])),
        'num_of_comments': util.format_big_num(browser.get_element_text(browser.get_elements_by_css('strong.tiktok-1y2yo26-StrongText')[(i-1)*3 +1]))
    }
    
if __name__ == '__main__':

    # url = f'https://www.tiktok.com/search/video?q={KEYWORD}'
    url = "https://www.tiktok.com"
    browser = Browser()
    posts = []

    browser.load_page(url)

    input("Press Enter to continue...")

    select_post(0)

    for i in range(1, 1+NUM_OF_POSTS):

        try:
            print(f'Post: {i}')
            time.sleep(2)
            posts.append(pull_post_data(browser, i))

            try:
                next_post_button = browser.get_element_by_css('button[data-e2e=arrow-right]')
                next_post_button.click()
            except:
                exit_button = browser.get_element_by_css('button.tiktok-bqtu1e-ButtonBasicButtonContainer-StyledCloseIconContainer')
                exit_button.click()

                scroll_and_load(browser)
                select_post(i)
        except:
            break

# browser.quit()

pd.DataFrame(posts).to_csv(f'output/{KEYWORD}-tiktok_data.csv', index=False)

# ended after 203 posts