import streamlit as st
import requests
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Bitcoin Guessing Game",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        padding: 12px;
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .price-display {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
    }
    .change-positive {
        color: #00cc00;
        font-size: 24px;
        font-weight: bold;
    }
    .change-negative {
        color: #ff0000;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_rounds' not in st.session_state:
    st.session_state.total_rounds = 0
if 'current_price' not in st.session_state:
    st.session_state.current_price = None
if 'game_phase' not in st.session_state:
    st.session_state.game_phase = "start"  # start, guessing, result
if 'previous_price' not in st.session_state:
    st.session_state.previous_price = None
if 'price_change' not in st.session_state:
    st.session_state.price_change = None
if 'user_guess' not in st.session_state:
    st.session_state.user_guess = None
if 'is_correct' not in st.session_state:
    st.session_state.is_correct = False

# API Configuration
API_URL = "https://api.coingecko.com/api/v3/simple/price"

def fetch_btc_price():
    """Fetch current Bitcoin price"""
    try:
        params = {
            'ids': 'bitcoin',
            'vs_currencies': 'usd'
        }
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        price = response.json()['bitcoin']['usd']
        return price
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Bitcoin price: {e}")
        return None

def reset_game():
    """Reset to start of new round"""
    st.session_state.game_phase = "start"
    st.session_state.current_price = None
    st.session_state.previous_price = None
    st.session_state.price_change = None
    st.session_state.user_guess = None
    st.session_state.is_correct = False

def start_round():
    """Start a new round"""
    price = fetch_btc_price()
    if price is not None:
        st.session_state.current_price = price
        st.session_state.game_phase = "guessing"
        st.rerun()

def make_guess(guess):
    """Record user's guess and fetch new price"""
    st.session_state.user_guess = guess
    st.session_state.previous_price = st.session_state.current_price
    st.session_state.game_phase = "waiting"
    st.rerun()

def reveal_result():
    """Fetch new price and show result"""
    new_price = fetch_btc_price()
    if new_price is not None:
        st.session_state.price_change = new_price - st.session_state.previous_price
        actual_direction = 'up' if st.session_state.price_change > 0 else ('down' if st.session_state.price_change < 0 else 'none')
        
        if actual_direction == 'none':
            st.session_state.is_correct = False
        else:
            st.session_state.is_correct = st.session_state.user_guess == actual_direction
        
        if st.session_state.is_correct:
            st.session_state.score += 1
        
        st.session_state.total_rounds += 1
        st.session_state.current_price = new_price
        st.session_state.game_phase = "result"
        st.rerun()

# Title and Header
st.markdown("# 🚀 Bitcoin Price Guessing Game")
st.markdown("---")

# Sidebar - Score Display
with st.sidebar:
    st.markdown("## 📊 Your Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Correct", st.session_state.score)
    with col2:
        st.metric("Total", st.session_state.total_rounds)
    
    if st.session_state.total_rounds > 0:
        accuracy = (st.session_state.score / st.session_state.total_rounds) * 100
        st.metric("Accuracy", f"{accuracy:.1f}%")
    
    if st.button("🔄 Reset Stats", key="reset_stats"):
        st.session_state.score = 0
        st.session_state.total_rounds = 0
        reset_game()
        st.rerun()

# Main Game Area
if st.session_state.game_phase == "start":
    st.markdown("### Welcome to the Bitcoin Guessing Game! 🎮")
    st.write("""
    **How it works:**
    1. Click "Start Round" to see the current Bitcoin price
    2. Predict if the price will go UP or DOWN
    3. See the result after 3 seconds
    4. Earn points for correct predictions!
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("🎯 Start Round", on_click=start_round, use_container_width=True, key="start_btn")

elif st.session_state.game_phase == "guessing":
    st.markdown(f"### Round {st.session_state.total_rounds + 1}")
    
    # Display current price
    st.markdown("#### Current Bitcoin Price")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f'<div class="price-display">${st.session_state.current_price:,.2f}</div>', 
                   unsafe_allow_html=True)
    
    st.write("")
    st.markdown("#### What will happen next?")
    
    # Prediction buttons
    col1, col2 = st.columns(2)
    with col1:
        st.button("📈 Price UP", 
                 on_click=make_guess, 
                 args=("up",),
                 use_container_width=True,
                 key="up_btn")
    with col2:
        st.button("📉 Price DOWN", 
                 on_click=make_guess, 
                 args=("down",),
                 use_container_width=True,
                 key="down_btn")

elif st.session_state.game_phase == "waiting":
    st.markdown(f"### Round {st.session_state.total_rounds + 1}")
    
    # Display current price
    st.markdown("#### Your Guess")
    if st.session_state.user_guess == "up":
        st.info("📈 You predicted the price will go UP")
    else:
        st.info("📉 You predicted the price will go DOWN")
    
    # Show countdown
    with st.spinner("⏳ Fetching new price..."):
        time.sleep(3)
    
    reveal_result()

elif st.session_state.game_phase == "result":
    st.markdown(f"### Round {st.session_state.total_rounds}")
    
    # Show prices
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Previous Price**")
        st.markdown(f'<div class="price-display" style="font-size: 32px;">${st.session_state.previous_price:,.2f}</div>', 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("**New Price**")
        st.markdown(f'<div class="price-display" style="font-size: 32px;">${st.session_state.current_price:,.2f}</div>', 
                   unsafe_allow_html=True)
    
    # Show price change
    st.write("")
    if st.session_state.price_change > 0:
        st.markdown(f'<div class="change-positive">📈 +${st.session_state.price_change:,.2f}</div>', 
                   unsafe_allow_html=True)
    elif st.session_state.price_change < 0:
        st.markdown(f'<div class="change-negative">📉 ${st.session_state.price_change:,.2f}</div>', 
                   unsafe_allow_html=True)
    else:
        st.info("Price remained the same!")
    
    # Show result with emoji and styling
    st.write("")
    if st.session_state.price_change == 0:
        st.warning("⚖️ Price didn't change - No points awarded")
    elif st.session_state.is_correct:
        st.success("✅ CORRECT! You earned 1 point! 🎉")
    else:
        st.error("❌ WRONG! Better luck next time!")
    
    # Updated score
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Correct", st.session_state.score)
    with col2:
        st.metric("Total", st.session_state.total_rounds)
    with col3:
        if st.session_state.total_rounds > 0:
            accuracy = (st.session_state.score / st.session_state.total_rounds) * 100
            st.metric("Accuracy", f"{accuracy:.1f}%")
    
    # Play again button
    st.write("")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("🎯 Next Round", on_click=reset_game, use_container_width=True, key="next_btn")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p><small>Built with ❤️ using Streamlit | Bitcoin data from CoinGecko API</small></p>
</div>
""", unsafe_allow_html=True)
