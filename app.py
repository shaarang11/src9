from flask import Flask, redirect,request, url_for,render_template
import datetime
import pickle
import pandas as pd
import re
import joblib

app = Flask(__name__)

@app.route('/submit/<name>')
def submit(name):
    return '%s' %  name

@app.route('/', methods = ['GET'])
def file2():
    print("GET")
    return render_template("File1.html")

@app.route('/', methods = ['POST'])
def file1():
    if request.method ==  'POST':
        print("POST")
        age =  request.form['AGE']
        age = int(age)
        sex = request.form['SEX']
        sex = str(sex)
        caste = request.form['Caste']
        caste = str(caste)

        surgery = request.form['SurgeryInput']
        surgery = str(surgery)
        surgery_ = surgery.split(",")
        surgery1 = surgery_[1]
        surgery2 = surgery_[3]

        village = request.form['VillageInput']
        village = str(village)
        village_ = village.split(",")
        village1 = village_[0]
        village2 = village_[1]
        village3 = village_[2]


        preauth = request.form['PREAUTH_AMOUNT']
        preauth = int(preauth)

        hospital =  request.form['HospitalInput']
        hospital = str(hospital)
        hospital_ = hospital.split(",")
        hospital1 = hospital_[0]
        hospital2 = hospital_[1]
        hospital3 = hospital_[2]

        SRC_REGISTRATION = request.form['SRC']
        SRC_REGISTRATION = str(SRC_REGISTRATION)

        preauth_date = request.form['PREAUTH_DATE']
        preauth_date = str(preauth_date)
        preauth_date = datetime.datetime.strptime(preauth_date, '%Y-%m-%d')

        surgery_date = request.form['SURGERY_DATE']
        surgery_date = str(surgery_date)
        surgery_date = datetime.datetime.strptime(surgery_date,'%Y-%m-%d')

        discharge_date = request.form['DISCHARGE_DATE']
        discharge_date = str(discharge_date)
        discharge_date = datetime.datetime.strptime(discharge_date, '%Y-%m-%d')

        Diff_SURGERY_PREAUTH = surgery_date - preauth_date
        Diff_Discharge_PREAUTH = discharge_date - preauth_date
        Diff_SURGERY_PREAUTH = Diff_SURGERY_PREAUTH.days
        Diff_Discharge_PREAUTH = Diff_Discharge_PREAUTH.days
        Diff_Discharge_PREAUTH = int(Diff_Discharge_PREAUTH)
        Diff_SURGERY_PREAUTH = int(Diff_SURGERY_PREAUTH)


