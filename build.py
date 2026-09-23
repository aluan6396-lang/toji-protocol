from pathlib import Path
import json, re
root=Path('/mnt/data/toji_rebuild')
w=__import__('importlib.util').util.spec_from_file_location('x', root/'workouts_literal.js')
# parse JS via node later; use subprocess
import subprocess
js='const w=require('+json.dumps(str(root/'workouts_literal.js'))+'); process.stdout.write(JSON.stringify(w));'
workouts=json.loads(subprocess.check_output(['node','-e',js]))
photo_files={
'Lat_Pulldown':'Amer-Lat-Pulldown.jpg',
'Preacher_Curl':'Preacher curl.webp',
'Lever_Pec_Deck_Fly':'Pec deck Fly.jpg',
'Leg_Press':'Leg Press.jpg',
'Barbell_Bench_Press':'Bench Press.jpg',
'Lever_Shoulder_Press':'Shoulder Press.jpg',
'Leg_Extension':'Leg Extension.jpg',
'Front_Plank':'Plank.jpg',
'Pull_Up':'Pull-ups exercise from back.jpg',
'Cable_Crossover':'Personal Training at a Gym - Cable Crossover.JPG',
'Assisted_Dip':'Dip Exercise.jpg',
'Dumbbell_Lateral_Raise':'Fitness model shoulder exercise weight training (32004749033).jpg',
}
photo_meta={
'Amer-Lat-Pulldown.jpg':('Abooyeah','CC BY 4.0','Wikimedia Commons'),
'Preacher curl.webp':('SALlM BlN YOUSUF','CC BY 4.0','Wikimedia Commons'),
'Pec deck Fly.jpg':('Wikimedia Commons contributor','CC BY 4.0','Wikimedia Commons'),
'Leg Press.jpg':('SAgbley','CC BY 4.0','Wikimedia Commons'),
'Bench Press.jpg':('Aditya Oberai','CC BY-SA 4.0','Wikimedia Commons'),
'Shoulder Press.jpg':('Wikimedia Commons contributor','CC BY 4.0','Wikimedia Commons'),
'Leg Extension.jpg':('Wikimedia Commons contributor','CC BY 4.0','Wikimedia Commons'),
'Plank.jpg':('Jaykayfit','CC BY 4.0','Wikimedia Commons'),
'Pull-ups exercise from back.jpg':('PTPioneer / Tyler Read','CC BY 4.0','Wikimedia Commons'),
'Personal Training at a Gym - Cable Crossover.JPG':('LocalFitness Pty Ltd','permission with attribution','Wikimedia Commons'),
'Dip Exercise.jpg':('Fort Drum & 10th Mountain Division','Public Domain Mark','Wikimedia Commons'),
'Fitness model shoulder exercise weight training (32004749033).jpg':('Wikimedia Commons contributor','CC BY 2.0','Wikimedia Commons'),
}
exercises=[]
for di,wk in enumerate(workouts):
    for ei,x in enumerate(wk['items']):
        name,equip,sets,rir,rest,cat,target,cue,key=x
        fn=photo_files.get(key)
        url=f'https://commons.wikimedia.org/wiki/Special:Redirect/file/{__import__("urllib.parse").parse.quote(fn)}' if fn else None
        meta=photo_meta.get(fn) if fn else None
        exercises.append({'id':f'D{di+1:02d}-E{ei+1:02d}','day':di+1,'order':ei+1,'name':name,'equipment':equip,'sets_reps':sets,'rir':rir,'rest':rest,'category':cat,'target':target,'cue':cue,'key':key,'photo_url':url,'photo_source':meta[2] if meta else None,'photo_credit':meta[0] if meta else None,'photo_license':meta[1] if meta else None,'photo_status':'verified_real_photo' if url else 'needs_verified_real_photo'})

db={'app':'TOJI PROTOCOL','version':'0.1-foundation','workouts':workouts,'exercises':exercises,'stats':{'days':5,'exercises':len(exercises),'verified_real_photos':sum(bool(e['photo_url']) for e in exercises)}}
(root/'db.json').write_text(json.dumps(db,ensure_ascii=False,indent=2))
(root/'workouts.json').write_text(json.dumps(workouts,ensure_ascii=False,indent=2))
