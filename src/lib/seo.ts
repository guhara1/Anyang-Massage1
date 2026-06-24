import { SITE } from "./site";

/** 80자 이내로 메타 디스크립션을 자른다 (단어 잘림 최소화) */
export function clampDescription(text: string, max = 80): string {
  const t = text.replace(/\s+/g, " ").trim();
  if (t.length <= max) return t;
  return t.slice(0, max - 1).trimEnd() + "…";
}

export function absoluteUrl(path: string): string {
  const base = SITE.url.replace(/\/$/, "");
  if (!path.startsWith("/")) path = "/" + path;
  return base + path;
}

interface Crumb {
  name: string;
  path: string;
}

/** BreadcrumbList JSON-LD */
export function breadcrumbSchema(crumbs: Crumb[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: crumbs.map((c, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: c.name,
      item: absoluteUrl(c.path),
    })),
  };
}

/** 사이트 전역 Organization 스키마 (방문형 서비스용 LocalBusiness 대체) */
export function organizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    "@id": absoluteUrl("/#organization"),
    name: SITE.name,
    alternateName: SITE.brandEn,
    url: SITE.url,
    image: absoluteUrl(SITE.ogImage),
    telephone: SITE.phone,
    description: clampDescription(SITE.tagline),
    areaServed: { "@type": "City", name: "안양시" },
    contactPoint: {
      "@type": "ContactPoint",
      telephone: SITE.phone,
      contactType: "reservations",
      areaServed: "KR",
      availableLanguage: ["Korean"],
    },
  };
}

/** WebSite 스키마 (사이트명 + 검색) */
export function websiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": absoluteUrl("/#website"),
    url: SITE.url,
    name: SITE.name,
    description: clampDescription(SITE.tagline),
    inLanguage: "ko-KR",
    publisher: { "@id": absoluteUrl("/#organization") },
    areaServed: { "@type": "City", name: "안양시" },
  };
}

interface FaqItem {
  q: string;
  a: string;
}

/** FAQPage 스키마 */
export function faqSchema(items: FaqItem[]) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    mainEntity: items.map((it) => ({
      "@type": "Question",
      name: it.q,
      acceptedAnswer: { "@type": "Answer", text: it.a },
    })),
  };
}

/** 서비스 지역 안내 페이지용 Service 스키마 */
export function serviceAreaSchema(areaName: string, path: string) {
  return {
    "@context": "https://schema.org",
    "@type": "Service",
    serviceType: "출장마사지·홈타이 방문 관리 안내",
    provider: { "@id": absoluteUrl("/#organization") },
    areaServed: { "@type": "Place", name: areaName },
    url: absoluteUrl(path),
  };
}

/** 이미지 객체 스키마 (OG 이미지용) */
export function imageObjectSchema(
  imageUrl: string,
  width = 1200,
  height = 630
) {
  return {
    "@context": "https://schema.org",
    "@type": "ImageObject",
    url: imageUrl,
    width: width,
    height: height,
  };
}

/** 웹페이지 스키마 (상세 페이지용) */
export function webPageSchema(
  title: string,
  description: string,
  path: string,
  imageUrl?: string
) {
  return {
    "@context": "https://schema.org",
    "@type": "WebPage",
    url: absoluteUrl(path),
    name: title,
    description: clampDescription(description),
    inLanguage: "ko-KR",
    datePublished: new Date().toISOString().split("T")[0],
    isPartOf: { "@id": absoluteUrl("/#website") },
    ...(imageUrl && { image: imageObjectSchema(imageUrl) }),
  };
}
