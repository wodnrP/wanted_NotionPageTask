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
    print('pre:',sub_page)

    while True:
        row = cursor.fetchone()
        
        if row == None:
            break
    
        sub_page.append(row[0])
    
    print('aft:',sub_page)

    
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

update_pages = """
    INSERT INTO Pages(title, content) 
    VALUES ('첫번째 부모 페이지', '첫번째 페이지 내용입니다');
"""

update_hierarchy = """
    INSERT INTO PageHierarchy(parent_id, child_id) 
    VALUES (1, 2), (1, 3), (1, 4);
"""

test_db = DataBase()
test_db[0].execute(create_pages)
test_db[0].execute(create_hierarchy)
test_db[0].execute(update_pages)
test_db[0].execute(update_hierarchy)
test_db[1].commit()
# 확인
print(get_PageInfo_Api(1))