import json
import random

# Load JSON file
with open('cards.json') as file:
    tarot_deck = json.load(file)

# Function to search a card by name
def search_card(card_name):
    for card in tarot_deck:
        if card['name'].lower() == card_name.lower():
            print(f"Card: {card['name']}")
            print(f"Description: {card['desc']}")
            print(f"Reversed Description: {card['rdesc']}")
            print(f"Card Drawing:\n{card['card']}")
            return

    print("Card not found.")

# Function to draw a card at random
def draw_card():
    card = random.choice(tarot_deck)
    print(f"Card: {card['name']}")
    print(f"Description: {card['desc']}")
    print(f"Card Drawing:\n{card['card']}")

# Function for a three-card tarot reading
def three_card_reading():
    print("Past:")
    draw_card()
    print("\nPresent:")
    draw_card()
    print("\nFuture:")
    draw_card()

# Test the functions
search_card('The High Priestess')
draw_card()
three_card_reading()