#AGE,SEX,CASTE_NAME,CATEGORY_CODE,SURGERY_CODE,VILLAGE,MANDAL_NAME,DISTRICT_NAME,PREAUTH_AMT,HOSP_NAME,HOSP_TYPE,HOSP_DISTRICT,Mortality Y / N,SRC_REGISTRATION,Diff_SURGERY_PREAUTH,Diff_Discharge_PREAUTH
        df2 = pd.read_csv("file5.1.csv")
        print("df2 read complete")
        column = col = df2.columns

        """
        
        max_age = 96; min_age = 0;

        if age >= max_age:
            df2["AGE"] = [1]

        elif age < max_age:
            age = (age-min_age)/(max_age-min_age)
            df2["AGE"] = [age]

        min_preauth_amt = 500;
        max_preauth_amt = 52000;

        if preauth >= max_preauth_amt:
            df2["PREAUTH_AMT"] = [1]

        elif preauth < max_preauth_amt:
            preauth = (preauth - min_preauth_amt) / (max_preauth_amt - min_preauth_amt)
            df2["PREAUTH_AMT"] = [preauth]

        min_Diff_SURGERY_PREAUTH = -94;
        max_Diff_SURGERY_PREAUTH = 424;

        if Diff_SURGERY_PREAUTH >= max_Diff_SURGERY_PREAUTH:
            df2["Diff_SURGERY_PREAUTH"] = [1]

        elif min_Diff_SURGERY_PREAUTH < Diff_SURGERY_PREAUTH < max_Diff_SURGERY_PREAUTH :
            diff = (Diff_SURGERY_PREAUTH - min_Diff_SURGERY_PREAUTH) / (max_Diff_SURGERY_PREAUTH - min_Diff_SURGERY_PREAUTH)
            df2["Diff_SURGERY_PREAUTH"] = [diff]

        elif Diff_SURGERY_PREAUTH <= min_Diff_SURGERY_PREAUTH:
            df2["Diff_SURGERY_PREAUTH"] = [0]

        min_Diff_Discharge_PREAUTH = -49;
        max_Diff_Discharge_PREAUTH = 484;

        if Diff_Discharge_PREAUTH >= max_Diff_Discharge_PREAUTH:
            df2["Diff_Discharge_PREAUTH"] = [1]

        elif min_Diff_Discharge_PREAUTH < Diff_Discharge_PREAUTH < max_Diff_Discharge_PREAUTH:
            diff = (Diff_Discharge_PREAUTH - min_Diff_Discharge_PREAUTH) / (max_Diff_Discharge_PREAUTH - min_Diff_Discharge_PREAUTH)
            df2["Diff_Discharge_PREAUTH"] = [diff]

        elif Diff_Discharge_PREAUTH <= min_Diff_Discharge_PREAUTH:
            df2["Diff_Discharge_PREAUTH"] = [0]
        """


        if sex == "Male":
            df2["SEX_Male"] = [1]
        else:
            df2["SEX_Female"] = [1]

        cs = "CASTE_NAME_" + caste
        if cs in column:
            df2[cs] = [1]

        cs = "CATEGORY_CODE_" + surgery1
        if cs in column:
            df2[cs] = [1]

        cs = "SURGERY_CODE_" + surgery2
        if cs in column:
            df2[cs] = [1]

        cs = "VILLAGE_" + village1
        if cs in column:
            df2[cs] = [1]

        cs = "MANDAL_NAME_" + village2
        if cs in column:
            df2[cs] = [1]

        cs = "DISTRICT_NAME_" + village3
        if cs in column:
            df2[cs] = [1]


        for i in col:
            string1 = str(df2[i].name)
            if "PREAUTH_AMT" in string1:
                s = re.findall(r"[-+]?\d*\.\d+|\d+", string1)
                #print(string1,s)
                if preauth in range(int(float(s[0])), int(float(s[1]))):
                    #print("string1:", preauth)
                    df2[i] = [1]
           

        cs = "HOSP_NAME_" + hospital1
        if cs in column:
            df2[cs] = [1]

        cs = "HOSP_TYPE_" + hospital2
        if cs in column:
            df2[cs] = [1]

        cs = "HOSP_DISTRICT_" + hospital3
        if cs in column:
            df2[cs] = [1]

        cs = "SRC_REGISTRATION_" + SRC_REGISTRATION
        if cs in column:
            df2[cs] = [1]

        for i in col:
            string1 = str(df2[i].name)
            if "Diff_SURGERY_PREAUTH" in string1:
                s = re.findall(r"[-+]?\d*\.\d+|\d+", string1)
                # print(string1,s)
                if preauth in range(int(float(s[0])), int(float(s[1]))):
                    #print("string1:", preauth)
                    df2[i] = [1]

        for i in col:
            string1 = str(df2[i].name)
            if "Diff_Discharge_PREAUTH" in string1:
                s = re.findall(r"[-+]?\d*\.\d+|\d+", string1)
                # print(string1,s)
                if Diff_Discharge_PREAUTH in range(int(float(s[0])), int(float(s[1]))):
                    #print("string1:", preauth)
                    df2[i] = [1]

        print("Update Complete")
        filename1 = 'DecisionTree.sav'
        loaded_model = joblib.load(open(filename1, 'rb'))
        print("Prediction Begin")

        """
        s1 = 0
        s2 = 0
        for x in col:
            if (df2[x] == 0) :
                s1+=1
            elif (df2[x] == 1):
                s2+=1
            else:
                print(x,df2[x])
        """

        y_pred = loaded_model.predict(df2)

        if y_pred[0] ==  0:
            string2 = "Low Risk"
        if y_pred[0] ==  1:
            string2 = "High Risk- Please cotact your doctor immediately"
        return redirect(url_for('submit', name=string2))


    else:
        print("GET")
        string2 = "GET"
        return redirect(url_for('submit', name=string2))



if __name__  == '__main__':
    app.run()

#<input placeholder = "Search Surgery" list = "surgery">
#<input list = "surgery" type = "text" id = "SurgeryInput"
#<input id = "s1" placeholder = "Search Surgery" list = "surgery">