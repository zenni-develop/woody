# 에셋 목록 (출처 · 라이선스 · 사용 위치)

## 사진 — 모두 Unsplash License (상업적 이용 가능, 출처 표기 의무 없음. 페이지 하단에 작가명 표기함)
분위기 연출용이며 실제 매장·메뉴 사진이 아닙니다. 사진 속 인물은 뒷모습뿐이라 식별 불가.

| 키 | 사용 위치 | 작가 | 원본 |
|---|---|---|---|
| hero | 히어로, OG 이미지 | Max van den Oetelaar | https://unsplash.com/photos/1e60bqR1Ar0 |
| room | 起 (공간) | PhilCreates | https://unsplash.com/photos/xPtiN7OmaXg |
| matcha | 承 (맛차라떼) | Jason Leung | https://unsplash.com/photos/Z-hvocTfR_s |
| dango | 承 (당고) | Diana Bondarenko | https://unsplash.com/photos/KMnVNWxbCVc |
| fig | 承 (가을 한정) | Heather Newsom | https://unsplash.com/photos/iW5MaQKTU6w |
| hojicha | 転 | Büşra İnce | https://unsplash.com/photos/djWJLL91_KQ |
| alley | 結 | Julien | https://unsplash.com/photos/7J50ltZEYdQ |

교체 방법: `src/data/site.json` → `images.<키>.src`를 새 경로(예: `../images/hero.webp`)로 바꾸고 `w`, `h`, `focus`(초점 위치), `author`, `page`를 수정. 자체 호스팅으로 바꾸면 CSP의 `img-src`에서 `images.unsplash.com`을 지워도 됩니다.

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
