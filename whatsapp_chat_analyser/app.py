import matplotlib.pyplot as plt
import streamlit as st
import helper
import preprocessor
import seaborn as sns
# import matplotlib.express as px
st.title("WhatsApp Chat Analyzer")

    # Sidebar layout
st.sidebar.title("Upload File")
uploaded_file = st.sidebar.file_uploader("Choose a file")

    # Main content
if uploaded_file is not None:
    try:
            # To read file as bytes
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8')
        # st.write(data)
        df=preprocessor.text_preprocessing(data)
    #
        st.dataframe(df)
    #
    # fetch the unique user
        user_list=df['User'].unique().tolist()
        user_list.remove("Group_notification")
        user_list.insert(0,"Overall")

        selected_user=st.sidebar.selectbox("Show analysis with respect to",user_list)
 #button to start analysis
        if st.sidebar.button('Show Analysis'):

            message_num,word_num,media_message_num=helper.fetch_stats(selected_user,df)
            #creating the col
            col1,col2,col3,col4=st.columns(4)
#for col1
            with col1:
                st.header("Total Message")
                st.title(message_num)
                #for col2

            with col2:
                st.header("Total Words")
                st.title(word_num)

            with col3:
                st.header("Total Media shared")
                st.title(media_message_num)
#link share is left

            if selected_user=="Overall":
                st.title("Most Busy User")

                #for the caliig most busy man function
                user_name,count,user_df=helper.most_busy_man(df)
                fig,ax=plt.subplots()

                col4, col5 = st.columns(2)
                with col4:
                    ax.bar(user_name,count,color='green')
                    plt.xticks(rotation="vertical")
                    st.pyplot(fig)

                with col5:
                    st.title("Data with name and percentage of message done by user.")
                    st.dataframe(user_df)

            #wordcloud
            st.title("Word frequently used by " +selected_user)
            df_wc=helper.create_word_cloud(selected_user,df)
            fig, ax = plt.subplots()

            ax.imshow(df_wc)
            st.pyplot(fig)

            #MOST COMMON WORD
            st.title("Top 20 commonly message used by "+selected_user)
            most_common_message=helper.most_common_word(selected_user,df)
            st.table(most_common_message)

                #on bargraph
            st.title("The bargraph of message used by "+ selected_user)
            fig,ax=plt.subplots()
            # bar graph
            # plt.figure(figsize=(10, 10))
            ax=sns.barplot(x=most_common_message['Message'], y=most_common_message['Count'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


#emoji analysis
            st.title("Emoji used by "+selected_user)
            emoji_data=helper.emoji_finding(selected_user,df)

            col6,col7 =st.columns(2)

            with col6:
                st.dataframe(emoji_data)

            with col7:
                #
                st.title("Graph chart")
#determing the field for plot

                fig,ax=plt.subplots()
#plottingn the chart

                sns.barplot(x=emoji_data['Type of emoji'],y=emoji_data['Count'],legend=True)
                # sns.set(style="darkgrid")  # Set the style to whitegrid for better visibility of the background color

                # ax.set_facecolor('whitegrid')
                st.pyplot(fig)

#plot the line plot
            st.title("Monthly Timeline")
            timeline_df=helper.mon_year_wise_message_count(selected_user,df)
            fig,ax=plt.subplots()
            #
            ax=plt.plot(timeline_df['time'], timeline_df['Message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

#daily time line
            st.title("Daily Timeline of "+ selected_user)
            timeline_df.dropna(subset=['only_date'], inplace=True)
            st.dataframe(timeline_df)
            fig, ax = plt.subplots()
            ax = plt.plot(timeline_df['only_date'], timeline_df['Message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)



#acitvity map
            st.title("Activity maps of " + selected_user)
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            st.dataframe(busy_day)
            ax = plt.bar(busy_day.index, busy_day.values)
            st.pyplot(fig)



    except Exception as e:
        st.error("An error occurred during preprocessing. Please check your input file.")


