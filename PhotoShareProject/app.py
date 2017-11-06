from flask import Flask, Response, request, render_template, redirect, url_for, session
from flaskext.mysql import MySQL
import datetime, os, shutil

app = Flask(__name__, static_folder="static")
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'I(E(ream7861'
app.config['MYSQL_DATABASE_DB'] = 'PhotoShare'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
now = datetime.datetime.now()

UPLOAD_FOLDER = "static/uploads/"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# This function collects Photos Comments and likes of all users to display on index as well as the home page
def Photo_Comment_like():


    top_tags=[]
    Photo_array = []
    pid_count = []
    likes_photo = []
    p1=[]
    q = ("SELECT * from photos")
    cursor.execute(q)
    if cursor.rowcount>0:
        d1 = cursor.fetchall()
        size_entries = len(d1)
        if size_entries > 0:

            print("number of photos",len(d1))
            for i in range(len(d1)):
                if (size_entries - i) >= 0:
                    Photo_array.append(d1[size_entries - 1 - i])
                    pid_count.append(size_entries - 1 - i)
                else:
                    break
            Photo_array.pop(0)
            print("THIS IS P ARRAY",Photo_array)
            pid_count.pop(-1)
            print(pid_count)
            cid_uid = ()
            q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
            cursor.execute(q1)
            p1 = cursor.fetchall()
            len_p1 = len(p1)
            # if len_p1 > 10:
            #     new_p1 = []
            #     for i in range(10):
            #         new_p1.append(p1[len_p1 - 1 - i])
            #     print(new_p1)
            #     p1 = new_p1
            print(p1)
            query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")

            print(likes_photo)
            for i in range(len(Photo_array)):
                cursor.execute(query_likes, Photo_array[i][0])
                likes_photo.append(extractData(cursor))
            print(likes_photo)
            cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")

            top_tags=extractData(cursor)

        return Photo_array,likes_photo,p1,top_tags

# This function redirects the user to the index page after logging off
def logoff_page(s):
    Photo_array, likes_photo, p1,top_tags = Photo_Comment_like()
    return render_template('index.html', data=s, Photo_array=Photo_array, c_uid=p1, likes=likes_photo,tags=top_tags)


# This function collects all the user data who are friends of friends to the user logged in and redirects to recos page.
@app.route('/recommend_friend/', methods=['GET' , 'POST'])
def recommend_friend():
    #This query finds out the uid of user from the session variable which has the email id of the user.
    # This query is used several times for the same reason as the uid is a foreign key in other tables.
    cursor.execute("Select uid from User where email=%s",(session['username']))
    uid_user=extractData(cursor)
    friend=("Select f.uid2 from friends_with f where f.uid1=%s")
    cursor.execute(friend,uid_user[0][0])
    friend_uid=extractData(cursor)
    friend_of_friend = ("Select uid2, count(*) from friends_with where uid1=%s and uid2<>%s group by uid2 having count(*)>0")
    friend_of_friend_uid=[]
    for i in friend_uid:
        cursor.execute(friend_of_friend,(i[0],uid_user[0][0]))
        friend_of_friend_uid.append(extractData(cursor))
    print(friend_of_friend_uid)
    recos=[]
    # this query finds the uid of Users who are friends of friends to the user who is logged in.
    recommendations=("Select uid from User where uid=%s and uid not in (Select uid2 from friends_with where uid1=%s )")
    for i in friend_of_friend_uid:
        for j in i:
            print(j[0])
            cursor.execute(recommendations,(j[0],uid_user[0][0]))
            recos.append(extractData(cursor))
    final_recos=[]
    print(recos)
    # This query does the extraction of uid fname and name for evrey uid found previously
    for i in recos:
        for j in i:
            cursor.execute("Select uid,fname,name from User where uid=%s",j[0])
            final_recos.append(extractData(cursor))

    print(final_recos)
    # this query is used several time maybe in all functions to calculate the mostl popular tags to be displayed in the list on the page
    # as we have not used frames we have included the top tags feature in every html page
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)

    return render_template( 'recos.html',data=final_recos, tags=top_tags)
