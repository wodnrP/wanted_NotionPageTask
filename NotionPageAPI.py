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
    return cursor


def get_PageInfo_Api(pageID):
    print(DataBase())
    DataBase().execute("SELECT * FROM Pages WHERE id=?", (pageID,))
    page_info = DataBase().fetchone()
    
    if page_info == None:
        return None 
    
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

DataBase().execute(create_pages)
DataBase().execute(create_hierarchy)

# 확인
print(get_PageInfo_Api(1))