import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
import emoji
import re
# def fetch_stats(selected_user,df):
#     if selected_user=="Overall":
#         #fetching the number of messeage
#         message_num=df.shape[0]
#         #num_of_word
#         words=[]
#         #gettingn the message
#         for message in df['Message']:
#             words.extend(message.split(" "))
#
#         #NUM OF WORD
#         word_num=len(words)
#         return message_num,word_num
#
#     else:
#         #getting the selested user
#
#         user_df=df[df['User'] == selected_user]
#         #getting the number meaage in seleted usee
#
#         message_num=user_df.shape[0]
#         words = []
#         # gettingn the message
#         for message in user_df['Message']:
#             words.extend(message.split(" "))
#
#         # NUM OF WORD
#         word_num = len(words)
#         return message_num, word_num


#shortcut technique
def fetch_stats(selected_user,df):
    if selected_user!="Overall":
        # getting the selected user
        df = df[df['User'] == selected_user]
        #fetching the number of messeage
    message_num=df.shape[0]
    #num_of_word
    words=[]
    #gettingn the message
    for message in df['Message']:
        words.extend(message.split(" "))

        #NUM OF WORD
    word_num=len(words)

    #counting the media message
    media_message_num=df[df['Message']=='<Media omitted>'].shape[0]
    return message_num,word_num,media_message_num



#for the graphplotting
def most_busy_man(df):
    user_df = df['User'].value_counts().head()

    #getting the name of user and their no of message
    name_user = user_df.index
    count = user_df.values
    #percatge of the message done by which user

    user_df = round((df['User'].value_counts()) / (df.shape[0]) * 100, 2).reset_index()
    user_df.rename(columns={'User': "Name", "count": "Percentage"},inplace=True)


    return name_user,count,user_df



def create_word_cloud(selected_user,df):

    if selected_user!="Overall":
        #getting the selectd user
        df=df[df["User"]==selected_user]

        # filtering the medial ommitted
        df = df[df['Message'] != '<Media omitted>']
        #making the obj of wordcloud
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='black')
#using the generate func of  wordcloud
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return  df_wc


#most commn word
def most_common_word(selected_user,df):
    if selected_user != "Overall":
        # getting the selectd user
        df = df[df["User"] == selected_user]

    # removing the group notification
    df = df[df['User'] != "Group_notification"]
    # filtering the medial ommitted
    final_df = df[df['Message'] != '<Media omitted>']
 #getting stopword

    nepali_stopwords = stopwords.words("nepali")
    english_stopwords = stopwords.words("english")
    nepanglish_stopword = ['Cha', 'Ra', 'Pani', 'Chhan', "Lagi", 'Bhaeko', 'Gareko', 'Bhane', 'Garna', 'Ho', 'Tatha',
                           'Yo', 'raheko', 'unale', 'thiyo', 'hune', 'thiye', 'gardai', 'tar', 'nai', 'ko', 'maa',
                           'hunu', 'bhanne', 'gari', 'ta', 'hunxa', 'aba', 'k', 'raheko', 'garer', 'chhain', 'Hlo', 'K']
    # total_stopword
    total_stopword = nepali_stopwords + english_stopwords + nepanglish_stopword


#word list
    word_list = []
    for word in final_df['Message']:
        if word not in total_stopword:
            word_list.extend(word.split())


    message_with_count = Counter(word_list).most_common(40)
    # into dataframe
    final_df = pd.DataFrame(message_with_count)
    final_df.rename(columns={0: "Message", 1: 'Count'},inplace=True)
    #remove
    final_df['Message']=final_df["Message"].replace("?")
    return final_df



def emoji_finding(selected_user,df):

    if selected_user!="Overall":
        df=df[df["User"]==selected_user]

    emojis=[]
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.rename(columns={0:"Type of emoji",1:"Count"},inplace=True)
    return  emoji_df


def mon_year_wise_message_count(selected_user,df):
    if selected_user != "Overall":
        # getting the selectd user
        df = df[df["User"] == selected_user]
#time line

    timeline_df = df.groupby(['Year', 'Month']).count()['Message'].reset_index()

        # join the name of month and year
    time_list = []
    for i in range(timeline_df.shape[0]):
        time_list.append(timeline_df['Month'][i] + "-" + str(timeline_df['Year'][i]))

    timeline_df['time'] = time_list
    timeline_df['only_date'] = df['date'].dt.date



    return timeline_df


def week_activity_map(selected_user,df):
    if selected_user != "Overall":
        # getting the selectd user
        df = df[df["User"] == selected_user]
# time line

    return df['day_name'].value_counts()

