'''
table 구조
create table page(
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    content VARCHAR(255),
    );
    
create table page_info(
    page_id INT,
    sub_page INT,
    parent_page INT,
    FOREIGN KEY (page_id) REFERENCES page (id),
    FOREIGN KEY (sub_page) REFERENCES page (id),
    FOREIGN KEY (parent_page) REFERENCES page (id)
)
'''

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DB_PASSWORD = os.environ.get('db_password')
DB_URL = f"mysql+mysqlconnector://root:{DB_PASSWORD}@localhost:3306/notion?charset=utf8"

database = create_engine(DB_URL, max_overflow = 0)

# ex_request = {"title":"test title",
#               "content":"test content"}

def get_page_info(what: str, page_id:int)->list:
    '''
    what : parent_page or sub_page 입력
    page_id에 해당하는 페이지의 부모 or 자식 페이지의 id를 리스트로 반환
    '''
    db = database.connect()
    page_info = db.execute(text(f"""
                SELECT {what} FROM page_info WHERE page_id=:page_id"""),{'page_id': int(page_id)}).fetchall()
    result = list(x[0] for x in page_info  if x[0] is not None)
    return result

def make_pages(breadcrumbs:list, request:dict)->dict:
    '''
    페이지 생성 api
    현재 페이지의 breadcrumbs를 받는 다는 전제하에, 다음과 같이 부모, 서브 페이지 정보 저장
    '''
    db = database.connect()    
    new_page_id = db.execute(text("""
                INSERT INTO page(title, content)
                VALUES (:title, :content)"""), request).lastrowid
    
    if len(breadcrumbs) >=1:
        for i in range(len(breadcrumbs)):
            parent_page = breadcrumbs[i].split('_')[1]
            db.execute(text("""
                INSERT INTO page_info(page_id, parent_page)
                VALUES (:page_id, :parent_page)"""),
                {'page_id':new_page_id, 'parent_page':parent_page})
    db.commit()
    return {"status":200, "msg":"ok"}

def get_page(page_id:int)->dict:
    '''
    페이지 조회 api
    '''
    db = database.connect()
    page_info = db.execute(text("""
                SELECT title,content FROM page WHERE id=:page_id"""),{'page_id': int(page_id)}).fetchone()
    
    breadcrumbs = []
    parent_pages = get_page_info('parent_page', page_id)
    sub_pages = get_page_info('sub_page', page_id)

    if parent_pages:
        for page in parent_pages:
            breadcrumbs.append(f'page_{page}')
    breadcrumbs.append(f'page_{page_id}')
    
    return {
        'page_id':page_id,
        'title':page_info[0],
        'content': page_info[1],
        'sub_pages' : sub_pages,
        'breadcrumbs' : breadcrumbs
    }