#This function finds the Top 10 users which is accessible to registered users and they increases the sense of competition
@app.route('/top10/', methods = ['GET','POST'])
def top10():

    c_pid= ("select count(*),u.uid from user u, photos p, album a where a.uid = u.uid and p.aid = a.aid group by u.uid")
    cursor.execute(c_pid)
    count_pid = extractData(cursor)
    print(count_pid)
    c_cid= ("select count(*), u.uid from user u, comments c where c.uid=u.uid group by u.uid")
    cursor.execute(c_cid)
    count_cid= extractData(cursor)
    print(count_cid)
    cursor.execute(("SELECT uid from user"))
    uid_count = extractData(cursor)
    uid_count_list= []
    count_cid.sort()
    count_pid.sort()
    final_count= [count_pid,count_cid]
    for i in range(len(final_count[0])):
        count = 0
        for j in range(len(final_count[1])):
            if final_count[0][i][1] == final_count[1][j][1]:
                count = count + 1
                temp_pid= final_count[0][i][0]
                temp_cid= final_count[1][j][0]
                uid_count_list.append((temp_cid+temp_pid,(final_count[0][i][1])))
        if(count==0):
            uid_count_list.append((final_count[0][i][0],final_count[0][i][1]))

    for i in count_cid:
        count =0
        for j in (uid_count_list):
            if i[1] == j[1]:
                count= count + 1
        if count == 0:
            uid_count_list.append(i)

    uid_count_list.sort()
    uname_list= []
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    if len(uid_count_list)<10:
        serial = 0
        for i in uid_count_list:
            cursor.execute(("SELECT fname,uid from user where uid=%s"),i[1])
            temp= extractData(cursor)
            print("this is temp",temp)
            serial = serial + 1
            uname_list.append((serial,temp))
            uid_count_list.reverse()
        print("list = ", uid_count_list)
        print("unamelist = ", uname_list)

        return render_template('top10.html', list= uid_count_list, uname= uname_list, count_cid= count_cid, count_pid= count_pid, count= 0,tags=top_tags)
    else:
        temp_uid_count_list= uid_count_list[-9:]
        serial= 0
        print(temp_uid_count_list,"TEMP")
        for i in temp_uid_count_list:
            cursor.execute(("SELECT fname from user where uid=%s"), i[1])
            temp = extractData(cursor)
            serial= serial + 1
            uname_list.append((serial,temp))
        print("list = ", uid_count_list)
        print("unamelist = ", uname_list)
        return render_template('top10.html', list= uid_count_list, uname= uname_list, count_cid= count_cid, count_pid= count_pid, count=0,tags=top_tags)


# This function returns all the photos in the particular album selected by the user
@app.route('/album/<data>', methods=['POST', 'GET'])
def album_display(data):
    assert data == request.view_args['data']
    print(data[0])
    albumid= data
    find_photos = ("SELECT p.data,p.pid from photos p WHERE p.aid =%s")
    cursor.execute(find_photos,albumid)
    picture_info = cursor.fetchall()
    print(picture_info)
    return render_template('displayalbum.html', pic = picture_info, data = data)
#This function deletes a particular picture from the album as well as the uploads folder.
@app.route('/deletepic/<data>', methods = ['GET', 'POST'])
def pic_delete(data):
    assert data == request.view_args['data']
    pic_id = data
    cursor.execute("Select data from Photos where pid=%s", pic_id)
    filepath = extractData(cursor)
    print(filepath[0][0])
    delete_pic = ("delete from photos where pid=%s")
    cursor.execute(delete_pic,pic_id)
    os.remove(os.path.join(app.static_folder,filepath[0][0]))
    print(pic_id,"has been deleted")
    return render_template('edit_album.html')
# this funtion deletes the particular album from the databse as well as the uploads folder.
@app.route('/deletealbum/<data>', methods =['GET', 'POST'])
def deletealbum(data):
    assert data == request.view_args['data']
    album_id= data
    delete_album=("delete from album where aid=%s")
    cursor.execute(delete_album,(album_id))
    conn.commit()
    shutil.rmtree(os.path.join(app.static_folder,"uploads/"+album_id))
    print(album_id, "has been deleted")
    return home()

