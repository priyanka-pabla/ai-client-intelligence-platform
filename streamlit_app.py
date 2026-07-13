import streamlit as st
import pandas as pd
import os
import plotly.express as px
from utils.scoring import calculate_lead_score
from utils.date_utils import parse_submitted_at
from utils.date_utils import calculate_reply_deadline
from openai import OpenAI
from datetime import datetime
import smtplib
from email.message import EmailMessage

client = OpenAI()

st.set_page_config(
    page_title="AI Client Intelligence Platform",
    page_icon="🤖",
    layout="wide"
)


# PREMIUM UI STYLE
st.markdown("""
<style>
.main {
    background-color: #f8fafc;
}

.hero-box {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero-title {
    font-size: 36px;
    font-weight: 800;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 18px;
    color: #e2e8f0;
}




.card {
    background-color: white;
    padding: 24px;
    border-radius: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    min-height: 210px;
    text-align: center;
    border: 1px solid #e5e7eb;
}

.card h4 {
    height: 52px;
    margin-bottom: 8px;
}

.card p {
    margin: 0;
    line-height: 1.5;
    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-box">
    <div class="hero-title">🤖 AI Client Intelligence Platform</div>
    <div class="hero-subtitle">
        Helping businesses automate customer engagement, qualify leads, and make smarter decisions with AI.
    </div>
</div>
""", unsafe_allow_html=True)


st.markdown("## 💼 Our Services")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <h2>🤖</h2>
        <h4>AI Chatbots</h4>
        <p>Smart AI assistants for customer support and lead generation.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h2>🌐</h2>
        <h4>Website Development</h4>
        <p>Modern, responsive websites designed to convert visitors into customers.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h2>⚙️</h2>
        <h4>Business Automation</h4>
        <p>Automate repetitive workflows to improve efficiency and save valuable time.</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <h2>📊</h2>
        <h4>Data Dashboards</h4>
        <p>Interactive dashboards that transform business data into actionable insights.</p>
    </div>
    """, unsafe_allow_html=True)



    

with st.sidebar:

    st.markdown("## 👩‍💻 Built by")

    st.markdown("""
### Priyanka Pabla

**Freelance AI Developer**

📍 Dubai, UAE

Helping businesses automate customer engagement and business operations using AI.

---

### 💡 Services

✅ AI Chatbots

✅ Website Development

✅ Business Automation

✅ Data Dashboards

---

📧 choudhary.pri@gmail.com

