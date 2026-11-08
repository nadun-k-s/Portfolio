"""Regenerate responsive assets using installed libwebp tools; originals are preserved."""
from pathlib import Path
import subprocess, json, concurrent.futures
ROOT=Path(__file__).resolve().parent.parent

def run(args):subprocess.run(args,cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def generate(job):
 source,target,width,lossless=job
 hero=Path(target).name.startswith('nadun-kaushalya-')
 quality=94 if hero else 92
 opts=['-lossless','-exact'] if lossless else ['-q',str(quality),'-sharp_yuv','-alpha_q','100']
 run(['cwebp',*opts,'-m','6','-resize',str(width),'0',source,'-o',target])
 return {'source':source,'output':target,'width':width,'bytes':(ROOT/target).stat().st_size,'encoding':'lossless' if lossless else f'WebP quality {quality}; lossless alpha'}

if __name__=='__main__':
 (ROOT/'img/responsive').mkdir(exist_ok=True)
 (ROOT/'img/masters').mkdir(exist_ok=True)
 # Faithful resampling, not AI detail recovery; never overwrite the original.
 master='img/masters/nadun-kaushalya-master.webp'
 run(['cwebp','-lossless','-exact','-m','6','-resize','2398','2624','img/nadun-kaushalya.webp','-o',master])
 sources=[*sorted(ROOT.glob('img/*.webp')),*sorted(ROOT.glob('logos/*.webp'))]
 before=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size} for p in [*sorted(ROOT.glob('img/*.*')),*sorted(ROOT.glob('logos/*.*'))] if p.suffix in ('.png','.webp','.jpg')]
 jobs=[]
 for p in sources:
  src=str(p.relative_to(ROOT));hero=p.stem=='nadun-kaushalya';logo=p.parent.name=='logos'
  widths=[96] if logo else [480,640,800,1000,1440,1800,2200] if hero else [480,800,1200]
  # Avoid a redundant upscale/downscale for variants below original resolution.
  for w in widths:jobs.append((master if hero and w>1199 else src,f'img/responsive/{p.stem}-{w}.webp',w,logo))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(generate,jobs))
 report={'original_assets':before,'generated_assets':assets,'portrait_master':{'path':master,'width':2398,'height':2624,'bytes':(ROOT/master).stat().st_size,'source':'img/nadun-kaushalya.webp','method':'2x faithful resampling; lossless RGBA; no recovered detail'}}
 report_path=ROOT/'image-optimization.json'
 if report_path.exists():report['original_assets']=json.loads(report_path.read_text())['original_assets']
 report_path.write_text(json.dumps(report,indent=2)+'\n')
 for row in assets:print(row['output'],row['bytes'])
