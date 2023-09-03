# wandted 팀 과제 : Notion API
---
## 요구사항
- 각 페이지는 제목, 내용, 서브페이지를 가질 수 있다.
- 특정 페이지에 대한 BreadCrumbs 반환 ex) 페이지 1 > 페이지 3 > 페이지 5 
- 내용 내에서 서브페이지 위치 고려는 하지 않는다. 
---
## 결과 출력 예시
```
{
		“pageId” : 1,
		“title” : 1,
		“subPages” : [],
		“breadcrumbs” : [“A”, “B”, “C”] or “A / B / C”
}
```
---

## 테이블 구조 : ERD
![](https://velog.velcdn.com/images/wodnr_09/post/84ab5b45-dfa7-4e68-9013-3033d69f4a2c/image.png)

---
## 비즈니스 로직
```python
import os
import sqlite3

# DB 및 SQLite cursor 생성
def DataBase():
    conect_db = sqlite3.connect("test_db")
    cursor = conect_db.cursor()
    return cursor, conect_db


# sub_page 생성 및 예외처리
def get_subPage(cursor, page_id):
    try:
        cursor.execute("SELECT child_id FROM PageHierarchy WHERE parent_id=? LIMIT 4", (page_id,))
        return [row[0] for row in cursor.fetchall()]
    except sqlite3.Error:
        print("SQL Query Error")
    return []


# breadcrumbs 저장 및 예외처리
# 자식 id 기준 부모 아이디 조회로 breadcrumbs 추출
# 만약 부모 아이디가 없으면 breadcumbs None으로 초기화
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


# notion page 정보 GET API
def get_PageInfo_Api(pageID):
    cursor = DataBase()[0]
    cursor.execute("SELECT * FROM Pages WHERE id=?", (pageID,))
    page_info = cursor.fetchone()
    
    if page_info == None:
        return None 
    page_id, title, content = page_info
    sub_page = get_subPage(cursor, page_id)
    breadcrumbs = get_breadcrumbs(cursor, page_id)
    
    return {
            "pageId": page_id,
	    "title": title,
            "content": content,
	    "subPages": sub_page if sub_page else [],
	    "breadcrumbs": breadcrumbs if breadcrumbs else []
           }
```

---

## 결과 정보
- 현재 페이지가 1일 경우
- 페이지 1의 하위 페이지 : 2, 3, 4
- 페이지 1의 상위 페이지 : 5(title: F), 6(title: G), 7(title: H)
```
{
    'pageId': 1,
    'title': 'A',
    'content': '첫번째 페이지 내용',
    'subPages': [2, 3, 4],
    'breadcrumbs': ['H', 'G', 'F', 'A']
}
```
