"""
Bitcoin Price Guessing Game
User guesses whether Bitcoin price will go UP or DOWN
"""

import requests
import time
from datetime import datetime

class BitcoinGuessingGame:
    def __init__(self):
        self.score = 0
        self.total_rounds = 0
        self.api_url = "https://api.coingecko.com/api/v3/simple/price"
        self.btc_prices = []
        
    def fetch_btc_price(self):
        """Fetch the current Bitcoin price in USD"""
        try:
            params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd'
            }
            response = requests.get(self.api_url, params=params, timeout=5)
            response.raise_for_status()
            price = response.json()['bitcoin']['usd']
            return price
        except requests.exceptions.RequestException as e:
            print(f"Error fetching Bitcoin price: {e}")
            return None
    
    def display_rules(self):
        """Display game rules"""
        print("\n" + "="*50)
        print("   BITCOIN PRICE GUESSING GAME")
        print("="*50)
        print("\nRULES:")
        print("1. You will see the current Bitcoin price")
        print("2. Guess if the price will go UP or DOWN")
        print("3. After 3 seconds, the new price is revealed")
        print("4. Correct guess = +1 point")
        print("5. Type 'quit' to exit\n")
    
    def play_round(self):
        """Play a single round"""
        # Get initial price
        print("\n" + "-"*50)
        current_price = self.fetch_btc_price()
        
        if current_price is None:
            print("Cannot fetch price. Please try again.")
            return False
        
        print(f"\nCurrent Bitcoin Price: ${current_price:,.2f}")
        print(f"[Round {self.total_rounds + 1}]")
        
        # Get user guess
        while True:
            guess = input("\nWill the price go UP or DOWN? (up/down/quit): ").lower().strip()
            if guess in ['up', 'down', 'quit']:
                break
            print("Invalid input. Please enter 'up' or 'down'.")
        
        if guess == 'quit':
            return False
        
        # Wait for price change (simulated with a small wait)
        print("\nFetching next price in 3 seconds...")
        time.sleep(3)
        
        # Get new price
        new_price = self.fetch_btc_price()
        
        if new_price is None:
            print("Cannot fetch new price. Please try again.")
            return True
        
        # Determine result
        price_change = new_price - current_price
        actual_direction = 'up' if price_change > 0 else 'down' if price_change < 0 else 'none'
        
        # Show result
        print(f"\nNew Bitcoin Price: ${new_price:,.2f}")
        print(f"Price Change: ${price_change:+,.2f}")
        
        # Check if guess is correct
        if actual_direction == 'none':
            print("Price remained the same! No points awarded.")
            result = False
        elif guess == actual_direction:
            print("✓ CORRECT! You earned 1 point!")
            self.score += 1
            result = True
        else:
            print("✗ WRONG! Better luck next time.")
            result = False
        
        self.total_rounds += 1
        self.display_score()
        
        return True
    
    def display_score(self):
        """Display current score"""
        accuracy = (self.score / self.total_rounds * 100) if self.total_rounds > 0 else 0
        print(f"\nScore: {self.score}/{self.total_rounds} ({accuracy:.1f}%)")
    
    def run(self):
        """Main game loop"""
        self.display_rules()
        
        try:
            while True:
                if not self.play_round():
                    break
        except KeyboardInterrupt:
            print("\n\nGame interrupted!")
        
        # Final summary
        print("\n" + "="*50)
        print("   GAME OVER - FINAL SUMMARY")
        print("="*50)
        print(f"Total Rounds Played: {self.total_rounds}")
        print(f"Correct Guesses: {self.score}")
        if self.total_rounds > 0:
            accuracy = (self.score / self.total_rounds * 100)
            print(f"Accuracy: {accuracy:.1f}%")
            
            # Performance feedback
            if accuracy == 100:
                print("Outstanding! You're a Bitcoin oracle! 🚀")
            elif accuracy >= 75:
                print("Great job! You have good prediction skills! 📈")
            elif accuracy >= 50:
                print("Not bad! Keep practicing! 💡")
            else:
                print("Keep trying! Stay in the game! 💪")
        print("="*50 + "\n")


def main():
    """Entry point"""
    game = BitcoinGuessingGame()
    game.run()


if __name__ == "__main__":
    main()
