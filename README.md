# Bitcoin Price Guessing Game

A beginner-friendly Python game where you predict whether the Bitcoin price will go UP or DOWN!

## Features

✅ **Live Bitcoin Price Fetching** - Uses CoinGecko API to get real-time BTC prices  
✅ **Interactive Gameplay** - Make predictions and test your intuition  
✅ **Score Tracking** - Keep track of your accuracy across multiple rounds  
✅ **Performance Feedback** - Get personalized feedback based on your accuracy  

## Requirements

- Python 3.6+
- `requests` library (for API calls)

## Installation

1. **Install Python** (if not already installed)
   - Download from https://www.python.org/

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

1. **Run the game:**
   ```bash
   python bitcoin_game.py
   ```

2. **Gameplay Flow:**
   - You'll see the current Bitcoin price in USD
   - Enter your guess: `up` (price will increase) or `down` (price will decrease)
   - Wait 3 seconds for the new price to be fetched
   - See if your guess was correct!
   - Your score is tracked automatically

3. **Exit the game:**
   - Type `quit` when prompted for a guess
   - Or press `Ctrl+C` to interrupt

## Game Rules

- Each round shows the current Bitcoin price
- You predict if the NEXT price will be higher (UP) or lower (DOWN)
- Correct predictions earn you 1 point
- Your accuracy percentage is calculated as: (Correct Guesses / Total Rounds) × 100

## Skills Demonstrated

- **Python**: Core programming language
- **API Integration**: Fetching real-time data from CoinGecko API
- **Control Flow**: if-else statements for decision making
- **Loops**: while loop for continuous gameplay
- **Time Handling**: Using `time.sleep()` for delays
- **Error Handling**: Try-except blocks for API requests
- **Object-Oriented Programming**: Class-based game structure

## API Used

This game uses the **CoinGecko API** (free, no API key required):
- Endpoint: `https://api.coingecko.com/api/v3/simple/price`
- Returns: Current Bitcoin price in USD

## Example Output

```
==================================================
   BITCOIN PRICE GUESSING GAME
==================================================

RULES:
1. You will see the current Bitcoin price
2. Guess if the price will go UP or DOWN
3. After 3 seconds, the new price is revealed
4. Correct guess = +1 point
5. Type 'quit' to exit

--------------------------------------------------

Current Bitcoin Price: $45,320.50
[Round 1]

Will the price go UP or DOWN? (up/down/quit): up

Fetching next price in 3 seconds...

New Bitcoin Price: $45,420.75
Price Change: +$100.25
✓ CORRECT! You earned 1 point!

Score: 1/1 (100.0%)
```

## Tips for Better Predictions

1. Bitcoin prices are highly volatile - don't expect 100% accuracy!
2. Consider market conditions and news when making guesses
3. Play multiple rounds to improve your intuition
4. Track patterns if you notice them

## Troubleshooting

**Problem:** "Error fetching Bitcoin price"
- **Solution:** Check your internet connection and try again

**Problem:** `ModuleNotFoundError: No module named 'requests'`
- **Solution:** Run `pip install -r requirements.txt`

## Future Enhancements

- Add multi-player functionality
- Include historical price trends
- Add difficulty levels (short/medium/long time gaps)
- Store game history to files
- Add cryptocurrency options beyond Bitcoin

## License

Free to use and modify!

---

Have fun and may your Bitcoin predictions be ever accurate! 🚀
