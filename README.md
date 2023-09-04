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
- Pages 테이블 : 페이지 제목과 내용 정보를 저장하는 테이블 입니다.
- PageHierarchy 테이블 : 페이지 계층 정보를 저장하는 테이블입니다.
- N:M 구조 입니다.
  
### why?
- 상위 페이지, 하위 페이지가 나뉘게 되므로 계층 구조를 생각, 이 정보를 저장하기 위해 PageHierarchy 테이블을 생성했습니다.
- 해당 페이지가 **상위 페이지인지, 하위 페이지인지 구분을 하기 위해** 자식_id와 부모_id로 구분하여 외래키로 저장했습니다.
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
- 페이지 1의 상위 페이지 : 5(title: F)
- 페이지 5의 상위 페이지 : 6(title: G)
- 페이지 6의 상위 페이지 : 7(title: H)
```
{
    'pageId': 1,
    'title': 'A',
    'content': '첫번째 페이지 내용',
    'subPages': [2, 3, 4],
    'breadcrumbs': ['H', 'G', 'F', 'A']
}
```
## ⭐️ 로직 설명
로직의 핵심은 try구문 Error 처리, get_breadcrumbs()에서 활용한 **양방향 큐**와 **DFS 깊이 우선 탐색 자료구조 활용** 입니다.

1. 현재 입력받은 페이지를 기준으로 부모 페이지 즉, 상위 페이지를 하나씩 탐색해가는 것이 핵심 입니다.
2. breadcrumbs에 제목을 저장하는 과정에서 insert(0,)의 O(n) 시간복잡도에 비해 양방향 큐 deque가 시간복잡도를 O(1)로 더 짧기때문에 활용했습니다. 

####  get_PageInfo_Api()
- 결과 정보를 반환하는 메인 함수
- DB에서 현재 입력받은 페이지 ID를 기준으로 Pages의 모든 데이터를 조회
- 조회한 데이터의 한 행에 담긴 속성들을 page_id, title, content에 담고 sub_page()함수를 실행
- page_id를 활용하여 get)breadcrumbs()함수를 실행
- pageId, title, content와 함께 sub_page,breadcrumbs는 값이 존재하면 실행 결과를 반환, 아니면 빈 리스트를 반환

#### sub_page()  
- page_id를 기준으로 서브 페이지의 정보를 반환, DB에러 사항을 대비하여 try 구문으로 예외처리 
- 에러가 발생하지 않는다면 입력받은 page_id를 부모 페이지 id라고 했을 때, 해당되는 자식 페이지 id를 조회
- 조회한 자식 페이지 id를 한 행씩 반복하여 리스트로 반환

#### get_breadcrumbs()
- 입력 받은 page_id를 현재 페이지로 저장
- breadcrumbs를 deque로 지정
- sub_page()와 같이 try 구문을 통해 예외처리, 현재 페이지가 존재한다면 자식 페이지라고 했을 때 부모 페이지 id를 조회
- 조회한 부모 페이지 id의 첫번 째 행을 parent_info에 저장
- breadcrumbs에 반환 될 페이지의 제목을 현재 페이지의 id로 조회
- 부모 페이지가 있을 경우 breadcrumbs의 가장 첫번째 인덱스에 조회한 제목을 저장, 현재 페이지는 부모 페이지로 바꿔 준 후 위 과정 반복
- 없을 경우 현재 페이지를 첫번째 인덱스에 저장, 반복문 탈출. 만약 부모 페이지가 없는 경우 저장했던 현재 페이지 제목을 삭제
- breadcrumbs를 list 타입으로 변경 후 반환

---

## ⭐️ 최종 선택 이유
- 코드 복잡도를 고려한 raw 쿼리문 활용 
- Try except 구문으로 Error 상황을 예외 사항으로 처리한 점
- 서브 페이지와 breadcrumbs 로직을 함수로 분리하여 유지보수, 확장성을 고려한 점
- 큐, DFS 같은 자료구조의 활용과 시간복잡도를 고려하여 로직을 작성한 점

