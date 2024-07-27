###### IMPORTS
import streamlit as st # streamlit module
import pandas as pd # for data manipulation
import seaborn as sns # for data visualization
import matplotlib.pyplot as plt # for data visualization


###### FUNCTIONS

#### Class for each user (SLA as each attribute)
##### Using Class to determine each user's input for calling convenience later on.
##### Then converting to dataframe
class input:
        def __init__(self, r, bms, cs, jlf, ie, pc):
                self.r = r
                self.bms = bms
                self.cs = cs
                self.jlf = jlf
                self.ie = ie
                self.pc = pc
        # def importance(self,r, bms, cs, jlf, ie, pc):



## Original List Values for each SLA & SLU
og = {
        0 : {
        "SLA": "Relationships",
        "SLU": ['Significant Other', 'Family', 'Friendship']
        },
        1:{
        "SLA": "Body, Mind, and Spirit",
        "SLU": ['Physical Health/Sports', 'Mental Health/Mindfulness', 'Spirituality/Faith', 'Sleep']
        },
        2: {
        "SLA": "Community & Society",
        "SLU": ['Community/Citizenship', 'Societal Engagement']
        },
        3: {
        "SLA": "Job, Learning, and Finances",
        "SLU": ['Job/Career', 'Education/learning', 'Finances']
        },
        4: {
        "SLA": "Interests & Entertainment",
        "SLU": ['Hobbies/Interests', 'Online entertainment', 'Offline entertainment']
        },
        5: {
        "SLA":"Personal Care",
        "SLU": ['Physiological needs', 'Activities of daily living']
        }
    } 

## Using functions to get user input to reduce redundancy and write more compact code
## selectSLU
def selectSLU(SLAtitle, SLUlist):
        x = st.multiselect(f"{SLAtitle}: ",
                            SLUlist)
        return x


## sliderHour
            
# df.sum(axis = 0, skipna = True) 
def hourInput(SLUlist, criteria):
        x = []  ## create an empty list
        for i in range(0, (len(SLUlist))): ## conduct the same action for each value in each column
                st.write(SLUlist.values[i])
                # st.write(i) ## for QA
                n = st.number_input("Select hours spent per week", 0, 168, key = criteria + str(i)) ## key needs to be unique across all widgets
                x.append(n)
        return x

## sliderScale (for importance, satisfaction)
## criteria: importance, satisfaction
## multi for loop, for each SLU in SLA list append to df
def sliderScale(SLUlist, criteria):
        x = []  ## create an empty list
        for i in range(0, (len(SLUlist))): ## conduct the same action for each value in each column
                st.write(SLUlist.values[i])
                # st.write(i) ## for QA
                n = st.slider("Select from scale (1: Least important/satisfied, 7: Very important/satisfied)", 1, 7, key = criteria + str(i)) ## key needs to be unique across all widgets
                x.append(n)
        return x

## collapsing sections
# st.subheader("A Chart you can show or hide")
# with st.section(label="the_chart"):
#     st.write(some_dataframe)

## additional resources
# st.divider() ## horizontal line divider
# st.tabs(["tab1", "tab2"]) ## tabs
# with st.expander("open to see more"): ## collapsible element
#         st.write("this is more content")




## chartformat
def setChartTheme():
        sns.set_style("whitegrid") # theme
        sns.set_palette("muted") # color palette
        ## assign color dictionary for each SLA (reference https://stackoverflow.com/questions/71397574/set-same-color-palette-for-multiple-plots-from-several-dataframes)

## scatterplot
def scatterPlot(df, x,y,title, color, size,label):
        plt.figure()
        fig = sns.scatterplot(data=df, x=x, y=y, hue=color, size = size,
                                sizes=(20, 250), legend = "full")
        # Changing Legend position
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.title(title)
        
        # Adding text labels
        [fig.text(p[0]-0.6, p[1]+0.2, p[2], color='black') for p in zip(df[x], df[y], df[label])]


        # Displaying quadrants for ease of analysis based on the mean 
        plt.axhline(y=4, color='k', linestyle='-', linewidth=1)           
        plt.axvline(x=4, color='k',linestyle='-', linewidth=1) 
        
        # Setting the axis
        fig.set_yticks([1,2,3,4,5,6,7])
        fig.set_xticks([1,2,3,4,5,6,7])
        return fig
        