# this function adds a photo to the album and also adds its caption and tags to the database
@app.route('/addphoto/',methods=['GET','POST'])
def addphoto():
    if request.method == 'POST':
        name = request.form['aname']
        find_aname=("select a.name,u.uid from album a,user u where a.uid=u.uid and u.email=%s and a.aid=%s")
        cursor.execute(find_aname,(session['username'],name))
        aname_found = extractData(cursor)
        print(aname_found,"is the aid for this album")
        print("name is:",name)
        name = aname_found[0][0]
        print(name)
        caption = request.form['caption']
        tags = request.form['tags']
       # DocCreation is necessary as we dont know what is the convention of date used by the computer and that used by mysql,
        #  so just to be sure
        year = str(now.year)
        month = str(now.month)
        day = str(now.day)
        DOCreation = year + "-" + month + "-" + day
        queryUID = ("SELECT uid FROM user WHERE email = %s")
        cursor.execute(queryUID, (session["username"]))
        data = cursor.fetchone()
        pid = ("SELECT MAX(pid) from Photos")
        cursor.execute(pid)
        count = cursor.fetchone()
        if count[0] is None:
            count_new = 1
        else:
            count_new = int(count[0]) + 1
        album_exists = ("Select * from Album where uid=%s and name=%s")
        cursor.execute(album_exists, (data[0], name))

        file = request.files['file']

        if cursor.rowcount == 1:
            ## This was used in the previous version of the PhotoShare project where if the album name entered by the user
            #  already exists the photo will be added to that album.
            data_album = cursor.fetchone()
            directory = str(data_album[0])
            folder = UPLOAD_FOLDER + directory
            file_name = str(count_new) + "." + file.filename.rsplit('.', 1)[1]
            path1 = "uploads/" + directory + "/" + file_name
            if file and allowed_file(file.filename):
                file.save(os.path.join(folder, file_name))

        else:
            # if the albumname does not exists it creates a new album and adds the photo to it.
            query_insert_album = ("Insert into Album (uid,name, DOCreation) Values (%s,%s,%s)")
            cursor.execute(query_insert_album, (data[0], name, DOCreation))
            conn.commit()

            cursor.execute(album_exists, (data[0], name))
            data_album = cursor.fetchone()
            directory = str(data_album[0])
            # variable "folder" is the folder where the file/photo is saved
            folder = UPLOAD_FOLDER + directory
            file_name = str(count_new) + "." + file.filename.rsplit('.', 1)[1]
            # path1 is the data to be stored in the database as the static folder is already considered as root
            # while displaying the photo
            path1 = "uploads/" + directory + "/" + file_name
            if not os.path.exists(folder):
                os.makedirs(folder)
            if file and allowed_file(file.filename):
                file.save(os.path.join(folder, file_name))
        query_picture_insert = ("INSERT INTO Photos (aid,caption,data) VALUES (%s,%s,%s)")
        cursor.execute(query_picture_insert, (directory, caption, path1))
        conn.commit()


        query_pid = ("SELECT pid from Photos WHERE data=%s")
        cursor.execute(query_pid, (path1))
        pid = cursor.fetchone()
        ## Here we seperate the tags entered by the user by spaces and store them individually
        query_tag = ("SELECT tid from Tags where tag_name=%s")
        insert_tid_pid = ("Insert Into consists_of (tid,pid) Values (%s,%s)")
        tag = [x.strip(' ') for x in tags.split(' ')]
        for i in tag:
            cursor.execute(query_tag, (i))

            if cursor.rowcount == 1:
                tid = cursor.fetchone()
                cursor.execute("Select * from consists_of where tid=%s and pid=%s", (tid[0], pid[0]))
                if cursor.rowcount == 0:
                    cursor.execute(insert_tid_pid, (tid[0], pid[0]))
                    conn.commit()
            else:
                insert_tag = ("Insert into Tags (tag_name) Values (%s)")
                cursor.execute(insert_tag, (i))
                conn.commit()
                cursor.execute(query_tag, (i))
                tid_1 = cursor.fetchone()
                cursor.execute(insert_tid_pid, (tid_1[0], pid[0]))
                conn.commit()

        return home()



# This function extracts data from the cursor
def extractData(cursor):
    data = []
    for item in cursor:
        data.append(item)
    return data

# this function collects data of photos and returns to the index page for display
@app.route('/')
def index():
    Photo_array, likes_photo, p1,top_tags = Photo_Comment_like()

    return render_template('index.html', data="Click 'Signup', if you are a new user",  Photo_array=Photo_array, c_uid = p1,
                           likes=likes_photo,tags=top_tags)

