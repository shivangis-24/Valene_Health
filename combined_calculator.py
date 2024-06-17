import streamlit as st

st.title('DSM-5 Disorder Calculator')

# Sidebar for selecting the disorder
disorder = st.sidebar.selectbox("Select Disorder", ["Major Depressive Episode Disorder", "Generalized Anxiety Disorder"])

if disorder == "Major Depressive Episode Disorder":
    st.header('DSM-5 Major Depressive Episode Disorder Calculator')

    st.subheader('Instructions:')
    st.write("Please select the symptoms the patient has experienced for most of the day, nearly every day, for at least two weeks:")

    # Symptoms
    symptoms = {
        "Depressed mood": False,
        "Markedly diminished interest or pleasure in all, or almost all, activities": False,
        "Significant weight loss when not dieting, weight gain, or decrease or increase in appetite": False,
        "Insomnia or hypersomnia": False,
        "Psychomotor agitation or retardation": False,
        "Fatigue or loss of energy": False,
        "Feelings of worthlessness or excessive or inappropriate guilt": False,
        "Diminished ability to think or concentrate, or indecisiveness": False,
        "Recurrent thoughts of death, recurrent suicidal ideation, or a suicide attempt": False
    }

    # Collect user input for symptoms
    for symptom in symptoms.keys():
        symptoms[symptom] = st.checkbox(symptom)

    st.subheader('Additional Criteria:')
    st.write("Please confirm if the following conditions are met:")

    # Additional criteria
    additional_criteria = {
        "The symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning.": False,
        "The symptoms are not due to the direct physiological effects of a substance (e.g., drug abuse, a prescribed medication’s side effects) or a medical condition (e.g., hypothyroidism).": False,
        "There has never been a manic episode or hypomanic episode.": False,
        "MDE is not better explained by schizophrenia spectrum or other psychotic disorders.": False
    }

    # Collect user input for additional criteria
    for criterion in additional_criteria.keys():
        additional_criteria[criterion] = st.checkbox(criterion)

    st.subheader('Assessment:')
    num_symptoms = sum(symptoms.values())

    # Criteria check
    if num_symptoms >= 5:
        if symptoms["Depressed mood"] or symptoms["Markedly diminished interest or pleasure in all, or almost all, activities"]:
            if all(additional_criteria.values()):
                st.success("Criteria for Major Depressive Episode are met.")
            else:
                st.warning("Not all additional criteria are met.")
        else:
            st.warning("At least 5 symptoms are present, but neither 'Depressed mood' nor 'Markedly diminished interest or pleasure' is selected.")
    else:
        st.warning("Criteria for Major Depressive Episode are not met.")

    st.write(f"Number of symptoms checked: {num_symptoms}/9")

elif disorder == "Generalized Anxiety Disorder":
    st.header('DSM-5 Generalized Anxiety Disorder Calculator')

    st.subheader('Instructions:')
    st.write("Please select the symptoms the patient has experienced more days than not for at least 6 months:")

    # Symptoms
    symptoms = {
        "Excessive anxiety and worry (apprehensive expectation), occurring more days than not for at least 6 months, about a number of events or activities (such as work or school performance)": False,
        "The individual finds it difficult to control the worry": False,
        "The anxiety and worry are associated with three (or more) of the following six symptoms (with at least some symptoms having been present for more days than not for the past 6 months)": False
    }

    associated_symptoms = {
        "Restlessness or feeling keyed up or on edge": False,
        "Being easily fatigued": False,
        "Difficulty concentrating or mind going blank": False,
        "Irritability": False,
        "Muscle tension": False,
        "Sleep disturbance (difficulty falling or staying asleep, or restless, unsatisfying sleep)": False
    }

    # Collect user input for symptoms
    for symptom in symptoms.keys():
        symptoms[symptom] = st.checkbox(symptom)

    st.subheader('Associated Symptoms:')
    st.write("Please select the associated symptoms experienced more days than not for the past 6 months:")

    # Collect user input for associated symptoms
    for symptom in associated_symptoms.keys():
        associated_symptoms[symptom] = st.checkbox(symptom)

    st.subheader('Additional Criteria:')
    st.write("Please confirm if the following conditions are met:")

    # Additional criteria
    additional_criteria = {
        "The anxiety, worry, or physical symptoms cause clinically significant distress or impairment in social, occupational, or other important areas of functioning.": False,
        "The disturbance is not attributable to the physiological effects of a substance (e.g., a drug of abuse, a medication) or another medical condition (e.g., hyperthyroidism).": False,
        "The disturbance is not better explained by another mental disorder (e.g., anxiety or worry about having panic attacks in panic disorder, negative evaluation in social anxiety disorder, contamination or other obsessions in obsessive-compulsive disorder, separation from attachment figures in separation anxiety disorder, reminders of traumatic events in posttraumatic stress disorder, gaining weight in anorexia nervosa, physical complaints in somatic symptom disorder, perceived appearance flaws in body dysmorphic disorder, having a serious illness in illness anxiety disorder, or the content of delusional beliefs in schizophrenia or delusional disorder).": False
    }

    # Collect user input for additional criteria
    for criterion in additional_criteria.keys():
        additional_criteria[criterion] = st.checkbox(criterion)

    st.subheader('Assessment:')
    num_associated_symptoms = sum(associated_symptoms.values())

    # Criteria check
    if symptoms["Excessive anxiety and worry (apprehensive expectation), occurring more days than not for at least 6 months, about a number of events or activities (such as work or school performance)"] and \
       symptoms["The individual finds it difficult to control the worry"] and \
       num_associated_symptoms >= 3:
        if all(additional_criteria.values()):
            st.success("Criteria for Generalized Anxiety Disorder are met.")
        else:
            st.warning("Not all additional criteria are met.")
    else:
        st.warning("Criteria for Generalized Anxiety Disorder are not met.")

    st.write(f"Number of associated symptoms checked: {num_associated_symptoms}/6")

# Additional Information
# st.subheader('Disclaimer:')
# st.write("This tool is for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health providers with any questions you may have regarding a medical condition.")
