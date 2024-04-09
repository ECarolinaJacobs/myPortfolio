class Card
{
    public readonly string Suit;
    public readonly string Rank;
    public Card(string suit, string rank)
    {
        Suit = suit;
        Rank = rank;
    }

    public string GetName()
    {
        if (Suit == "Joker")
        {
            return $"{Rank} Joker";
        }
        return $"{Rank} of {Suit}";
    }
}