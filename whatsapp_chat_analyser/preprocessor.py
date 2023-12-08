import pandas as pd
import re
import streamlit as st


def text_preprocessing(text):
    # reading the tetx
    # f = open(text, 'r')

    # data = text.read()
    # pattern for splitting the message data and message
    # meaage
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s*[apmAPM]{2}\s-\s'
    message = re.split(pattern, text)[1:]
    # date
    date = re.findall(pattern, text)

    # making the dataframe
    data_dict = {'user_message': message, "date": date}
    print(data_dict)
    # data fraome
    df = pd.DataFrame(data_dict)

    # # Attempt to convert the 'date' column to datetime or 24 hr form
    # try:
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p - ')
    # except ValueError as e:
    #     print(f"Error: {e}")
    #
    # # #user and their message splitter
    def user_and_message_splitter(text):
        parts = text.split(":")
        user = parts[0].strip()  # Get the user part and remove leading/trailing whitespaces
        message = parts[1].strip() if len(parts) > 1 else ''  # Get the message part or an empty string if not present
        return user, message

    # # Apply the function to 'user_message' and create new columns 'user' and 'message'
    df[['User', 'Message']] = pd.DataFrame(df['user_message'].apply(user_and_message_splitter).tolist())
    #
    # # dropping the user_mesage
    df = df.drop(columns='user_message')
    #
    # # splitting the date in year,mon.day,hr,min
    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute
    df['day_name']=df['date'].dt.day_name()
    # # renming
    #
    df['User'].replace(['Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.','Your security code with  changed . Tap to learn more.'], "Group_notification",
                       inplace=True)

    return df