💬 Available for freelance projects
""")

    st.markdown("---")

    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:

        admin_password = st.text_input(
            "Enter Admin Password",
            type="password"
        )

        if admin_password == st.secrets["ADMIN_PASSWORD"]:
            st.session_state.admin_logged_in = True
            st.success("✅ Admin access granted")
            st.rerun()

        elif admin_password:
            st.error("❌ Incorrect password")

    else:
        st.success("✅ Admin Logged In")

        if st.button("Logout"):
            st.session_state.admin_logged_in = False
            st.rerun()

    admin_mode = st.session_state.admin_logged_in


st.markdown("## 🚀 Let's Build Your AI Solution")
st.caption("Complete the form below and we'll recommend the best AI solution for your business.")







def send_email(to_email, subject, text_body, html_body=None):
    try:
        sender_email = st.secrets["EMAIL_ADDRESS"]
        sender_password = st.secrets["EMAIL_APP_PASSWORD"]

        msg = EmailMessage()
        msg["From"] = sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.set_content(text_body)

        if html_body:
            msg.add_alternative(html_body, subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return True

    except Exception as e:
        st.error(f"Email sending failed: {e}")
        return False



with st.form("lead_form"):
    company = st.text_input("Company Name")
    name = st.text_input("Your Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone / WhatsApp")

    service = st.selectbox(
        "Service Interested In",
        [
            "AI Chatbots",
            "Website Development",
            "Business Automation",
            "Data Dashboards"
        ]
    )

    message = st.text_area("Tell us about your project")

    submitted = st.form_submit_button("🚀 Get Started")






if submitted:

    if not company or not name or not email or not phone or not message:
        st.warning("Please fill in all fields before submitting.")

    else:
        lead_score = calculate_lead_score(message, service)

        submitted_at = datetime.now().strftime("%d-%m-%Y %I:%M %p")

        if lead_score == "Hot Lead":
            suggested_action = "🔥 Call this lead within 1 hour."

        elif lead_score == "Warm Lead":
            suggested_action = "✨ Send follow-up email within 24 hours."

        else:
            suggested_action = "❄️ Add lead to nurture campaign."

        lead_data = {
            "Submitted At": submitted_at,
            "Company": company,
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Service": service,
            "Message": message,
            "Lead Score": lead_score,
            "Lead Status": "New"
        }

        df = pd.DataFrame([lead_data])

        os.makedirs("data", exist_ok=True)

        file_exists = os.path.exists("data/leads.csv")

        df.to_csv(
            "data/leads.csv",
            mode="a",
            header=not file_exists,
            index=False
        )


        client_text_body = f"""
        Hi {name},

        Thank you for contacting AI & Automation Solutions.

        We have received your consultation request for {service}.

        Our team will review your details and contact you shortly.

        Best regards,
        AI & Automation Solutions
        """

        client_html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color:#f8fafc; padding:30px;">
        <div style="max-width:600px; margin:auto; background:white; border-radius:14px; padding:28px; border:1px solid #e5e7eb;">
        
            <h2 style="color:#1e3a8a;">Thank you, {name}!</h2>
        
            <p style="font-size:16px; color:#334155;">
                We have received your consultation request for:
            </p>

            <div style="background:#eff6ff; padding:16px; border-radius:10px; margin:18px 0;">
            <strong style="color:#1d4ed8;">Service Requested:</strong> {service}
            </div>

            <p style="font-size:15px; color:#475569;">
                Our team will review your requirements and contact you shortly with the next steps.
            </p>

            <hr style="border:none; border-top:1px solid #e5e7eb; margin:24px 0;">

            <p style="font-size:14px; color:#64748b;">
                Best regards,<br>
                <strong>AI & Automation Solutions</strong><br>
                Smart chatbot, automation, and business intelligence solutions.
            </p>
       </div>
       </body>
       </html>
       """




        send_email(
        email,
        "Your consultation request has been received",
        client_text_body,
        client_html_body
        )







        admin_text_body = f"""
        New lead received!
        
        Company: {company}
        Name: {name}
        Email: {email}
        Phone: {phone}
        Service: {service}
        Lead Score: {lead_score}

        Message:
        {message}

        Suggested Action:
        {suggested_action}
        """


        if lead_score == "Hot Lead":
            score_bg = "#fee2e2"
            score_color = "#991b1b"

        elif lead_score == "Warm Lead":
            score_bg = "#fef3c7"
            score_color = "#92400e"

        else:
            score_bg = "#dbeafe"
            score_color = "#1e40af"




        

        admin_html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background-color:#f8fafc; padding:30px;">
        <div style="max-width:650px; margin:auto; background:white; border-radius:14px; padding:28px; border:1px solid #e5e7eb;">
        
            <h2 style="color:#0f172a;">🚨 New Lead Received</h2>

        <div style="background:{score_bg}; color:{score_color}; padding:14px; border-radius:10px; margin:18px 0;">
            <strong>Lead Score:</strong> {lead_score}
        </div>

        <table style="width:100%; border-collapse:collapse; font-size:15px;">
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;"><strong>Company</strong></td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{company}</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;"><strong>Name</strong></td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{name}</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;"><strong>Email</strong></td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{email}</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;"><strong>Phone</strong></td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{phone}</td>
            </tr>
            <tr>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;"><strong>Service</strong></td>
                <td style="padding:10px; border-bottom:1px solid #e5e7eb;">{service}</td>
            </tr>
        </table>

        <h3 style="margin-top:24px; color:#1e3a8a;">Client Message</h3>

        <div style="background:#f1f5f9; padding:16px; border-radius:10px; color:#334155;">
            {message}
        </div>

        <p style="margin-top:24px; font-size:14px; color:#475569;">
            <strong>Suggested Action:</strong> {suggested_action}
        </p>
        </div>
      </body>
      </html>
      """

        send_email(
            st.secrets["ADMIN_EMAIL"],
            f"🚨 New {lead_score}: {service}",
            admin_text_body,
            admin_html_body
        )







        st.markdown("""
    <div style="
        background-color:#dcfce7;
        padding:18px;
        border-radius:12px;
        color:#166534;
        font-weight:600;
        margin-top:15px;
    ">
    ✅ Thank you! Your consultation request has been submitted successfully.
    </div>
    """, unsafe_allow_html=True)


    
if admin_mode:
    st.markdown("---")
    st.subheader("📊 Admin Intelligence Dashboard")

    try:
        leads_df = pd.read_csv("data/leads.csv")

        leads_df["Submitted DateTime"] = leads_df["Submitted At"].apply(parse_submitted_at)

        leads_df["Submitted At"] = leads_df["Submitted DateTime"].dt.strftime(
            "%d-%m-%Y %I:%M %p"
        )

        leads_df["Lead Score"] = leads_df.apply(
            lambda row: calculate_lead_score(
                row["Message"],
                row["Service"]
            ),
            axis=1
        )
        
        leads_df["Submitted DateTime"] = leads_df["Submitted At"].apply(parse_submitted_at)

        leads_df["Submitted At"] = leads_df["Submitted DateTime"].dt.strftime(
            "%d-%m-%Y %I:%M %p"
        )

        total_leads = len(leads_df)
        hot_leads = len(leads_df[leads_df["Lead Score"] == "Hot Lead"])
        warm_leads = len(leads_df[leads_df["Lead Score"] == "Warm Lead"])
        cold_leads = len(leads_df[leads_df["Lead Score"] == "Cold Lead"])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Leads", total_leads)
        col2.metric("Hot Leads", hot_leads)
        col3.metric("Warm Leads", warm_leads)
        col4.metric("Cold Leads", cold_leads)

        conversion_rate = round((hot_leads / total_leads) * 100, 1) if total_leads > 0 else 0

        st.success(f"🎯 High-Priority Leads: {conversion_rate}%")

        st.markdown("### 📈 Lead Analytics")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            service_counts = leads_df["Service"].value_counts().reset_index()
            service_counts.columns = ["Service", "Count"]

            fig_service = px.pie(
                service_counts,
                names="Service",
                values="Count",
                title="Service Demand Breakdown",
                hole=0.45
            )

            st.plotly_chart(fig_service, use_container_width=True)

        with chart_col2:
            score_counts = leads_df["Lead Score"].value_counts().reset_index()
            score_counts.columns = ["Lead Score", "Count"]

            fig_score = px.bar(
                score_counts,
                x="Lead Score",
                y="Count",
                color="Lead Score",
                title="Lead Quality Overview",
                text="Count",
                color_discrete_map={
                "Hot Lead": "red",
                "Warm Lead": "lightblue",
                "Cold Lead": "darkblue"
               }
            )

            st.plotly_chart(fig_score, use_container_width=True)

            csv = leads_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="📥 Download Leads Report",
                data=csv,
                file_name="client_leads_report.csv",
                mime="text/csv"
            )

            st.markdown("### 🔔 Recent Activity Feed")

            recent_leads = leads_df.tail(5).sort_values(by="Submitted At", ascending=False)

            for index, row in recent_leads.iterrows():
                if row["Lead Score"] == "Hot Lead":
                    icon = "🔥"
                elif row["Lead Score"] == "Warm Lead":
                    icon = "✨"
                else:
                    icon = "❄️"

                st.markdown(
                    f"""
                    <div style="
                        background-color:#ffffff;
                        padding:14px;
                        border-radius:12px;
                        margin-bottom:10px;
                        border-left:5px solid #2563eb;
                        box-shadow:0 3px 10px rgba(0,0,0,0.06);
                    ">
                        {icon} <b>{row["Name"]}</b> submitted a 
                        <b>{row["Lead Score"]}</b> inquiry for 
                        <b>{row["Service"]}</b><br>
                        <small>📅 {row["Submitted At"]}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )

        st.markdown("### 🧠 AI Business Insights")

        top_service = leads_df["Service"].value_counts().idxmax()

        st.info(f"📌 Most requested service: {top_service}")

        if hot_leads > warm_leads:
            st.success("🔥 Hot leads are dominating. High conversion potential detected.")

        elif warm_leads > hot_leads:
            st.warning("✨ Many warm leads detected. Follow-up campaigns recommended.")

        else:
            st.info("📊 Lead quality distribution is balanced.")


            
        st.markdown("### 📌 Update Lead Status")

        lead_options = [
            f"{row['Name']} ({row['Email']})"
            for _, row in leads_df.iterrows()
        ]

        selected_lead = st.selectbox(
            "Select Lead",
            lead_options
        )

        new_status = st.selectbox(
            "Update Status",
            ["New", "Contacted", "Proposal Sent", "Won", "Lost"]
        )



        if st.button("Save Lead Status"):

            selected_email = selected_lead.split("(")[1].replace(")", "")

            leads_df.loc[
                leads_df["Email"] == selected_email,
                "Lead Status"
            ] = new_status

            leads_df.to_csv("data/leads.csv", index=False)

            st.success(f"Lead status updated to {new_status}")
            st.rerun()   



        st.markdown("### 🔍 CRM Filters")

        search_query = st.text_input(
            "Search Lead",
            placeholder="Search by name, email, phone, service, or message..."
        )

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:
            score_filter = st.selectbox(
                "Filter by Lead Score",
                ["All", "Hot Lead", "Warm Lead", "Cold Lead"]
            )

        with filter_col2:
            service_filter = st.selectbox(
                "Filter by Service",
                ["All"] + list(leads_df["Service"].unique())
            )

        filtered_df = leads_df.copy()

        if search_query:
            search_query = search_query.lower()

            filtered_df = filtered_df[
                filtered_df["Name"].astype(str).str.lower().str.contains(search_query) |
                filtered_df["Email"].astype(str).str.lower().str.contains(search_query) |
                filtered_df["Phone"].astype(str).str.lower().str.contains(search_query) |
                filtered_df["Service"].astype(str).str.lower().str.contains(search_query) |
                filtered_df["Message"].astype(str).str.lower().str.contains(search_query)
            ]

        if score_filter != "All":
            filtered_df = filtered_df[
                filtered_df["Lead Score"] == score_filter
            ]

        if service_filter != "All":
            filtered_df = filtered_df[
                filtered_df["Service"] == service_filter
            ]





        st.markdown("### 🧾 Leads CRM")

        def highlight_status(row):
            status = row["Lead Status"]

            if status == "New":
                return ["background-color: #dbeafe"] * len(row)

            elif status == "Contacted":
                return ["background-color: #fef3c7"] * len(row)

            elif status == "Proposal Sent":
                return ["background-color: #ede9fe"] * len(row)

            elif status == "Won":
                return ["background-color: #dcfce7"] * len(row)

            elif status == "Lost":
                return ["background-color: #fee2e2"] * len(row)

            else:
                return [""] * len(row)

            #Create reply countdown
        filtered_df["Reply Time Left"] = filtered_df.apply(
                calculate_reply_deadline,
                axis=1
            )

            # Status priority order
        status_order = {
                "New": 1,
                "Contacted": 2,
                "Proposal Sent": 3,
                "Won": 4,
                "Lost": 5
            }

        filtered_df["Status Order"] = filtered_df["Lead Status"].map(status_order)

            # Sort active leads first, oldest first
        display_df = filtered_df.sort_values(
                by=["Status Order", "Submitted DateTime"],
                ascending=[True, True]
            )

            # Hide helper columns only if they exist
        display_df = display_df.drop(
                columns=["Status Order", "Submitted DateTime"],
                errors="ignore"
            )
        

        display_df.insert(
            0,
            "Lead ID",
            [f"LD-{i:03}" for i in range(1, len(display_df) + 1)]
        )


        styled_df = display_df.style.apply(
                highlight_status,
                axis=1
            )

        st.dataframe(
                styled_df,
                use_container_width=True,
                hide_index=True
            )
      



        st.markdown("### 🤖 AI Follow-Up Email Generator")

        lead_options = leads_df["Name"].tolist()

        selected_followup_lead = st.selectbox(
            "Select lead for AI follow-up",
            lead_options,
            key="followup_lead"
        )

        selected_row = leads_df[
            leads_df["Name"] == selected_followup_lead
        ].iloc[0]

        if st.button("Generate AI Follow-Up Email"):

            prompt = f"""
            Write a professional follow-up email.

            Lead Name: {selected_row['Name']}
            Service: {selected_row['Service']}
            Lead Score: {selected_row['Lead Score']}
            Client Message: {selected_row['Message']}

            Encourage the client to schedule a consultation.
            Keep the email professional and concise.
            """

            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional sales assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            st.session_state.followup_email = response.choices[0].message.content
            st.session_state.followup_recipient = selected_row["Email"]

        if "followup_email" in st.session_state:

            st.text_area(
                "Generated Follow-Up Email",
                st.session_state.followup_email,
                height=250
            )

            if st.button("📧 Send Follow-Up Email"):

                send_success = send_email(
                    st.session_state.followup_recipient,
                    "Following Up On Your Inquiry",
                    st.session_state.followup_email
                )

                if send_success:
                    st.success(
                        f"Follow-up email sent to {st.session_state.followup_recipient}"
                    )
                else:
                    st.error("Follow-up email could not be sent.")

        

    except FileNotFoundError:
        st.info("No leads submitted yet.")



        