## barchart
def barChart(x, y, data, title):
        plt.figure()
        chart = sns.barplot(x=y, y=x, data = data)
        plt.title(title)
        return chart
## stackedchart (or piechart)
def pieChart(data, sla, title):
        plt.figure()
        chart = plt.pie(data, labels=sla, autopct='%.0f%%')
        plt.title(title)
        return chart

## stacked barchart
def stackedChart(data, title):
        plt.figure()
        chart = data.plot(kind='bar', stacked=True)
        plt.title(title)
        return chart


###### MAIN APP


##### BACKGROUND
st.markdown('# Life Strategy Tool')
hbr_link = 'https://www.youtube.com/watch?v=dbiNhAZlXZk'
st.link_button("Strategic Thinking to Create the Life You Want by HBR", hbr_link)
## intro
st.markdown("### Introduction")
st.markdown(""" Based on Harvard Business Review YT video, that applies corporate strategy to optimize your life. Whether you're feeling low in life, stuck, or just curious, take some time assessing your life using this tool.
            Note that this tool will make a lot more sense after watching the video.""")

st.markdown("### Definitions")
st.markdown("""
            - SLA: Strategic Life Areas
            - SLU: Strategic Life Units
            - Importance: Is this a priority?
            - Satisfaction: Are you happy with this?
            """)

st.markdown("### Scale")
st.markdown(""" 7-point scale with 1 being lowest importance or lowest satisfaction and 7 being highest in importance or satisfaction""")

## create empty dataframe
df = pd.DataFrame(columns = ['SLA', 'SLU', 'Importance', 'Satisfaction', 'Average Time Spent per Week'])

# DIVIDER
st.divider()


##### USER INPUTS (APPEND TO DATAFRAME)
st.header("Let's get started, shall we?")
## For each of the Strategic Life Areas, choose Strategic Life Units
st.markdown("##### For each of the Strategic Life Areas below, choose the Strategic Life Units that are most relevant to you:")
            # Using a multi select box

## Example
# for loop and then just automatically append to df
sla = []
slu = []
for i in range(6):
        r = selectSLU(og[i]["SLA"],og[i]["SLU"])
        # st.write(list(r)) ## for QA
        for n in range(len(r)):
                sla.append(og[i]["SLA"]) ## add each SLA value (for each SLU values)
                slu.append(r[n]) ## Add each SLU value
                # st.write(r[n]) ## for QA
# st.write(sla) ## for QA
# st.write(slu) ## for QA

df = pd.DataFrame(slu, sla) ## SLU column becomes an index at this point
if df.empty:
        st.warning('You need to choose at least one SLU to move on.', icon ="⚠️")
