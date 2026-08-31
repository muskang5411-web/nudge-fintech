import streamlit as st
import time
from datetime import datetime, timedelta

# ============================================================
# NUDGE — AI Behavioral Firewall
# Submission-ready Streamlit prototype for BUILD$BANK
# ============================================================

st.set_page_config(
    page_title="NUDGE — AI Behavioral Firewall",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1250px;}
    .hero {
        padding: 1.4rem 1.6rem;
        border: 1px solid rgba(128,128,128,.25);
        border-radius: 20px;
        margin-bottom: 1rem;
    }
    .hero h1 {margin: 0; font-size: 2.35rem;}
    .hero p {margin: .35rem 0 0; font-size: 1.05rem; opacity: .78;}
    .mini {font-size:.82rem; opacity:.68; text-transform:uppercase; letter-spacing:.08em;}
    .risk-box {
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255, 80, 80, .35);
        background: rgba(255, 80, 80, .06);
        margin: .8rem 0 1rem;
    }
    .safe-box {
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(60, 180, 110, .35);
        background: rgba(60, 180, 110, .06);
        margin: .8rem 0 1rem;
    }
    .metric-card {
        padding: 1rem 1.05rem;
        border: 1px solid rgba(128,128,128,.22);
        border-radius: 16px;
        min-height: 110px;
    }
    .metric-value {font-size:1.65rem; font-weight:700; margin-top:.2rem;}
    .metric-label {font-size:.85rem; opacity:.7;}
    .signal {
        padding: .65rem .8rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,.18);
        margin-bottom: .5rem;
    }
    .footer {
        text-align:center; opacity:.55; font-size:.8rem;
        padding-top:1.5rem;
    }
    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,.20);
        padding: 12px;
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session state
# -----------------------------
defaults = {
    "monthly_budget_pool": 15000.0,
    "days_left_in_month": 30,
    "mindful_streak": 4,
    "goal_saved": 10000.0,
    "vault": [],
    "transactions": [],
    "last_result": None,
    "last_purchase": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Sidebar: profile
# -----------------------------
with st.sidebar:
    st.markdown("## 💡 NUDGE")
    st.caption("AI Behavioral Firewall")
    st.divider()

    st.markdown("### Your financial context")
    monthly_income = st.number_input(
        "Monthly income (₹)", min_value=0, value=30000, step=1000
    )
    monthly_savings_goal = st.number_input(
        "Monthly savings goal (₹)", min_value=0, value=10000, step=500
    )

    user_goal_name = st.text_input(
        "Target goal", value="Trip to Goa 🌴"
    )
    user_goal_cost = st.number_input(
        "Goal cost (₹)", min_value=1, value=18000, step=1000
    )

    user_mood = st.selectbox(
        "How are you feeling?",
        [
            "Calm / Focused",
            "Stressed / Exhausted",
            "Bored / Just Scrolling",
            "Excited / Impulsive",
        ],
    )

    st.divider()
    daily_allowance = round(
        st.session_state.monthly_budget_pool /
        max(1, st.session_state.days_left_in_month)
    )

    st.metric("🔥 Mindful streak", f"{st.session_state.mindful_streak} days")
    st.metric("🛡️ Safe daily limit", f"₹{daily_allowance:,}")
    st.metric("💰 Flexible pool", f"₹{st.session_state.monthly_budget_pool:,.0f}")

    if st.button("↺ Reset demo", use_container_width=True):
        st.session_state.monthly_budget_pool = 15000.0
        st.session_state.days_left_in_month = 30
        st.session_state.mindful_streak = 4
        st.session_state.goal_saved = 10000.0
        st.session_state.vault = []
        st.session_state.transactions = []
        st.session_state.last_result = None
        st.session_state.last_purchase = None
        st.rerun()

# -----------------------------
# Header
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="mini">BUILD$BANK • FINTECH PROTOTYPE</div>
    <h1>💡 NUDGE</h1>
    <p><b>Pause before you pay.</b> A real-time behavioral firewall for digital spending.</p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Dashboard cards
# -----------------------------
goal_progress = min(1.0, st.session_state.goal_saved / max(1, user_goal_cost))
remaining_goal = max(0, user_goal_cost - st.session_state.goal_saved)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("💰 Flexible pool", f"₹{st.session_state.monthly_budget_pool:,.0f}")
with c2:
    st.metric("🛡️ Safe today", f"₹{daily_allowance:,}")
with c3:
    st.metric("🎯 Goal remaining", f"₹{remaining_goal:,.0f}")
with c4:
    st.metric("🔥 Mindful streak", f"{st.session_state.mindful_streak} days")

st.progress(goal_progress, text=f"🎯 {user_goal_name} — {goal_progress*100:.0f}% funded")

# -----------------------------
# Main interaction
# -----------------------------
st.markdown("## 💳 Simulate a payment")
st.caption("See what NUDGE does when a user is about to make a purchase.")

left, right = st.columns([1.25, 1])

with left:
    purchase_type = st.radio(
        "Purchase category",
        ["Micro-spend • Food / Shopping", "Macro-decision • Gadget / EMI"],
        horizontal=True,
    )

    if purchase_type.startswith("Micro"):
        item_name = st.text_input(
            "What are you buying?",
            value="Swiggy / Casual Shopping",
        )
        item_cost = st.number_input(
            "Purchase amount (₹)",
            min_value=0,
            value=350,
            step=50,
        )
    else:
        item_name = st.text_input(
            "What are you buying?",
            value="Flash Sale Gadget",
        )
        item_cost = st.number_input(
            "Purchase amount (₹)",
            min_value=0,
            value=3500,
            step=500,
        )

    attempt = st.button(
        "⚡ Attempt Payment",
        type="primary",
        use_container_width=True,
    )

with right:
    st.markdown("### What NUDGE checks")
    st.markdown("""
    <div class="signal">💸 <b>Budget pressure</b><br><span class="metric-label">Is this above today's safe pace?</span></div>
    <div class="signal">🧠 <b>Self-reported mood</b><br><span class="metric-label">Is the user feeling impulsive or depleted?</span></div>
    <div class="signal">🎯 <b>Goal impact</b><br><span class="metric-label">How much of the target could this consume?</span></div>
    <div class="signal">⏱️ <b>Cooling-off option</b><br><span class="metric-label">Can the decision wait 24 hours?</span></div>
    """, unsafe_allow_html=True)

# -----------------------------
# Risk engine
# -----------------------------
def calculate_risk(cost, allowance, mood, category):
    score = 0
    reasons = []

    if cost > allowance:
        score += 45
        reasons.append(("Budget pressure", "High", "Purchase exceeds today's safe spending pace."))
    else:
        score += 10
        reasons.append(("Budget pressure", "Low", "Purchase fits inside today's safe spending pace."))

    emotional = mood in [
        "Stressed / Exhausted",
        "Bored / Just Scrolling",
        "Excited / Impulsive",
    ]
    if emotional:
        score += 30
        reasons.append(("Mood signal", "Elevated", f"Current mood: {mood}."))
    else:
        reasons.append(("Mood signal", "Low", "User reports feeling calm/focused."))

    if category.startswith("Macro"):
        score += 15
        reasons.append(("Purchase size", "Significant", "A larger discretionary decision deserves extra friction."))
    elif cost > 200:
        score += 10
        reasons.append(("Purchase size", "Moderate", "Above the prototype's micro-spend comfort threshold."))
    else:
        reasons.append(("Purchase size", "Low", "Small discretionary purchase."))

    if cost > allowance * 2:
        score += 10
        reasons.append(("Pacing shock", "High", "Amount is more than twice today's safe limit."))

    score = min(score, 100)

    if score >= 60:
        level = "HIGH"
    elif score >= 35:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, reasons

if attempt:
    st.divider()

    risk_score, risk_level, reasons = calculate_risk(
        item_cost, daily_allowance, user_mood, purchase_type
    )

    goal_impact_percentage = round(
        (item_cost / max(1, user_goal_cost)) * 100, 1
    )
    goal_impact_fraction = min(
        1.0, item_cost / max(1, user_goal_cost)
    )

    st.session_state.last_purchase = {
        "item": item_name,
        "cost": item_cost,
        "risk": risk_level,
        "score": risk_score,
    }

    if risk_level == "HIGH":
        st.markdown(f"""
        <div class="risk-box">
            <div class="mini">NUDGE RISK ENGINE</div>
            <h2 style="margin:.25rem 0;">🛑 High impulse risk</h2>
            <p style="margin:0;">NUDGE detected multiple signals worth pausing for.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Analyzing spending signals…"):
            time.sleep(1.2)

        st.write(
            f"You are about to spend **₹{item_cost:,.0f}** on **{item_name}**."
        )

        # Risk summary
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Risk score", f"{risk_score}/100")
        r2.metric("Daily limit", f"₹{daily_allowance:,}")
        r3.metric("Goal impact", f"{goal_impact_percentage}%")
        r4.metric("Mood", "Elevated")

        st.markdown("### 🔎 Why NUDGE stepped in")
        for name, status, explanation in reasons:
            st.markdown(
                f"**{name} — {status}**  \n{explanation}"
            )

        st.markdown("### 🎯 Impact on your goal")
        st.write(
            f"This purchase would consume **{goal_impact_percentage}%** "
            f"of your **{user_goal_name}** target."
        )
        st.progress(goal_impact_fraction)

        st.info(
            "💡 **NUDGE recommendation:** introduce friction instead of "
            "blocking the payment. A 24-hour Cool-Down Vault gives you time "
            "to decide without losing the purchase opportunity."
        )

        st.markdown("### Choose your next move")
        a, b, c = st.columns(3)

        with a:
            if st.button("🛡️ Cool down for 24 hours", use_container_width=True):
                unlock_at = datetime.now() + timedelta(hours=24)
                st.session_state.vault.append({
                    "item": item_name,
                    "cost": item_cost,
                    "unlock": unlock_at,
                })
                st.session_state.mindful_streak += 1
                st.session_state.transactions.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "item": item_name,
                    "amount": item_cost,
                    "status": "Vault",
                })
                st.session_state.last_result = "vault"
                st.success("🔒 Purchase placed in the 24-hour Vault. Streak protected!")
                st.rerun()

        with b:
            if st.button("🎯 Cancel & protect goal", use_container_width=True):
                st.session_state.mindful_streak += 1
                st.session_state.transactions.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "item": item_name,
                    "amount": item_cost,
                    "status": "Avoided",
                })
                st.session_state.last_result = "cancel"
                st.success(
                    f"🎉 Great decision. Your {user_goal_name} stays on track."
                )
                st.rerun()

        with c:
            if st.button("⚠️ Proceed anyway", use_container_width=True):
                st.session_state.monthly_budget_pool = max(
                    0, st.session_state.monthly_budget_pool - item_cost
                )
                st.session_state.mindful_streak = 0
                st.session_state.transactions.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "item": item_name,
                    "amount": item_cost,
                    "status": "Purchased",
                })
                st.session_state.last_result = "purchase"
                st.warning(
                    "Payment approved. Your flexible pool and mindful streak were updated."
                )
                st.rerun()

    elif risk_level == "MEDIUM":
        st.markdown("""
        <div class="risk-box">
            <div class="mini">NUDGE RISK ENGINE</div>
            <h2 style="margin:.25rem 0;">🟠 Worth a quick pause</h2>
            <p style="margin:0;">This purchase isn't automatically blocked, but NUDGE sees some friction signals.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write(
            f"₹{item_cost:,.0f} is **{goal_impact_percentage}%** of your "
            f"{user_goal_name} target."
        )
        st.progress(goal_impact_fraction)

        if st.button("👍 Continue with payment", use_container_width=True):
            st.session_state.monthly_budget_pool = max(
                0, st.session_state.monthly_budget_pool - item_cost
            )
            st.session_state.transactions.append({
                "time": datetime.now().strftime("%H:%M"),
                "item": item_name,
                "amount": item_cost,
                "status": "Purchased",
            })
            st.success("Payment approved — NUDGE recorded the decision.")
            st.rerun()

    else:
        st.markdown("""
        <div class="safe-box">
            <div class="mini">NUDGE RISK ENGINE</div>
            <h2 style="margin:.25rem 0;">✅ Low risk — you're good</h2>
            <p style="margin:0;">This purchase fits your current spending pace.</p>
        </div>
        """, unsafe_allow_html=True)

        st.write(
            f"₹{item_cost:,.0f} fits inside your ₹{daily_allowance:,} "
            "safe daily limit. Enjoy it guilt-free. 🎉"
        )

        if st.button("💳 Confirm payment", use_container_width=True):
            st.session_state.monthly_budget_pool = max(
                0, st.session_state.monthly_budget_pool - item_cost
            )
            st.session_state.transactions.append({
                "time": datetime.now().strftime("%H:%M"),
                "item": item_name,
                "amount": item_cost,
                "status": "Purchased",
            })
            st.success("Payment approved and budget updated.")
            st.rerun()

# -----------------------------
# Vault + activity
# -----------------------------
st.divider()
tab1, tab2 = st.tabs(["🛡️ Cool-Down Vault", "📜 Recent activity"])

with tab1:
    if not st.session_state.vault:
        st.info(
            "Your Vault is empty. When NUDGE detects a high-risk purchase, "
            "you can park it here for 24 hours."
        )
    else:
        for i, item in enumerate(st.session_state.vault):
            unlock = item["unlock"]
            remaining = max(timedelta(0), unlock - datetime.now())
            hours = int(remaining.total_seconds() // 3600)
            mins = int((remaining.total_seconds() % 3600) // 60)

            st.markdown(
                f"**{item['item']}** — ₹{item['cost']:,.0f}  \n"
                f"🔒 Available after cooldown: **{hours}h {mins}m**"
            )

with tab2:
    if not st.session_state.transactions:
        st.caption("No decisions yet — try the payment simulator above.")
    else:
        for tx in reversed(st.session_state.transactions[-8:]):
            icon = {
                "Vault": "🛡️",
                "Avoided": "🎯",
                "Purchased": "💳",
            }.get(tx["status"], "•")
            st.write(
                f"{icon} **{tx['item']}** — ₹{tx['amount']:,.0f} "
                f"· {tx['status']} · {tx['time']}"
            )

# -----------------------------
# Product / pitch note
# -----------------------------
st.divider()
st.markdown("### 🚀 What makes NUDGE different?")
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("**1. Intervenes before payment**")
    st.caption("NUDGE adds a moment of reflection exactly when an impulse happens.")

with p2:
    st.markdown("**2. Personalized, not punitive**")
    st.caption("It uses budget pace, purchase size and self-reported mood to tailor friction.")

with p3:
    st.markdown("**3. Protects long-term goals**")
    st.caption("Every decision is translated into a concrete impact on what the user cares about.")

st.markdown(
    '<div class="footer">NUDGE is a hackathon prototype. Risk scoring is a transparent demo model, not financial advice.</div>',
    unsafe_allow_html=True,
)
