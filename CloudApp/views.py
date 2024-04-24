from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
import os
import pymysql
from django.core.files.storage import FileSystemStorage
import os
import time
import sys
import numpy
import matplotlib.pyplot as plt
from Crypto.Cipher import Blowfish, AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import IpLibrary.ip as chinnu
import requests



from struct import pack
import pyotp
import boto3

from django.views.decorators.cache import never_cache

global username, filename

def getCrowKey():
    key = "key must be 4 to 56 bytes".encode()
    #key = get_random_bytes(32)  # 256-bit key for AES
    return key

def getAESKey():
    key = get_random_bytes(32)  # 256-bit key for AES
    return key

def EncryptionResults(request):
    if request.method == 'GET':
        username = request.session.get('username')
        
        con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com', port=3306, user='admin', password='Nikhil123', database='multistagecloud', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT encryption_type, AVG(encryption_time) AS avg_encryption_time, AVG(compression_ratio) AS avg_compression_ratio FROM files WHERE username=%s GROUP BY encryption_type", (username,))
            rows = cur.fetchall()
            
            encryption_times = []
            compression_ratios = []
            for row in rows:
                encryption_type = row[0]
                avg_encryption_time = row[1]
                avg_compression_ratio = row[2]
                encryption_times.append(avg_encryption_time)
                compression_ratios.append(avg_compression_ratio)
            
            # Create plots
            plt.figure(figsize=(8, 4))
            plt.subplot(1, 2, 1)
            plt.bar(['Blowfish', 'AES'], encryption_times)
            plt.xlabel('Encryption Type')
            plt.ylabel('Average Encryption Time (s)')
            plt.title('Encryption Time Comparison')
            
            plt.subplot(1, 2, 2)
            plt.bar(['Blowfish', 'AES'], compression_ratios)
            plt.xlabel('Encryption Type')
            plt.ylabel('Average Compression Ratio')
            plt.title('Compression Ratio Comparison')
            
            plt.tight_layout()
            
            # Save the plot image
            plot_filename = 'encryption_results.png'
            plot_path = os.path.join(settings.MEDIA_ROOT, plot_filename)
            plt.savefig(plot_path)
            
            context = {
                'encryption_times': encryption_times,
                'compression_ratios': compression_ratios,
                'plot_filename': plot_filename
            }
            return render(request, "EncryptionResults.html", context)

def DownloadFile(request):
    if request.method == 'GET':
        username = request.session.get('username')
        font = '<font size="" color="white">'
        output = '<table border="1" align="center" width="100%"><tr><th>' + font + 'Username</th><td>' + font + 'Filename</th><td>' + font + 'Download File</th></tr>'
        con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com', port=3306, user='admin', password='Nikhil123', database='multistagecloud', charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM files WHERE username=%s", (username,))
            rows = cur.fetchall()
            for row in rows:
                output += "<tr><td>" + font + row[0] + "</td><td>" + font + row[1] + "</td>"
                output += '<td><a href=\'DownloadFileAction?fname=' + row[1] + '&encryption_type=' + row[3] + '\'><font size=3 color=white>Click Here</font></a></td></tr>'
        context = {'data': output}
        return render(request, "DownloadFile.html", context)
    
