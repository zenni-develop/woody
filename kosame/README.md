# 카페 코사메(小雨) 소개 페이지

인천 구월동의 작은 일본식 찻집 **카페 코사메**를 소개하는 3개 국어(한국어·日本語·English) 원페이지입니다.
기승전결(起承転結) 네 장으로 구성했습니다.

| 장 | 내용 |
|---|---|
| 히어로 | 가랑비 저녁의 창, 세로쓰기 `小雨`, 길 찾기, 실시간 영업 상태 |
| 起 들어서며 | 이름의 뜻, 골목 안의 공간, 오래 이어온 시간 |
| 承 머무르며 | 차림표(당고·차·코사메의 음료·커피), 사장님 추천 조합 |
| 転 돌아보며 | "당고 좋아하세요?", 플랫폼 평점, 국내·해외 방문객 이야기, 알고 가면 좋은 점 |
| 結 찾아가며 | 영업시간·주소·교통·주차, 지도 앱 3종, 자주 묻는 질문 |

## 구조
```
kosame/
├─ build.mjs              # 빌드 (외부 패키지 없음, Node 18+)
├─ src/
│  ├─ layout.mjs          # 레이아웃 1벌
│  ├─ i18n/ko|ja|en.json  # 언어별 문구
│  └─ data/site.json      # 영업시간·가격·링크·사진 등 공통 정보
├─ public/assets/         # CSS, JS, 파비콘, 서브셋 폰트
├─ tools/subset-fonts.py  # 사용 글자만 남긴 woff2 폰트 생성
└─ docs/                  # 조사 자료, 디자인 플랜, 검토 로그, 에셋 목록, 용어집
```

## 실행
```bash
node build.mjs                 # dist/ 생성
python3 -m http.server -d dist # http://localhost:8000/ko/
```

## 문구를 바꿨을 때
문구에 새 글자가 생기면 폰트 서브셋을 다시 만들어야 합니다.
```bash
node build.mjs
python3 tools/subset-fonts.py   # fontTools 필요, Noto CJK·Inter 폰트 설치 필요
node build.mjs --check          # 빠진 글자가 있으면 실패
```
`--check`는 GitHub Actions에서도 실행되므로 폰트를 갱신하지 않으면 배포가 멈춥니다.

## 정보 수정
- 영업시간·휴무: `src/data/site.json`의 `hours` (요일 번호 0=일요일 … 4=목요일) + 각 언어 `ketsu.info`
- 가격: `src/data/site.json`의 `menu`
- 사진 교체: `docs/asset-list.md` 참고
- 정보 기준일: `src/data/site.json`의 `updated`

## 배포 (GitHub Pages)
1. 저장소 Settings → Pages → Source를 **GitHub Actions**로 설정
2. `main`에 푸시하면 `.github/workflows/kosame-pages.yml`이 빌드·배포
3. 주소: `https://zenni-develop.github.io/woody/` (커스텀 도메인을 쓰면 `site.json`의 `siteUrl` 변경)

## 분석 연결 (선택)
CTA 클릭 시 `window.dataLayer`(GA4/GTM) 또는 `window.plausible`이 있으면 `cta_click` 이벤트를 언어 정보와 함께 보냅니다.
도구를 추가할 때는 `src/layout.mjs`의 CSP에 해당 도메인을 추가하고, 개인정보처리방침(3개 국어)을 함께 준비하세요.
