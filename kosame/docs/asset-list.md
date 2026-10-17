# 에셋 목록 (출처 · 라이선스 · 사용 위치)

## 일러스트 — 이 페이지를 위해 직접 그린 오리지널 SVG (저작권: 페이지 제작자, 외부 소스 없음)
`tools/illustrations.py`가 같은 팔레트·화풍으로 생성합니다(난수 시드 고정, 다시 실행해도 같은 그림). 분위기 연출용이며 실제 매장·메뉴와 다를 수 있습니다.

| 파일 | 사용 위치 | 내용 |
|---|---|---|
| images/hero.svg | 히어로 | 유리 지붕 아래 덩굴·몬스테라·화분이 가득한 찻집, 창밖 가랑비, 말차와 당고가 놓인 테이블 |
| images/room.svg | 起 | 햇살 드는 창가 선반과 의자 위 화분들 |
| images/matcha.svg | 承 | 잎 모양 라테아트의 말차라떼 (위에서 본 모습) |
| images/dango.svg | 承 | 미타라시·말차·인절미 당고 세 꼬치와 매실 절임 방울토마토 |
| images/fig.svg | 承 (가을 한정) | 리넨 위의 무화과와 단면 |
| images/hojicha.svg | 転 | 우유 위에 호지차를 올린 라테 |
| images/window.svg | 結 | 가랑비 내리는 창가에 줄지은 화분 |
| og/og-image.jpg | 공유 미리보기 (1200×630) | hero.svg에서 `tools/og-image.py`로 생성 |

수정 방법: `tools/illustrations.py`의 색(`C`)이나 장면 함수를 고친 뒤 `python3 tools/illustrations.py && python3 tools/og-image.py`. 실제 사진으로 바꾸려면 `src/data/site.json`의 `images.<키>.src`를 새 파일로 바꾸면 됩니다.

## 폰트 — 모두 SIL Open Font License 1.1, 사용 글자만 남긴 woff2 서브셋으로 직접 호스팅
| 파일 | 원본 | 용도 |
|---|---|---|
| sans-ko-400/500 | Noto Sans CJK KR | 한국어 본문 |
| sans-ja-400/500 | Noto Sans CJK JP | 일본어 본문 |
| sans-en-400/500 | Inter | 영어 본문 |
| sans-root-400/500 | Noto Sans CJK KR | 언어 선택 페이지 |
| serif-* | Noto Serif CJK (KR/JP) SemiBold | 제목, 세로쓰기 한자 |

## 아이콘·로고
| 파일 | 출처 |
|---|---|
| public/assets/favicon.svg | 직접 제작 (빗줄기 + 등불 점) |

## 텍스트 출처
페이지 하단 "정보 출처"와 `docs/research.md` 참고. 리뷰는 요약만 사용, 리뷰어 이름은 싣지 않음.