def DownloadFileAction(request):
    if request.method == 'GET':
        global username
        img = request.GET.get('fname', False)
        encryption_type = request.GET.get('encryption_type', False)
        
     
        # Download the encrypted file from S3
        s3 = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_obj = s3.get_object(Bucket=bucket_name, Key=img)
        encrypted_data = file_obj['Body'].read()
        
        decrypted_data = None  # Initialize decrypted_data variable

        if encryption_type == 'blowfish':
            # Decrypt the file using Blowfish
            cipher = Blowfish.new(getCrowKey(), mode=Blowfish.MODE_CBC, iv=encrypted_data[:8])
            decrypted_data = cipher.decrypt(encrypted_data[8:])
            decrypted_data = unpad(decrypted_data, Blowfish.block_size)
        elif encryption_type == 'aes':
            # Retrieve the AES key from the database
            con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com', port=3306, user='admin', password='Nikhil123', database='multistagecloud', charset='utf8')
            with con:
                cur = con.cursor()
                cur.execute("SELECT aes_key FROM files WHERE filename=%s", (img,))
                row = cur.fetchone()
                if row:
                    aes_key_hex = row[0]
                    aes_key = bytes.fromhex(aes_key_hex)  # Convert the hexadecimal string back to bytes

                    # Decrypt the file using AES with the retrieved key
                    cipher = AES.new(aes_key, AES.MODE_CBC, iv=encrypted_data[:16])
                    decrypted_data = cipher.decrypt(encrypted_data[16:])
                    decrypted_data = unpad(decrypted_data, AES.block_size)
        
        response = HttpResponse(decrypted_data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s' % img
        return response

@never_cache    
def UploadFileAction(request):
    if request.method == 'POST':
        username = request.session.get('username')  # Retrieve username from session
        filename = request.FILES['username'].name
        myfile = request.FILES['username'].read()
        encryption_type = request.POST.get('encryption_type', False)
        aes_key = None  # Initialize aes_key with a default value
        start_time = time.time()
        print ('Start time outside block ', start_time)
        if encryption_type == 'blowfish':
            start_time = time.time()  # Record the start time before encryption
            print ('Start time inside block Blow fish', start_time)
            # Encrypt the file using Blowfish
            bs = Blowfish.block_size
            cipher = Blowfish.new(getCrowKey(), mode=Blowfish.MODE_CBC)
            plen = bs - len(myfile) % bs
            padding = [plen] * plen
            padded_data = myfile + bytes(padding)
            encrypted_data = cipher.iv + cipher.encrypt(padded_data)
            
            print("start time ",  start_time)
            end_time = time.time()
            print ('End time inside block Blow fish', end_time)
        elif encryption_type == 'aes':
            start_time = time.time()  # Record the start time before encryption
            print ('Start time inside block AES', start_time)
            print (' AES', start_time)
            # Encrypt the file using AES
            key = getAESKey()
            cipher = AES.new(key, AES.MODE_CBC)
            padded_data = pad(myfile, AES.block_size)
            encrypted_data = cipher.iv + cipher.encrypt(padded_data)
            aes_key = key.hex()
            end_time = time.time()
        
            print ('End time inside block AES', end_time)
        
        end_time = time.time()
        print("End time outside block ",  end_time)
        
        encryption_time = end_time - start_time
        print("Encryption time ",  encryption_time)
        original_size = len(myfile)
        encrypted_size = len(encrypted_data)
        compression_ratio = encrypted_size / original_size
        

        # Upload the encrypted file to S3
        s3 = boto3.client('s3')
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3.put_object(Body=encrypted_data, Bucket=bucket_name, Key=filename)
        
        # Save the file details in the database
        db_connection = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com', port=3306, user='admin', password='Nikhil123', database='multistagecloud', charset='utf8')
        db_cursor = db_connection.cursor()
        
        student_sql_query = "INSERT INTO files(username, filename, filekeys, encryption_type, aes_key, encryption_time, compression_ratio) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        db_cursor.execute(student_sql_query, (username, filename, 'qwerty', encryption_type, aes_key, encryption_time, compression_ratio))

        db_connection.commit()
        
        context = {'data': 'Encrypted file uploaded to S3'}
        return render(request, "UploadFile.html", context)
    
def UserLogin(request):
    global username
    if request.method == 'POST':
        global username
        status = "none"
        users = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com',port = 3306,user = 'admin', password = 'Nikhil123', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username,password FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == users and row[1] == password:
                    request.session['username'] = users  # Store the username in the session
                    status = "success"
                    break
        if status == 'success':
            context= {'data':'Enter the TOTP code from your authenticator app'}
            return render(request, "LoginTOTP.html", context)
        else:
            context= {'data':'Invalid username'}
            return render(request, 'User.html', context)

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def UploadFile(request):
    if request.method == 'GET':
       return render(request, 'UploadFile.html', {})    

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def User(request):
    if request.method == 'GET':
        return render(request, 'User.html', {})

def LoginTOTPAction(request):
    if request.method == 'POST':
        username = request.session.get('username') 
        totp_code = request.POST.get('totp_code', False)
        
        con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com',port = 3306,user = 'admin', password = 'Nikhil123', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("SELECT totp_secret FROM register WHERE username=%s", (username,))
            row = cur.fetchone()
            if row:
                totp_secret = row[0]
                totp = pyotp.TOTP(totp_secret)
                if totp.verify(totp_code):
                    context = {'data':'Welcome '+username}
                    return render(request, "UserScreen.html", context)
        
        context = {'data':'Invalid TOTP code. Please try again.'}
        return render(request, 'LoginTOTP.html', context)
        
def get_client_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    ip = x_forwarded_for.split(',')[0]
  else:
    ip = request.META.get('REMOTE_ADDR')
  url = f'http://ip-api.com/json/{ip}'
  response = requests.get(url)
  data = response.json()

  # Handle potential absence of 'city' key
  city = data.get('city', 'Unknown')  # Use 'Unknown' if 'city' is missing
  location = f"{city}, {data.get('regionName', '')}, {data.get('country','Ireland')}"  # Use empty strings for missing keys
  return ip, location    

def Signup(request):
    if request.method == 'POST':
        global username
        username = request.POST.get('username', False)
        contact = request.POST.get('contact', False)
        email = request.POST.get('email', False)
        address = request.POST.get('address', False)
        password = request.POST.get('password', False)
        
        output = "none"
        con = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com',port = 3306,user = 'admin', password = 'Nikhil123', database = 'multistagecloud',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    output = username+" Username already exists"
                    break                
        if output == "none":
            totp_secret = pyotp.random_base32()
            db_connection = pymysql.connect(host='x22156411.chwlezgyi7rm.eu-west-1.rds.amazonaws.com',port = 3306,user = 'admin', password = 'Nikhil123', database = 'multistagecloud',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO register(username,password,contact,email,address,totp_secret) VALUES(%s,%s,%s,%s,%s,%s)"
            db_cursor.execute(student_sql_query, (username,password,contact,email,address,totp_secret))
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = "Signup process completed. Scan this QR code in your authenticator app: <br><img src='https://api.qrserver.com/v1/create-qr-code/?data=otpauth://totp/SecureCloud:"+username+"?secret="+totp_secret+"&size=200x200'/>"
        context= {'data':output}
        return render(request, 'Register.html', context)

