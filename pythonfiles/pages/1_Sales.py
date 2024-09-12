import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
##=============================================================================================
def login():
    st.title("login")
    username=st.text_input("Username")
    password=st.text_input("Password",type="password")
    if st.button("login"):
        if username=="admin" and password=="password":
            st.session_state.logged_in=True
            st.success("login Sucessful")
        else:
            st.error("invalid username or password")
def dashboard():
##=====================================================================================
    st.set_page_config(page_title="SalesAnalysis!!!", page_icon=":bar_chart:",layout="wide")

    st.title(" :bar_chart: CCL Group Sales Analysis")
    st.markdown('<style>div.block-container{padding-center:1rem;}</style>',unsafe_allow_html=True)

    fl = st.sidebar.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
    if fl is not None:
        filename = fl.name
        st.write(filename)
        df = pd.read_csv(filename, encoding = "ISO-8859-1")
    else:
        os.chdir(r"C:\Users\Ramesh.M\OneDrive - CCL Products (India) Ltd\Desktop\Streamlit")
        df = pd.read_csv("Sales.csv", encoding = "ISO-8859-1")

    Options = df['Month'].unique()
    selected_options = st.sidebar.multiselect('Select the Month:', options=Options,default=['JUL'])
    df = df[df['Month'].isin(selected_options)].copy()

    st.sidebar.header("Choose your filter: ")
    region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
    if not region:
        df2 = df.copy()
    else:
        df2 = df[df["Region"].isin(region)]
    country = st.sidebar.multiselect("Pick the Country", df2["Country"].unique())
    if not country:
        df3 = df2.copy()
    else:
        df3 = df2[df2["Country"].isin(country)]
    customer = st.sidebar.multiselect("Pick the Customer",df3["Customer name"].unique())

    if not region and not country and not customer:
        filtered_df = df
    elif not country and not customer:
        filtered_df = df[df["Region"].isin(region)]
    elif not region and not customer:
        filtered_df = df[df["Country"].isin(country)]
    elif country and customer:
        filtered_df = df3[df["Country"].isin(country) & df3["Customer name"].isin(customer)]
    elif region and customer:
        filtered_df = df3[df["Region"].isin(region) & df3["Customer name"].isin(customer)]
    elif region and country:
        filtered_df = df3[df["Region"].isin(region) & df3["Country"].isin(country)]
    elif customer:
        filtered_df = df3[df3["Customer name"].isin(customer)]
    else:
        filtered_df = df3[df3["Region"].isin(region) & df3["Country"].isin(country) & df3["Customer name"].isin(customer)]
    ##==================================
    group=filtered_df.groupby(by=['Customer name'],as_index=False)[['LY QTY (MT)',"LY Val(Lakhs)",'Budget Vol(MT)','Budget Val(Lakhs)',"CY QTY (MT)","CY Val(Lakhs)"]].sum()
    BgrowthM=(group['Budget Vol(MT)'].sum()/group['LY QTY (MT)'].sum()-1)*100
    BgrowthV=(group['Budget Val(Lakhs)'].sum()/group['LY Val(Lakhs)'].sum()-1)*100
    CgrowthM=(group['CY QTY (MT)'].sum()/group['LY QTY (MT)'].sum()-1)*100
    CgrowthV=(group['CY Val(Lakhs)'].sum()/group['LY Val(Lakhs)'].sum()-1)*100
    AAchM=(group['CY QTY (MT)'].sum()/group['Budget Vol(MT)'].sum())*100
    AAchV=(group['CY Val(Lakhs)'].sum()/group['Budget Val(Lakhs)'].sum())*100
    group['LY Avg Price(₹)']=group["LY Val(Lakhs)"]/(group['LY QTY (MT)']*1000)
    group['Budget Avg Price(₹)']=group['Budget Val(Lakhs)']/(group['Budget Vol(MT)']*1000)
    group['CY Avg Price(₹)']=group["CY Val(Lakhs)"]/(group['CY QTY (MT)']*1000)
    group1=group[['Customer name','LY QTY (MT)',"LY Val(Lakhs)",'LY Avg Price(₹)','Budget Vol(MT)','Budget Val(Lakhs)','Budget Avg Price(₹)','CY QTY (MT)',"CY Val(Lakhs)",'CY Avg Price(₹)']]
    group2=group1.sort_values('CY QTY (MT)',ascending=0).round(2)
    lymt=group2['LY QTY (MT)'].sum()
    budgetmt=group2['Budget Vol(MT)'].sum()
    budgetval=group2['Budget Val(Lakhs)'].sum()
    cymt=group2['CY QTY (MT)'].sum()
    cyval=group2["CY Val(Lakhs)"].sum()
    group3=group2['LY Avg Price(₹)'].dropna()
    group4=group2['Budget Avg Price(₹)'].dropna()
    group5=group2['CY Avg Price(₹)'].dropna()

    lyAvg=group3.values.tolist()
    budAvg=group4.values.tolist()
    cyAvg=group5.values.tolist()



    total1,total2,total3,total4,total5 = st.columns(5,gap='large')
    with total1:
        st.info('LY Sales in (MT)')
        st.metric('Sum of sales Qty',f"{lymt:,.0f} MT",f"Bud Vol Gr(%) : {BgrowthM:,.0f} %")
    with total2:
        st.info('Budget QTY (MT)')
        st.metric('Sum of Budget Qty',f"{budgetmt:,.0f} MT",f"CY Vol Ach(%) : {AAchM:,.0f} %")
    with total3:
        st.info('CY Sales in (MT)')
        st.metric('Sum of sales Qty',f"{cymt:,.0f} MT",f"CY Vol Gr(%) : {CgrowthM:,.0f} %")
    with total4:
        st.info('Budget val(₹)')
        st.metric('Sum of Budget value',f"₹{budgetval:,.0f} L",f"CY Val Gr(%) : {CgrowthV:,.0f} %")
    with total5:
        st.info('CY Sales Val(₹)')
        st.metric('Sum of sales value',f"₹{cyval:,.0f} L",f"CY Val Ach(%) : {AAchV:,.0f} %")

    ##=======================================
    volumes_df = filtered_df.groupby(by = ["Business"], as_index = False)["CY QTY (MT)"].sum()
    volsal_bus=volumes_df['Business'].values.tolist()
    volsal_qty=volumes_df['CY QTY (MT)'].values.tolist()

    Lvolumes_df = filtered_df.groupby(by = ["Business"], as_index = False)["LY QTY (MT)"].sum()
    Lvolsal_bus=Lvolumes_df['Business'].values.tolist()
    Lvolsal_qty=Lvolumes_df['LY QTY (MT)'].values.tolist()

    values_df = filtered_df.groupby(by = ["Business"], as_index = False)["CY Val(Lakhs)"].sum()
    valsal_bus=values_df['Business'].values.tolist()
    valsal_qty=values_df['CY Val(Lakhs)'].values.tolist()

    Lvalues_df = filtered_df.groupby(by = ["Business"], as_index = False)["LY Val(Lakhs)"].sum()
    Lvalsal_bus=Lvalues_df['Business'].values.tolist()
    Lvalsal_qty=Lvalues_df['LY Val(Lakhs)'].values.tolist()

    Budget_vol = filtered_df.groupby(by=["Business"],as_index=False)["Budget Vol(MT)"].sum()
    volbud_bus=Budget_vol['Business'].values.tolist()
    volbud_qty=Budget_vol['Budget Vol(MT)'].values.tolist()

    Budget_val = filtered_df.groupby(by=["Business"],as_index=False)["Budget Val(Lakhs)"].sum()
    valbud_bus=Budget_val['Business'].values.tolist()
    valbud_qty=Budget_val['Budget Val(Lakhs)'].values.tolist()
    ##========================================
    mvolumes_df = filtered_df.groupby(by = ["Marketing Rep."], as_index = False)["CY QTY (MT)"].sum()
    mvolsal_bus=mvolumes_df["Marketing Rep."].values.tolist()
    mvolsal_qty=mvolumes_df['CY QTY (MT)'].values.tolist()

    Lmvolumes_df = filtered_df.groupby(by = ["Marketing Rep."], as_index = False)["LY QTY (MT)"].sum()
    Lmvolsal_bus=Lmvolumes_df["Marketing Rep."].values.tolist()
    Lmvolsal_qty=Lmvolumes_df['LY QTY (MT)'].values.tolist()

    mvalues_df = filtered_df.groupby(by = ["Marketing Rep."], as_index = False)["CY Val(Lakhs)"].sum()
    mvalsal_bus=mvalues_df["Marketing Rep."].values.tolist()
    mvalsal_qty=mvalues_df['CY Val(Lakhs)'].values.tolist()

    Lmvalues_df = filtered_df.groupby(by = ["Marketing Rep."], as_index = False)["LY Val(Lakhs)"].sum()
    Lmvalsal_bus=Lmvalues_df["Marketing Rep."].values.tolist()
    Lmvalsal_qty=Lmvalues_df['LY Val(Lakhs)'].values.tolist()

    mBudget_vol = filtered_df.groupby(by=["Marketing Rep."],as_index=False)["Budget Vol(MT)"].sum()
    mvolbud_bus=mBudget_vol["Marketing Rep."].values.tolist()
    mvolbud_qty=mBudget_vol['Budget Vol(MT)'].values.tolist()

    mBudget_val = filtered_df.groupby(by=["Marketing Rep."],as_index=False)["Budget Val(Lakhs)"].sum()
    mvalbud_bus=mBudget_val["Marketing Rep."].values.tolist()
    mvalbud_qty=mBudget_val['Budget Val(Lakhs)'].values.tolist()
    ##===========================================================
    Bdf1=filtered_df.groupby(['Business'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    BdfA=Bdf1['CY QTY (MT)'].sum()
    BdfB=Bdf1['Budget Vol(MT)'].sum()
    BdfC=Bdf1['LY QTY (MT)'].sum()
    Bdf2=Bdf1.sort_values('CY QTY (MT)',ascending=0).round(2)
    Bdf2.loc['Grand_Total']= Bdf1.sum(numeric_only=True, axis=0).round(2)
    Bdf2["Ach%"]=(Bdf2['CY QTY (MT)']/Bdf2['Budget Vol(MT)']*100).round(2)
    Bdf2['QTY Growth%']=((Bdf2['CY QTY (MT)']/Bdf2['LY QTY (MT)']-1)*100).round(2)

    Bdf3=filtered_df.groupby(['Business'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    BdfA=Bdf3['CY Val(Lakhs)'].sum()
    BdfB=Bdf3['Budget Val(Lakhs)'].sum()
    BdfC=Bdf3['LY Val(Lakhs)'].sum()
    Bdf4=Bdf3.sort_values('CY Val(Lakhs)',ascending=0).round(2)
    Bdf4.loc['Grand_Total']= Bdf4.sum(numeric_only=True, axis=0).round(2)
    Bdf4["Ach%"]=(Bdf4['CY Val(Lakhs)']/Bdf4['Budget Val(Lakhs)']*100).round(2)
    Bdf4['Val Growth%']=((Bdf4['CY Val(Lakhs)']/Bdf4['LY Val(Lakhs)']-1)*100).round(2)

    Rdf1=filtered_df.groupby(['Marketing Rep.'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    RdfA=Rdf1['CY QTY (MT)'].sum()
    RdfB=Rdf1['Budget Vol(MT)'].sum()
    RdfC=Rdf1['LY QTY (MT)'].sum()
    Rdf2=Rdf1.sort_values('Marketing Rep.',ascending=1).round(2)
    Rdf2.loc['Grand_Total']= Rdf2.sum(numeric_only=True, axis=0).round(2)
    Rdf2["Ach%"]=(Rdf2['CY QTY (MT)']/Rdf2['Budget Vol(MT)']*100).round(2)
    Rdf2['QTY Growth%']=((Rdf2['CY QTY (MT)']/Rdf2['LY QTY (MT)']-1)*100).round(2)

    Rdf3=filtered_df.groupby(['Marketing Rep.'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    RdfA=Rdf3['CY Val(Lakhs)'].sum()
    RdfB=Rdf3['Budget Val(Lakhs)'].sum()
    RdfC=Rdf3['LY Val(Lakhs)'].sum()
    Rdf4=Rdf3.sort_values('Marketing Rep.',ascending=1).round(2)
    Rdf4.loc['Grand_Total']= Rdf4.sum(numeric_only=True, axis=0).round(2)
    Rdf4["Ach%"]=(Rdf4['CY Val(Lakhs)']/Rdf4['Budget Val(Lakhs)']*100).round(2)
    Rdf4['Val Growth%']=((Rdf4['CY Val(Lakhs)']/Rdf4['LY Val(Lakhs)']-1)*100).round(2)

    Pdf1=filtered_df.groupby(['Type'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    Pdf1["Ach%"]=Pdf1['CY QTY (MT)']/Pdf1['Budget Vol(MT)']*100
    PdfA=Pdf1['CY QTY (MT)'].sum()
    PdfB=Pdf1['Budget Vol(MT)'].sum()
    PdfC=Pdf1['LY QTY (MT)'].sum()
    Pdf1["Vol Growth%"]=(Pdf1['CY QTY (MT)']/Pdf1['LY QTY (MT)']-1)*100
    Pdf1['QTY Cont%']=Pdf1['CY QTY (MT)']/PdfA*100
    Pdf1['Bud Cont%']=Pdf1['Budget Vol(MT)']/PdfB*100
    Pdf2=Pdf1.sort_values('CY QTY (MT)',ascending=0).round(2)

    Pdf3=filtered_df.groupby(['Type'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    Pdf3["Ach%"]=Pdf3['CY Val(Lakhs)']/Pdf3['Budget Val(Lakhs)']*100
    PdfA=Pdf3['CY Val(Lakhs)'].sum()
    PdfB=Pdf3['Budget Val(Lakhs)'].sum()
    PdfC=Pdf3['LY Val(Lakhs)'].sum()
    Pdf3["Val Growth%"]=(Pdf3['CY Val(Lakhs)']/Pdf3['LY Val(Lakhs)']-1)*100
    Pdf3['QTY Cont%']=Pdf3['CY Val(Lakhs)']/PdfA*100
    Pdf3['Bud Cont%']=Pdf3['Budget Val(Lakhs)']/PdfB*100
    Pdf4=Pdf3.sort_values('CY Val(Lakhs)',ascending=0).round(2)

    Cdf1=filtered_df.groupby(['Pack Cat'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    Cdf1["Ach%"]=Cdf1['CY QTY (MT)']/Cdf1['Budget Vol(MT)']*100
    CdfA=Cdf1['CY QTY (MT)'].sum()
    CdfB=Cdf1['Budget Vol(MT)'].sum()
    CdfC=Cdf1['Budget Vol(MT)'].sum()
    Cdf1["QTY Growth%"]=(Cdf1['CY QTY (MT)']/Cdf1['LY QTY (MT)']-1)*100
    Cdf2=Cdf1.sort_values('CY QTY (MT)',ascending=0).round(2)

    Cdf3=filtered_df.groupby(['Pack Cat'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    Cdf3["Ach%"]=Cdf3['CY Val(Lakhs)']/Cdf3['Budget Val(Lakhs)']*100
    CdfA=Cdf3['CY Val(Lakhs)'].sum()
    CdfB=Cdf3['Budget Val(Lakhs)'].sum()
    CdfC=Cdf3['LY Val(Lakhs)'].sum()
    Cdf3["Val Growth%"]=(Cdf3['CY Val(Lakhs)']/Cdf3['LY Val(Lakhs)']-1)*100
    Cdf4=Cdf3.sort_values('CY Val(Lakhs)',ascending=0).round(2)

    Tdf1=filtered_df.groupby(['Pack Type'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    Tdf1["Ach%"]=Tdf1['CY QTY (MT)']/Tdf1['Budget Vol(MT)']*100
    TdfA=Tdf1['CY QTY (MT)'].sum()
    TdfB=Tdf1['Budget Vol(MT)'].sum()
    TdfC=Tdf1['LY QTY (MT)'].sum()
    Tdf1["QTY Growth%"]=(Tdf1['CY QTY (MT)']/Tdf1['LY QTY (MT)']-1)*100
    Tdf1['QTY Cont%']=Tdf1['CY QTY (MT)']/TdfA*100
    Tdf1['Bud Cont%']=Tdf1['Budget Vol(MT)']/TdfB*100
    Tdf2=Tdf1.sort_values('CY QTY (MT)',ascending=0).round(2)

    Tdf3=filtered_df.groupby(['Pack Type'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    Tdf3["Ach%"]=Tdf3['CY Val(Lakhs)']/Tdf3['Budget Val(Lakhs)']*100
    TdfA=Tdf3['CY Val(Lakhs)'].sum()
    TdfB=Tdf3['Budget Val(Lakhs)'].sum()
    TdfC=Tdf3['LY Val(Lakhs)'].sum()
    Tdf3["Val Growth%"]=(Tdf3['CY Val(Lakhs)']/Tdf3['LY Val(Lakhs)']-1)*100
    Tdf3['QTY Cont%']=Tdf3['CY Val(Lakhs)']/TdfA*100
    Tdf3['Bud Cont%']=Tdf3['Budget Val(Lakhs)']/TdfB*100
    Tdf4=Tdf3.sort_values('CY Val(Lakhs)',ascending=0).round(2)

    ReTdf1=filtered_df.groupby(['Region'])[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)']].sum()
    ReTdf1["Ach%"]=ReTdf1['CY QTY (MT)']/ReTdf1['Budget Vol(MT)']*100
    ReTdfA=ReTdf1['CY QTY (MT)'].sum()
    ReTdfB=ReTdf1['Budget Vol(MT)'].sum()
    ReTdfC=ReTdf1['LY QTY (MT)'].sum()
    ReTdf1["QTY Growth%"]=(ReTdf1['CY QTY (MT)']/ReTdf1['LY QTY (MT)']-1)*100
    ReTdf1['QTY Cont%']=ReTdf1['CY QTY (MT)']/ReTdfA*100
    ReTdf1['Bud Cont%']=ReTdf1['Budget Vol(MT)']/ReTdfB*100
    ReTdf2=ReTdf1.sort_values('CY QTY (MT)',ascending=0).round(2)   

    ReTdf3=filtered_df.groupby(['Region'])[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    ReTdf3["Ach%"]=ReTdf3['CY Val(Lakhs)']/ReTdf3['Budget Val(Lakhs)']*100
    ReTdfA=ReTdf3['CY Val(Lakhs)'].sum()
    ReTdfB=ReTdf3['Budget Val(Lakhs)'].sum()
    ReTdfC=ReTdf3['LY Val(Lakhs)'].sum()
    ReTdf3["Val Growth%"]=(ReTdf3['CY Val(Lakhs)']/ReTdf3['LY Val(Lakhs)']-1)*100
    ReTdf3['QTY Cont%']=ReTdf3['CY Val(Lakhs)']/ReTdfA*100
    ReTdf3['Bud Cont%']=ReTdf3['Budget Val(Lakhs)']/ReTdfB*100
    ReTdf4=ReTdf3.sort_values('CY Val(Lakhs)',ascending=0).round(2)
    ##==========================================================================================
    col1, col2=st.columns((2))
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=Lvolsal_bus,y=Lvolsal_qty,name='LY Sales Volumes',marker_color='#3BB9FF',
            text=['{:,.0f}MT'.format(x) for x in Lvolsal_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=volbud_bus,y=volbud_qty,name='Budget Volumes',marker_color='#EB5406',
            text=['{:,.0f}MT'.format(x) for x in volbud_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=volsal_bus,y=volsal_qty,name='CY Sales Volumes',marker_color='#228B22',
            text=['{:,.0f}MT'.format(x) for x in volsal_qty],textposition='auto'
        ))
        
        fig.update_layout(
            title="Sales Volume (MT) by Unit - LY vs Budget vs CY",xaxis_title='Business Type',
            yaxis_title='Volumes(MT)',barmode='group'
        )

        st.plotly_chart(fig,use_container_width=True, height = 200)
        st.write(Bdf2)
    with col2:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=Lvalsal_bus,y=Lvalsal_qty,name='LY Sales Values',marker_color='#3BB9FF',
            text=['₹{:,.0f}'.format(x) for x in Lvalsal_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=valbud_bus,y=valbud_qty,name='Budget Values',marker_color='#EB5406',
            text=['₹{:,.0f}'.format(x) for x in valbud_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=valsal_bus,y=valsal_qty,name='CY Sales Values',marker_color='#228B22',
            text=['₹{:,.0f}'.format(x) for x in valsal_qty],textposition='auto'
        ))
        fig.update_layout(
            title="Sales Value (₹, Lakhs) by Unit - LY vs Budget vs CY",xaxis_title='Business Type',
            yaxis_title='Values in Lakhs',barmode='group'
        )

        st.plotly_chart(fig,use_container_width=True, height = 200)
        st.write(Bdf4)

    cl1, cl2 = st.columns((2))
    with cl1:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=Lmvolsal_bus,y=Lmvolsal_qty,name='LY Sales Volumes',marker_color='#3BB9FF',
            text=['{:,.0f}MT'.format(x) for x in Lmvolsal_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=mvolbud_bus,y=mvolbud_qty,name='Budget Volumes',marker_color='#EB5406',
            text=['{:,.0f}MT'.format(x) for x in mvolbud_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=mvolsal_bus,y=mvolsal_qty,name='CY Sales Volumes',marker_color='#228B22',
            text=['{:,.0f}MT'.format(x) for x in mvolsal_qty],textposition='auto'
        ))
        fig.update_layout(
            title="Sales Volume (MT) by Representative - LY vs Budget vs CY",xaxis_title='Marketing Representive Type',
            yaxis_title='Volumes(MT)',barmode='group'
        )

        st.plotly_chart(fig,use_container_width=True, height = 200)
        st.write(Rdf2)

    with cl2:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=Lmvalsal_bus,y=Lmvalsal_qty,name='LY Sales Values',marker_color='#3BB9FF',
            text=['₹{:,.0f}'.format(x) for x in Lmvalsal_qty],textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=mvalbud_bus,y=mvalbud_qty,name='Budget Values',marker_color='#EB5406',
            text=['₹{:,.0f}'.format(x) for x in mvalbud_qty],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=mvalsal_bus,y=mvalsal_qty,name='CY Sales Values',marker_color='#228B22',
            text=['₹{:,.0f}'.format(x) for x in mvalsal_qty],textposition='auto'
        ))
        fig.update_layout(
            title="Sales Value (₹, Lakhs) by Representative - LY vs Budget vs CY",xaxis_title='Marketing Representive Type',
            yaxis_title='Values in Lakhs',barmode='group'
        )

        st.plotly_chart(fig,use_container_width=True, height = 200)
        st.write(Rdf4)
    ch1, ch2 = st.columns((2))
    with ch1:
        st.subheader('Budget Volumes (MT) by Region')
        fig = px.pie(filtered_df, values = "Budget Vol(MT)", names = "Region", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Region"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(ReTdf2)
    with ch2:
        st.subheader('Sales Volumes (MT) by Region')
        fig = px.pie(filtered_df, values = "CY QTY (MT)", names = "Region", template = "gridon")
        fig.update_traces(text = filtered_df["Region"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(ReTdf4)

    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Budget Volumes (MT) by Product Type')
        fig = px.pie(filtered_df, values = "Budget Vol(MT)", names = "Type", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Type"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Pdf2)
    with chart2:
        st.subheader('Sales Volumes (MT) by Product Type')
        fig = px.pie(filtered_df, values = "CY QTY (MT)", names = "Type", template = "gridon")
        fig.update_traces(text = filtered_df["Type"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Pdf4)

    PackType_df = filtered_df.groupby(by = ["Pack Type"], as_index = False)["CY QTY (MT)"].sum()
    char1, char2 = st.columns((2))
    with char1:
        st.subheader('Budget Volumes (MT) by Pack Type')
        fig = px.pie(filtered_df, values = "Budget Vol(MT)", names = "Pack Type", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Pack Type"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Tdf2)
    with char2:
        st.subheader('Sales Volumes (MT) by Pack Type')
        fig = px.pie(filtered_df, values = "CY QTY (MT)", names = "Pack Type", template = "gridon")
        fig.update_traces(text = filtered_df["Pack Type"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Tdf4)

    cht1, cht2 = st.columns((2))
    with cht1:
        st.subheader('Budget Volumes (MT) by Pack Category')
        fig = px.pie(filtered_df, values = "Budget Vol(MT)", names = "Pack Cat", template = "plotly_dark")
        fig.update_traces(text = filtered_df["Pack Cat"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Cdf2)
    with cht2:
        st.subheader('Sales Volumes (MT) Pack category')
        fig = px.pie(filtered_df, values = "CY QTY (MT)", names = "Pack Cat", template = "gridon")
        fig.update_traces(text = filtered_df["Pack Cat"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)
        st.write(Cdf4)
    filtered_df['smonth']=pd.DatetimeIndex(filtered_df['Dispatch Date']).month
    filtered_df3=filtered_df.sort_values('smonth',ascending=1)
    Month_df=filtered_df3.groupby(by = ["Month"], as_index = False)[['LY QTY (MT)',"Budget Vol(MT)",'CY QTY (MT)']].sum()
    Month_df['ACH%']=Month_df['CY QTY (MT)']/Month_df['Budget Vol(MT)']*100
    Month_df['Vol Growth%']=((Month_df['CY QTY (MT)']/Month_df['LY QTY (MT)'])-1)*100
    Monthv_df=filtered_df.groupby(by = ["Month"], as_index = False)[['LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    Monthv_df['ACH%']=Monthv_df['CY Val(Lakhs)']/Monthv_df['Budget Val(Lakhs)']*100
    Monthv_df['Vol Growth%']=((Monthv_df['CY Val(Lakhs)']/Monthv_df['LY Val(Lakhs)'])-1)*100

    ##==================================================================================
    filtered_df['Month']=pd.DatetimeIndex(filtered_df['Dispatch Date']).month
    Data1=filtered_df[['Business','CY QTY (MT)','Country','Budget Vol(MT)','CY Val(Lakhs)','Budget Val(Lakhs)','LY QTY (MT)','LY Val(Lakhs)']]
    Data=Data1.groupby(['Country'])[['CY QTY (MT)','Budget Vol(MT)','CY Val(Lakhs)','Budget Val(Lakhs)','LY QTY (MT)','LY Val(Lakhs)']].sum()
    Data["Vol Difference"]=Data['Budget Vol(MT)']-Data['CY QTY (MT)']
    Data["Val Difference"]=Data['Budget Val(Lakhs)']-Data['CY Val(Lakhs)']
    Data["Vol Ach%"]=Data['CY QTY (MT)']/Data['Budget Vol(MT)']*100
    Data["Val Ach%"]=Data['CY Val(Lakhs)']/Data['Budget Val(Lakhs)']*100
    Data["Vol Growth%"]=Data['CY QTY (MT)']/Data['LY QTY (MT)']*100
    Data["Val Growth%"]=Data['CY Val(Lakhs)']/Data['LY Val(Lakhs)']*100
    DataL=Data[['LY QTY (MT)','CY QTY (MT)','Budget Vol(MT)','Vol Difference','Vol Ach%','Vol Growth%','LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)','Val Difference','Val Ach%','Val Growth%']]
    Data1=DataL.sort_values('CY QTY (MT)',ascending=0)

    st.subheader("Hierarchical view of Sales using TreeMap")
    fig3 = px.treemap(filtered_df, path = ["Region","Country","Customer name"], values = "CY QTY (MT)",hover_data = ["CY QTY (MT)"],
                    color = "Customer name")
    fig3.update_layout(width = 800, height = 650)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("TOP 15 Customers Analysis")
    Tcustome=filtered_df.groupby(by = ["Customer name"], as_index = False)[["LY QTY (MT)",'CY QTY (MT)','Budget Vol(MT)','LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    Tcustomer=Tcustome.sort_values('CY QTY (MT)',ascending=0).head(15)
    Cvol_cust=Tcustomer["Customer name"].values.tolist()
    CvolB_qty=Tcustomer['Budget Vol(MT)'].values.tolist()
    CvolC_qty=Tcustomer['CY QTY (MT)'].values.tolist()
    CvolA_qty=Tcustomer['LY QTY (MT)'].values.tolist()
    Tcustomer['Vol Growth%']=(Tcustomer['CY QTY (MT)']/Tcustomer['LY QTY (MT)']-1)*100
    Tcustomer['Vol Diff']=Tcustomer['CY QTY (MT)']-Tcustomer['LY QTY (MT)']
    Tcustomer['Val Growth%']=(Tcustomer['CY Val(Lakhs)']/Tcustomer['LY Val(Lakhs)']-1)*100
    Tcustomer['Val Diff']=Tcustomer['CY Val(Lakhs)']-Tcustomer['LY Val(Lakhs)']
    Tcustomer['LY Avg Price']=(Tcustomer['CY Val(Lakhs)']*100000)/(Tcustomer['LY QTY (MT)']*1000)
    Tcustomer['CY Avg Price']=(Tcustomer['LY Val(Lakhs)']*100000)/(Tcustomer['LY QTY (MT)']*1000)
    Tcustomer['Budget Avg Price']=(Tcustomer['Budget Val(Lakhs)']*100000)/(Tcustomer['Budget Vol(MT)']*1000)

    Tcustomer1=Tcustomer[["Customer name","LY QTY (MT)",'LY Val(Lakhs)','LY Avg Price','CY QTY (MT)','CY Val(Lakhs)','CY Avg Price','Budget Vol(MT)','Budget Val(Lakhs)','Budget Avg Price',"Vol Growth%","Val Growth%"]]

    fig8 = go.Figure()

    fig8.add_trace(go.Bar(
        x=Cvol_cust,y=CvolA_qty,name='LY QTY (MT)',marker_color='#3BB9FF',
        text=['{:,.0f}MT'.format(x) for x in CvolA_qty],textposition='auto'
    ))
    fig8.add_trace(go.Bar(
    x=Cvol_cust,y=CvolB_qty,name='Budget Vol(MT)',marker_color='#EB5406',
    text=['{:,.0f}MT'.format(x) for x in CvolB_qty],
        textposition='auto'
    ))
    fig8.add_trace(go.Bar(
        x=Cvol_cust,y=CvolC_qty,name='CY QTY (MT)',marker_color='#228B22',
        text=['{:,.0f}MT'.format(x) for x in CvolC_qty],textposition='auto'
    ))
    fig8.update_layout(
        title="TOP 15 Customers Analysis",xaxis_title='Customer Name',
        yaxis_title='Volumes (MT)',barmode='group'
    )

    st.plotly_chart(fig8,use_container_width=True, height = 200)
    with st.expander("TOP 15 Customers Data"):
        st.write(Tcustomer1.set_index("Customer name").sort_values("CY QTY (MT)",ascending=0).round(0))
    ##============================================================================================================
    st.subheader("TOP 15 Blends Analysis")
    BLTcustome=filtered_df.groupby(by = ["Uni - Blend"], as_index = False)[["LY QTY (MT)",'CY QTY (MT)','Budget Vol(MT)','LY Val(Lakhs)','CY Val(Lakhs)','Budget Val(Lakhs)']].sum()
    BLTcustomer=BLTcustome.sort_values('CY QTY (MT)',ascending=0).head(15)
    BLCvol_cust=BLTcustomer["Uni - Blend"].values.tolist()
    BLCvolB_qty=BLTcustomer['Budget Vol(MT)'].values.tolist()
    BLCvolC_qty=BLTcustomer['CY QTY (MT)'].values.tolist()
    BLCvolA_qty=BLTcustomer['LY QTY (MT)'].values.tolist()
    BLTcustomer['Vol Growth%']=(BLTcustomer['CY QTY (MT)']/BLTcustomer['LY QTY (MT)']-1)*100
    BLTcustomer['Vol Diff']=BLTcustomer['CY QTY (MT)']-BLTcustomer['LY QTY (MT)']
    BLTcustomer['Val Growth%']=(BLTcustomer['CY Val(Lakhs)']/BLTcustomer['LY Val(Lakhs)']-1)*100
    BLTcustomer['Val Diff']=BLTcustomer['CY Val(Lakhs)']-BLTcustomer['LY Val(Lakhs)']
    BLTcustomer['LY Avg Price']=(BLTcustomer['CY Val(Lakhs)']*100000)/(BLTcustomer['LY QTY (MT)']*1000)
    BLTcustomer['CY Avg Price']=(BLTcustomer['LY Val(Lakhs)']*100000)/(BLTcustomer['LY QTY (MT)']*1000)
    BLTcustomer['Budget Avg Price']=(BLTcustomer['Budget Val(Lakhs)']*100000)/(BLTcustomer['Budget Vol(MT)']*1000)

    BLTcustomer1=BLTcustomer[["Uni - Blend","LY QTY (MT)",'LY Val(Lakhs)','LY Avg Price','CY QTY (MT)','CY Val(Lakhs)','CY Avg Price','Budget Vol(MT)','Budget Val(Lakhs)','Budget Avg Price',"Vol Growth%","Val Growth%"]]

    fig8 = go.Figure()
    fig8.add_trace(go.Bar(
        x=BLCvol_cust,y=BLCvolA_qty,name='LY QTY (MT)',marker_color='#3BB9FF',
        text=['{:,.0f}MT'.format(x) for x in BLCvolA_qty],textposition='auto'
    ))
    fig8.add_trace(go.Bar(
    x=BLCvol_cust,y=BLCvolB_qty,name='Budget Vol(MT)',marker_color='#EB5406',
    text=['{:,.0f}MT'.format(x) for x in BLCvolB_qty],
        textposition='auto'
    ))
    fig8.add_trace(go.Bar(
        x=BLCvol_cust,y=BLCvolC_qty,name='CY QTY (MT)',marker_color='#228B22',
        text=['{:,.0f}MT'.format(x) for x in BLCvolC_qty],textposition='auto'
    ))
    fig8.update_layout(
        title="TOP 15 Blends Analysis",xaxis_title='Blend Names',
        yaxis_title='Volumes (MT)',barmode='group'
    )

    st.plotly_chart(fig8,use_container_width=True, height = 200)
    with st.expander("TOP 15 Blends Data"):
        st.write(BLTcustomer1.set_index("Uni - Blend").sort_values("CY QTY (MT)",ascending=0).round(0))
    ##=============================================================================================

    Dataline=filtered_df[['Dispatch Date','CY QTY (MT)']]
    Dataline1=Dataline.dropna()
    dateline = Dataline1.groupby(by=['Dispatch Date'],as_index=False)['CY QTY (MT)'].sum()
    st.markdown("Date wise line Trend")
    st.area_chart(dateline,x="Dispatch Date",y="CY QTY (MT)")


    #hist_data = [lyAvg, budAvg, cyAvg]

    #group_labels = ['LY Avg Price(₹)', 'Budget Avg Price(₹)', 'CY Avg Price(₹)']

    #st.subheader("Year wise Avg sales price analysis define customes consumed avg prices(₹)")
    #fig = ff.create_distplot(hist_data, group_labels, bin_size=[2,5,10])

    #st.plotly_chart(fig, use_container_width=True)

    ##============================================================================************
    filtered_df1=filtered_df[['Country','CY QTY (MT)']]
    filtered_df2=filtered_df1.groupby(['Country'])['CY QTY (MT)'].agg(['sum']).reset_index()
    filtered_df3=filtered_df2.round(2)
    st.title('World Map with Country-wise Sales')
    fig4 = px.choropleth(filtered_df3, 
                        locations='Country', locationmode='country names',
                        color='sum',color_continuous_scale='Viridis',
                        range_color=(0, filtered_df3['sum'].max()),
                        labels={'sum':'Sales Volumes in MT'},title='Country-wise Sales')
    fig4.update_layout(height=450, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig4)

    tb1,tb2=st.columns((2))
    with tb1:
        st.write(Month_df.set_index('Month').sort_values('CY QTY (MT)',ascending=0).round(0))
    with tb2:
        st.write(Monthv_df.set_index('Month').sort_values('CY Val(Lakhs)',ascending=0).round(0))
    with st.expander("Country wise Actual Vs Budget Volumes & Values Data"):
        st.write(Data1.round(2))


    csv = df.to_csv(index = False).encode('utf-8')
    st.download_button('Download Data', data = csv, file_name = "Sales.csv",mime = "text/csv")

    st.markdown('CCL Sales Budget Vs Softschedule')
    power_bi_url = "https://app.powerbi.com/reportEmbed?reportId=7c775c45-f871-4d83-a538-aedee7535bee&autoAuth=true&ctid=3edf27d4-21f4-4951-a8e5-81d719a69ec0"
    st.markdown(f'<iframe width="100%" height="600px" src="{power_bi_url}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)

    mtotal1,mtotal2,mtotal3,mtotal4,mtotal5 = st.columns(5,gap='large')
    with mtotal1:
        st.metric('Mr.Balaji',f"{lymt:,.0f} MT",f"Ach(%) : {BgrowthM:,.0f} %")
    with mtotal2:
        st.metric('Mr.Ravisai',f"{budgetmt:,.0f} MT",f"Ach(%) : {AAchM:,.0f} %")
    with mtotal3:
        st.metric('Mr.Yashwant',f"{cymt:,.0f} MT",f"Ach(%) : {CgrowthM:,.0f} %")
    with mtotal4:
        st.metric('Mr.Revanth',f"₹{budgetval:,.0f} L",f"Ach(%) : {CgrowthV:,.0f} %")
    with mtotal5:
        st.metric('Mr.Prabin',f"₹{cyval:,.0f} L",f"Ach(%) : {AAchV:,.0f} %")

    st.title('Competitor analysis')
    compet = pd.read_excel("C:\\Users\\Ramesh.M\\OneDrive - CCL Products (India) Ltd\\Desktop\\Sales File\\Reports\\Indian Exports\\Exports Data.xlsx")
    chart1, chart2 = st.columns((2))
    with chart1:
        st.subheader('Competitor wise Sales Volumes in KGS')
        fig = px.pie(compet, values = "Standard Qty", names = "Shipper Name", template = "plotly_dark")
        fig.update_traces(text = ["Shipper Name"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    with chart2:
        st.subheader('Competitor wise Sales Values in $')
        fig = px.pie(compet, values = "Estimated  F.O.B Value $", names = "Shipper Name", template = "plotly_dark")
        fig.update_traces(text = ["Shipper Name"], textposition = "inside")
        st.plotly_chart(fig,use_container_width=True)

    compet1=compet.groupby(by = ["Shipper Name"], as_index = False)[['Standard Qty','Estimated  F.O.B Value $']].sum().sort_values('Standard Qty',ascending=0)
    compet1['Estimated Unit Rate $']=compet1['Estimated  F.O.B Value $']/compet1['Standard Qty']
    bar1, bar2=st.columns((2))
    with bar1:
        st.subheader("Competitor wise Sales Volumes in Kg")
        fig = px.bar(compet1, x = "Shipper Name", y = "Standard Qty", text = ['{:,.0f}MT'.format(x) for x in compet1["Standard Qty"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)
    with bar2:
        st.subheader("Competitor wise Sales Values in $")
        fig = px.bar(compet1, x = "Shipper Name", y = "Estimated  F.O.B Value $", text = ['${:,.0f}'.format(x) for x in compet1["Estimated  F.O.B Value $"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 200)
    compet2=compet1.set_index('Shipper Name')
    st.write(compet2.round(2))

    TOP=pd.read_excel("C:\\Users\\Ramesh.M\\OneDrive - CCL Products (India) Ltd\\Desktop\\Streamlit\\Top customers.xlsx")
    TOP1 = TOP.groupby(by = ["Customer name","UNIT"], as_index = False)["QTY (MT)"].sum().sort_values('QTY (MT)',ascending=0)
    Options1 = TOP['UNIT'].unique()
    st.header("JUL Customer Contract Details Total")
    tr1, tr2 =st.columns((2))
    with tr1:
        selected_options1 = st.multiselect('Select the Unit:', options=Options1,default=Options1)
        TOP = TOP[TOP['UNIT'].isin(selected_options1)].copy()
        TOP2 = TOP.groupby(by = ["Customer name","UNIT"], as_index = False)["QTY (MT)"].sum().sort_values('QTY (MT)',ascending=0)
        st.write(TOP2.set_index('Customer name').round(0))
    with tr2:
        st.text("Customer wise contract Trend")
        fig = px.bar(TOP1, x = "Customer name", y = "QTY (MT)", text = ['{:,.2f}MT'.format(x) for x in TOP1["QTY (MT)"]],
                    template = "seaborn")
        st.plotly_chart(fig,use_container_width=True, height = 800)

    if st.sidebar.button("sign out"):
        st.session_state.logged_in=False
        st.experimental_rerun()

if "logged_in" not in st.session_state:
    st.session_state.logged_in=False
if st.session_state.logged_in:
    dashboard()
else:
    login()
