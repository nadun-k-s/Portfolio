"""Regenerate responsive assets using installed libwebp tools; originals are preserved."""
from pathlib import Path
import subprocess, json, concurrent.futures
ROOT=Path(__file__).resolve().parent.parent

def run(args):subprocess.run(args,cwd=ROOT,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def generate(job):
 source,target,width,lossless=job
 opts=['-lossless','-exact'] if lossless else ['-q','92','-sharp_yuv','-alpha_q','100']
 run(['cwebp',*opts,'-m','6','-resize',str(width),'0',source,'-o',target])
 return {'source':source,'output':target,'width':width,'bytes':(ROOT/target).stat().st_size,'encoding':'lossless' if lossless else 'WebP quality 92; lossless alpha'}

if __name__=='__main__':
 (ROOT/'img/responsive').mkdir(exist_ok=True)
 sources=[*sorted(ROOT.glob('img/*.webp')),*sorted(ROOT.glob('logos/*.webp'))]
 before=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size} for p in [*sorted(ROOT.glob('img/*.*')),*sorted(ROOT.glob('logos/*.*'))] if p.suffix in ('.png','.webp','.jpg')]
 jobs=[]
 for p in sources:
  src=str(p.relative_to(ROOT));hero=p.stem=='nadun-kaushalya';logo=p.parent.name=='logos'
  widths=[96] if logo else [480,800,1199] if hero else [480,800,1200]
  for w in widths:jobs.append((src,f'img/responsive/{p.stem}-{w}.webp',w,logo))
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:assets=list(pool.map(generate,jobs))
 report={'original_assets':before,'generated_assets':assets}
 report_path=ROOT/'image-optimization.json'
 if report_path.exists():report['original_assets']=json.loads(report_path.read_text())['original_assets']
 report_path.write_text(json.dumps(report,indent=2)+'\n')
 for row in assets:print(row['output'],row['bytes'])
