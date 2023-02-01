import pygame
import random

colors = ['black', 'red']
types = ['C', 'S', 'H', 'D']
values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
numbers = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
size = (82, 125)
distance_between_cards = 32


class Card:
    """
    Class Card holds information about a card
    """
    def __init__(self, card_image_path, back_of_card_image_path, value, card_type, color, number):
        self.card = pygame.image.load(card_image_path)
        self.back_of_card = pygame.image.load(back_of_card_image_path)
        self.card = pygame.transform.scale(self.card, size)
        self.back_of_card = pygame.transform.scale(self.back_of_card, size)
        self.rect = self.card.get_rect()
        self.value = value
        self.card_type = card_type
        self.color = color
        self.number = number
        self.display_front = True

    def get_value(self):
        return self.value

    def get_card_type(self):
        return self.card_type

    def get_color(self):
        return self.color

    def change_display_type(self):
        """
        Changes the face of the card. If display_front is True the face of the card will pe displayed,
         else the back of the card will be displayed
        :return: None
        """
        if self.display_front is True:
            self.display_front = False
        else:
            self.display_front = True

    def display_card(self, screen, position):
        """
        Draw the card of the screen at the specified position
        :param screen:
        :param position:
        :return: None
        """
        if self.display_front is True:
            screen.blit(self.card, position)
        else:
            screen.blit(self.back_of_card, position)


class Deck:
    def __init__(self):
        self.list_of_card = self.__load_deck()
        self.shuffle_deck()

    @staticmethod
    def __load_deck():
        """
        Load the images of the cards and set up various information about the cards
        :return: a list of loaded cards
        """
        card_list = []
        i = 0
        for n in numbers:
            for t in types:
                if t in ('C', 'S'):
                    color = 'black'
                else:
                    color = 'red'
                path_f = "cards/" + n + t + '.png'
                path_b = 'cards/gray_back.png'
                card_list.append(Card(
                    card_image_path=path_f,
                    back_of_card_image_path=path_b,
                    value=values[i],
                    card_type=t,
                    color=color,
                    number=n))
            i = i + 1
        return card_list

    def shuffle_deck(self):
        random.shuffle(self.list_of_card)

    def get_card(self):
        """
        Returns a random card from the deck if possible
        :return: a card from the deck
        """
        if not self.list_of_card:
            return -1
        card = random.choice(self.list_of_card)
        self.list_of_card.remove(card)
        return card

    def add_card(self, card):
        self.list_of_card.append(card)


class PileOfCards:
    """
    Piles of the game. Each piles is represented by a border and the cards inside it.
    """
    def __init__(self, pile_type, position, x, y, width, height):
        self.list_of_cards = []
        self.pile_type = pile_type
        self.position = position
        self.x = x
        self.y = y
        self.red = (139, 0, 0)
        self.border_radius = 3
        self.pos1 = (self.x, self.y)  # left top corner
        self.pos2 = (self.x + width, self.y)  # right top corner
        self.pos3 = (self.x, self.y + height)  # left bottom corner
        self.pos4 = (self.x + width, self.y + height)  # right bottom corner

    def clicked_on_pile(self, position):
        if self.pos1[0] < position[0] < self.pos4[0] and self.pos1[1] < position[1] < self.pos4[1]:
            return True
        return False

    def get_pile_type(self):
        return self.pile_type

    def empty_pile(self):
        if not self.list_of_cards:
            return True
        return False

    def get_last_card(self):
        card = self.list_of_cards[-1]
        del self.list_of_cards[-1]
        return card

    def add_card(self, card):
        self.list_of_cards.append(card)

    def remove_card(self, card):
        self.list_of_cards.remove(card)

    def display_pile(self, screen):
        """
        Display the pile based on it's type
        :param screen:
        :return: None
        """
        self.__create_rect(screen)
        if self.pile_type == 'play':
            self.__display_play_pile_cards(screen)
        if self.pile_type == 'deck':
            self.__display_deck_pile_cards(screen)
        if self.pile_type == 'to-take':
            self.__display_to_take_pile_cards(screen)
        if self.pile_type == 'finish':
            self.__display_finish_pile_cards(screen)

    def get_cards_by_mouse_position(self, mouse_pos):
        """
        Used to take cards from playing piles.
        Check the card at the mouse position and creates a list of cards with all the cards between it.
        :param mouse_pos:
        :return: List of cards or -1 in case of no possible cards returned
        """
        if self.empty_pile():
            return -1
        if len(self.list_of_cards) == 1:
            pos1 = self.position
            pos2 = (self.position[0] + size[0], self.position[1] + size[1])
            if pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1]:
                return self.list_of_cards
        elif len(self.list_of_cards) > 1:
            l_cards = []
            k = None
            for i in range(len(self.list_of_cards) - 1):
                pos1 = (self.position[0], self.position[1] + distance_between_cards * i)
                pos2 = (self.position[0] + size[0], self.position[1] + distance_between_cards * (i + 1))
                if pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1]:
                    k = i
                    break
            if k is None:  # Nu am gasit pozitia unei carti si verific ultima carte
                d = distance_between_cards * (len(self.list_of_cards) - 1)
                pos1 = (self.position[0], self.position[1] + d)
                pos2 = (self.position[0] + size[0], self.position[1] + d + size[1])
                if pos1[0] < mouse_pos[0] < pos2[0] and pos1[1] < mouse_pos[1] < pos2[1]:
                    l_cards.append(self.list_of_cards[-1])
                else:
                    return -1
            else:
                if self.list_of_cards[k].display_front is False:  # Verific daca cartea este cu fata in sus
                    return -1
                else:
                    # Merg de la cartea buna gasita pana la final si formez lista
                    for i in range(k, len(self.list_of_cards)):
                        l_cards.append(self.list_of_cards[i])
            return l_cards
        return -1

    def __create_rect(self, screen):
        """
        Draw the borders of the piles
        :param screen:
        :return: None
        """
        pygame.draw.line(screen, self.red, self.pos1, self.pos2, self.border_radius)
        pygame.draw.line(screen, self.red, self.pos2, self.pos4, self.border_radius)
        pygame.draw.line(screen, self.red, self.pos4, self.pos3, self.border_radius)
        pygame.draw.line(screen, self.red, self.pos3, self.pos1, self.border_radius)

    def __display_play_pile_cards(self, screen):
        i = 0
        for card in self.list_of_cards:
            position = self.position[0], self.position[1] + distance_between_cards * i
            card.display_card(screen, position)
            i = i + 1

    def __display_deck_pile_cards(self, screen):
        for card in self.list_of_cards:
            card.display_card(screen, self.position)

    def __display_to_take_pile_cards(self, screen):
        i = 0
        if len(self.list_of_cards) < 5:
            l_cards = self.list_of_cards
        else:
            l_cards = self.list_of_cards[-5:]
        for card in l_cards:
            position = self.position[0] + distance_between_cards * i, self.position[1]
            card.display_card(screen, position)
            i = i + 1

    def __display_finish_pile_cards(self, screen):
        for card in self.list_of_cards:
            card.display_card(screen, self.position)