def get_ai_response(query):
    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a professional AI business assistant helping customers "
                    "with automation, websites, chatbots, and business growth. "
                    "Remember the conversation context and continue naturally. "
                    "Keep answers practical, specific, and helpful."
                )
            }
        ]

        for role, message in st.session_state.messages:
            messages.append({"role": role, "content": message})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI response is currently unavailable. Error: {e}"
    
    
faqs = {
    "services": "We offer website development, AI chatbot setup, automation, and data dashboard services.",
    "pricing": "Our basic package starts from AED 999. Custom projects are priced after consultation.",
    "booking": "You can book a free consultation by sending your name, email, and preferred time.",
    "support": "Our support team is available Monday to Friday, 9 AM to 6 PM.",
    "refund": "Refunds are available within 7 days if the project work has not started."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#64748b; font-size:14px; padding:15px 0;">
        <strong>© 2026 AI Client Intelligence Platform</strong><br><br>
        Designed & Developed by <strong>Priyanka Pabla</strong><br>
        Freelance AI Developer | Dubai, UAE
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("## 💬 AI Business Advisor")
st.caption("Get AI-powered recommendations tailored to your business needs.")






for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.write(message)
        
query = st.chat_input("Ask your question here...")

if query:
    st.session_state.messages.append(("user", query))

    query_lower = query.lower()

    service_keywords = ["services", "what do you offer", "offer"]
    pricing_keywords = ["pricing", "price", "cost", "package", "packages"]
    booking_keywords = ["book", "booking", "consultation", "appointment"]
    support_keywords = ["support hours", "customer support", "contact support"]
    refund_keywords = ["refund", "cancel", "cancellation"]

    if any(word in query_lower for word in service_keywords):
        response = f"Thanks for your interest. {faqs['services']}"

    elif any(word in query_lower for word in pricing_keywords):
        response = f"Our pricing is designed to suit different business needs. {faqs['pricing']}"

    elif any(word in query_lower for word in booking_keywords):
        response = f"Great choice. {faqs['booking']}"

    elif any(word in query_lower for word in support_keywords):
        response = f"We’re always happy to help. {faqs['support']}"

    elif any(word in query_lower for word in refund_keywords):
        response = f"Sure, here’s our refund policy. {faqs['refund']}"


    else:
        if "website" in query_lower:
            response = "A professional business website combined with an AI chatbot would be a great starting point."

        elif "automation" in query_lower:
            response = "Our automation solutions can help reduce manual work and improve business efficiency."

        else:
            with st.spinner("🤖 AI is analyzing your request..."):
                response = get_ai_response(query)
 

    st.session_state.messages.append(("assistant", response))
    st.rerun()





