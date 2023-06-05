Feature: Trello API Test

  Scenario: Board Operations
    Given a Trello board does not exist
    When I create a board
    Then the board should be created successfully
    When I create 3 cards on the board
    Then 3 cards should be created successfully
    When I edit the card
    Then The card should be edited successfully
    Then The first card should be deleted successfully
    When I add a comment to the card
    Then The comment should be added successfully