# This is where the user data is store in the database using the sign up page
@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        email = request.form['username']
        fname = request.form['fname']
        lname = request.form['lname']
        pass1 = request.form['pass']
        pass2 = request.form['pass2']

        bday_year = request.form['bday_year']
        bday_month = request.form['bday_month']
        bday_day = request.form['bday_day']
        bday = bday_year + "-" + bday_month + "-" + bday_day
        gender = request.form['gender']
        htown = request.form['htown']
        email_check_query = ("Select * from User where email=%s")
        cursor.execute(email_check_query, (email))
        if cursor.rowcount == 1:
            return render_template('signup.html', data="User already exists.")
        elif pass1 != pass2:
            return render_template('signup.html', data="Passwords do not match.")
        elif bday_year is None or bday_month is None or bday_day is None:
            return render_template('signup.html', data="Enter Birthdate.")
        else:
            query = ("INSERT INTO user( fname,name,DOB,gender,email,hometown,password) VALUES (%s,%s,%s,%s,%s,%s,%s)")
            cursor.execute(query, (fname, lname, bday, gender, email, htown, pass1))
            conn.commit()
            return index()

# Login of user is not done using flask libraries instaed we have made sessions popped session variables when not logged in.
@app.route('/login/', methods=['POST', 'GET'])
def login():
    username = request.form['username']
    password = request.form['pass']
    query = ("Select * from User where email= %s AND password= %s")
    cursor.execute(query, (username, password))
    if not cursor.rowcount:
        Photo_array, likes_photo, p1, top_tags = Photo_Comment_like()

        return render_template('index.html', data="Invalid Credentials", Photo_array=Photo_array,
                               c_uid=p1, likes=likes_photo,tags=top_tags)
    else:
        session['username'] = username
        return home()

# This function redirects user to edit_album page with appropriate data
@app.route('/edit/', methods=['POST', 'GET'])
def edit():
    if check_user() == False:
        return render_template('index.html', data='Sign In To Get Started')
    else:
        find_album = ("SELECT a.name,a.aid,count(p.pid) from album a, user u,photos p where a.uid=u.uid and u.email=%s and p.aid=a.aid GROUP by a.aid")
        cursor.execute(find_album,(session['username']))
        album_info = cursor.fetchall()
        print(album_info)
        cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
        top_tags = extractData(cursor)
        return render_template('edit_album.html', album_info=album_info, tags=top_tags)

# Redirects user to upload.html page
@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    if check_user() == False:
        return logoff_page('Sign in to get started')
    else:
        cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
        top_tags = extractData(cursor)
        return render_template('upload.html',tags=top_tags)

#This function logs out the user by overwritting users session variable
@app.route('/logout/', methods=['POST', 'GET'])
def logout():
    session['username'] = "loggedout"
    return logoff_page('You have successfully Logged off')

# this function returns user to home page
@app.route('/home/', methods=['POST', 'GET'])
def home():
    if check_user() == False:
        return logoff_page('Sign in to get started.')
    else:
        query_userdata = ("Select * from USER where email=%s")
        cursor.execute(query_userdata, (session['username']))
        user_name = cursor.fetchall()
        print(user_name)
        Photo_array, likes_photo, p1, top_tags = Photo_Comment_like()
        cursor.execute("Select * from  consists_of")
        photo_tags=extractData(cursor)

        if len(Photo_array)>0:
            return render_template('home.html', data=user_name[0][1], Photo_array=Photo_array, c_uid = p1, likes=likes_photo,tags=top_tags, all_tags=photo_tags)
        else:
            return render_template('home.html', data=user_name[0][1])


# this function is used to check if user is logged in or not if not it returns false and user is redirected to the index page
def check_user():
    if session['username'] == "loggedout":
        return False
    else:
        return True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/newalbum/', methods=['POST', 'GET'])
