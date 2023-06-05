Feature: Trello Board Actions
  Scenario: Verify board and perform actions
    Given I am logged in to Trello
    Then I should see 2 cards on the board
    When I add a new comment to that card and give green status
    Then I should see a card with a comment
    When I set the card as DONE
    Then the card should be marked as DONE


