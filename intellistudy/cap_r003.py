import asyncio, time, json
from playwright.async_api import async_playwright
NOTES=("Photosynthesis happens in the chloroplasts of plant cells. Chlorophyll absorbs light energy, which is used to convert carbon dioxide and water into glucose and oxygen. "
"The word equation is: carbon dioxide + water -> glucose + oxygen, using light energy. "
"The rate of photosynthesis can be limited by light intensity, carbon dioxide concentration and temperature.")
frames=[]
async def shot(pg,dur,tag=''):
    n=len(frames); f=f'cap/f{n:04d}.png'; await pg.screenshot(path=f); frames.append([f,dur,tag])
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={'width':390,'height':760},device_scale_factor=3)
        await pg.goto('https://intelli-study.com',wait_until='networkidle',timeout=60000)
        ta=pg.locator('textarea').first
        await ta.scroll_into_view_if_needed()
        await pg.evaluate("window.scrollBy(0,-120)")
        await pg.wait_for_timeout(500)
        await shot(pg,0.6,'empty')
        await ta.click()
        # typing in chunks
        words=NOTES.split(' '); step=3
        for i in range(step,len(words)+step,step):
            await ta.fill(' '.join(words[:i])); await shot(pg,0.12,'type')
        await shot(pg,0.5,'typed')
        btn=pg.get_by_text('Make my flashcards').first
        await btn.hover(); await shot(pg,0.3,'hover')
        t0=time.time(); await btn.click()
        while True:
            await shot(pg,0.25,'wait')
            body=await pg.inner_text('body')
            if 'CARD 1' in body or 'Card 1' in body: break
            if time.time()-t0>40: break
        gen=time.time()-t0
        await pg.wait_for_timeout(400); await shot(pg,0.6,'cards')
        for k in range(36):
            await pg.evaluate("window.scrollBy(0,14)"); await shot(pg,0.07,'scroll')
        await shot(pg,1.8,'read')
        for k in range(30):
            await pg.evaluate("window.scrollBy(0,14)"); await shot(pg,0.07,'scroll2')
        await shot(pg,2.0,'read2')
        txt=await pg.inner_text('body'); i=txt.find('CARD 1')
        json.dump({'frames':frames,'gen_seconds':gen,'cards':txt[i:i+900]},open('cap.json','w'),indent=1)
        print('gen',gen); print(txt[i:i+900])
        await b.close()
asyncio.run(main())
