# 🚀 IndexNow & 자동 인덱싱 셋업 가이드

## 📋 개요

이 사이트는 다음과 같이 구성되어 있습니다:

- **IndexNow 키**: `7a8d3c91-2f4e-4b7a-9d2e-1f3a5c8e7d2b`
- **사이트 URL**: `https://anyang-massage1.pages.dev`
- **Sitemap**: `https://anyang-massage1.pages.dev/sitemap.xml`
- **IndexNow Key File**: `https://anyang-massage1.pages.dev/indexnow-key.txt`
- **Robots.txt**: `https://anyang-massage1.pages.dev/robots.txt`

---

## 🔑 IndexNow 설정 (수동)

### 1단계: 키 파일 검증
`/public/indexnow-key.txt` 파일에 IndexNow 키가 저장되어 있습니다.

```
7a8d3c91-2f4e-4b7a-9d2e-1f3a5c8e7d2b
```

### 2단계: Bing 웹마스터 도구에 등록
1. [Bing 웹마스터 도구](https://www.bing.com/webmasters) 접속
2. 사이트 추가: `https://anyang-massage1.pages.dev`
3. IndexNow 키 등록 (위의 키 사용)
4. 로봇 파일 및 사이트맵 인증 완료

### 3단계: Naver 서치어드바이저 등록
1. [Naver 서치어드바이저](https://searchadvisor.naver.com) 접속
2. 사이트 추가: `https://anyang-massage1.pages.dev`
3. IndexNow 키 등록 (위의 키 사용)
4. 로봇 파일 및 사이트맵 인증 완료

---

## ⚡ 자동 인덱싱 (Python 스크립트)

### 준비
```bash
# 필요한 패키지 설치
pip install requests

# 또는 requirements.txt에서 설치
pip install -r requirements.txt
```

### 사용법

#### 1. 모든 URL을 Bing/Naver에 통보
```bash
# 실제 통보
npm run build
python3 tools/indexnow.py

# 또는
cd /home/user/Anyang-Massage1
python3 tools/indexnow.py
```

#### 2. 먼저 확인만 (DRY RUN)
```bash
python3 tools/indexnow.py --dry-run
```

#### 3. URL 목록만 출력
```bash
python3 tools/indexnow.py --urls
```

#### 4. 사이트맵 경로 지정
```bash
python3 tools/indexnow.py --sitemap custom/path/sitemap.xml
```

---

## 📊 결과

스크립트 실행 후:

```
📖 사이트맵 로드: dist/sitemap.xml
✅ 976개 URL 발견

🚀 IndexNow 통보 시작...
   사이트: https://anyang-massage1.pages.dev
   IndexNow 키: 7a8d3c91-2f4e-4b7a-9d2e-1f3a5c8e7d2b

📤 배치 1/1 통보 중...
   URL 개수: 976

✅ Bing IndexNow: 200

============================================================
✅ 통보 완료!
   총 976개 URL
   1개 배치
============================================================

⏰ 완료 시간: 2026-06-24 04:15:30
```

---

## 🔄 자동 통보 스케줄 (선택)

### GitHub Actions로 자동화 (Git 푸시 시)

`.github/workflows/indexnow.yml` 생성:

```yaml
name: IndexNow Auto Notify

on:
  push:
    branches: [main, claude/practical-newton-vt6ip9]

jobs:
  indexnow:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Build site
        run: npm ci && npm run build
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install Python deps
        run: pip install requests
      
      - name: Notify IndexNow
        run: python3 tools/indexnow.py
```

### Cron으로 정기 통보 (선택)

매주 월요일 00:00 자동 통보:

```yaml
name: IndexNow Weekly Notify

on:
  schedule:
    - cron: '0 0 * * 1'  # 매주 월요일 자정

jobs:
  indexnow:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Build & Notify
        run: npm ci && npm run build && pip install requests && python3 tools/indexnow.py
```

---

## 🌐 구글 Indexing API (선택 - 추가 설정)

구글은 IndexNow를 지원하지 않으므로, 별도로 구글 Indexing API를 사용할 수 있습니다.

### 준비
1. [구글 클라우드 콘솔](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성
3. Indexing API 활성화
4. 서비스 어카운트 생성 및 JSON 키 다운로드
5. `credentials.json`을 프로젝트 루트에 저장

### 스크립트 실행
```bash
python3 tools/google_indexing.py
```

---

## ✅ 확인 사항

### Bing 웹마스터 도구
- [Bing Webmaster Tools](https://www.bing.com/webmasters/home)
- URL 제출 현황 확인
- 크롤링 상태 모니터링

### Naver 서치어드바이저
- [Naver Search Advisor](https://searchadvisor.naver.com)
- 사이트맵 제출 확인
- 색인 현황 확인

### 구글 서치 콘솔
- [Google Search Console](https://search.google.com/search-console)
- 사이트맵 제출
- 색인 상태 모니터링

---

## 📝 Sitemap & Robots.txt

### Sitemap
- **경로**: `/dist/sitemap.xml`
- **URL**: `https://anyang-massage1.pages.dev/sitemap.xml`
- **크기**: ~194KB
- **URL 개수**: 976개

### Robots.txt
- **경로**: `/public/robots.txt`
- **URL**: `https://anyang-massage1.pages.dev/robots.txt`
- **내용**: 모든 봇 허용, 사이트맵 및 IndexNow 키 명시

---

## 🚨 트러블슈팅

### 문제: `requests` 모듈 없음
```bash
pip install requests
```

### 문제: 사이트맵 파일 없음
```bash
npm run build  # 먼저 빌드 실행
python3 tools/indexnow.py
```

### 문제: IndexNow API 오류
- IndexNow 키가 정확한지 확인
- 호스트명이 정확한지 확인
- 키 파일이 공개 접근 가능한지 확인

---

## 📞 참고 링크

- [IndexNow 공식 문서](https://www.indexnow.org/)
- [Bing 웹마스터 도구](https://www.bing.com/webmasters)
- [Naver 서치어드바이저](https://searchadvisor.naver.com)
- [구글 Search Console](https://search.google.com/search-console)

---

**마지막 업데이트**: 2026-06-24
