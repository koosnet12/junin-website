# 사이트 생성 스크립트

HTML은 이 스크립트로 만듭니다. 손으로 고친 내용은 다시 생성할 때 덮어써집니다.

```
JUNIN_OUT=/path/to/output python3 src/build_en.py   # 한국어 + 영문(/en/) + sitemap.xml, robots.txt
```

데이터(연도별 납품량, 대표 프로젝트, 제품 구성 CSV)는 `build.py`의 `DATA` 경로에서 읽습니다.
