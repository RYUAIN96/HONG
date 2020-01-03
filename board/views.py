from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode 
# byte배열을 base64로 변경함.

cursor = connection.cursor() #sql문 수행위한 cursor객체

@csrf_exempt  
def edit(request):
    if request.method == 'GET':
        no = request.GET.get("no",0)

        sql = """
            SELECT NO, TITLE, CONTENT
            FROM BOARD_TABLE1
            WHERE NO=%s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone() 
        return render(request, 'board/edit.html', {"one":data})
    
    elif request.method == "POST":
        no = request.POST['no']
        ti = request.POST['title']
        co = request.POST['content']

        arr = [ti, co, no]
        sql = """
            UPDATE BOARD_TABLE1 SET TITLE=%s, 
            CONTENT=%s WHERE NO= %s
        """
        cursor.execute(sql, arr)
        return redirect("/board/content?no="+no)


@csrf_exempt  
def delete(request):
    if request.method == 'GET':
        no = request.GET.get("no",0)

        sql = """
            DELETE FROM BOARD_TABLE1
            WHERE NO = %s
        """
        cursor.execute(sql, [no])

        return redirect("/board/list")

# 127.0.0.1:8000/board/content?no=34
# 127.0.0.1:8000/board/content    ?no=0  => 오류발생
@csrf_exempt  
def content(request):
    if request.method == 'GET':
        no = request.GET.get('no', 0)  
        # request.GET['no']
        if no == 0 :
            return redirect("/board/list") # <a href와 같음

        if request.session['hit'] == 1:
            #조회수 1증가 시킴
            sql = """
                UPDATE BOARD_TABLE1 SET HIT=HIT+1
                WHERE NO = %s    
            """
            cursor.execute(sql, [no])
            request.session['hit'] = 0

        # 이전글 번호 가져오기
        sql = """
            SELECT NVL(MAX(NO), 0)
            FROM BOARD_TABLE1
            WHERE NO < %s
        """
        cursor.execute(sql, [no])
        prev = cursor.fetchone()

        # 다음글 번호 가져오기
        sql = """
            SELECT NVL(MIN(NO), 0)
            FROM BOARD_TABLE1
            WHERE NO > %s
        """
        cursor.execute(sql, [no])
        next = cursor.fetchone()

        # 게시물 내용 가져오기
        sql = """
            SELECT 
                NO, TITLE, CONTENT, WRITER, HIT,  
                TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS'),
                IMG 
            FROM 
                BOARD_TABLE1
            WHERE
                NO = %s
        """
        cursor.execute(sql, [no])
        data = cursor.fetchone()  # (1,2,3,4,5,6)

        if data[6] : # DB에 BLOB로 있는 경우
            img = data[6].read() # 바이트배열을 img에 넣음
            img64 = b64encode(img).decode("utf-8")
        else : # 없는 경우
            file = open('./static/img/default.jpg', 'rb')
            img = file.read()
            img64 = b64encode(img).decode("utf-8")

        #print(no)
        return render(request, 'board/content.html',
             {"one":data, "image":img64, 
             "prev":prev[0], "next":next[0]}) 


@csrf_exempt  
def list(request):
    if request.method == 'GET':
        request.session['hit'] = 1  #세션에 hit=1
        sql = """
            SELECT 
                NO, TITLE, WRITER, 
                HIT, TO_CHAR(REGDATE, 'YYYY-MM-DD HH:MI:SS') 
            FROM 
                BOARD_TABLE1
            ORDER BY NO DESC
        """
        cursor.execute(sql)
        data = cursor.fetchall()
        print( type(data) ) 
        print( data )        #[(    ),(    ) ]
        return render(request, 'board/list.html', {"list":data}) 


@csrf_exempt  
def write(request):
    if request.method == 'GET':
        return render(request, 'board/write.html') 
    elif request.method == 'POST':

        print("BBB")
        tmp = None

        if 'img' in request.FILES:
            print("AAA")
            print(request.FILES)

            img = request.FILES['img']        
            tmp = img.read()

        arr = [ 
            request.POST['title'],
            request.POST['content'],
            request.POST['writer'],
            tmp
        ]
        try :
            # print(arr)
            sql = """
                INSERT INTO BOARD_TABLE1
                (TITLE, CONTENT, WRITER, IMG, HIT, REGDATE)
                VALUES(%s, %s, %s, %s, 234, SYSDATE)
            """
            cursor.execute(sql, arr)
        except Exception as e:
            print(e)    
        
        return redirect("/board/list") # <a href와 같음

