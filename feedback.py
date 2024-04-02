import streamlit as st

def main():
    st.title("Customer Feedback")
    user_id = st.text_input("Enter your Mail-ID")

    # CSAT Feedback
    st.header("Customer Satisfaction Score (CSAT)")
    csat_options = ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied']
    csat_feedback = st.selectbox("How satisfied are you with the service received?", csat_options)

    # Call Rating Feedback
    st.header("Call Rating")
    call_rating = st.slider("How would you rate the quality of the call?", min_value=0, max_value=5, step=1)

    # Convert slider value to star design
    rating_stars = "★" * call_rating + "☆" * (5 - call_rating)
    st.write(f"Your rating: {rating_stars}")

    # Submit Button
    if st.button("Submit Feedback"):
        if user_id:
            st.success(f"Thank you, {user_name} (ID: {user_id}), for your feedback!")
        else:
            st.error("Please enter both your name and user ID before submitting feedback.")

        # You can add further processing or saving of the feedback data here


if __name__ == "__main__":
    main()


# import streamlit as st
# from pymongo import MongoClient

# # Function to connect to MongoDB database
# def connect_to_mongodb():
#     client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
#     db = client["customer_feedback"]  # Replace "customer_feedback" with your database name
#     collection = db["feedback"]  # Replace "feedback" with your collection name
#     return collection

# def main():
#     st.title("Customer Feedback")

#     # CSAT Feedback
#     st.header("Customer Satisfaction Score (CSAT)")
#     csat_options = ['Very Satisfied', 'Satisfied', 'Neutral', 'Dissatisfied', 'Very Dissatisfied']
#     csat_feedback = st.selectbox("How satisfied are you with the service received?", csat_options)

#     # Call Rating Feedback
#     st.header("Call Rating")
#     call_rating = st.slider("How would you rate the quality of the call?", min_value=0, max_value=5, step=1)

#     # Convert slider value to star design
#     rating_stars = "★" * call_rating + "☆" * (5 - call_rating)
#     st.write(f"Your rating: {rating_stars}")

#     # Submit Button
#     if st.button("Submit Feedback"):
#         st.success("Thank you for your feedback!")

#         # Connect to MongoDB
#         collection = connect_to_mongodb()

#         # Prepare feedback data
#         feedback_data = {
#             "csat_feedback": csat_feedback,
#             "call_rating": call_rating
#         }

#         # Insert feedback data into MongoDB
#         collection.insert_one(feedback_data)
#         st.write("Feedback data sent to MongoDB.")

# if __name__ == "__main__":
#     main()