def createNewAlbum():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    else:
        if request.method == 'POST':
            name = request.form['aname']
            caption = request.form['caption']
            tags = request.form['tags']
            year = str(now.year)
            month = str(now.month)
            day = str(now.day)
            DOCreation = year + "-" + month + "-" + day
            queryUID = ("SELECT uid FROM user WHERE email = %s")
            cursor.execute(queryUID, (session["username"]))
            data = cursor.fetchone()
            pid = ("SELECT MAX(pid) from Photos")
            cursor.execute(pid)
            count = cursor.fetchone()
            if count[0] is None:
                count_new = 1
            else:
                count_new = int(count[0]) + 1
            album_exists = ("Select * from Album where uid=%s and name=%s")
            cursor.execute(album_exists, (data[0], name))

            file = request.files['file']

            if cursor.rowcount == 1:
                data_album = cursor.fetchone()
                directory = str(data_album[0])
                folder = UPLOAD_FOLDER + directory
                file_name = str(count_new) + "." + file.filename.rsplit('.', 1)[1]
                path1 = "uploads/" + directory + "/" + file_name
                if file and allowed_file(file.filename):
                    file.save(os.path.join(folder, file_name))

            else:
                query_insert_album = ("Insert into Album (uid,name, DOCreation) Values (%s,%s,%s)")
                cursor.execute(query_insert_album, (data[0], name, DOCreation))
                conn.commit()
                cursor.execute(album_exists, (data[0], name))
                data_album = cursor.fetchone()
                directory = str(data_album[0])
                folder = UPLOAD_FOLDER + directory
                file_name = str(count_new) + "." + file.filename.rsplit('.', 1)[1]
                path1 = "uploads/" + directory + "/" + file_name
                if not os.path.exists(folder):
                    os.makedirs(folder)
                if file and allowed_file(file.filename):
                    file.save(os.path.join(folder, file_name))
            query_picture_insert = ("INSERT INTO Photos (aid,caption,data) VALUES (%s,%s,%s)")
            cursor.execute(query_picture_insert, (directory, caption, path1))
            conn.commit()
            query_pid = ("SELECT pid from Photos WHERE data=%s")
            cursor.execute(query_pid, (path1))
            pid = cursor.fetchone()
            query_tag = ("SELECT tid from Tags where tag_name=%s")
            insert_tid_pid = ("Insert Into consists_of (tid,pid) Values (%s,%s)")
            tag = [x.strip(' ') for x in tags.split(' ')]
            for i in tag:
                cursor.execute(query_tag, (i))

                if cursor.rowcount == 1:
                    tid = cursor.fetchone()
                    cursor.execute("Select * from consists_of where tid=%s and pid=%s",(tid[0], pid[0]))
                    if cursor.rowcount == 0:
                        cursor.execute(insert_tid_pid, (tid[0], pid[0]))
                        conn.commit()
                else:
                    insert_tag = ("Insert into Tags (tag_name) Values (%s)")
                    cursor.execute(insert_tag, (i))
                    conn.commit()
                    cursor.execute(query_tag, (i))
                    tid_1 = cursor.fetchone()
                    cursor.execute(insert_tid_pid, (tid_1[0], pid[0]))
                    conn.commit()



            return home()

# This function searches the first and last name of users which match with the entered first and last name by the user who is logged in.
@app.route('/search_friends/', methods=['POST', 'GET'])
def search_friends():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    if request.method == 'POST':
        data = []
        friend_name = request.form['search_friends']
        if friend_name is None:
            return render_template('search_friend.html', data="Please type the first and/or last name of your friend!")
        name = [x.strip(' ') for x in friend_name.split(' ')]
        for i in name:
            query_find_friends = ("Select * from User where (fname=%s or name=%s) and email<>%s")
            cursor.execute(query_find_friends, (i, i, session['username']))
            data.append(extractData(cursor))
        no_duplicates = []
        cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
        top_tags = extractData(cursor)
        for i in data:
            if i not in no_duplicates:
                no_duplicates.append(i)
        print("This is no duplicates",no_duplicates)
        return render_template('search_friend.html', name=friend_name, results=no_duplicates,tags=top_tags)
    else:
        return home()


# this returns all the users of the website except the users who are already friends with the user
@app.route('/users/', methods=['POST', 'GET'])
def users():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    get_users=("SELECT * FROM user where email<>%s and uid <>'5' and  uid not in (Select uid2 from friends_with where uid1=%s) ")
    cursor.execute("Select uid from User where email=%s", (session['username']))
    uid_user = extractData(cursor)
    cursor.execute(get_users,(session['username'],uid_user[0][0]))
    user_data= extractData(cursor)
    print(user_data)
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    return render_template('users.html', name="All Users", results=user_data, tags=top_tags)

