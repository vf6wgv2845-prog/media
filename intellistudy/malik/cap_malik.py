"""Kai Day 1: real Playwright capture of intelli-study.com's no-account demo, 1080x1920 (360x640 @3x), IGCSE Chemistry ionic bonding notes."""
import asyncio, time, json, os
from playwright.async_api import async_playwright
NOTES=("In a chemical reaction, atoms are not created or destroyed, so a balanced equation has the same number of each type of atom on both sides. "
"You balance an equation by changing the coefficients in front of the formulas, never the subscripts. "
"For example, hydrogen and oxygen make water: 2H2 + O2 -> 2H2O. That gives four hydrogen atoms and two oxygen atoms on each side.")
os.makedirs('cap',exist_ok=True); frames=[]
async def shot(pg,dur,tag=''):
    f=f'cap/f{len(frames):04d}.png'; await pg.screenshot(path=f); frames.append([f,dur,tag])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':360,'height':640},device_scale_factor=3)
        await pg.goto('https://intelli-study.com',wait_until='networkidle',timeout=60000)
        ta=pg.locator('textarea').first
        await ta.scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-100)"); await pg.wait_for_timeout(500)
        await ta.click(); await ta.fill(NOTES); await pg.wait_for_timeout(300); await shot(pg,0.5,'typed')
        btn=pg.get_by_text('Make my flashcards').first
        await btn.scroll_into_view_if_needed(); await shot(pg,0.3,'btn')
        t0=time.time(); await btn.click()
        while True:
            await shot(pg,0.2,'wait'); body=await pg.inner_text('body')
            if 'CARD 1' in body or 'Card 1' in body: break
            if time.time()-t0>45: break
        gen=time.time()-t0
        await pg.wait_for_timeout(400)
        loc=pg.get_by_text('CARD 1').first
        try: await loc.scroll_into_view_if_needed(); await pg.evaluate("window.scrollBy(0,-60)")
        except Exception as e: print('scroll',e)
        await pg.wait_for_timeout(300); await shot(pg,0.6,'cards')
        for k in range(40):
            await pg.evaluate("window.scrollBy(0,12)"); await shot(pg,0.06,'scroll')
        await shot(pg,1.5,'read')
        txt=await pg.inner_text('body'); i=txt.find('CARD 1')
        json.dump({'frames':frames,'gen_seconds':gen,'cards':txt[i:i+1200]},open('cap.json','w'),indent=1)
        print('gen',round(gen,2)); print(txt[i:i+1200]); await b.close()
asyncio.run(main())
