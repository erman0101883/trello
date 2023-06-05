import time
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import pytest
from pytest_bdd import scenario, given, then, when
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    # Set up the WebDriver instance
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--window-size=1920,1080")  # Set window size
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    yield driver
    # Teardown - quit the WebDriver instance
    driver.quit()

@scenario('trellos.feature', 'Verify board and perform actions')
def test_board():
    pass

@given('I am logged in to Trello')
def step_login_to_trello(driver):
    driver.get("https://trello.com/login")
    driver.find_element(By.ID, "user").send_keys("username")
    driver.find_element(By.ID, "login").click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("password")
    driver.find_element(By.ID, "login-submit").click()



@then('I should see 2 cards on the board')
def step_verify_cards_on_board(driver):
    # Wait for the cards to load on the board
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//ul[@class='boards-page-board-section-list']")))

    cards = driver.find_elements(By.XPATH, "//ul[@class='boards-page-board-section-list']")

    print("cards = " + str(cards))

    for card in cards:
        print(card.text)
        if "My New Test Board" or "My New2 Test Board" in card.text :
            return True
        else:
            print("there is no card in list that you expected")


@when('I add a new comment to that card and give green status')
def step_add_comment_to_card(driver):
    # Perform the steps to add a new comment to the card
    #clcik the card first
    card_with_comment = driver.find_element(By.XPATH, '//div[@title="My New2 Test Board"]')
    card_with_comment.click()
    time.sleep(5)
    card = driver.find_element(By.XPATH, '//span[@class="list-card-title js-card-name"]')
    card_name = card.text
    print("card name " + card_name)
    if card_name == "Card 2":
        card.click()
        time.sleep(5)
        driver.find_element(By.XPATH, "//input[@data-testid='card-back-new-comment-input-skeleton']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "(//div[@aria-label='Main content area, start typing to enter text.'])[2]").send_keys("This is a new comment")
        time.sleep(2)
        driver.find_element(By.XPATH, "//button[@data-testid='card-back-comment-save-button']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//span[@class='icon-sm icon-label']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "(//span[@class='VhaiZhQslxcjfC'])[1]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//button[@aria-label='Close popover']").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//a[@class='icon-md icon-close dialog-close-button js-close-window']").click()

    else:
        print("can not find your card")


@then('I should see a card with a comment')
def step_verify_card_with_comment(driver):
    # Locate a card with a comment
    card_with_comment = driver.find_element(By.XPATH, "(//div[@title='Comments'])[1]")

    assert card_with_comment is not None


@when('I set the card as DONE')
def step_set_card_as_done(driver):

    # create list as Done
    driver.find_element(By.XPATH, "//a[@class='open-add-list js-open-add-list']").click()
    time.sleep(1)

    # give the card name
    driver.find_element(By.XPATH, "//input[@class='list-name-input']").send_keys("DONE")

    #click add list
    driver.find_element(By.XPATH, "//input[@type='submit']").click()

    time.sleep(5)
    # Locate the source element (element to be dragged)
    source_element = driver.find_element(By.XPATH, '(//div[@class="list-card-details js-card-details"])[1]')

    # Locate the destination element (element to drop onto)
    destination_element = driver.find_element(By.XPATH, '(//div[@class="list js-list-content"])[2]/div[2]')
    time.sleep(2)
    # Perform the drag and drop action
    actions = ActionChains(driver)
    actions.drag_and_drop(source_element, destination_element).perform()


@then('the card should be marked as DONE')
def step_the_card_should_be_marked_done(driver):

    card = driver.find_element(By.XPATH, '(//div[@class="list js-list-content"])[2]/div[2]')

    if card is not None:
        card_name = driver.find_element(By.XPATH, '(//div[@class="list js-list-content"])[2]/div[2]/a/div[3]/span').text
        assert card_name == 'Card 2'








