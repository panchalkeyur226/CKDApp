import streamlit as st
import re
import sqlite3 
import pickle
import pandas as pd
st.set_page_config(page_title="CKD Classification", page_icon="kidney.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

def set_bg_hack_url():
    '''
    A function to unpack an image from url and set as bg.
    Returns
    -------
    The background.
    '''
        
    st.markdown(
          f"""
          <style>
          .stApp {{
              background: url("https://allianceurology.com/wp-content/uploads/2021/09/image2.jpg");
              background-size: cover
          }}
          </style>
          """,
          unsafe_allow_html=True
      )
set_bg_hack_url()


conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()

st.subheader("Welcome To Chronic kidney disease (CKD) Prediction System")
menu = ["Home","SignUp","Login"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
    """
    <p align="justify">
    <b style="color:white">Chronic kidney disease (CKD) is a global health problem with high morbidity and mortality rate, and it induces other diseases. Since there are no obvious symptoms during the early stages of CKD, patients often fail to notice the disease. With early chronic kidney disease (CKD), people tend not to feel ill or notice any symptoms as kidney function deteriorates slowly over time. For this reason it has been referred to as the “silent killer.” Early detection of CKD enables patients to receive timely treatment to ameliorate the progression of this disease. In the deep learning model, classification is done on the basis of the attributes of CKD patients who is suffered from HIV. These classification models achieves reasonable accuracy in Chronic Kidney Disease prediction.
</b>
    </p>
    """
    ,unsafe_allow_html=True)

if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Password Does Not Match")
            
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    age=float(st.slider('age Value', 0, 90))
                    bp=float(st.slider('BP Value', 50, 110))
                    sg=float(st.slider('SG Value', 1.0, 1.5))
                    al=float(st.slider('al Value', 0.0, 4.0))
                    su=float(st.slider('su Value', 0.0, 5.0))
                    rbc1 = ["normal", "abnormal"]
                    rbc=st.selectbox("Select rbc",rbc1)
                    pc1 = ["normal", "abnormal"]
                    pc=st.selectbox("Select pc",pc1)
                    pcc1 = ["present", "notpresent"]
                    pcc=st.selectbox("Select pcc",pcc1)
                    ba1 = ["present", "notpresent"]
                    ba=st.selectbox("Select ba",ba1)
                    bgr=float(st.slider('bgr Value', 70.0, 490.0))
                    bu=float(st.slider('bu Value', 10.0, 309.0))
                    sc=float(st.slider('sc Value', 0.4, 15.2))
                    sod=float(st.slider('sod Value', 111.0, 115.0))
                    pot=float(st.slider('pot Value', 2.5, 47.0))
                    hemo=float(st.slider('hemo Value', 3.1, 17.8))
                    pcv=float(st.slider('pcv Value', 9.0, 54.0))
                    wc=float(st.slider('wc Value', 3800.0, 26400.0))
                    rc=float(st.slider('rc Value', 2.1, 8.0))
                    htn1 = ["yes", "no"]
                    htn=st.selectbox("Select htn",htn1)
                    dm1 = ["yes", "no"]
                    dm=st.selectbox("Select dm",dm1)
                    cad1 = ["yes", "no"]
                    cad=st.selectbox("Select cad",cad1)
                    appet1= ["poor", "good"]
                    appet=st.selectbox("Select appet",appet1)
                    pe1 = ["yes", "no"]
                    pe=st.selectbox("Select pe",pe1)
                    ane1 = ["yes", "no"]
                    ane=st.selectbox("Select ane",ane1)
                    sex1 = ["male", "female"]
                    sex=st.selectbox("Select rbc",sex1)
                    my_array=[age, bp, sg, al, su, rbc, pc, pcc, ba, bgr, bu,
                           sc, sod, pot, hemo, pcv, wc, rc, htn, dm, cad,
                           appet, pe, ane] 
                    
                    b2=st.button("Predict")
                    model=pickle.load(open("model.pkl",'rb'))
                                           
                    if b2:                        
                        df = pd.DataFrame([my_array], 
                                          columns=['age', 'bp', 'sg', 'al', 'su', 'rbc', 'pc', 'pcc', 'ba', 'bgr', 'bu',
                                                 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 'htn', 'dm', 'cad',
                                                 'appet', 'pe', 'ane'])
                        category_colums=['rbc','pc','pcc','ba','htn','dm','cad','appet','pe','ane']
                        encoder=pickle.load(open("encoder.pkl",'rb'))
                        df[category_colums] = df[category_colums].apply(encoder.fit_transform)
                        tdata=df.to_numpy()
                        #st.write(tdata)
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict(tdata)
                            query=test_prediction[0]
                       
                        if choice2=="SVM":
                            test_prediction = model[1].predict(tdata)
                            query=test_prediction[0]
                                     
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict(tdata)
                            query=test_prediction[0]
                        
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict(tdata)
                            query=test_prediction[0]
                         
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict(tdata)
                            query=test_prediction[0]
                        
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict(tdata)
                            query=test_prediction[0]
                    
                        if choice2=="VotingClassifier":
                            test_prediction = model[6].predict(tdata)
                            query=test_prediction[0]
                        if query=="ckd":
                            st.error("You have Chronic kidney disease (CKD)")
                            def calculate_egfr(scr, age, sex):
                                """
                                Calculate estimated Glomerular Filtration Rate (eGFR) using the CKD-EPI equation.
                                :param scr: Serum creatinine (mg/dL)
                                :param age: Age in years
                                :param sex: 'male' or 'female'
                                :return: eGFR value
                                """
                                if sex.lower() == 'male':
                                    kappa = 0.9
                                    alpha = -0.411
                                    sex_adjustment = 1.0
                                else:
                                    kappa = 0.7
                                    alpha = -0.329
                                    sex_adjustment = 1.018
                                
                                egfr = 141 * min(scr / kappa, 1) ** alpha * max(scr / kappa, 1) ** -1.209 * 0.993 ** age * sex_adjustment
                                return round(egfr, 2)
                            
                            
                            def determine_ckd_stage(egfr):
                                """
                                Determine CKD stage based on eGFR value.
                                :param egfr: Estimated glomerular filtration rate
                                :return: CKD stage as a string
                                """
                                if egfr >= 90:
                                    st.error("Stage 1: Normal function with some kidney damage")
                                elif 60 <= egfr < 90:
                                    st.error("Stage 2: Mild decrease in kidney function")
                                elif 45 <= egfr < 60:
                                    st.error("Stage 3a: Mild to moderate decrease")
                                elif 30 <= egfr < 45:
                                    st.error("Stage 3b: Moderate to severe decrease")
                                elif 15 <= egfr < 30:
                                    st.error("Stage 4: Severe decrease in kidney function")
                                else:
                                    st.error("Stage 5: Kidney failure (End-Stage Renal Disease)")
                            
                            
                            # Example Usage
                            scr = sc
                            age = age
                            
                            egfr = calculate_egfr(scr, age, sex)
                            determine_ckd_stage(egfr)

                            st.success("Please consent Doctor")
                        else:
                            st.success("You are in good health")
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           

        

    