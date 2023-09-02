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

import sqlite3

def DataBase():
    conect_db = sqlite3.connect("test_db")
    cursor = conect_db.cursor()
    return cursor, conect_db


def get_PageInfo_Api(pageID):
    cursor = DataBase()[0]
    cursor.execute("SELECT * FROM Pages WHERE id=?", (pageID,))

    page_info = cursor.fetchone()
    
    if page_info == None:
        return None 
    
    page_id, title, content = page_info

    # 최대 4개 조회
    cursor.execute("SELECT child_id FROM PageHierarchy WHERE parent_id=? LIMIT 4", (page_id,))

    sub_page = []

    while True:
        row = cursor.fetchone()
        
        if row == None:
            break
    
        sub_page.append(row[0])
    

    # 자식 id 기준 부모 아이디 조회로 breadcrumbs 추출
    # 만약 부모 아이디가 없으면 breadcumbs None으로 초기화
    breadcrumbs = []
    cur_page = page_id

    while cur_page != None:
        cursor.execute("SELECT parent_id FROM PageHierarchy WHERE child_id=?", (cur_page,))
        parent_info = cursor.fetchone()
        cursor.execute("SELECT title FROM Pages WHERE id=?", (cur_page,))
        breadcrumbs_title = cursor.fetchone()

        if parent_info != None:
            breadcrumbs.insert(0, breadcrumbs_title[0])
            cur_page = parent_info[0]

        else:
            breadcrumbs.insert(0, breadcrumbs_title[0])
            if breadcrumbs[0] == page_id:
                breadcrumbs.clear()
            break
    
    return {
        "pageId": page_id,
	    "title": title,
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

update_pages1 = """
    INSERT INTO Pages(id, title, content) VALUES(1, 'A', '첫번째 페이지 내용');
"""
update_pages2 = """
    INSERT INTO Pages(id, title, content) VALUES(2, 'B', '두번째 페이지 내용');
"""
update_pages3 = """
    INSERT INTO Pages(id, title, content) VALUES(3, 'C', '세번째 페이지 내용');
"""
update_pages4 = """
    INSERT INTO Pages(id, title, content) VALUES(4, 'D', '네번째 페이지 내용');
"""
update_pages5 = """
    INSERT INTO Pages(id, title, content) VALUES(5, 'F', '다섯번째 페이지 내용');
"""
update_pages6 = """
    INSERT INTO Pages(id, title, content) VALUES(6, 'G', '여섯번째 페이지 내용');
"""
update_pages7 = """
    INSERT INTO Pages(id, title, content) VALUES(7, 'H', '일곱번째 페이지 내용');
"""

update_hierarchy = """
    INSERT INTO PageHierarchy(parent_id, child_id) 
    VALUES (1, 2), (1, 3), (1, 4), (5, 1), (6, 5), (7, 6);
"""

# 테스트 DB 생성 및 dummy data 추가 후 저장
# test_db = DataBase()
# test_db[0].execute(create_pages)
# test_db[0].execute(create_hierarchy)
# test_db[0].execute(update_pages1)
# test_db[0].execute(update_pages2)
# test_db[0].execute(update_pages3)
# test_db[0].execute(update_pages4)
# test_db[0].execute(update_pages5)
# test_db[0].execute(update_pages6)
# test_db[0].execute(update_pages7)
# test_db[0].execute(update_hierarchy)
# test_db[1].commit()

#확인
print(get_PageInfo_Api(1))