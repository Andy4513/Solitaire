from card import *
import sys

distance_between_cards = 32
piles_types = ['play', 'deck', 'finish', 'to-take']

x_card_pos_in_piles = 9
y_card_pos_in_piles = 10

x_play_pile_start = 100
y_play_pile_start = 225
width_play_pile = 100
height_play_pile = 650

x_deck_pile_start = 100
y_deck_pile_start = 50
width_deck_pile = 100
heigh_deck_pile = 150

x_finish_pile_start = 550
y_finish_pile_start = 50
width_finish_pile = width_deck_pile
heigh_finish_pile = heigh_deck_pile

x_take_pile_start = 250
y_take_pile_start = 50
width_take_pile = width_deck_pile * 2 + 50
heigh_take_pile = heigh_deck_pile

circle_radius = 5


class Game:
    """
    Class Game initializes the game, checks for events and updates the screen
    """
    def __init__(self):
        self.size = 1200, 900
        self.green = 0, 100, 0
        self.blue = (0, 0, 205)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.deck = Deck()
        self.piles = self.__init_piles()
        self.game_on = True
        self.screen = None

    def __init_piles(self):
        """
        Initialize the piles of the game
        :return: None
        """
        piles = []
        #   Playing piles
        distance_between_piles = 0
        for i in range(7):
            pile = PileOfCards(
                piles_types[0],
                (x_play_pile_start + i * width_play_pile + x_card_pos_in_piles + distance_between_piles,
                 y_play_pile_start + y_card_pos_in_piles),
                x_play_pile_start + i * width_play_pile + distance_between_piles,
                y_play_pile_start,
                width_play_pile,
                height_play_pile)
            for j in range(i + 1):
                card = self.deck.get_card()
                if j != i:
                    card.change_display_type()
                pile.add_card(card)
            piles.append(pile)
            distance_between_piles = distance_between_piles + 50
        #   Deck pile
        pile = PileOfCards(
            piles_types[1],
            (x_deck_pile_start + x_card_pos_in_piles, y_deck_pile_start + y_card_pos_in_piles),
            x_deck_pile_start,
            y_deck_pile_start,
            width_deck_pile,
            heigh_deck_pile
        )
        card = self.deck.get_card()
        while card != -1:
            card.change_display_type()
            pile.add_card(card)
            card = self.deck.get_card()
        piles.append(pile)
        #   Finish pile
        distance_between_piles = 0
        for i in range(4):
            pile = PileOfCards(
                piles_types[2],
                (x_finish_pile_start + i * width_finish_pile + x_card_pos_in_piles + distance_between_piles,
                 y_finish_pile_start + y_card_pos_in_piles),
                x_finish_pile_start + i * width_finish_pile + distance_between_piles,
                y_finish_pile_start,
                width_finish_pile,
                heigh_finish_pile
            )
            piles.append(pile)
            distance_between_piles = distance_between_piles + 50
        #   Cards to-take pile
        pile = PileOfCards(
            piles_types[3],
            (x_take_pile_start + x_card_pos_in_piles, y_take_pile_start + y_card_pos_in_piles),
            x_take_pile_start,
            y_take_pile_start,
            width_take_pile,
            heigh_take_pile
        )
        piles.append(pile)
        return piles

    def init_game(self):
        """
        Initialize the screen of the game
        :return: None
        """
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)

    def listen_for_events(self):
        """
        Listen for the events: mouse clicks on the piles
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos1 = pygame.mouse.get_pos()
                # print(mouse_pos1)
                for pile in self.piles:

                    # Deck funcitonlality

                    if pile.clicked_on_pile(mouse_pos1) is True and pile.pile_type == 'deck':
                        if not pile.empty_pile():
                            self.__move_from_deck_to_take(pile.get_last_card())
                        else:
                            self.__remake_deck_pile(pile)

                    # To-take pile functionality

                    elif pile.clicked_on_pile(mouse_pos1) is True and pile.pile_type == 'to-take':
                        pygame.draw.circle(self.screen, self.blue, mouse_pos1, circle_radius)
                        pygame.display.flip()
                        aux_cards = []
                        if not pile.empty_pile():
                            aux_cards.append(pile.get_last_card())
                        else:
                            aux_cards = -1
                        if aux_cards != -1:
                            cond = True
                            while cond:
                                for ev in pygame.event.get():
                                    # Ceva caz special -> bug
                                    ok = False
                                    if ev.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_pos2 = pygame.mouse.get_pos()
                                        for p in self.piles:
                                            if p.clicked_on_pile(mouse_pos2) is True and p.pile_type == 'play':
                                                if self.__check_if_cards_can_be_placed_on_playing_piles(p, aux_cards):
                                                    self.__move_to_pile(p, aux_cards)
                                                    ok = True
                                                    break
                                            elif p.clicked_on_pile(mouse_pos2) is True and p.pile_type == 'finish':
                                                if self.__check_if_card_can_be_placed_on_finish_piles(p, aux_cards[0]):
                                                    self.__move_to_pile(p, aux_cards)
                                                    ok = True
                                                    break
                                        if ok is False:
                                            self.__move_to_pile(pile, aux_cards)
                                        cond = False
                                        self.display()
                                        break

                    #    Playing piles functionality

                    elif pile.clicked_on_pile(mouse_pos1) is True and pile.pile_type == 'play':
                        pygame.draw.circle(self.screen, self.blue, mouse_pos1, circle_radius)
                        pygame.display.flip()
                        aux_cards = self.__make_aux_cards_from_playing_pile(pile, mouse_pos1)
                        if aux_cards == -1:
                            pass
                        else:
                            cond = True
                            while cond:
                                for ev in pygame.event.get():
                                    if ev.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_pos2 = pygame.mouse.get_pos()
                                        for p in self.piles:
                                            # Move to other pile
                                            if p.clicked_on_pile(mouse_pos2) and p.pile_type == 'play':
                                                if self.__check_if_cards_can_be_placed_on_playing_piles(p, aux_cards):
                                                    self.__move_to_pile(p, aux_cards)
                                                    self.__remove_from_pile(pile, aux_cards)
                                                    break
                                            # Move to finish pile
                                            if p.clicked_on_pile(mouse_pos2) and p.pile_type == 'finish':
                                                if len(aux_cards) == 1:
                                                    if self.__check_if_card_can_be_placed_on_finish_piles(
                                                            p,
                                                            aux_cards[0]):
                                                        self.__move_to_pile(p, aux_cards)
                                                        self.__remove_from_pile(pile, aux_cards)
                                                        break
                                        cond = False
                                        self.display()
                                        break

    def update(self):
        """
        Check if the game is over
        :return: None
        """
        cards = 0
        for pile in self.piles:
            if pile.pile_type == 'finish':
                if not pile.empty_pile():
                    cards = cards + len(pile.list_of_cards)
        if cards == 52:
            self.game_on = False

    def display(self):
        """
        Display the objects of the game on the screen
        :return: None
        """
        if self.game_on:
            self.screen.fill(self.green)
            for pile in self.piles:
                pile.display_pile(self.screen)
            pygame.display.flip()
        else:
            self.screen.fill(self.black)
            font = pygame.font.Font('freesansbold.ttf', 128)
            text = font.render('You won', True, self.blue, self.white)
            text_rect = text.get_rect()
            text_rect.center = (self.size[0] // 2, self.size[1] // 2)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(5000)
            sys.exit(0)

    def __move_from_deck_to_take(self, card):
        """
        Move 1 card from the deck pile to the pile which we then can take cards from
        :param card: The card that get moved
        :return: None
        """
        card.change_display_type()
        for pile in self.piles:
            if pile.pile_type == 'to-take':
                pile.add_card(card)

    def __remake_deck_pile(self, deck_pile):
        """
        Remake the deck pile and shuffles the cards
        :param deck_pile:
        :return: None
        """
        pile = [i for i in self.piles if i.get_pile_type() == 'to-take']
        pile = pile[0]
        while pile.empty_pile() is False:
            card = pile.get_last_card()
            self.deck.add_card(card)
        self.deck.shuffle_deck()
        card = self.deck.get_card()
        while card != -1:
            card.change_display_type()
            deck_pile.add_card(card)
            card = self.deck.get_card()

    @staticmethod
    def __check_if_cards_can_be_placed_on_playing_piles(pile, cards):
        """
        Check if the cards can be placed on the play piles
        :param pile:
        :param cards:
        :return: True if possible, else False
        """
        # if pile is empty first card must be K
        f_card = cards[0]
        if pile.empty_pile():
            if f_card.value == 13:
                return True
            else:
                return False
        # if pile is not empty check for last card in pile in see if
        # the first card is lower and different color then the last pile card
        l_card = pile.list_of_cards[-1]
        if f_card.value == l_card.value - 1 and f_card.color != l_card.color:
            return True
        return False

    @staticmethod
    def __move_to_pile(pile, cards):
        """
        Move the cards to the specified pile
        :param pile:
        :param cards:
        :return: None
        """
        for card in cards:
            pile.add_card(card)

    @staticmethod
    def __check_if_card_can_be_placed_on_finish_piles(pile, card):
        """
        Check if the chosen card can be placed on the specified finish pile
        :param pile:
        :param card:
        :return: True if possible, else False
        """
        if pile.empty_pile():
            if card.value == 1:
                return True
        else:
            l_card = pile.list_of_cards[-1]
            if card.value == l_card.value + 1 and card.card_type == l_card.card_type:
                return True
        return False

    @staticmethod
    def __make_aux_cards_from_playing_pile(pile, mouse_pos):
        """
        Make a list of cards than can be moved to another playing pile
        :param pile:
        :param mouse_pos:
        :return: a list of the specified cards or -1 in case of error
        """
        aux = pile.get_cards_by_mouse_position(mouse_pos)
        return aux

    @staticmethod
    def __remove_from_pile(pile, cards):
        """
        Remove the specified cards from the specified pile
        :param pile:
        :param cards:
        :return: None
        """
        for card in cards:
            pile.remove_card(card)
        if not pile.empty_pile():
            if not pile.list_of_cards[-1].display_front:
                pile.list_of_cards[-1].change_display_type()