else:
        df.reset_index(inplace = True) ## index is reset, SLU column becomes 2nd column
        df.columns = ['SLA', 'SLU']
        st.write(df)
        
        st.divider()
        
        st.markdown("##### Next, rate your chosen SLUs based on the 3 factors: Time Spent, Importance, Satisfaction. Please take your time for more accurate results.")
        tab1, tab2, tab3 = st.tabs (['Time Spent','Importance', 'Satisfaction'])

        ## Time spent
        with tab1:
                time_spent = hourInput(df['SLU'], 'Time')
                # st.write(time_spent) ## for QA
                ## with total value of 1 week hour (so users can know how many hours they have left to "spare")
                x = sum(time_spent) ## total time spent based on each life units
                st.write("Hours left in one week:", 168-x)
                if x > 168:
                        st.error('Total hours add up to more than the weekly hours available (168 hrs). Please adjust the hours accordingly for proper analysis.', icon="🚨")
                elif x < 168:
                        st.warning('Total hours is less than weekly hours available (168 hours). Please assign all the hours to the appropriate category.', icon = "⚠️")
                else:
                        df = df.assign(TimeSpent=time_spent)
                         ## Calculate Share of Weekly Hours
                        df['ShareOfWeeklyHours (%)'] = (df['TimeSpent']/df['TimeSpent'].sum())*100
                        df['ShareOfWeeklyHours (%)'] = df['ShareOfWeeklyHours (%)'].round(2)
                
                
        # ## Importance Scale
        with tab2:
                ## Determine Importance for each Strategic Life Units
                st.markdown("##### Think about how important these SLUs are to you, and select a scale that makes sense")
                importance = sliderScale(df['SLU'], 'Importance')
                # st.write(importance) ## for QA
                df = df.assign(Importance=importance)

        ## Satisfaction Scale
        ## Determine average time spent per week (hour) on each life units
        with tab3:
                satisfaction = sliderScale(df['SLU'], 'Satisfaction')
                # st.write(satisfaction) ## for QA
                df = df.assign(Satisfaction=satisfaction)

        st.divider()

       
        st.write(df)

        if x != 168:
              st.warning('You need to complete the time spent, importance, or satisfaction section first before charts can be generated.', icon ="⚠️")  
        else:
                st.markdown("### Now here's the fun part....")



        ##### VISUALIZATION
                ## SCATTERPLOT (using seaborn)
                ## strategic life areas as color
                ## simple explanation of which areas to pay attention to (high life importance but low satisfaction, and low life importance but low satisfaction)
                setChartTheme()

                plot = scatterPlot(df, 'Satisfaction', 'Importance', 'Strategic Life Portfolio', 'SLA', 'TimeSpent', 'SLU')
                scatter = st.pyplot(plot.get_figure())

                ## Filtered df
                good = df.loc[(df['Satisfaction']>=4)]
                good = good.sort_values(by=['Satisfaction'], ascending = False) ## sort by Satisfaction desc

                improvement = df.loc[(df['Satisfaction']<4)]
                improvement = improvement.sort_values(by=['Satisfaction']) ## sort by Satisfaction asc


                ## Highlights
                st.write("You're doing really well in these areas (based on SLUs with Satisfaction rate of 4 and above): ")
                st.write(good)


                st.write("However, here's where you need to work on (based on SLUs rated Satisfaction rate of below 4):")
                st.write(improvement)


                ## How to fix it?
                too_much_time = improvement.loc[(improvement['Importance']<4)]
                too_little_time = improvement.loc[(improvement['Importance']>=4)]
                st.write("You're spending too much time on these, despite being low importance (less than 4):")
                st.write(too_much_time)
                st.write("These SLUs are important (4 and above), but you're not prioritizing these: ")
                st.write(too_little_time)

                ##### HIGHLIGHTS
                ## filter out to only those with low satisfaction
                ## run another chart with highlights if they are in lower satisfaction areas


                st.markdown("#### A glimpse into how you are doing based on your SLAs:")

                ###### SUMMARY STATS
                        ## bar chart average for strategic life areas (importance, satisfaction)
                df_sla = df.groupby(["SLA"]).agg(totalTimeSpent = ('TimeSpent', 'sum'), average_satisfaction = ('Satisfaction', 'mean'), average_importance = ('Importance', 'mean'), total_time_share_pct = ('ShareOfWeeklyHours (%)', 'sum')).round()
                df_sla.reset_index(inplace = True)
                st.write(df_sla)

                ## Sort based on Importance
                df_sla = df_sla.sort_values(by = ["average_importance"], ascending = False)
                sla_imp = barChart('SLA', 'average_importance', df_sla, 'SLA by Average Importance')
                imp = st.pyplot(sla_imp.get_figure())

                ## Sort based on Satisfaction
                df_sla = df_sla.sort_values(by = ["average_satisfaction"], ascending = False)
                sla_satisfaction = barChart('SLA', 'average_satisfaction', df_sla, 'SLA by Average Satisfaction')
                satisfaction = st.pyplot(sla_satisfaction.get_figure())
                                # ## agg using average for importance & satisfaction, while total timespent
                        ## pie chart/stacked bar chart: share of weekly hours
                        ## highlight which units with the biggest influence

                ## time share
                # sla_time_share = pieChart(df_sla['total_time_share'], df_sla['SLA'], 'Share of Weekly Hours by SLA')
                # # time_share = st.pyplot(sla_time_share.show())
                # time_share = st.plotly_chart(sla_time_share)
                # sla_time_share = stackedChart(df_sla, 'Share of Weekly Hours by SLA')
                # time_share = st.pyplot(sla_time_share.get_figure())
        st.write('If you are feeling stuck in life, here is the opportunity to work on the areas in your life where you feel less satisfied, but is highly important to you. I hope this tool has helped you reflect on your current life circumstances in some way.')
        st.write('Thank you so much for taking your time! Please reach out to me on LinkedIn for feedback, comments, suggestions or tips! Thanks again :)')
        st.markdown("[![Crystal Hariga LinkedIn Profile](https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg)](www.linkedin.com/in/cahyarini-hariga/)")
        
