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
