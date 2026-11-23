// node render.js <fontsDir> <outDir> — покадровый рендер motion.html (30 fps, 38 c)
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
const [fontsDir,out]=process.argv.slice(2);const FPS=30,DUR=38;
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
if(fontsDir)await p.route('**/font/*.woff2',r=>r.fulfill({body:fs.readFileSync(path.join(fontsDir,r.request().url().split('/').pop())),contentType:'font/woff2'}));
await p.goto('file://'+path.resolve(__dirname,'motion.html'));await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>document.getAnimations().forEach(a=>a.pause()));
const el=await p.$('#v');
for(let f=0;f<FPS*DUR;f++){const t=f*1000/FPS;await p.evaluate(t=>document.getAnimations().forEach(a=>a.currentTime=t),t);
await el.screenshot({path:path.join(out,String(f).padStart(5,'0')+'.jpg'),type:'jpeg',quality:92});}
await b.close()})();
