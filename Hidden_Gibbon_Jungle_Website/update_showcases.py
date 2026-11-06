#!/usr/bin/env python3
"""Refresh YouTube feed and best-effort public Moxfield profile data; stdlib only."""
import json, os, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'showcase-data.json'
CHANNEL='UCAEQfI7q8gRJjiLo2fE-G3Q'
PROFILE='TheHiddenGibbon'
UA={'User-Agent':'Mozilla/5.0 (compatible; HiddenGibbonWebsite/1.0; public metadata refresh)','Accept':'application/json,text/html,application/xml;q=0.9,*/*;q=0.8'}
def get(url):
 req=urllib.request.Request(url,headers=UA)
 with urllib.request.urlopen(req,timeout=20) as resp:return resp.read().decode('utf-8')
def load():
 try:return json.loads(OUT.read_text('utf-8'))
 except Exception:return {'videos':[],'decks':[]}
data=load(); updates=[]
try:
 xml=get('https://www.youtube.com/feeds/videos.xml?channel_id='+CHANNEL)
 root=ET.fromstring(xml); ns={'a':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
 videos=[]
 for entry in root.findall('a:entry',ns):
  vid=entry.findtext('yt:videoId',default='',namespaces=ns)
  if not re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):continue
  videos.append({'id':vid,'title':entry.findtext('a:title',default='Hidden Gibbon MTG video',namespaces=ns),'published':entry.findtext('a:published',default='',namespaces=ns),'url':'https://www.youtube.com/watch?v='+vid,'image':'https://i.ytimg.com/vi/'+vid+'/hqdefault.jpg'})
 if videos:data['videos']=videos[:15];updates.append('YouTube: '+str(len(videos)))
 else:print('YouTube feed returned no entries; trying fallback')
except Exception as exc:print('YouTube RSS refresh failed:',exc)
# Fallback: use the public channel uploads page if RSS is blocked or channel ID changes.
if not data.get('videos') or 'YouTube:' not in ' '.join(updates):
 try:
  import subprocess
  result=subprocess.run(['yt-dlp','--flat-playlist','--playlist-end','15','--dump-single-json','--no-warnings','https://www.youtube.com/@hiddengibbonmtg/videos'],capture_output=True,text=True,timeout=100,check=True)
  payload=json.loads(result.stdout)
  entries=payload.get('entries') or []
  videos=[]
  for entry in entries:
   vid=entry.get('id','')
   if not re.fullmatch(r'[A-Za-z0-9_-]{11}',vid):continue
   videos.append({'id':vid,'title':entry.get('title') or 'Hidden Gibbon MTG video','published':'','url':'https://www.youtube.com/watch?v='+vid,'image':'https://i.ytimg.com/vi/'+vid+'/hqdefault.jpg'})
  if videos:data['videos']=videos[:15];updates.append('YouTube fallback: '+str(len(videos)))
 except Exception as exc:print('YouTube fallback unavailable:',exc)
# Moxfield has no guaranteed stable public profile feed. This is best effort,
# and NEVER erases previous decks if its public interface changes or blocks us.
try:
 url='https://api2.moxfield.com/v2/users/'+urllib.parse.quote(PROFILE)+'/decks?pageNumber=1&pageSize=30'
 payload=json.loads(get(url))
 entries=payload.get('data',payload.get('decks',[])) if isinstance(payload,dict) else payload
 decks=[]
 if isinstance(entries,list):
  for d in entries:
   if not isinstance(d,dict):continue
   did=d.get('publicId') or d.get('public_id')
   title=d.get('name') or d.get('title')
   if not isinstance(did,str) or not re.fullmatch(r'[\w-]{5,100}',did) or not isinstance(title,str):continue
   # Only public Commander decks, where format is provided.
   fmt=str(d.get('format') or d.get('formatName') or '').lower()
   if fmt and fmt not in ('commander','edh'):continue
   commander=d.get('commanders') or d.get('commander')
   art=None
   if isinstance(commander,dict):
    for v in commander.values():
     if isinstance(v,dict):
      card=v.get('card',v); art=(card.get('image_uris') or {}).get('normal') if isinstance(card,dict) else None
      if art:break
   decks.append({'title':title[:160],'url':'https://www.moxfield.com/decks/'+did,'image':art if isinstance(art,str) and art.startswith('https://cards.scryfall.io/') else None,'description':'Public Commander deck on Moxfield'})
 if decks:data['decks']=decks[:24];updates.append('Moxfield: '+str(len(decks)))
 else:print('No compatible Moxfield deck data returned; retaining previous entries')
except Exception as exc:print('Moxfield public lookup unavailable; retaining previous entries:',exc)
if updates:
 data['updated_at']=datetime.now(timezone.utc).isoformat()
 OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n','utf-8')
print('Updated:',', '.join(updates) if updates else 'metadata timestamp only; existing data retained')
