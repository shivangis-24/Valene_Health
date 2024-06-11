import streamlit as st
import openai
import re

# Initialize the OpenAI client with your API key
openai.api_key = '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'

def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0]['message']['content'].strip()

def diagnose(past_diagnosis, symptoms, duration):
    mdd_criteria = [
        "Little interest or pleasure in doing things",
        "Feeling down, depressed, or hopeless",
        "Trouble falling or staying asleep, or sleeping too much",
        "Feeling tired or having little energy",
        "Poor appetite or overeating",
        "Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
        "Trouble concentrating on things, such as reading the newspaper or watching television",
        "Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
        "Thoughts that you would be better off dead or of hurting yourself in some way"
    ]

    gad_criteria = [
        "Feeling nervous, anxious or on edge",
        "Not being able to stop or control worrying",
        "Worrying too much about different things",
        "Trouble relaxing",
        "Being so restless that it is hard to sit still",
        "Becoming easily annoyed or irritable",
        "Feeling afraid as if something awful might happen"
    ]

    prompt = (
        f"The symptoms are: {', '.join(symptoms)}.\n\n"
        f"Using the following criteria for MDD and GAD, please determine the number of matching criteria for each.\n\n"
        f"MDD Criteria:\n- {', '.join(mdd_criteria)}\n\n"
        f"GAD Criteria:\n- {', '.join(gad_criteria)}\n\n"
        "Please provide the number of matching criteria for MDD and GAD in the following format:\n"
        "MDD: <number>\nGAD: <number>\n"
        "Also, provide a brief explanation of the matches."
    )
    
    response = generate_response(prompt)
    print("GPT-4 Response:\n", response)

    # Extract MDD and GAD scores from the response
    mdd_score, gad_score = 0, 0
    try:
        mdd_score = int(re.search(r'MDD:\s*(\d+)', response).group(1))
        gad_score = int(re.search(r'GAD:\s*(\d+)', response).group(1))
    except Exception as e:
        print(f"Error parsing response: {e}")

    diagnosis = ""
    if mdd_score >= 5:
        if duration == "<2 weeks":
            diagnosis = 'Brief Depressive Episode'
        else:
            diagnosis = 'Major Depressive Disorder'
        if gad_score >= 1:
            diagnosis += ' + Anxiety Disorder'
    elif gad_score >= 4:
        if duration == "<6 months":
            diagnosis = 'Anxiety Disorder'
        else:
            diagnosis = 'Generalized Anxiety Disorder'
        if mdd_score >= 1:
            diagnosis += ' + Brief Depressive Episode'
    elif mdd_score >= 1:
        diagnosis = 'Brief Depressive Episode'
    elif gad_score >= 1:
        diagnosis = 'Anxiety Disorder'
    else:
        diagnosis = 'Undiagnosed'

    if past_diagnosis:
        diagnosis = past_diagnosis + ' + ' + diagnosis

    return diagnosis, mdd_score >= 5

st.set_page_config(page_title="Mental Health Diagnostic Tool", page_icon="🧠")

