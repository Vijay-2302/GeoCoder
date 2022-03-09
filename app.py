from fileinput import filename
from flask import Flask, render_template,request,send_file
import pandas as pd
from geopy.geocoders import Nominatim


geolocator=Nominatim(user_agent="GeoCoder")

app= Flask(__name__)


@app.route("/")
def index():
   return render_template("index.html")

@app.route("/success",methods=['POST'])
def success():
    global file
    global filename
    if request.method == 'POST':
        file = request.files["file"]
        filename=file.filename
        lat=[]
        lon=[]
        try:
            datas=pd.read_csv(file)
            if 'address' in  datas.columns or 'Address' in  datas.columns:
                
                try:
                    for data in datas["Address"]:
                        location=geolocator.geocode(data)
                        lat.append(location.latitude)
                        lon.append(location.longitude)
                        
                except:
                    for data in datas["address"]:
                        location=geolocator.geocode(data)
                        lat.append(location.latitude)
                        lon.append(location.longitude)
                        
                datas["Latitude"]=lat
                datas["Longitude"]=lon
                db=pd.DataFrame(datas)
                db.to_csv(f"uploads/{filename}.csv",index=False)
                
                return render_template("index.html",content=f'<div style="text-align:center;">{datas.to_html()}</div>',btn="download.html")   
            else:
                return render_template("index.html",content="Please make sure you have an address column on your csv file")
        except:
            return render_template("index.html",content="Please select Only the csv file, Only the csv files are accepted")
    else:
        return render_template("index.html")
        
@app.route("/download")
def download():
    return send_file(f"uploads/{filename}.csv",attachment_filename="yourfile.csv",as_attachment=True)



if __name__ == "__main__":
    app.debug=True
    app.run()
