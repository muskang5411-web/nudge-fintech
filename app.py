import streamlit as st
import time

# Page Configuration
st.set_page_config(page_title="Nudge AI Prototype", page_icon="💡", layout="centered")

st.title("💡 NUDGE: AI Behavioral Firewall")
st.write("Your real-time pocket mentor for mindful spending.")

# --- INITIALIZE SESSION STATE (For advanced tracking) ---
if "monthly_budget_pool" not in st.session_state:
    st.session_state.monthly_budget_pool = 15000 
if "days_left_in_month" not in st.session_state:
    st.session_state.days_left_in_month = 30
if "mindful_streak" not in st.session_state:
    st.session_state.mindful_streak = 4  # Gamified streak counter!

# --- SIDEBAR: User Profile, Context & Streaks ---
st.sidebar.header("User Profile & Context")
monthly_income = st.sidebar.number_input("Monthly Income (₹)", value=30000, step=1000)
monthly_savings_goal = st.sidebar.number_input("Monthly Savings Goal (₹)", value=10000, step=500)

user_goal_name = st.sidebar.text_input("Your Target Goal (e.g., Goa Trip)", value="Trip to Goa 🌴")
user_goal_cost = st.sidebar.number_input("Goal Cost (₹)", value=18000, step=1000)

user_mood = st.sidebar.selectbox("How are you feeling right now?", ["Calm / Focused", "Stressed / Exhausted", "Bored / Just Scrolling", "Excited / Impulsive"])

# Calculate Daily Allowance
daily_allowance = round(st.session_state.monthly_budget_pool / max(1, st.session_state.days_left_in_month))

st.sidebar.divider()
st.sidebar.metric(label="🔥 Mindful Streak", value=f"{st.session_state.mindful_streak} Days Safe")
st.sidebar.metric(label="Today's Safe Daily Limit", value=f"₹{daily_allowance}")

# --- MAIN SCREEN: Purchase Simulation ---
st.subheader("Simulate Purchase Transaction")

purchase_type = st.radio("Select Purchase Category:", ["Micro-Spend (Food/Shopping)", "Macro-Decision (Laptop/Gadget/EMI)"])

if purchase_type == "Micro-Spend (Food/Shopping)":
    item_name = st.text_input("Item Description", value="Swiggy / Casual Shopping")
    item_cost = st.number_input("Cost (₹)", value=350, step=50)
else:
    item_name = st.text_input("Item Description", value="Flash Sale Gadget (Impulse Buy)")
    item_cost = st.number_input("Cost (₹)", value=3500, step=500)

# Trigger Button
if st.button("Attempt Checkout"):
    st.divider()
    
    is_over_daily_limit = item_cost > daily_allowance
    is_emotional_spend = user_mood in ["Stressed / Exhausted", "Bored / Just Scrolling", "Excited / Impulsive"]
    is_risky = is_over_daily_limit or (is_emotional_spend and item_cost > 200)
    
    goal_impact_percentage = round((item_cost / user_goal_cost) * 100, 1)
    goal_impact_fraction = min(1.0, item_cost / user_goal_cost)
    
    if is_risky:
        st.warning("⏳ **Hold on a second...** Evaluating your daily pacing and emotional state.")
        with st.spinner("Nudge AI analyzing psychological triggers..."):
            time.sleep(3)
            
        st.error(f"🛑 **Intervention Triggered: High Impulse Risk!**")
        st.write(f"You want to spend **₹{item_cost}** on *{item_name}*. Your safe daily limit is **₹{daily_allowance}**.")
        
        # Visual Impact Meter
        st.write(f"📊 **Impact on your 3-Month '{user_goal_name}':** Consumes **{goal_impact_percentage}%** of your target pool.")
        st.progress(goal_impact_fraction)
        
        st.info(f"💡 **AI Rebalancing & Vault Notice:** Proceeding will shrink your monthly pool and adjust your future daily limits. Furthermore, high-risk items can be placed in our **24-Hour Cool-Down Vault** to stop late-night regret.")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Lock in 24-Hr Vault 🛡️"):
                st.success(f"🔒 Item secured in the Vault! You have 24 hours to think about it. Streak protected!")
                st.session_state.mindful_streak += 1
        with c2:
            if st.button("Save & Cancel 🎉"):
                st.success(f"🎉 Amazing choice! Your streak grew, and your **{user_goal_name}** is safe.")
                st.session_state.mindful_streak += 1
        with c3:
            if st.button("Proceed Anyway ⚠️"):
                st.session_state.monthly_budget_pool = max(0, st.session_state.monthly_budget_pool - item_cost)
                st.session_state.mindful_streak = 0  # Reset streak on impulse override
                st.warning(f"⚠️ Purchase approved. Monthly pool lowered. Streak reset to 0.")
                
    else:
        st.success("✅ **Within Daily Limit!**")
        st.write(f"This ₹{item_cost} purchase fits nicely inside your ₹{daily_allowance} daily allowance. Enjoy it guilt-free!")
        st.session_state.monthly_budget_pool = max(0, st.session_state.monthly_budget_pool - item_cost)
        