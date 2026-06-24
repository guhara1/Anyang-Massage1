import rss from '@astrojs/rss';
import { SITE } from '../lib/site';
import { anyangDongs } from '../lib/data';

export async function GET(context: any) {
  const dongs = anyangDongs();

  const rssItems = dongs.map(dong => ({
    title: `${dong.name} 출장마사지·홈타이 예약 안내`,
    description: dong.metaDescription || dong.blurb,
    link: `/gyeonggi/anyang/${dong.gu}/${dong.slug}/`,
    pubDate: new Date('2026-06-24'),
  }));

  rssItems.unshift({
    title: '안양 출장마사지·홈타이 지역별 예약 안내',
    description: '안양 만안구·동안구 전역 출장마사지·홈타이 지역별 생활권 예약 안내',
    link: '/gyeonggi/anyang/',
    pubDate: new Date('2026-06-24'),
  });

  return rss({
    title: '안양 출장마사지·홈타이 | 바로 GO',
    description: '안양 만안구·동안구 전역 출장마사지·홈타이 지역별 생활권 예약 안내',
    site: SITE.url,
    items: rssItems,
    customData: `<language>ko-kr</language>`,
  });
}
