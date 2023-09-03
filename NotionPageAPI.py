"""
1. 테이블 구조
페이지를 저장하는 테이블 : 각 페이지의 정보
각 페이지의 계층 구조를 저장하는 테이블 : 페이지 간의 관계 

- DB생성 : sqLite
- 테이블 생성 ex)
페이지 테이블 
CREATE TABLE Pages (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);


CREATE TABLE PageHierarchy (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER,
    child_id INTEGER,
    
	FOREIGN KEY(parent_id) REFERENCES Pages(id),
	FOREIGN KEY(child_id) REFERENCES Pages(id)
);

2. 페이지 정보 불러오는 함수 : input pageID
    - DB에서 페이지 정보 불러오기
    - 서브 페이지 불러오기
    - 브로드 크럼스 
    - return {
"pageId" : 1,
"title" : 1,
"subPages" : [],
"breadcrumbs" : ["A", "B", "C",] // 혹은 "breadcrumbs" : "A / B / C"
} 
"""
import os
import sqlite3

def DataBase():
    conect_db = sqlite3.connect("test_db")
    cursor = conect_db.cursor()
    return cursor, conect_db

def get_subPage(cursor, page_id):
    try:
        cursor.execute("SELECT child_id FROM PageHierarchy WHERE parent_id=? LIMIT 4", (page_id,))
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error:
        print("SQL Query Error")
    return []

# insert(0,) -> deque() O(n) -> O(1) 개선
def get_breadcrumbs(cursor, page_id):
    from collections import deque
    breadcrumbs = deque()
    cur_page = page_id

    try:
        while cur_page != None:
            cursor.execute("SELECT parent_id FROM PageHierarchy WHERE child_id=?", (cur_page,))
            parent_info = cursor.fetchone()
            cursor.execute("SELECT title FROM Pages WHERE id=?", (cur_page,))
            breadcrumbs_title = cursor.fetchone()

            if parent_info != None:
                breadcrumbs.appendleft(breadcrumbs_title[0])
                cur_page = parent_info[0]

            else:
                breadcrumbs.appendleft(breadcrumbs_title[0])
                if breadcrumbs[0] == page_id:
                    breadcrumbs.clear()
                break
        return list(breadcrumbs)
    
    except sqlite3.Error:
        print("SQL Query Error")
    return []

def get_PageInfo_Api(pageID):
    cursor = DataBase()[0]
    cursor.execute("SELECT * FROM Pages WHERE id=?", (pageID,))

    page_info = cursor.fetchone()
    
    if page_info == None:
        return None 
    
    page_id, title, content = page_info

    # 최대 4개 조회
    sub_page = get_subPage(cursor, page_id)

    # 자식 id 기준 부모 아이디 조회로 breadcrumbs 추출
    # 만약 부모 아이디가 없으면 breadcumbs None으로 초기화
    breadcrumbs = get_breadcrumbs(cursor, page_id)
    
    return {
        "pageId": page_id,
	    "title": title,
        "content": content,
	    "subPages": sub_page if sub_page else [],
	    "breadcrumbs": breadcrumbs if breadcrumbs else []
    }

    
# PagesTable, PageHiierarchyTable 생성
create_pages = """
    CREATE TABLE Pages (
    id INTEGER PRIMARY KEY, 
    title TEXT NOT NULL, 
    content TEXT NOT NULL);
    """

create_hierarchy = """
    CREATE TABLE PageHierarchy (
    id INTEGER PRIMARY KEY, 
    parent_id INTEGER, 
    child_id INTEGER, 
    FOREIGN KEY(parent_id) REFERENCES Pages(id), 
    FOREIGN KEY(child_id) REFERENCES Pages(id));
    """

insert_pages = [
    (1, 'A', '첫번째 페이지 내용'),
    (2, 'B', '두번째 페이지 내용'),
    (3, 'C', '세번째 페이지 내용'),
    (4, 'D', '네번째 페이지 내용'),
    (5, 'F', '다섯번째 페이지 내용'),
    (6, 'G', '여섯번째 페이지 내용'),
    (7, 'H', '일곱번째 페이지 내용')
]

update_hierarchy = """
    INSERT INTO PageHierarchy(parent_id, child_id) 
    VALUES (1, 2), (1, 3), (1, 4), (5, 1), (6, 5), (7, 6);
"""

# 테스트 DB 생성 및 dummy data 추가 후 저장
if not os.path.exists("test_db"):
    test_db = DataBase()
    test_db[0].execute(create_pages)
    test_db[0].execute(create_hierarchy)
    for i in insert_pages:
        test_db[0].execute("INSERT INTO Pages(id, title, content) VALUES(?,?,?)", i)
    test_db[0].execute(update_hierarchy)
    test_db[1].commit()

#확인
print(get_PageInfo_Api(1))