# This function is used to search tags. Here the user can even search multiple tags by seperating each tag by a space.
@app.route('/search_tags/', methods=['POST', 'GET'])
def search_tags():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    if request.method == 'POST':
        button_you=request.form['Submit']
        print(button_you)
        data_tags = []
        no_duplicates = []
        cursor.execute("Select uid from User where email=%s", (session['username']))
        uid_user = extractData(cursor)
        tags = request.form['search_tags']
        tag_name = [x.strip(' ') for x in tags.split(' ')]
        print(tag_name)
        if button_you=="Tags by all!" or button_you=="Display Tag":
            query_find_tags = ("Select * from Photos As p INNER JOIN Consists_of As c ON p.pid=c.pid where c.tid=(Select t.tid from Tags As t where t.tag_name=%s)")
        elif button_you=="Tags by You!":
            query_find_tags = ("Select * from Photos As p INNER JOIN Consists_of As c ON p.pid=c.pid  where c.tid=(Select t.tid from Tags As t where t.tag_name=%s) and p.aid in (Select aid from Album where uid=%s)")
        elif button_you=="Conjunctive Tags!":
            query_find_tags = ("Select * from Photos As p INNER JOIN Consists_of As c ON p.pid=c.pid where c.tid=(Select t.tid from Tags As t where t.tag_name=%s)")
            query_find_tags2 = ("Select * from Photos As p INNER JOIN Consists_of As c ON p.pid=c.pid where c.tid=(Select t.tid from Tags As t where t.tag_name=%s)")
        if button_you=="Conjunctive Tags!":
            cursor.execute(query_find_tags,tag_name[0])
            tag2=extractData(cursor)
            cursor.execute(query_find_tags2,tag_name[1])
            tag1=extractData(cursor)
            for i in tag2:
                for j in tag1:
                    if i[0]==j[0]:
                        data_tags.append(i)
        else:
            for t in tag_name:
                if button_you=="Tags by You!":
                    cursor.execute(query_find_tags, (t,uid_user[0][0]))
                elif button_you=="Tags by all!" or button_you=="Display Tag":
                    cursor.execute(query_find_tags, (t))

            data_tags.append(extractData(cursor))
        for i in data_tags:
            if i not in no_duplicates:
                no_duplicates.append(i)
        if button_you == "Conjunctive Tags!":
            q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
            print(data_tags)
            cursor.execute(q1)
            p1 = cursor.fetchall()
            len_p1 = len(p1)
            if len_p1 > 10:
                new_p1 = []
                for i in range(10):
                    new_p1.append(p1[len_p1 - 1 - i])
                print(new_p1)
                p1 = new_p1
            print(p1)
            print(data_tags)
            query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
            likes_photo = []
            for i in data_tags:
                # for j in i:
                print(i[0])
                cursor.execute(query_likes, i[0])
                likes_photo.append(extractData(cursor))
            print(likes_photo)
            q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")

            cursor.execute(q1)
            p1 = cursor.fetchall()
            len_p1 = len(p1)
            if len_p1 > 10:
                new_p1 = []
                for i in range(10):
                    new_p1.append(p1[len_p1 - 1 - i])
                print(new_p1)
                p1 = new_p1
            print(p1)
            query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
            likes_photo = []
            for i in data_tags:
                # for j in i:
                print(i[0])
                cursor.execute(query_likes, i[0])
                likes_photo.append(extractData(cursor))
            print(likes_photo)
            cursor.execute(
                "Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
            top_tags = extractData(cursor)
            return render_template('click_tag.html', name=tags, results=data_tags, likes=likes_photo, c_uid=p1,
                                   tags=top_tags)

        else:

            q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
            print(no_duplicates)
            cursor.execute(q1)
            p1 = cursor.fetchall()
            len_p1 = len(p1)
            if len_p1 > 10:
                new_p1 = []
                for i in range(10):
                    new_p1.append(p1[len_p1 - 1 - i])
                print(new_p1)
                p1 = new_p1
            print(p1)

            query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
            likes_photo = []
            for i in no_duplicates:
                for j in i:
                    print(j[0])
                    cursor.execute(query_likes, j[0])
                    likes_photo.append(extractData(cursor))
            print(likes_photo)
            q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
            print(no_duplicates)
            cursor.execute(q1)
            p1 = cursor.fetchall()
            len_p1 = len(p1)
            if len_p1 > 10:
                new_p1 = []
                for i in range(10):
                    new_p1.append(p1[len_p1 - 1 - i])
                print(new_p1)
                p1 = new_p1
            print(p1)
            query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
            likes_photo = []
            for i in no_duplicates:
                for j in i:
                    print(j[0])
                    cursor.execute(query_likes, j[0])
                    likes_photo.append(extractData(cursor))
            print(likes_photo)
            cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
            top_tags = extractData(cursor)
            return render_template('search_tags.html', name=tags, results=no_duplicates, likes=likes_photo, c_uid=p1, tags=top_tags)
    else:
        return home()
# this searches the comment exactly and returns the photos that have that comment
@app.route('/search_comment/', methods=['POST', 'GET'])
def search_comment():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    if request.method == 'POST':
        data_comment = []

        comment = request.form['search_comment']

        query_find_comment = ("Select * from Photos As p INNER JOIN Comments As c ON p.pid=c.pid where c.cid=(Select t.cid from Comments As t where t.comment=%s)")
        cursor.execute(query_find_comment, (comment))
        data_comment.append(extractData(cursor))
        print(data_comment)
        cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
        top_tags = extractData(cursor)
        return render_template('search_tags.html', name=comment, results=data_comment, tags=top_tags)
    else:
        return home()

# This function returns the friends of the logged in user.
@app.route('/my_friends/', methods=['POST', 'GET'])
def my_friends():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    cursor.execute("Select uid from User where email=%s", (session['username']))
    uid_user = extractData(cursor)
    friends_query="Select * from User where uid in (Select uid2 from friends_with where uid1=%s )"
    cursor.execute(friends_query,uid_user[0][0])
    list_friends=extractData(cursor)
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    print(list_friends)
    return render_template('friend_list.html', data=list_friends, tags=top_tags)

# This function is activated by pressing the add friend button and the person is added as friends for the user logged in.
# But not for the other user.
@app.route('/add_friend/<data>', methods=['POST', 'GET'])
def add_friend(data):
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    assert data == request.view_args['data']
    print(data[0])
    query_userdata = ("Select * from USER where email=%s")
    cursor.execute(query_userdata, (session['username']))
    user_name = cursor.fetchall()
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    cursor.execute("Select * from friends_with where uid1=%s and uid2=%s",(user_name[0][0],data[0]))
    if cursor.rowcount==0:
        add_friend_query=("Insert into friends_with(uid1,uid2) Values(%s,%s)")
        cursor.execute(add_friend_query,(user_name[0][0],data[0]))
        conn.commit()
        return render_template("added_friend.html",data="Added as friend",tags=top_tags)
    else:
        return render_template("added_friend.html",data="Friend already exists.",tags=top_tags)


@app.route('/who_liked/<data>', methods=['POST', 'GET'])
def who_liked(data):
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    assert data == request.view_args['data']
    cursor.execute("Select fname, name, email, Photo.data from User, Photos Photo where uid=(Select p.uid from likes p where p.pid=%s) and photo.pid=%s",(data,data))
    names=extractData(cursor)
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    print(names)
    return render_template("who_liked.html", data=names,tags=top_tags)


"""@app.route('/upload_pictures/', methods=['POST', 'GET'])
def upload_pictures():
    queryUID = ("SELECT uid FROM user WHERE email = %s")
    cursor.execute(queryUID, (session["username"]))
    data_uid = cursor.fetchone()
    uploaded_files = request.files.getlist("file[]")
    print(uploaded_files)
    return """


# this function adds comment to the photo
@app.route('/comment/<photo_d>', methods=['POST','GET'])
def comment(photo_d):
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    assert photo_d == request.view_args['photo_d']
    print(photo_d)
    comment = request.args.get('user_comment')
    uid_user= ("SELECT uid from USER where email =%s")
    cursor.execute(uid_user,session['username'])
    uid= extractData(cursor)
    print("THE UID IS:",uid)
    if comment:
        insert_comment="Insert into comments(pid,uid,comment) Values (%s,%s,%s)"
        cursor.execute(insert_comment,(photo_d,uid,comment))
        conn.commit()
    return home()
# this function is used for anoinymous comments i.e comments made from the index page.
@app.route('/anonymous_comment/<photo_d>', methods=['POST','GET'])
def anonymous_comment(photo_d):
    assert photo_d == request.view_args['photo_d']
    print(photo_d)
    comment = request.args.get('user_comment')
    if comment:
        insert_comment="Insert into comments(pid,uid,comment) Values (%s,5,%s)"
        cursor.execute(insert_comment,(photo_d,comment))
        conn.commit()
    return index()
#This function handles the like button to every photo and adds likes to the database .
@app.route('/likephoto/<photo_d>', methods=['POST','GET'])
def likephoto(photo_d):
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    if request.method == 'GET':
        print(session['username'])
        cursor.execute("SELECT uid from USER where email =%s", session['username'])
        uid = extractData(cursor)
        print("UID FOR THIS PHOTO IS:",uid)
        assert photo_d == request.view_args['photo_d']
        check_query=cursor.execute("Select * from likes where uid=%s and pid=%s",(uid, photo_d))
        if cursor.rowcount==1:
            return home()
        cursor.execute("INSERT INTO likes(uid,pid) VALUES (%s,%s)",(uid, photo_d))
        conn.commit()
    return home()

#this function returns photos recommended to the user by the tags used by the user.
# If the user uses a particular tag more than 3 times, all photos uploaded by other users using this tag are recommended to the user.
@app.route('/recommended_photos/', methods=['POST','GET'])
def recommended_photos():
    if check_user() == False:
        return logoff_page('Sign in to get started!')
    likes_photo = []

    cursor.execute("Select c.tid,count(*) from consists_of c, photos p, User u, Album a where p.pid=c.pid and p.aid=a.aid and a.uid=u.uid and u.email=%s Group by(c.tid) Having count(*)>3 ",session['username'])
    tags_used = extractData(cursor)
    photos=[]
    for tag_id in tags_used:
        photo_recos=("Select p.pid,p.aid,p.caption,p.data from Photos p, consists_of c, tags t, Album a, User u where c.tid=%s and c.pid=p.pid and p.aid=a.aid and a.uid=u.uid and u.email<>%s")
        cursor.execute(photo_recos,(tag_id[0],session['username']))
        photos.append(extractData(cursor))
    print(photos)
    q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
    cursor.execute(q1)
    p1 = cursor.fetchall()
    len_p1 = len(p1)
    if len_p1 > 10:
        new_p1 = []
        for i in range(10):
            new_p1.append(p1[len_p1 - 1 - i])
        print(new_p1)
        p1 = new_p1
    print(p1)
    query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")

    print(likes_photo)
    for j in photos:
        for i in range(len(j)):
            cursor.execute(query_likes, j[i][0])
            likes_photo.append(extractData(cursor))
    print(likes_photo)
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    if photos is None:
        return render_template('error.html',data="No recommendations for you right now!")
    photos_set=set(photos[0])
    return render_template('photo_recos.html', Photo_array=photos_set, c_uid=p1, likes=likes_photo,
                           tags=top_tags)


@app.route('/click_tag/<tag>', methods = ['GET', 'POST'])
def click_tag(tag):
    no_duplicates=[]
    assert tag == request.view_args['tag']
    query_find_tags = ("Select * from Photos As p INNER JOIN Consists_of As c ON p.pid=c.pid where c.tid=(Select t.tid from Tags As t where t.tid=%s)")
    cursor.execute(query_find_tags,tag)
    data_tags=extractData(cursor)
    for i in data_tags:
        if i not in no_duplicates:
            no_duplicates.append(i)
    q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
    print(no_duplicates)
    cursor.execute(q1)
    p1 = cursor.fetchall()
    len_p1 = len(p1)
    if len_p1 > 10:
        new_p1 = []
        for i in range(10):
            new_p1.append(p1[len_p1 - 1 - i])
        print(new_p1)
        p1 = new_p1
    print(p1)

    query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
    likes_photo = []
    for i in no_duplicates:
        #for j in i:
        print(i[0])
        cursor.execute(query_likes, i[0])
        likes_photo.append(extractData(cursor))
    print(likes_photo)
    q1 = ("SELECT u.fname,u.uid,c.pid,c.comment from user u,comments c where u.uid=c.uid ")
    print(no_duplicates)
    cursor.execute(q1)
    p1 = cursor.fetchall()
    len_p1 = len(p1)
    if len_p1 > 10:
        new_p1 = []
        for i in range(10):
            new_p1.append(p1[len_p1 - 1 - i])
        print(new_p1)
        p1 = new_p1
    print(p1)
    query_likes = ("Select pid,COUNT(*) From likes where pid=%s group by pid")
    likes_photo = []
    for i in no_duplicates:
        #for j in i:
        print(i[0])
        cursor.execute(query_likes, i[0])
        likes_photo.append(extractData(cursor))
    print(likes_photo)
    cursor.execute("Select * from tags t where t.tid IN (Select tid from consists_of group by(tid) having COUNT(*)>4 )")
    top_tags = extractData(cursor)
    return render_template('click_tag.html', name=tag, results=no_duplicates, likes=likes_photo, c_uid=p1,
                           tags=top_tags)
if __name__ == '__main__':
    app.secret_key = 'PhotoShare_VaibhavPranav'
    app.run()