# Custom CSS for the Chatbase-like layout
st.markdown(
    """
    <style>
    .main {
        background-color: #121212;
        color: #FFFFFF;
        padding: 20px;
    }
    .chat-container {
        background-color: #1E1E1E;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
        width: 100%;
    }
    .message {
        background-color: #333333;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        color: #FFFFFF;
    }
    .message.bot {
        background-color: #444444;
    }
    .message.user {
        background-color: #6200EE;
        align-self: flex-end;
    }
    .input-container {
        display: flex;
        justify-content: space-between;
        margin-top: 20px;
    }
    .input-container input {
        width: 80%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #333333;
        color: #FFFFFF;
    }
    .input-container button {
        width: 15%;
        padding: 10px;
        border: none;
        border-radius: 5px;
        background-color: #6200EE;
        color: #FFFFFF;
        cursor: pointer;
    }
    .footer-buttons {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }
    .footer-buttons button {
        background-color: #6200EE;
        color: #FFFFFF;
        border: none;
        border-radius: 5px;
        padding: 10px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Main title
st.title("Mental Health Diagnostic Tool")

# Chat container
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

# Initial bot message
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "content": "Hi I'm Valene, how can I help you today? 🧑‍⚕️"},
        {"role": "bot", "content": "Let's start by telling me your name."}
    ]
    st.session_state.stage = 0
    st.session_state.name = ""
    st.session_state.past_diagnosis = ""
    st.session_state.symptoms = []
    st.session_state.duration = ""
    st.session_state.additional_info = {
        "first_notice": "",
        "significant_changes": "",
        "suicidal_thoughts": "",
        "prior_treatment": ""
    }
    st.session_state.mdd_confirmed = False

def get_next_question(stage):
    questions = [
        "What brings you in today?",
        "When did you first notice these symptoms? And have you experienced any similar symptoms in the past?",
        "Have there been any significant changes or stressors in your life recently?",
        "Do you have any active or passive suicidal thoughts or ideations? Any thoughts of self-harm?",
        "Have you sought any prior mental health treatment? If so, what?",
        "Have you ever been diagnosed with any past mental health issues? (yes/no)",
        "Can you tell me what symptoms you're experiencing? Please list them separated by commas.",
        "How long have you been experiencing these symptoms? (e.g., <2 weeks, >2 weeks, <6 months, >6 months)"
    ]
    return questions[int(stage)] if stage < len(questions) else "Thank you for your responses."

# Display messages
for message in st.session_state.messages:
    role = "bot" if message["role"] == "bot" else "user"
    st.markdown(f'<div class="message {role}">{message["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Input container
with st.form(key='input_form', clear_on_submit=True):
    user_input = st.text_input("Your response:", "")
    submit_button = st.form_submit_button(label='Send')

if submit_button and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    if st.session_state.stage == 0:
        st.session_state.name = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": f"Thanks {st.session_state.name}. What brings you in today?"})
    elif st.session_state.stage == 1:
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "When did you first notice these symptoms? And have you experienced any similar symptoms in the past?"})
    elif st.session_state.stage == 2:
        st.session_state.additional_info["first_notice"] = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "Have there been any significant changes or stressors in your life recently?"})
    elif st.session_state.stage == 3:
        st.session_state.additional_info["significant_changes"] = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "Do you have any active or passive suicidal thoughts or ideations? Any thoughts of self-harm?"})
    elif st.session_state.stage == 4:
        st.session_state.additional_info["suicidal_thoughts"] = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "Have you sought any prior mental health treatment? If so, what?"})
    elif st.session_state.stage == 5:
        st.session_state.additional_info["prior_treatment"] = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "Have you ever been diagnosed with any past mental health issues? (yes/no)"})
    elif st.session_state.stage == 6:
        if "yes" in user_input.lower():
            st.session_state.past_diagnosis = user_input
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "Can you tell me what symptoms you're experiencing? Please list them separated by commas."})
    elif st.session_state.stage == 7:
        st.session_state.symptoms = [symptom.strip() for symptom in user_input.split(",")]
        st.session_state.stage += 1
        st.session_state.messages.append({"role": "bot", "content": "How long have you been experiencing these symptoms? (e.g., <2 weeks, >2 weeks, <6 months, >6 months)"})
    elif st.session_state.stage == 8:
        st.session_state.duration = user_input
        diagnosis, mdd_confirmed = diagnose(st.session_state.past_diagnosis, st.session_state.symptoms, st.session_state.duration)
        st.session_state.mdd_confirmed = mdd_confirmed
        st.session_state.messages.append({"role": "bot", "content": "Based on your symptoms, we need to ask a few more questions to confirm your diagnosis. Please answer the following questions:"})
        
        if mdd_confirmed:
            st.session_state.messages.append({"role": "bot", "content": "Based on your symptoms, we need to ask a few more questions to confirm your diagnosis. Please answer the following questions:"})
    
    st.rerun()

if st.session_state.mdd_confirmed:
    st.markdown("## Additional Questions for MDD Diagnosis")
    mdd_questions = [
        "A1: Depressed mood (indicated by subjective report or observation by others)?",
        "A2: Loss of interest or pleasure in almost all activities?",
        "A3: Significant unintentional weight loss/gain or decrease/increase in appetite?",
        "A4: Sleep disturbance (insomnia or hypersomnia)?",
        "A5: Psychomotor changes (agitation or retardation)?",
        "A6: Tiredness, fatigue, or low energy?",
        "A7: A sense of worthlessness or excessive, inappropriate, or delusional guilt?",
        "A8: Impaired ability to think, concentrate, or make decisions?",
        "A9: Recurrent thoughts of death, suicidal ideation, or suicide attempts?",
    ]

    mdd_responses = {}
    for question in mdd_questions:
        mdd_responses[question] = st.selectbox(question, options=["Yes", "No"])

    if st.button("Submit Additional MDD Information"):
        st.session_state.mdd_responses = mdd_responses
        st.session_state.mdd_confirmed = False
        st.session_state.messages.append({"role": "bot", "content": "Thank you for providing additional information. Based on your responses, we'll review your condition further. Please wait for a moment."})
        
        # Display thank you message and options
        st.session_state.messages.append({"role": "bot", "content": "Thank you for completing the assessment. Here are your options:"})
        st.markdown(
            """
            <div class="footer-buttons">
                <button onclick="window.location.href='https://valenehealth.com/self-evaluation'">Recommend content and self-exploration tool</button>
                <button onclick="window.location.href='https://valenehealth.com/book-appointment'">Book an appointment with Valene Health professionals</button>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.rerun()

# Hide the input box and send button after the MDD confirmation questions are displayed
if not st.session_state.mdd_confirmed:
    st.markdown(
        """
        <div class="footer-buttons">
            <button>Self-evaluation</button>
            <button>Connect to Professional</button>
            <button>Learn more about mental health</button>
        </div>
        """,
        unsafe_allow_html=True
    )
