import collections
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        logger.info(f'Card: {self._cards}')

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


fd = FrenchDeck()
