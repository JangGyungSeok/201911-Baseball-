from flask import Flask, escape, request, render_template
from bs4 import BeautifulSoup
import requests
import time
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import urllib.request
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
import re
import asyncio
import pickle


# -------------------------장경석 , 김수연 작성 시작 -------------------------


# 필요없는 값을 필터링하기 위한 정규식 compile 객체들
comp=re.compile('grid_multi') 
comp2=re.compile('[(]')
comp3=re.compile('grid_postseason')
comp4=re.compile('rgRow ')
comp5=re.compile('rgAltRow ')
url1='https://www.fangraphs.com/'
app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World") # get 방식으로 name을 받아온다. default값은 World이다.
    return f'Hello, {escape(name)}!' # 스트링 형태의 html 코드를 전송해 그려준다.


@app.route('/player')
def player():
    return render_template('player.html') # player.html을 호출해 그려준다.


@app.route('/result',methods=['GET'])
def result():
    
    user_input=request.args.get('user_input') # get방식으로 result.html에서 user_input을 받아온다.
    driver1 = webdriver.Chrome('chromedriver.exe') # 크롤링을 위해 chromedriver를 킨다.
    driver1.get(url1) # fangraphs 사이트에 들어간다.
    time.sleep(2) # 틀어갈때까지 기다린다.
    driver1.find_element_by_class_name('search-query').send_keys(user_input) # 받아온 user_input을 키워드로 검색창에 입력한다.
    time.sleep(2)

    # 입력된 키워드로 검색을 누른다.
    driver1.find_element_by_css_selector('#rootSearch > div > div.search-results > ul.major > a:nth-child(1) > li > span.player-name').click()
    time.sleep(2)
    
    html=driver1.page_source # 선수 정보가 포함된 page source를 받아온다.
    #html=requests.get(driver.current_url,'utf-8').text
    soup = BeautifulSoup(html,'html.parser')
    contents=soup.find_all('div',{'style':'white-space:nowrap;'}) # 선수정보 테이블이 들어있는 div를 가져온다.

    data_list={
        'team':[],'year':[],'BABIP':[],'ERA':[],'WAR':[],'TBF':[],'H':[],'HR':[],'BB':[],'HBP':[],'SO':[],'WHIP':[],'FIP':[],
        'LD':[],'GB':[],'FB':[],'IFFB':[],'Swing':[],'SWStr':[]
            }


    # 필요한 데이터들만 모아서 data_list에 담는 과정

    bodys=contents[0].select('tbody')
    for body in bodys:
        trs=body.select('tr')
        for tr in trs[:-2]:
            tds=tr.select('td')
            season=tds[0].text
            team=tds[1].text
            
            year=tds[0].text
            BABIP=tds[11].text
            ERA=tds[15].text
            WAR=tds[18].text
            if comp.search(str(tr))==None and comp3.search(str(tr))==None and season!='2020' and season!='Total':
                if comp2.search(team)==None:
                    data_list['year'].append(year)
                    data_list['BABIP'].append(BABIP)
                    data_list['ERA'].append(ERA)
                    data_list['WAR'].append(WAR)
                    data_list['team'].append(team)



    # #==========================================================================================
    bodys=contents[1].select('tbody')
    for body in bodys:
        trs=body.select('tr')
        for tr in trs[:-1]:
            tds=tr.select('td')
            team=tds[1].text
            season=tds[0].text

            TBF=tds[13].text
            H=  tds[14].text
            HR= tds[17].text
            BB= tds[18].text
            HBP=tds[20].text
            SO= tds[23].text
            if comp.search(str(tr))==None and comp3.search(str(tr))==None and season!='2020' and season!='Total':
                if comp2.search(team)==None:
                    data_list['TBF'].append(TBF)
                    data_list['H'].append(H)
                    data_list['HR'].append(HR)
                    data_list['BB'].append(BB)
                    data_list['HBP'].append(HBP)
                    data_list['SO'].append(SO)
                    print(season)

                    print(team)
    # #==========================================================================================
    bodys=contents[2].select('tbody')
    for body in bodys:
        trs=body.select('tr')
        for tr in trs[:-1]:
            tds=tr.select('td')
            team=tds[1].text
            season=tds[0].text

            WHIP= tds[10].text
            FIP= tds[15].text
            if comp.search(str(tr))==None and comp4.search(str(tr))==None and comp5.search(str(tr))==None and season!='2020' and season!='Total':
                if comp2.search(team)==None:
                    data_list['WHIP'].append(WHIP)
                    data_list['FIP'].append(FIP)
    # #==========================================================================================
    bodys=contents[3].select('tbody')
    for body in bodys:
        trs=body.select('tr')
        for tr in trs[:-1]:
            tds=tr.select('td')
            season=tds[0].text
            team=tds[1].text
            
            LD=(tds[3].text.split('%')[0]).strip()
            GB=(tds[4].text.split('%')[0]).strip()
            FB=(tds[5].text.split('%')[0]).strip()
            IFFB=(tds[6].text.split('%')[0]).strip()
            if comp.search(str(tr))==None and comp4.search(str(tr))==None and comp5.search(str(tr))==None and season!='2020' and season!='Total':
                if comp2.search(team)==None:
                    data_list['LD'].append(LD)
                    data_list['GB'].append(GB)
                    data_list['FB'].append(FB)
                    data_list['IFFB'].append(IFFB)



    # #==========================================================================================
    bodys=contents[11].select('tbody')
    for body in bodys:
        trs=body.select('tr')
        for tr in trs[:-1]:
            tds=tr.select('td')
            season=tds[0].text
            team=tds[1].text

            Swing= tds[4].text
            if Swing=='\xa0':
                Swing=np.nan
            SWStr= tds[10].text
            if comp.search(str(tr))==None and season!='2020' and season!='Total':
                if comp2.search(team)==None:
                    data_list['Swing'].append(Swing)
                    data_list['SWStr'].append(SWStr)

    new_list=pd.DataFrame(data_list) # data_list를 데이터프레임으로 바꿔서 new_list에 넣는다.
    new_list=new_list.drop(columns='year')
    new_list=new_list.drop(columns='team')
    new_list=new_list.astype('float')
    new_list['pitcher_name']=user_input
    new_list = new_list.groupby(['pitcher_name'], as_index=False).mean()
    new_list[['GB','FB','IFFB']]=new_list[['GB','FB','IFFB']]/100
    new_list=new_list.drop(columns='pitcher_name')
    new_list.rename(columns={'ERA':"ERA_x",'TBF':'TBF_x','H':'H_x'}, inplace = True)
    
    new_list_arr = np.array(new_list) # 크롤링한 데이터를 트리에 넣기 위해 가공된 형태
    
    # url2='https://baseballsavant.mlb.com/statcast_search'
    # driver2 = webdriver.Chrome('chromedriver.exe')
    # driver2.get(url2)

    # user_input2=user_input.split(' ')[1]+', '+user_input.split(' ')[0]

    # search_bar=driver2.find_element_by_css_selector('#pitchers_lookup_chosen>ul>li>input')
    # search_bar.click()
    # search_bar.send_keys(user_input2)
    # time.sleep(1)
    # search_bar.send_keys(Keys.ENTER)
    # driver2.find_element_by_css_selector('#pfx_form > div.row.search-buttons > div > input.btn.btn-default.search-button').click()
    # driver2.find_element_by_css_selector('#csv_all_pid_ > img').click()
    # time.sleep(4)
    # practice=pd.read_csv('C:/Users/student/Downloads/savant_data.csv'.format(),encoding='utf-8')
    # os.remove('C:/Users/student/Downloads/savant_data.csv')


    with open('trees.p', 'rb') as file: # 크롤링한 데이터를 검사할 트리파일을 load한다.
        dt_clf11=pickle.load(file)
        dt_clf9=pickle.load(file)

    with open('test_tree2.p','rb') as file:
        dt_clf8=pickle.load(file)

    idxs=len(data_list['team'])

    avg_list=[]
    data_list['ERA']=list(map(float,data_list['ERA']))
    data_list['WAR']=list(map(float,data_list['WAR']))
    data_list['TBF']=list(map(float,data_list['TBF']))
    data_list['H']=list(map(float,data_list['H']))
    data_list['HR']=list(map(float,data_list['HR']))
    data_list['BB']=list(map(float,data_list['BB']))
    data_list['HBP']=list(map(float,data_list['HBP']))
    data_list['SO']=list(map(float,data_list['SO']))
    data_list['WHIP']=list(map(float,data_list['WHIP']))
    data_list['FIP']=list(map(float,data_list['FIP']))
    data_list['LD']=list(map(float,data_list['LD']))
    data_list['GB']=list(map(float,data_list['GB']))
    data_list['FB']=list(map(float,data_list['FB']))
    data_list['IFFB']=list(map(float,data_list['IFFB']))
    data_list['Swing']=list(map(float,data_list['Swing']))
    data_list['SWStr']=list(map(float,data_list['SWStr']))
    
    # 우리가 테스트할 데이터는 평균값이 입력으로 들어가기에 이를 계산해주는 과정
    avg_list.append(round(sum(data_list['ERA'],0.0)/len(data_list['ERA']),2))
    avg_list.append(round(sum(data_list['WAR'],0.0)/len(data_list['WAR']),2))
    avg_list.append(round(sum(data_list['TBF'],0.0)/len(data_list['TBF']),2))
    avg_list.append(round(sum(data_list['H'],0.0)/len(data_list['H']),2))
    avg_list.append(round(sum(data_list['HR'],0.0)/len(data_list['HR']),2))
    avg_list.append(round(sum(data_list['BB'],0.0)/len(data_list['BB']),2))
    avg_list.append(round(sum(data_list['HBP'],0.0)/len(data_list['HBP']),2))
    avg_list.append(round(sum(data_list['SO'],0.0)/len(data_list['SO']),2))
    avg_list.append(round(sum(data_list['WHIP'],0.0)/len(data_list['WHIP']),2))
    avg_list.append(round(sum(data_list['FIP'],0.0)/len(data_list['FIP']),2))
    avg_list.append(round(sum(data_list['LD'],0.0)/len(data_list['LD']),2))
    avg_list.append(round(sum(data_list['GB'],0.0)/len(data_list['GB']),2))
    avg_list.append(round(sum(data_list['FB'],0.0)/len(data_list['FB']),2))
    avg_list.append(round(sum(data_list['IFFB'],0.0)/len(data_list['IFFB']),2))
    avg_list.append(round(sum(data_list['Swing'],0.0)/len(data_list['Swing']),2))
    avg_list.append(round(sum(data_list['SWStr'],0.0)/len(data_list['SWStr']),2))
    
    if dt_clf8.predict(new_list_arr)==0:
        result_str='선수는 KBO에서 평균이상의 성적을 낼 것으로 예측됩니다.'
    else:
        result_str='선수는 KBO에서 평균 이하의 성적을 낼 것으로 예측됩니다.'
    # 도출한 결과를 result.html에 추가해 그려준다.
    return render_template('result.html',user_input=user_input,idxs=idxs,avg_list=avg_list,data_list=data_list,result=dt_clf8.predict(new_list_arr),result_str=result_str)#practice=practice,


# __name__ 이 __main__ 이면 debug를 하며 실행해라.
if __name__ == '__main__':
    app.run(debug=True)

# -------------------------장경석 , 김수연 작성 끝 -------------------------
