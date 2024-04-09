class Deck
{
    public readonly bool AreJokersIncluded;
    public readonly List<Card> Cards = new List<Card>();

    public Deck(bool yesJoker)
    {
        AreJokersIncluded = yesJoker;
        createDeck();
    }
    public void createDeck()
    {
        string[] suits = { "Diamonds", "Clubs", "Hearts", "Spades" };
        string[] ranks = { "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King" };

        foreach (string suit in suits)
        {
            foreach (string rank in ranks)
            {
                Cards.Add(new Card(suit, rank));
            }
        }

        if (AreJokersIncluded)
        {
            Cards.Add(new Card("Joker", "Red"));
            Cards.Add(new Card("Joker", "Black"));
        }

    }
    public void Shuffle()
    {
        Random rando = new Random();
        int lastIndex = Cards.Count - 1;

        while (lastIndex > 0)
        {
            int randomIndex = rando.Next(0, lastIndex + 1);
            Card temporaryValue = Cards[lastIndex];
            Cards[lastIndex] = Cards[randomIndex];
            Cards[randomIndex] = temporaryValue;
            lastIndex--;
        }
    }
    public Card? Draw()
    {
        if (Cards.Count == 0) return null;

        Card topCard = Cards[Cards.Count - 1];
        Cards.RemoveAt(Cards.Count - 1);
        return topCard;
    }
}
