import time

from pytest_bdd import given, when, then, scenario
import requests

#parametrize values below
API_KEY = '8c3fe58a1c81265cac589f131d1bbaed'
API_TOKEN = 'ATTA159d302ac07b99ddc944476409e80b213b4e3a5858336553a882e05ec733c582A0FB6AFE'
BASE_URL = 'https://api.trello.com/1'
BOARDS_URL = BASE_URL + '/boards'
CARDS_URL = BASE_URL + '/cards'
LIST_URL = BASE_URL + '/lists'
board_id = ""
card_id= ""

@scenario('trello.feature', 'Board Operations')
def test_board():
    pass


@given("a Trello board does not exist")
def delete_trello_board():
    #need to be sure no board remained

    # Step 1: Get a list of all boards
    boards_url = f'https://api.trello.com/1/members/me/boards?key={API_KEY}&token={API_TOKEN}'
    response = requests.get(boards_url)
    boards = response.json()
    # Step 2: Delete each board
    for board in boards:
        boards_id = board['id']
        delete_url = f'https://api.trello.com/1/boards/{boards_id}?key={API_KEY}&token={API_TOKEN}'
        response = requests.delete(delete_url)
        if response.status_code == 200:
            print(f"Successfully deleted board with ID: {boards_id}")
        else:
            print(f"Failed to delete board with ID: {boards_id}")


@when("I create a board")
def create_trello_board():
    global board_id
    url = f"{BOARDS_URL}?key={API_KEY}&token={API_TOKEN}"
    data = {
        'name': 'My New2 Test Board',
        'defaultLists': False
    }

    response = requests.post(url, json=data)
    board_id = response.json()['id']
    time.sleep(10)

@then("the board should be created successfully")
def verify_board_creation():
    global board_id
    url = f"{BOARDS_URL}?key={API_KEY}&token={API_TOKEN}"
    data = {
        'name': 'My New2 Test Board',
        'defaultLists': False
    }

    response = requests.get(f"{BOARDS_URL}/{board_id}?key={API_KEY}&token={API_TOKEN}", json=data)
    if  response.status_code == 200:
        print(f"Board created successfully with ID: {board_id}")

    else:
        print(f"Error creating board: {response.text}")

@when("I create 3 cards on the board")
def create_cards():
    global board_id
    global card_id

    query = {
        'name': "new list",
        'idBoard': board_id,
        'key': API_KEY,
        'token': API_TOKEN
    }

    response_list = requests.post(f"{LIST_URL}?key={API_KEY}&token={API_TOKEN}", params=query)
    new_list = response_list.json()

    print(f"List Name: {new_list['name']}")
    print(f"List ID: {new_list['id']}")
    global list_id
    list_id = new_list['id']


    for i in range(3):
        url = f"{CARDS_URL}?key={API_KEY}&token={API_TOKEN}"
        query = {
            'idList': list_id,
            'key': API_KEY,
            'token': API_TOKEN,
            'name': f'Card {i+1}',

        }
        response = requests.post(url, params=query)
        if response.status_code == 200:
            card_data = response.json()
            card_id = card_data['id']
            print(f"Card {i+1} created successfully with ID: {card_id}")
        else:
            print(f"Error creating Card {i+1}: {response.text}")



@then("3 cards should be created successfully")
def verify_card_creation():
    url = f'{CARDS_URL}/{card_id}?key={API_KEY}&token={API_TOKEN}'
    print("url =", url)

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
    }
    response = requests.get(url, headers=headers, params=query)
    print("response =", response.text)
    assert response.status_code == 200




@when("I edit the card")
def edit_card():
    url = f"{CARDS_URL}/{card_id}"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'name': 'Updated Card',
    }
    response = requests.put(url, params=query)
    assert response.status_code == 200


@then("The card should be edited successfully")
def verify_card_edit():
    url = f"{CARDS_URL}/{card_id}"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'fields': 'name',
    }
    response = requests.get(url, params=query)
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated Card'

@then("The first card should be deleted successfully")
def verify_card_deletion():

    firstID = str(get_card_list())
    print("firstID " + firstID)
    url = f"{CARDS_URL}/{firstID}"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
    }
    response = requests.delete(url, params=query)
    assert response.status_code == 200


@when("I add a comment to the card")
def add_comment():
    url = f"{CARDS_URL}/{card_id}/actions/comments"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'text': 'Test comment',
    }
    response = requests.post(url, params=query)
    assert response.status_code == 200


@then("The comment should be added successfully")
def verify_comment_addition():
    url = f"{CARDS_URL}/{card_id}/actions"
    query = {
        'key': API_KEY,
        'token': API_TOKEN,
        'filter': 'commentCard',
    }
    response = requests.get(url, params=query)
    assert response.status_code == 200
    assert any(action['type'] == 'commentCard' for action in response.json())

#you need to get card list for using into method above
card_list = []

def get_card_list():
    global new_list
    global list_id
    global first_id

    query = {
        'key': API_KEY,
        'token': API_TOKEN
    }
    response= requests.get(f"{LIST_URL}/{list_id}?key={API_KEY}&token={API_TOKEN}", params=query)


    if response.status_code == 200:


        new_list = response.json()

        print(f"List Name: {new_list['name']}")
        print(f"List ID: {new_list['id']}")
        list_id = new_list['id']

        query2 = {
            'key': 'APIKey',
            'token': 'APIToken'
        }

        response_cards = requests.get(f"{LIST_URL}/{list_id}/cards?key={API_KEY}&token={API_TOKEN}", params=query2)
        print("response cards  = " + str(response_cards))
        print("response =", str(response_cards.text))


        first_id = response_cards.json()[0]['id']
        print("first_id " + first_id)

        return first_id

    else:
        print("Error retrieving cards from the list.")


