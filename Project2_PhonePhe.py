import pandas as pd 
import plotly.express as px
import streamlit as st 
import warnings
import pymysql
import mysql.connector
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu

warnings.filterwarnings("ignore")
st. set_page_config(layout="wide")

def setting_bg():
    st.markdown(f""" <style>.stApp {{
                     background: url("");
                       background-size: cover}}
                    </style>""",unsafe_allow_html=True) 
  
setting_bg()

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["TRANSACTIONS ANALYSIS","USER BASED ANALYSIS","TOP 3 STATEWISE ANALYSIS","MAP VISUALIZATION"], 
                icons=["graph-up-arrow","pie-chart","bar-chart-line", "map"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "15px", "text-align": "left", "margin": "-2px", "--hover-color": ""},
                        "nav-link-selected": {"background-color": "#8B8878"}})


################## Creating connection with mysql workbench ##################
mySqldb = mysql.connector.connect(user='root', password='Mysql123@',host='127.0.0.1', database='guviphonepe',auth_plugin='mysql_native_password')
myCursor = mySqldb.cursor()

colT1,colT2 = st.columns([2,8])
with colT2:
    st.title(':violet[PhonePe Data Analysis]')
if selected == "TRANSACTIONS ANALYSIS":
    ################################### TRANSACTIONS ANALYSIS ###################################
    st.write('# :green[TRANSACTION ANALYSIS :]')
    tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS", "YEAR ANALYSIS", "OVERALL ANALYSIS"])
    ############################### STATE ANALYSIS ###############################

    myCursor.execute(f"select state, Year,Quarter, Transaction_type, Transaction_count,Transaction_amount from guviphonepe.data_aggregated_transactions;")
    df_Data_Aggregated_Transaction = pd.DataFrame(myCursor.fetchall(), columns=['State', 'Year','Quarter','Transaction_type','Transaction_count','Transaction_amount'])

    with tab1:
        Data_Aggregated_Transaction=df_Data_Aggregated_Transaction.copy()
        #Data_Aggregated_Transaction.drop(Data_Aggregated_Transaction.index[(Data_Aggregated_Transaction["State"] == "india")],axis=0,inplace=True)
        State_PaymentMode=Data_Aggregated_Transaction.copy()
        # st.write('### :green[State & PaymentMode]')
        col1, col2= st.columns(2)
        with col1:
            mode = st.selectbox(
                'Please Select The Mode',
                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='a')
        with col2:
            state = st.selectbox(
            'Please select the State',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'),key='b')
        State= state
        Year_List=[2018,2019,2020,2021,2022,2023] 
        Mode=mode
        #st.warning(State_PaymentMode)
        State_PaymentMode=State_PaymentMode.loc[(State_PaymentMode['State'] == State ) & (State_PaymentMode['Year'].isin(Year_List)) & 
                                (State_PaymentMode['Transaction_type']==Mode )]
        State_PaymentMode = State_PaymentMode.sort_values(by=['Year'])
        State_PaymentMode["Quarter"] = "Q"+State_PaymentMode['Quarter'].astype(str)
        State_PaymentMode["Year_Quarter"] = State_PaymentMode['Year'].astype(str) +"-"+ State_PaymentMode["Quarter"].astype(str)
        fig = px.bar(State_PaymentMode, x='Year_Quarter', y='Transaction_count',color="Transaction_count",
                    color_continuous_scale="Viridis")
        
        colT1,colT2 = st.columns([7,3])
        with colT1:
            st.write('#### '+State.upper()) 
            st.plotly_chart(fig,use_container_width=True)
        with colT2:
            st.success(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by user
            - X Axis is basically all Years with all quarters 
            - Y Axis represents Total Transactions in selected mode of payments        
            """
            )
            st.warning(
            """
            Important Observations:
            - User can observe the pattern of payment modes in a State 
            - We get basic idea about which mode of payments are either increasing or decreasing in a state
            """
            )
    ###########################  DISTRICTS ANALYSIS ###########################
    myCursor.execute(f"select State,Year,Quarter,District,Count as Tracsaction_Count,Amount from guviphonepe.Data_Map_Transactions")
    df_Data_Map_Transaction = pd.DataFrame(myCursor.fetchall(), columns=['State','Year','Quarter','District','Tracsaction_Count','Amount'])

    with tab2:
        col1, col2, col3= st.columns(3)
        with col1:
            Year = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022','2023'),key='y1')
        with col2:
            state = st.selectbox(
            'Please select the State',
            ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
            'assam', 'bihar', 'chandigarh', 'chhattisgarh',
            'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
            'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
            'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
            'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
            'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
            'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
            'uttarakhand', 'west-bengal'),key='dk')
        with col3:
            Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'),key='qwe')
        districts=df_Data_Map_Transaction.loc[(df_Data_Map_Transaction['State'] == state ) & (df_Data_Map_Transaction['Year']==int(Year))
                                            & (df_Data_Map_Transaction['Quarter']==int(Quarter))]

        #st.warning(districts)
        l=len(districts)    
        fig = px.bar(districts, x='District', y='Tracsaction_Count',color="Tracsaction_Count",
                    color_continuous_scale="Viridis")   
        colT1,colT2 = st.columns([7,3])
        with colT1:
            st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
            st.plotly_chart(fig,use_container_width=True)
        with colT2:
            st.success(
            """
            Details of BarGraph:
            - This entire data belongs to state selected by you
            - X Axis represents the districts of selected state
            - Y Axis represents total transactions        
            """
            )
            st.warning(
            """
            Important Observations:
            - User can observe how transactions are happening in districts of a selected state 
            - We can observe the leading distric in a state 
            """
            )
    ###########################  YEAR ANALYSIS ###########################
    with tab3:
        #st.write('### :green[PaymentMode and Year]')
        col1, col2= st.columns(2)
        with col1:
            M = st.selectbox(
                'Please select the Mode',
                ('Recharge & bill payments', 'Peer-to-peer payments', 'Merchant payments', 'Financial Services','Others'),key='D')
        with col2:
            Y = st.selectbox(
            'Please select the Year',
            ('2018', '2019', '2020','2021','2022','2023'),key='F')
        Year_PaymentMode=Data_Aggregated_Transaction.copy()
        Year=int(Y)
        Mode=M
        Year_PaymentMode=Year_PaymentMode.loc[(Year_PaymentMode['Year']==Year) & 
                                (Year_PaymentMode['Transaction_type']==Mode )]
        States_List=Year_PaymentMode['State'].unique()
        State_groupby_YP=Year_PaymentMode.groupby('State')
        Year_PaymentMode_Table=State_groupby_YP.sum()
        Year_PaymentMode_Table['states']=States_List
        del Year_PaymentMode_Table['Quarter'] 
        del Year_PaymentMode_Table['Year']
        Year_PaymentMode_Table = Year_PaymentMode_Table.sort_values(by=['Transaction_count'])
        fig2= px.bar(Year_PaymentMode_Table, x='states', y='Transaction_count',color="Transaction_count",
                    color_continuous_scale="Viridis",)   
        colT1,colT2 = st.columns([7,3])
        with colT1:
            st.write('#### '+str(Year)+' DATA ANALYSIS')
            st.plotly_chart(fig2,use_container_width=True) 
        with colT2:
            st.info(
            """
            Details of BarGraph:
            - This entire data belongs to selected Year
            - X Axis is all the states in increasing order of Total transactions
            - Y Axis represents total transactions in selected mode        
            """
            )
            st.error(
            """
            Important Observations:
            - We can observe the leading state with highest transactions in particular mode
            - We get basic idea about regional performance of Phonepe
            - Depending on the regional performance Phonepe can provide offers to particular place
            """
            )
    ########################### OVERALL ANALYSIS ###########################
    with tab4:    
        years=Data_Aggregated_Transaction.groupby('Year')
        years_List=Data_Aggregated_Transaction['Year'].unique()
        payMode_List=Data_Aggregated_Transaction['Transaction_type'].unique()
        #st.warning(payMode_List)
        years_Table=years.sum()
        del years_Table['Quarter']
        years_Table['year']=years_List
        #years_Table['Transaction_type']=payMode_List
        total_trans=years_Table['Transaction_count'].sum() # this data is used in sidebar    
        fig1 = px.pie(years_Table, values='Transaction_count', names='year',color_discrete_sequence=px.colors.sequential.Viridis, title='TOTAL TRANSACTIONS (2018 TO 2023)')
        col1, col2= st.columns([0.65,0.35])
        with col1:
            st.write('### :green[Drastical Increase in Transactions :]')
            st.plotly_chart(fig1)
        with col2:  
            st.write('#### :green[Year Wise Transaction count in INDIA]')      
            st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
if selected == "USER BASED ANALYSIS":
        ######################### USER ANALYSIS #########################

        st.write('# :orange[USERS DATA ANALYSIS ]')
        tab1, tab2, tab3, tab4 = st.tabs(["STATE ANALYSIS", "DISTRICT ANALYSIS","YEAR ANALYSIS","OVERALL ANALYSIS"])


        myCursor.execute(f"select State,Year,Quarter,District,Registered_user,App_opens from guviphonepe.data_map_user")
        df_Data_Aggregated_User_Summary = pd.DataFrame(myCursor.fetchall(), columns=['State','Year','Quarter','District','Registered_user','App_opens'])
        #df_Data_Aggregated_User = df_Data_Aggregated_User_Summary.copy

    ############################ USER STATE ANALYSIS ############################
        with tab1:
            st.write('### :blue[State & Userbase]')
            state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='W')
            app_opening=df_Data_Aggregated_User_Summary.groupby(['State','Year'])
            a_state=app_opening.sum()
            la=df_Data_Aggregated_User_Summary['State'] +"-"+ df_Data_Aggregated_User_Summary["Year"].astype(str)
            a_state["state_year"] = la.unique()
            sta=a_state["state_year"].str[:-5]
            a_state["state"] = sta
            sout=a_state.loc[(a_state['state'] == state) ]
            ta=sout['App_opens'].sum()
            tr=sout['Registered_user'].sum()
            sout['App_opens']=sout['App_opens'].mul(100/ta)
            sout['Registered_user']=sout['Registered_user'].mul(100/tr).copy()
            fig = go.Figure(data=[
                go.Bar(name='App_opens %', y=sout['App_opens'], x=sout['state_year'], marker={'color': 'pink'}),
                go.Bar(name='Registered_user %', y=sout['Registered_user'], x=sout['state_year'],marker={'color': 'orange'})
            ])
            # Change the bar mode
            fig.update_layout(barmode='group')
            colT1,colT2 = st.columns([7,3])
            with colT1:
                st.write("#### ",state.upper())
                st.plotly_chart(fig, use_container_width=True, height=200)
            with colT2:
                st.warning(
                """
                Details of BarGraph:
                - user need to select a state 
                - The X Axis shows both Registered users and App openings 
                - The Y Axis shows the Percentage of Registered users and App openings
                """
                )
                st.error(
                """
                Important Observations:
                - User can observe how the App Openings are growing and how Registered users are growing in a state
                - We can clearly obseve these two parameters with time
                - one can observe how user base is growing
                """
                )

        ############################ USER DISTRICT ANALYSIS ############################
        myCursor.execute(f"select State,Year,Quarter,District,Registered_user,App_opens from guviphonepe.data_map_user")
        df_Data_Map_User_Table = pd.DataFrame(myCursor.fetchall(), columns=['State','Year','Quarter','District','Registered_user','App_opens'])


        with tab2:
            col1, col2, col3= st.columns(3)
            with col1:
                Year = st.selectbox(
                    'Please select the Year',
                    ('2022', '2021','2020','2019','2018'),key='y12')
            with col2:
                state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='dk2')
            with col3:
                Quarter = st.selectbox(
                    'Please select the Quarter',
                    ('1', '2', '3','4'),key='qwe2')
            districts=df_Data_Map_User_Table.loc[(df_Data_Map_User_Table['State'] == state ) & (df_Data_Map_User_Table['Year']==int(Year))
                                                & (df_Data_Map_User_Table['Quarter']==int(Quarter))]
            l=len(districts)    
            fig = px.bar(districts, x='District', y='App_opens',color="App_opens",
                        color_continuous_scale="reds")   
            colT1,colT2 = st.columns([7,3])
            with colT1:
                if l:
                    st.write('#### '+state.upper()+' WITH '+str(l)+' DISTRICTS')
                    st.plotly_chart(fig,use_container_width=True)
                else:
                    st.write('#### NO DISTRICTS DATA AVAILABLE FOR '+state.upper())

            with colT2:
                if l:
                    st.error(
                """
                Details of BarGraph:
                - This entire data belongs to state selected by you
                - X Axis represents the districts of selected state
                - Y Axis represents App Openings       
                """
                    )
                    st.warning(
                """
                Important Observations:
                - User can observe how App Openings are happening in districts of a selected state 
                - We can observe the leading distric in a state 
                """
                    )
        ############################ USER YEAR ANALYSIS ############################
        myCursor.execute(f"select a.State as State,a.Year as Year,a.Quarter as Quarter,a.District as District,a.App_opens as App_opens,b.Brands,b.Count as Registered_user,b.Percentage from guviphonepe.data_map_user a , guviphonepe.data_aggregated_user b where a.state = b.State and a.Year = b.Year and a.Quarter=b.Quarter")
        df_Data_Aggregated_User = pd.DataFrame(myCursor.fetchall(), columns=['State','Year','Quarter','District','App_opens','Brands','Registered_user','Percentage'])

        with tab3:
            st.write('### :orange[Brand Share] ')
            col1, col2= st.columns(2)
            with col1:
                state = st.selectbox(
                'Please select the State',
                ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                'haryana', 'himachal-pradesh', 'jammu-&-kashmir',
                'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep',
                'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan',
                'sikkim', 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                'uttarakhand', 'west-bengal'),key='Z')
            with col2:
                Y = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022'),key='X')
            y=int(Y)
            s=state
            brand=df_Data_Aggregated_User[df_Data_Aggregated_User['Year']==y] 
            brand=df_Data_Aggregated_User.loc[(df_Data_Aggregated_User['Year'] == y) & (df_Data_Aggregated_User['State'] ==s)]
            myb= brand['Brands'].unique()
            x = sorted(myb).copy()
            b=brand.groupby('Brands').sum()
            b['brand']=x
            br=b['Registered_user'].sum()
            labels = b['brand']
            values = b['Registered_user'] # customdata=labels,
            fig3 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,textinfo='label+percent',texttemplate='%{label}<br>%{percent:1%f}',insidetextorientation='horizontal',textfont=dict(color='#000000'),marker_colors=px.colors.qualitative.Prism)])
            
            colT1,colT2 = st.columns([7,3])
            with colT1:
                st.write("#### ",state.upper()+' IN '+Y)
                st.plotly_chart(fig3, use_container_width=True)        
            with colT2:
                st.success(
                """
                Details of Donut Chart:        
                - Initially we select data by means of State and Year
                - Percentage of registered users is represented with dounut chat through Device Brand
                """
                )
                st.info(
                """
                Important Observations:
                - User can observe the top leading brands in a particular state
                - Brands with less users
                - Brands with high users
                - Can make app download advices to growing brands
                """
                )

            b = b.sort_values(by=['Registered_user'])
            fig4= px.bar(b, x='brand', y='Registered_user',color="Registered_user",
                        title='In '+state+' in '+str(y),
                        color_continuous_scale="oranges",)
            with st.expander("See Bar graph for the same data"):
                st.plotly_chart(fig4,use_container_width=True) 

        ############################ USER OVERALL ANALYSIS ############################

            with tab4:
                years=df_Data_Aggregated_User_Summary.groupby('Year')
                years_List=df_Data_Aggregated_User_Summary['Year'].unique()
                #state_List=df_Data_Aggregated_User_Summary['State'].unique()
                #st.warning(state_List)
                years_Table=years.sum()
                del years_Table['Quarter']
                years_Table['year']=years_List
                total_trans=years_Table['Registered_user'].sum() # this data is used in sidebar    
                fig1 = px.pie(years_Table, values='Registered_user', names='year',color_discrete_sequence=px.colors.sequential.RdBu, title='TOTAL REGISTERED USERS (2018 TO 2022)')
                col1, col2= st.columns([0.7,0.3])
                with col1:
                    # st.write('### :green[Drastical Increase in Transactions :rocket:]')
                    labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India",
                        "Rest of World"]

                    # Create subplots: use 'domain' type for Pie subplot
                    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
                    fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['Registered_user'], name="REGISTERED USERS"),
                                1, 1)
                    fig.add_trace(go.Pie(labels=years_Table['year'], values=years_Table['App_opens'], name="APP OPENINGS"),
                                1, 2)

                    # Use `hole` to create a donut-like pie chart
                    fig.update_traces(hole=.6, hoverinfo="label+percent+name")

                    fig.update_layout(
                        title_text="USERS DATA (2018 TO 2022)",
                        # Add annotations in the center of the donut pies.
                        annotations=[dict(text='USERS', x=0.18, y=0.5, font_size=20, showarrow=False),
                                    dict(text='APP', x=0.82, y=0.5, font_size=20, showarrow=False)])
                    # st.plotly_chart(fig1)
                    st.plotly_chart(fig)
                with col2:  
                    # st.write('#### :green[Year Wise Transaction Analysis in INDIA]')      
                    st.markdown(years_Table.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                    st.info(
                    """
                    Important Observation:
                    -  We can see that the Registered Users and App openings are increasing year by year
                    
                    """
                    )
if selected == "TOP 3 STATEWISE ANALYSIS":
    ############################ TOP 3 STATES DATA ############################         
    myCursor.execute(f"select State,Year,Quarter,sum(Registered_user) as Registered_user ,sum(App_opens) as App_opens from guviphonepe.data_map_user group by State,Year,Quarter order by State DESC;")
    df_Data_Map_User = pd.DataFrame(myCursor.fetchall(), columns=['State','Year','Quarter','Registered_user','App_opens'])

    myCursor.execute(f"select state, Year,Quarter, Transaction_type, Transaction_count,Transaction_amount from guviphonepe.data_aggregated_transactions;")
    df_Data_Aggregated_Transaction = pd.DataFrame(myCursor.fetchall(), columns=['State', 'Year','Quarter','Transaction_type','Transaction_count','Transaction_amount'])

    st.write('# :red[TOP 3 STATES DATA]')
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
                'Please select the Year',
                ('2023','2022', '2021','2020','2019','2018'),key='y3t')
    with c2:
        Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'),key='q3t')
    #Data_Map_User=df_Data_Aggregated_User.copy() 
    top_states=df_Data_Map_User.loc[(df_Data_Map_User['Year'] == int(Year)) & (df_Data_Map_User['Quarter'] ==int(Quarter))]
    top_states_r = top_states.sort_values(by=['Registered_user'], ascending=False)
    #st.warning(top_states_r)
    top_states_a = top_states.sort_values(by=['App_opens'], ascending=False) 
    top_states_T=df_Data_Aggregated_Transaction.loc[(df_Data_Aggregated_Transaction['Year'] == int(Year)) & (df_Data_Aggregated_Transaction['Quarter'] ==int(Quarter))]
    topst=top_states_T.groupby('State')
    x=topst.sum().sort_values(by=['Transaction_count'], ascending=False)
    y=topst.sum().sort_values(by=['Transaction_amount'], ascending=False)
    col1, col2, col3, col4= st.columns([2.5,2.5,2.5,2.5])
    with col1:
        rt=top_states_r[0:3]
        st.markdown("#### :orange[Registered Users]")
        st.markdown(rt[[ 'State','Registered_user']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    with col2:
        at=top_states_a[0:3]
        st.markdown("#### :orange[PhonePeApp Openings]")
        st.markdown(at[['State','App_opens']].style.hide(axis="index").to_html(), unsafe_allow_html=True)
    with col3:
        st.markdown("#### :orange[Total Transactions]")
        st.write(x[['Transaction_count']][0:3])
    with col4:
        st.markdown("#### :orange[Total Amount]")
        st.write(y['Transaction_amount'][0:3])      
            
if selected == "MAP VISUALIZATION":
    ############################ INDIA MAP ANALYSIS ############################
    Scatter_Geo_Dataset =  pd.read_csv(r'C:\\Thiyagu\\GUVI\\Project_2_Phonepe\\data\\Data_Map_Districts_Longitude_Latitude.csv')
    Coropleth_Dataset =  pd.read_csv(r'C:\\Thiyagu\\GUVI\\Project_2_Phonepe\\data\\Data_Map_IndiaStates_TU.csv')
    Data_Map_Transaction_df = pd.read_csv(r'C:\\Thiyagu\\GUVI\\Project_2_Phonepe\\data\\Data_Map_Transaction_Table.csv')
    Indian_States= pd.read_csv(r'C:\\Thiyagu\\GUVI\\Project_2_Phonepe\\data\\Longitude_Latitude_State_Table.csv')
    c1,c2=st.columns(2)
    with c1:
        Year = st.selectbox(
                'Please select the Year',
                ('2018', '2019', '2020','2021','2022'))
    with c2:
        Quarter = st.selectbox(
                'Please select the Quarter',
                ('1', '2', '3','4'))
    year=int(Year)
    quarter=int(Quarter)
    Transaction_scatter_districts=Data_Map_Transaction_df.loc[(Data_Map_Transaction_df['Year'] == year ) & (Data_Map_Transaction_df['Quarter']==quarter) ].copy()
    Transaction_Coropleth_States=Transaction_scatter_districts[Transaction_scatter_districts["State"] == "india"]
    Transaction_scatter_districts.drop(Transaction_scatter_districts.index[(Transaction_scatter_districts["State"] == "india")],axis=0,inplace=True)
    # Dynamic Scattergeo Data Generation
    Transaction_scatter_districts = Transaction_scatter_districts.sort_values(by=['Place_Name'], ascending=False)
    Scatter_Geo_Dataset = Scatter_Geo_Dataset.sort_values(by=['District'], ascending=False) 
    Total_Amount=[]
    for i in Transaction_scatter_districts['Total_Amount']:
        Total_Amount.append(i)
    Scatter_Geo_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_scatter_districts['Total_Transactions_count']:
        Total_Transaction.append(i)
    Scatter_Geo_Dataset['Total_Transactions']=Total_Transaction
    Scatter_Geo_Dataset['Year_Quarter']=str(year)+'-Q'+str(quarter)
    # Dynamic Coropleth
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['state'], ascending=False)
    Transaction_Coropleth_States = Transaction_Coropleth_States.sort_values(by=['Place_Name'], ascending=False)
    Total_Amount=[]
    for i in Transaction_Coropleth_States['Total_Amount']:
        Total_Amount.append(i)
    Coropleth_Dataset['Total_Amount']=Total_Amount
    Total_Transaction=[]
    for i in Transaction_Coropleth_States['Total_Transactions_count']:
        Total_Transaction.append(i)
    Coropleth_Dataset['Total_Transactions']=Total_Transaction


    ############################ INDIA MAP ############################
    #scatter plotting the states codes 
    Indian_States = Indian_States.sort_values(by=['state'], ascending=False)
    Indian_States['Registered_Users']=Coropleth_Dataset['Registered_Users']
    Indian_States['Total_Amount']=Coropleth_Dataset['Total_Amount']
    Indian_States['Total_Transactions']=Coropleth_Dataset['Total_Transactions']
    Indian_States['Year_Quarter']=str(year)+'-Q'+str(quarter)
    fig=px.scatter_geo(Indian_States,
                        lon=Indian_States['Longitude'],
                        lat=Indian_States['Latitude'],                                
                        text = Indian_States['code'], #It will display district names on map
                        hover_name="state", 
                        hover_data=['Total_Amount',"Total_Transactions","Year_Quarter"],
                        )
    fig.update_traces(marker=dict(color="white" ,size=0.3))
    fig.update_geos(fitbounds="locations", visible=False,)
        # scatter plotting districts
    Scatter_Geo_Dataset['col']=Scatter_Geo_Dataset['Total_Transactions']
    fig1=px.scatter_geo(Scatter_Geo_Dataset,
                        lon=Scatter_Geo_Dataset['Longitude'],
                        lat=Scatter_Geo_Dataset['Latitude'],
                        color=Scatter_Geo_Dataset['col'],
                        size=Scatter_Geo_Dataset['Total_Transactions'],     
                        #text = Scatter_Geo_Dataset['District'], #It will display district names on map
                        hover_name="District", 
                        hover_data=["State", "Total_Amount","Total_Transactions","Year_Quarter"],
                        title='District',
                        size_max=22,)
    fig1.update_traces(marker=dict(color="rebeccapurple" ,line_width=1))    #rebeccapurple
    #coropleth mapping india
    fig_ch = px.choropleth(
                        Coropleth_Dataset,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',                
                        locations='state',
                        color="Total_Transactions",                                       
                        )
    fig_ch.update_geos(fitbounds="locations", visible=False,)
    #combining districts states and coropleth
    fig_ch.add_trace( fig.data[0])
    fig_ch.add_trace(fig1.data[0])
    st.write("### **:blue[PhonePe India Map]**")
    colT1,colT2 = st.columns([6,4])
    with colT1:
        st.plotly_chart(fig_ch, use_container_width=True)
    with colT2:
        st.info(
        """
        Details of Map:
        - The darkness of the state color represents the total transactions
        - The Size of the Circles represents the total transactions dictrict wise
        - The bigger the Circle the higher the transactions
        - Hover data will show the details like Total transactions, Total amount
        """
        )
        st.info(
        """
        Important Observations:
        - User can observe Transactions of PhonePe in both statewide and Districtwide.
        - We can clearly see the states with highest transactions in the given year and quarter
        - We get basic idea about transactions district wide
        """
        )
    ############################ TRANSACTION MAP HIDDEN BARGRAPH ############################
    Coropleth_Dataset = Coropleth_Dataset.sort_values(by=['Total_Transactions'])
    fig = px.bar(Coropleth_Dataset, x='state', y='Total_Transactions',title=str(year)+" Quarter-"+str(quarter))
    with st.expander("See Bar graph for the same data"):
        st.plotly_chart(fig, use_container_width=True)
        st.info('**:blue[The above bar graph showing the increasing order of PhonePe Transactions according to the states of India, Here we can observe the top states with highest Transaction by looking at graph]**')
