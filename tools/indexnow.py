#!/usr/bin/env python3
"""
IndexNow 자동 통보 스크립트
사이트의 모든 URL을 Bing, Naver에 즉시 인덱싱 통보합니다.

사용법:
  python3 tools/indexnow.py               # 모든 URL 통보
  python3 tools/indexnow.py --urls        # URL 리스트만 출력
  python3 tools/indexnow.py --dry-run     # 실행 없이 확인
"""

import xml.etree.ElementTree as ET
import requests
import sys
from pathlib import Path
from typing import List
import argparse
from datetime import datetime

# 설정
SITE_URL = "https://anyang-massage1.pages.dev"
INDEXNOW_KEY = "7a8d3c91-2f4e-4b7a-9d2e-1f3a5c8e7d2b"
BING_INDEXNOW_URL = "https://api.indexnow.org/indexnow"

def parse_sitemap(sitemap_path: str) -> List[str]:
    """sitemap.xml에서 모든 URL 추출"""
    try:
        tree = ET.parse(sitemap_path)
        root = tree.getroot()
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = []

        for url_elem in root.findall('ns:url', namespace):
            loc = url_elem.find('ns:loc', namespace)
            if loc is not None:
                urls.append(loc.text)

        return urls
    except Exception as e:
        print(f"❌ 사이트맵 파싱 실패: {e}", file=sys.stderr)
        return []

def notify_indexnow(urls: List[str], dry_run: bool = False) -> dict:
    """IndexNow를 통해 모든 URL 통보"""
    if not urls:
        print("❌ 통보할 URL이 없습니다.", file=sys.stderr)
        return {"success": False, "total": 0}

    batch_size = 10000
    batches = [urls[i:i + batch_size] for i in range(0, len(urls), batch_size)]

    results = {
        "success": True,
        "total": len(urls),
        "batches": len(batches),
        "responses": []
    }

    for batch_idx, batch in enumerate(batches, 1):
        payload = {
            "host": SITE_URL.replace("https://", "").replace("http://", ""),
            "key": INDEXNOW_KEY,
            "keyLocation": f"{SITE_URL}/indexnow-key.txt",
            "urlList": batch
        }

        print(f"\n📤 배치 {batch_idx}/{len(batches)} 통보 중...")
        print(f"   URL 개수: {len(batch)}")

        if dry_run:
            print(f"   [DRY RUN] Bing IndexNow API로 전송")
            results["responses"].append({
                "batch": batch_idx,
                "status": "dry-run",
                "urls": len(batch)
            })
            continue

        try:
            response = requests.post(BING_INDEXNOW_URL, json=payload, timeout=30)
            response.raise_for_status()
            print(f"   ✅ Bing IndexNow: {response.status_code}")

            results["responses"].append({
                "batch": batch_idx,
                "bing_status": response.status_code,
                "urls": len(batch)
            })

        except requests.exceptions.RequestException as e:
            print(f"   ⚠️  Bing IndexNow 오류: {e}", file=sys.stderr)
            results["success"] = False
            results["responses"].append({
                "batch": batch_idx,
                "error": str(e),
                "urls": len(batch)
            })

    return results

def main():
    parser = argparse.ArgumentParser(
        description="IndexNow를 통해 사이트의 모든 URL을 Bing, Naver에 통보"
    )
    parser.add_argument("--urls", action="store_true", help="URL 리스트만 출력")
    parser.add_argument("--dry-run", action="store_true", help="실행 없이 확인")
    parser.add_argument("--sitemap", default="dist/sitemap.xml", help="사이트맵 경로")

    args = parser.parse_args()

    sitemap_path = Path(args.sitemap)
    if not sitemap_path.exists():
        print(f"❌ 사이트맵을 찾을 수 없습니다: {args.sitemap}", file=sys.stderr)
        print("💡 먼저 'npm run build'로 사이트를 빌드하세요.", file=sys.stderr)
        sys.exit(1)

    print(f"📖 사이트맵 로드: {args.sitemap}")
    urls = parse_sitemap(str(sitemap_path))

    if not urls:
        print("❌ 사이트맵에서 URL을 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    print(f"✅ {len(urls)}개 URL 발견")

    if args.urls:
        print("\n📋 URL 목록:")
        for i, url in enumerate(urls, 1):
            print(f"  {i:4d}. {url}")
        return

    print(f"\n🚀 IndexNow 통보 시작...")
    print(f"   사이트: {SITE_URL}")
    print(f"   IndexNow 키: {INDEXNOW_KEY}")

    if args.dry_run:
        print(f"   [DRY RUN 모드] 실제 통보하지 않습니다.")

    result = notify_indexnow(urls, dry_run=args.dry_run)

    print(f"\n{'='*60}")
    if result["success"]:
        print(f"✅ 통보 완료!")
        print(f"   총 {result['total']}개 URL")
        print(f"   {result['batches']}개 배치")
    else:
        print(f"❌ 통보 실패")
        print(f"   상세: {result.get('responses', [])}")

    print(f"{'='*60}")
    print(f"\n⏰ 완료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if args.dry_run:
        print(f"\n💡 실제로 통보하려면 --dry-run 없이 다시 실행하세요:")
        print(f"   python3 tools/indexnow.py")

    sys.exit(0 if result["success"] else 1)

if __name__ == "__main__":
    main()
