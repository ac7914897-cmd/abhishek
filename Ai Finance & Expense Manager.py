import datetime
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Finance & Expense Manager", page_icon="💰", layout="wide"
)

st.title("🤖 Advanced AI Finance & Expense Manager")
st.markdown(
    "Aapka smart assistant jo transactions analyze karta hai, charts banata"
    " hai, forecasting karta hai, aur receipts generate karta hai!"
)

# Initialize Session State for Expenses
if "expenses" not in st.session_state:
  st.session_state.expenses = [
      {
          "id": 1,
          "date": "2026-05-01",
          "title": "Grocery Shopping",
          "amount": 3500,
          "category": "Groceries",
      },
      {
          "id": 2,
          "date": "2026-05-05",
          "title": "Office Cab",
          "amount": 600,
          "category": "Transport",
      },
      {
          "id": 3,
          "date": "2026-05-10",
          "title": "Restaurant Dinner",
          "amount": 1500,
          "category": "Food & Dining",
      },
      {
          "id": 4,
          "date": "2026-05-15",
          "title": "Electricity Bill",
          "amount": 2200,
          "category": "Utilities",
      },
      {
          "id": 5,
          "date": "2026-05-20",
          "title": "Movie Tickets",
          "amount": 800,
          "category": "Entertainment",
      },
  ]


# Simulated AI Categorization Function
def ai_categorize(desc):
  d = desc.lower()
  if any(w in d for w in ["khana", "dinner", "lunch", "restaurant", "cafe"]):
    return "Food & Dining"
  elif any(w in d for w in ["cab", "uber", "metro", "petrol", "train"]):
    return "Transport"
  elif any(w in d for w in ["grocery", "sabzi", "dukaan", "supermarket"]):
    return "Groceries"
  elif any(w in d for w in ["bijli", "electricity", "water", "bill", "wifi"]):
    return "Utilities"
  elif any(w in d for w in ["movie", "netflix", "game", "party"]):
    return "Entertainment"
  else:
    return "Miscellaneous"


# Sidebar for Adding New Expense
st.sidebar.header("➕ Naya Transaction Jodein")
with st.sidebar.form("expense_form"):
  desc = st.text_input(
      "Description (Jaise: 'Coffee 200 ki')", placeholder="Yahan likhein..."
  )
  amount = st.number_input("Amount (₹)", min_value=1.0, step=10.0)
  date = st.date_input("Date", datetime.date.today())
  submit = st.form_submit_button("Add & Process AI")

  if submit and desc:
    category = ai_categorize(desc)
    new_id = len(st.session_state.expenses) + 1
    st.session_state.expenses.append({
        "id": new_id,
        "date": str(date),
        "title": desc,
        "amount": amount,
        "category": category,
    })
    st.sidebar.success(f"Added! AI ne category **{category}** assign ki hai.")

# Load Data into DataFrame
df = pd.DataFrame(st.session_state.expenses)

# Main Application Tabs for the 4 Key Features
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 1. Transaction Analysis",
    "📈 2. Expense Charts",
    "🔮 3. Expense Forecasting",
    "🧾 4. Bill / Receipt Generator",
])

# -------------------------------------------------------------
# TAB 1: Transaction Analysis
# -------------------------------------------------------------
with tab1:
  st.subheader("🔍 AI Transaction Analysis & Summary")
  if not df.empty:
    total_spent = df["amount"].sum()
    avg_spent = df["amount"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spent", f"₹ {total_spent:,.2f}")
    col2.metric("Total Transactions", len(df))
    col3.metric("Average per Txn", f"₹ {avg_spent:,.2f}")

    st.markdown("### 📋 Complete Transaction Ledger")
    st.dataframe(df, use_container_width=True)

    # AI Insights
    st.markdown("### 🤖 AI Smart Insight")
    max_cat = df.groupby("category")["amount"].sum().idxmax()
    max_val = df.groupby("category")["amount"].sum().max()
    st.info(
        f"💡 **AI Recommendation:** Aapka sabse zyada kharcha **{max_cat}**"
        f" category mein hua hai (₹ {max_val:,.2f}). Is par control karne se"
        " savings improve hogi."
    )
  else:
    st.warning("Abhi tak koi transaction nahi hai.")

# -------------------------------------------------------------
# TAB 2: Expense Charts
# -------------------------------------------------------------
with tab2:
  st.subheader("📊 Category-wise Expense Visualizations")
  if not df.empty:
    cat_df = df.groupby("category")["amount"].sum().reset_index()

    c1, c2 = st.columns(2)
    with c1:
      st.markdown("#### Bar Chart View")
      st.bar_chart(cat_df.set_index("category"))

    with c2:
      st.markdown("#### Pie Chart View")
      fig, ax = plt.subplots()
      ax.pie(
          cat_df["amount"],
          labels=cat_df["category"],
          autopct="%1.1f%%",
          startangle=90,
          colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"],
      )
      ax.axis("equal")
      st.pyplot(fig)
  else:
    st.info("Charts dikhane ke liye data add karein.")

# -------------------------------------------------------------
# TAB 3: Expense Forecasting
# -------------------------------------------------------------
with tab3:
  st.subheader("🔮 AI Expense Forecasting & Predictions")
  if not df.empty:
    st.markdown(
        "AI aapke spending trends ko analyze karke agle mahine ke kharche"
        " predict karta hai:"
    )

    current_total = df["amount"].sum()
    predicted_next_month = current_total * 1.12

    col1, col2 = st.columns(2)
    col1.metric("Current Period Total", f"₹ {current_total:,.2f}")
    # Completely clean metric without delta_value / conflicting arguments
    col2.metric("Projected Next Month Spend", f"₹ {predicted_next_month:,.2f}")

    st.warning(
        "⚠️ **AI Alert:** Forecast ke mutabiq aapka agla mahina thoda costly"
        " ho sakta hai. Suggestion: Entertainment aur Dining par 15% kam kharch"
        " karein."
    )
  else:
    st.info("Forecast ke liye transactions add karein.")

# -------------------------------------------------------------
# TAB 4: Bill / Receipt Generation
# -------------------------------------------------------------
with tab4:
  st.subheader("🧾 Automated Bill & Receipt Generator")
  if not df.empty:
    st.markdown(
        "Kisi bhi specific transaction ke liye digital receipt generate karein"
        " aur download karein:"
    )

    selected_title = st.selectbox(
        "Transaction Select Karein:", df["title"].tolist()
    )
    selected_row = df[df["title"] == selected_title].iloc[0]

    receipt_content = f"""
    ========================================
        AI FINANCE MANAGER - DIGITAL RECEIPT
    ========================================
    Transaction ID : TXN-{selected_row['id']}
    Date           : {selected_row['date']}
    Description    : {selected_row['title']}
    Category       : {selected_row['category']}
    ----------------------------------------
    Total Amount   : ₹ {selected_row['amount']:,.2f}
    ----------------------------------------
    Status         : PAID & VERIFIED BY AI
    Thank you for managing expenses smartly!
    ========================================
    """

    st.text(receipt_content)

    st.download_button(
        label="📥 Download Receipt (.txt)",
        data=receipt_content,
        file_name=f"receipt_{selected_row['id']}.txt",
        mime="text/plain",
    )
  else:
    st.info("Receipt generate karne ke liye data add karein.")