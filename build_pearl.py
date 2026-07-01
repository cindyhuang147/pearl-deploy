# -*- coding: utf-8 -*-
"""珍珠日記 App v3：可愛動態貓 + 理智統計排程 + 統計作答對照評分 + 錯題本 + 考前倒數 + 獎勵養成。"""
import json, io
RM = json.load(open('_rm_data.json', encoding='utf-8'))
STAT = json.load(open('_stat_data.json', encoding='utf-8'))
STATFULL = json.load(open('_stat_full.json', encoding='utf-8'))
OUT = r"C:\Users\Cindy\Downloads\Cindy's Agent\珍珠日記.html"

T = r'''<!DOCTYPE html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>珍珠日記</title>
<style>
 :root{--bg:#FAF6EF;--surface:#FFFFFF;--surface2:#F2ECE1;--ink:#3E3A34;--muted:#7A7264;--hint:#A89E8C;--line:#E2D9CA;
   --sage:#5B6C5D;--clay:#B07A5A;--olive:#6B7257;--gold:#A07D4B;--teal:#1D9E75;--purple:#7F77DD;--ok:#1D9E75;--no:#C0503A;--pink:#D88C9A;}
 @media (prefers-color-scheme:dark){:root{--bg:#23211D;--surface:#2C2A25;--surface2:#332F28;--ink:#EDE7DA;--muted:#B5AC9C;
   --hint:#8A8170;--line:#3D392F;--sage:#8FA38F;--clay:#D29B7B;--olive:#9DAA86;--gold:#C9A66B;--teal:#3CB98C;--ok:#3CB98C;--no:#D9745C;--pink:#E0A6B2;}}
 *{box-sizing:border-box;-webkit-tap-highlight-color:transparent;}
 body{margin:0;background:var(--bg);color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Microsoft JhengHei","PingFang TC","Noto Sans TC",sans-serif;line-height:1.7;font-size:16px;}
 .wrap{max-width:720px;margin:0 auto;padding:16px 16px 70px;}
 .card{background:var(--surface);border:.5px solid var(--line);border-radius:14px;padding:16px;margin-bottom:13px;}
 .soft{background:var(--surface2);border-radius:12px;padding:12px 14px;}
 h1{font-size:22px;font-weight:600;margin:0;} h2{font-size:16px;font-weight:600;margin:0 0 8px;}
 .sub{font-size:13px;color:var(--muted);} .mini{font-size:12px;color:var(--hint);}
 .row{display:flex;gap:10px;flex-wrap:wrap;}
 button{font-family:inherit;font-size:15px;border-radius:10px;border:.5px solid var(--line);background:var(--surface);color:var(--ink);padding:10px 14px;cursor:pointer;min-height:44px;}
 button:active{transform:scale(.98);} .primary{background:var(--sage);color:#FAF6EF;border-color:var(--sage);}
 textarea,input{font-family:inherit;font-size:15px;width:100%;border:.5px solid var(--line);border-radius:10px;padding:10px;background:var(--surface);color:var(--ink);resize:vertical;}
 .metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(72px,1fr));gap:8px;}
 .metric{background:var(--surface2);border-radius:10px;padding:8px 4px;text-align:center;}
 .metric .v{font-size:20px;font-weight:600;} .metric .l{font-size:11px;color:var(--muted);}
 .entry{border-left:3px solid var(--teal);background:var(--surface);border:.5px solid var(--line);border-radius:10px;padding:9px 12px;margin-bottom:8px;}
 .entry .t{font-size:12px;color:var(--hint);} .entry .b{font-size:14.5px;margin-top:2px;}
 .pin{border-left-color:var(--gold);background:var(--surface2);}
 .wk{cursor:pointer;display:flex;justify-content:space-between;align-items:center;padding:9px 11px;background:var(--surface2);border-radius:10px;}
 .day{display:flex;gap:9px;align-items:flex-start;padding:8px 9px;border:.5px solid var(--line);border-radius:9px;margin-top:6px;cursor:pointer;}
 .chk{flex:0 0 auto;width:19px;height:19px;border-radius:50%;border:1.5px solid var(--line);margin-top:2px;display:flex;align-items:center;justify-content:center;font-size:12px;color:#fff;}
 .chk.on{background:var(--teal);border-color:var(--teal);}
 a.copy{font-size:12px;color:var(--muted);text-decoration:none;cursor:pointer;}
 .opt{display:block;width:100%;text-align:left;margin:7px 0;padding:11px 13px;white-space:normal;line-height:1.5;}
 .opt.ok{background:#E1F5EE;border-color:var(--ok);color:#0F6E56;} .opt.no{background:#FAE7E1;border-color:var(--no);color:#8a3a26;} .opt.selp{background:var(--surface2);border-color:var(--muted);}
 @media (prefers-color-scheme:dark){.opt.ok{background:#163a30;color:#7fe0bf;}.opt.no{background:#3a201a;color:#f0a78f;}}
 .pill{font-size:12px;padding:3px 9px;border-radius:8px;background:var(--surface2);color:var(--muted);}
 .ttl{cursor:pointer;padding:10px 12px;border:.5px solid var(--line);border-radius:10px;margin-bottom:7px;display:flex;justify-content:space-between;gap:8px;align-items:center;}
 .count{background:var(--surface2);border-radius:14px;padding:12px 14px;text-align:center;margin-bottom:13px;}
 .count .big{font-size:30px;font-weight:600;color:var(--clay);line-height:1.1;}
 .catwrap{text-align:center;}
 .cat{display:inline-block;animation:bob 3.4s ease-in-out infinite;transform-origin:center bottom;cursor:pointer;}
 .cat.wig{animation:wig .55s ease;}
 @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-7px)}}
 @keyframes wig{0%,100%{transform:rotate(0)}25%{transform:rotate(-7deg)}75%{transform:rotate(7deg)}}
 @keyframes blink{0%,93%,100%{transform:scaleY(1)}96%{transform:scaleY(.08)}}
 @keyframes tail{0%,100%{transform:rotate(-4deg)}50%{transform:rotate(10deg)}}
 @keyframes tailf{0%,100%{transform:rotate(-10deg)}50%{transform:rotate(14deg)}}
 @keyframes fly{0%{opacity:0;transform:translateY(6px) scale(.6)}25%{opacity:1}100%{opacity:0;transform:translateY(-46px) scale(1.1)}}
 .eyes{transform-origin:center;animation:blink 5s infinite;}
 .tl{transform-origin:24px 120px;animation:tail 2.6s ease-in-out infinite;}
 .tlf{transform-origin:24px 120px;animation:tailf 1s ease-in-out infinite;}
 .hrt{animation:fly 2.6s ease-in infinite;}
 .lvbar{height:8px;background:var(--surface2);border-radius:6px;overflow:hidden;}
 .lvfill{height:100%;background:var(--gold);}
 .bdg{display:inline-flex;align-items:center;gap:4px;font-size:12px;padding:4px 9px;border-radius:9px;border:.5px solid var(--line);}
 .bdg.on{background:#FAEEDA;color:#854F0B;border-color:#E9CB8E;} .bdg.off{opacity:.45;}
</style></head><body><div class="wrap" id="app"></div>
<script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-app-compat.js"></script><script src="https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore-compat.js"></script><script>try{firebase.initializeApp({apiKey:"AIzaSyD6Wly2tuEkRSwlM-gf-7GpV_AV8GeMJ5c",authDomain:"pearl-diary-shihan.firebaseapp.com",projectId:"pearl-diary-shihan",storageBucket:"pearl-diary-shihan.firebasestorage.app",messagingSenderId:"239508958239",appId:"1:239508958239:web:c8e2a2b1a4958c8d69b92a"});window._db=firebase.firestore();}catch(e){window._db=null;}</script>
<script>window.RM=__RM__;window.STAT=__STAT__;window.STATFULL=__STATFULL__;</script>
<script>
(function(){
 var SHARE=__SHARE__;var SEEDLOCAL=__SEEDLOCAL__;var DEFAULT_ANCHOR='詩涵，不要給自己那麼大的壓力。我們都在旁邊支持你，不用擔心，你已經很棒了。老師以你為榮！';
 var KEY=(SHARE?'pearl_share_v1':'pearl_v3'),WD=['日','一','二','三','四','五','六'];
 function p2(n){return(n<10?'0':'')+n;} function ymd(d){return d.getFullYear()+'-'+p2(d.getMonth()+1)+'-'+p2(d.getDate());}
 function stamp(d){return d.getFullYear()+'/'+p2(d.getMonth()+1)+'/'+p2(d.getDate())+'（'+WD[d.getDay()]+'）'+p2(d.getHours())+':'+p2(d.getMinutes());}
 function md(d){return(d.getMonth()+1)+'/'+d.getDate();}
 function addD(d,n){var x=new Date(d.getFullYear(),d.getMonth(),d.getDate());x.setDate(x.getDate()+n);return x;}
 function diff(a,b){return Math.round((new Date(b.getFullYear(),b.getMonth(),b.getDate())-new Date(a.getFullYear(),a.getMonth(),a.getDate()))/864e5);}
 function same(a,b){return ymd(a)===ymd(b);} function esc(s){return(s+'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
 function pick(a,k){return a[((k%a.length)+a.length)%a.length];}
 function yname(s){s=(''+s).slice(0,4);return s.slice(0,3)+'學年第'+s.slice(3)+'學期';}
 function statByYear(){var m={},o=[];['high','mid','low'].forEach(function(g){STAT[g].forEach(function(tp,ti){var key=g+ti;tp.years.forEach(function(y){var sem=(''+y[0]).slice(0,4);if(!(sem in m)){m[sem]=[];o.push(sem);}m[sem].push({qno:y[1],desc:y[2],key:key,title:tp.title});});});});o.sort();return {m:m,o:o};}

 var SEED_PIN=[{b:'我「沒想過」，卻讀到了博士班。'},{b:'我「沒想過」，卻考進了博士班。'},{b:'我「沒想過」，卻留下來了。'}];
 var SEED=[{date:'2026-06-19',t:'2026/06/19（五）12:45',b:'我想到一個很棒的日記 app 點子（後來命名為「珍珠日記」）；並且透過對話，看見了真實的自己。'},
   {date:'2026-06-19',t:'2026/06/19（五）13:00',b:'我替這本日記取了名字「珍珠日記」；並且第一次主動對自己說：我想學著被稱讚。'},
   {date:'2026-06-19',t:'2026/06/19（五）18:28',b:'珍珠陪我看清「我是什麼樣的人」——一個被自己低估、卻又柔軟又有力量的人。這次我沒有反駁。'}];
 if(!SEEDLOCAL){SEED=[];SEED_PIN=[];}
 // 排程：[科,標題,連結]　連結 stat:high0 / rm:1 / rm:wrong / ''
 var CUR=[
  // 階段一：三階段打底（每筆深連結到該題型，點了直接從 ①前測 開始）
  ['統計','三階段 ① 因素分析','plan:stat:high0'],['研方','三階段 ① 因素分析類','plan:rm:因素分析'],
  ['統計','三階段 ② Multivariate Paired 多變量配對','plan:stat:high1'],['統計','三階段 ③ GLT 一般線性檢定','plan:stat:high2'],
  ['研方','三階段 ② 抽樣','plan:rm:抽樣'],['統計','三階段 ④ 後驗機率 分類','plan:stat:high4'],
  ['統計','三階段 ⑤ Partial R² 偏判定係數','plan:stat:high11'],['研方','三階段 ③ 信度','plan:rm:信度'],
  ['複習','默寫 因素/Paired/GLT/後驗/Partial R²',''],
  ['統計','三階段 ⑥ ANCOVA','plan:stat:high3'],['統計','三階段 ⑦ Logistic 歸類','plan:stat:high5'],
  ['研方','三階段 ④ 效度','plan:rm:效度'],['統計','三階段 ⑧ AR(1) 自我迴歸','plan:stat:high9'],
  ['統計','三階段 ⑨ Durbin-Watson','plan:stat:high10'],['研方','三階段 ⑤ 實驗設計','plan:rm:實驗設計'],
  ['統計','三階段 ⑩ 聯立/T²/Wilks','plan:stat:high6'],['統計','三階段 ⑪ MANOVA/Profile','plan:stat:high7'],
  ['統計','三階段 ⑫ Canonical 正準相關','plan:stat:high8'],['研方','三階段 ⑥ 研究哲學','plan:rm:研究哲學'],
  ['複習','默寫 ANCOVA/Logistic/AR(1)/T²/MANOVA/Canonical',''],
  ['研方','三階段 ⑦ 問卷與調查','plan:rm:問卷與調查'],['研方','三階段 ⑧ 質性研究','plan:rm:質性研究'],
  ['研方','三階段 ⑨ 理論與假設','plan:rm:理論與假設'],['研方','三階段 ⑩ 統計與測量','plan:rm:統計與測量'],
  ['研方','三階段 ⑪ 研究流程與倫理','plan:rm:研究流程與倫理'],['複習','默寫 研方 11 類核心重點',''],['彈性','彈性日 · 補進度或休息（沒做也沒關係）',''],
  // 階段二：進一步練習
  ['統計','中頻：迴歸假設/BLUE＋其他迴歸','stat:mid0'],['統計','中頻：DA前置＋變異數同質','stat:mid2'],
  ['統計','中頻：Odds＋Repeated','stat:mid4'],['統計','低頻群組A：完整一輪','stat:low0'],
  ['統計','低頻群組B：完整一輪','stat:low4'],['統計','CFA／SEM 專題（新範圍）',''],
  ['研方','整年刷題 第1回 1051-1062','rm:1'],['研方','整年刷題 第2回 1071-1102','rm:2'],
  ['研方','整年刷題 第3回 1112-1141','rm:3'],['研方','清研方錯題本','rm:wrong'],
  ['複習','默寫 12 高頻核心公式',''],['彈性','彈性日 · 補進度或休息（沒做也沒關係）',''],
  ['模擬','統計 自測歷屆整卷（計時）',''],['模擬','統計 該年訂正＋錯題回讀',''],
  ['模擬','研方 練習版 計時重寫','rm:1'],['模擬','研方 訂正＋錯題本','rm:wrong'],
  ['模擬','衝刺模擬考（研方＋統計，看預估）',''],['彈性','彈性日 · 補進度或休息（沒做也沒關係）',''],
  ['統計','弱點題型加強（看錯題本／今日複習）',''],['研方','研方錯題本最終清零','rm:wrong'],
  ['綜合','暑假總驗收','']
 ];
 var FLEX=['彈性','彈性複習 / 補進度（或休息）',''];
 var SCOL={'統計':'#1D9E75','研方':'#7F77DD','複習':'#BA7517','模擬':'#D85A30','綜合':'#5F5E5A','彈性':'#888780'};
 var START=new Date(2026,5,20),SEND=new Date(2026,7,31),EXAM=new Date(2026,10,20);
 var days=[],ix=0;
 for(var dd=new Date(START);dd<=SEND;dd=addD(dd,1)){if(dd.getDay()===0)continue;var u=ix<CUR.length?CUR[ix]:FLEX;days.push({i:ix,date:new Date(dd),id:ymd(dd),subj:u[0],title:u[1],link:u[2],est:(dd.getDay()===6?2:3),week:Math.floor(ix/6)});ix++;}
 var nW=days.length?days[days.length-1].week+1:0;

 var st={entries:[],done:{},open:{},filter:{},statOpen:{},statAns:{},wrongRM:[],wrongStat:[],points:0,aff:0,view:'home',sess:null,awd:{},mem:{},yearDesc:false,statSess:null,mock:null,mockSel:{rmN:40,nN:8,qN:6},handMode:false,syncCode:'',_ts:0,phase:{},planStat:null,planMode:'rm',planTip:null,planSol:false,planFocus:null,planAll:false,pins:[],anchor:'',papers:[],curPaper:null,gkey:'',rem:{on:false,am:'08:00',pm:'21:00',fired:{},day:'',seq:0,_help:false}};
 try{var s=JSON.parse(localStorage.getItem(KEY));if(s)for(var k in s)st[k]=s[k];}catch(e){}
 if(SEEDLOCAL){if(!st.entries||!st.entries.length)st.entries=SEED.slice();if(!st.pins||!st.pins.length)st.pins=SEED_PIN.map(function(x){return x.b;});if(!st.anchor)st.anchor=DEFAULT_ANCHOR;}
 function nowMs(){return (new Date()).getTime();}function save(){st._ts=nowMs();try{localStorage.setItem(KEY,JSON.stringify({entries:st.entries,done:st.done,filter:st.filter,statOpen:st.statOpen,statAns:st.statAns,wrongRM:st.wrongRM,wrongStat:st.wrongStat,points:st.points,aff:st.aff,awd:st.awd,mem:st.mem,phase:st.phase,pins:st.pins,anchor:st.anchor,papers:st.papers,gkey:st.gkey,rem:st.rem,syncCode:st.syncCode,_ts:st._ts}));}catch(e){}schedulePush();}function cloudDoc(){return (window._db&&st.syncCode)?window._db.collection('pearl').doc(st.syncCode):null;}var _pt;function schedulePush(){if(!cloudDoc())return;clearTimeout(_pt);_pt=setTimeout(cloudPush,1500);}function cloudPush(){var d=cloudDoc();if(!d)return;try{d.set({data:localStorage.getItem(KEY)||'{}',ts:st._ts||nowMs()}).then(function(){st._syncMsg='已同步雲端';}).catch(function(){st._syncMsg='雲端寫入失敗';});}catch(e){}}function cloudPull(cb){var d=cloudDoc();if(!d){cb&&cb(null);return;}d.get().then(function(snap){cb&&cb(snap.exists?snap.data():null);}).catch(function(){cb&&cb(null);});}function applyCloud(c){try{localStorage.setItem(KEY,c.data);var o=JSON.parse(c.data);for(var k in o)st[k]=o[k];st._ts=o._ts||c.ts||st._ts;if(SEEDLOCAL){if(!st.pins||!st.pins.length)st.pins=SEED_PIN.map(function(x){return x.b;});if(!st.anchor)st.anchor=DEFAULT_ANCHOR;}}catch(e){}}
 function pts(n){st.points=(st.points||0)+n;if(st.points<0)st.points=0;}
 var _pendingPdf=null,_pendingErr='';
 var now=new Date();
 function todayDay(){for(var i=0;i<days.length;i++)if(same(days[i].date,now))return days[i];return null;}
 function todayEntry(){return st.entries.some(function(e){return e.date===ymd(now);});}
 function curWeek(){if(now<START)return 0;if(now>SEND)return nW-1;for(var i=0;i<days.length;i++)if(days[i].date>=now)return days[i].week;return nW-1;}
 function streakE(){var n=0,d=new Date(now);for(var k=0;k<400;k++){var h=st.entries.some(function(e){return e.date===ymd(d);});if(k===0&&!h){d=addD(d,-1);continue;}if(h){n++;d=addD(d,-1);}else break;}return n;}
 var LVT=[0,40,100,180,300,460,660,900,1200];
 function level(){var p=st.points||0,l=0;for(var i=0;i<LVT.length;i++)if(p>=LVT[i])l=i;return l;}
 var INT=[1,2,4,9,19,40];
 function schedRev(key,lvl){var m=st.mem[key]||{box:0};var b=lvl==='熟'?Math.min(5,(m.box||0)+1):(lvl==='不熟'?0:Math.max(0,m.box||0));st.mem[key]={box:b,due:ymd(addD(now,INT[b])),last:ymd(now)};}
 function seedMem(key){if(key&&!st.mem[key])st.mem[key]={box:0,due:ymd(addD(now,2)),last:ymd(now)};}
 function dueList(){var a=[];for(var k in st.mem){if(st.mem[k].due<=ymd(now)){var ft=findKey(k);if(ft)a.push({key:k,m:st.mem[k],ft:ft});}}a.sort(function(x,y){return x.m.due<y.m.due?-1:1;});return a;}
 function lvInfo(){var l=level(),cur=LVT[l],nx=LVT[l+1]||(cur+400);return {l:l+1,cur:cur,nx:nx,pct:Math.min(100,Math.round(((st.points-cur)/(nx-cur))*100))};}
 var ACC=[[3,'🧣 圍巾'],[5,'👑 皇冠'],[7,'🪽 翅膀'],[9,'😇 光環']];
 function accLine(){return ACC.map(function(a){return level()>=a[0]?'<span style="color:var(--gold)">'+a[1]+' ✓</span>':'<span style="opacity:.45">Lv.'+a[0]+' '+a[1]+'</span>';}).join('　');}

 var TEASE=['喵？今天那格還躺著喔——是它先動，還是你先動？','我看到那題了，你也看到了。我們之中有一個在裝睡。','昨天可是把我擼到翻肚的人耶，今天這點事難得倒你？','不催你，只是…那塊空白一直在看你。我先看著。','你不是不會，是不准自己開始。動一下，我就閉嘴。'];
 var WHITE=['（珍珠翻過肚子，蹭了蹭你的手）','（珍珠瞇眼打呼：嚕嚕嚕～）','（珍珠把尾巴捲上你的手腕）'];
 var NEUT=['（珍珠瞇著眼，安靜等你今天的一筆）','（珍珠理了理毛，沒催你，只是在）'];
 var PURR=['嚕嚕嚕～','喵♡','（瞇眼蹭你）','（呼嚕呼嚕）','（用頭頂你的手）'];var DODGE=['喵～休想摸我！','追不到吧～','哼，先去做任務啦！','摸不到～摸不到～','差一點！我比拖延快一步。','（黑珍珠俐落地閃開）','想用摸的收買我？沒門～'];
 var RMTIPS={'研究哲學':'先抓題幹核心詞(positivism/ontology/epistemology/paradigm)回到定義層次；看到「staying positive」一律刪。','抽樣':'先判機率/非機率：分層·群集·系統·簡單隨機=機率，便利·配額·雪球·判斷=非機率；n↑→抽樣誤差↓。','信度':'信度=一致性：test-retest(時間)、Cronbach/split-half(內部)、Kappa(評分者)；不穩定構念不適用重測。','效度':'效度=測到該測的：content(涵蓋面)、criterion(效標)、construct(理論)、ecological≠external。','因素分析':'轉軸改 loading 不改總變異；正交=Varimax、斜交=Oblimin/Promax；EFA 探索、CFA 驗證。','實驗設計':'factorial 條件數=各水準相乘；main effect=單因子、interaction=效果隨另一因子變；隨機分派控干擾變數。','問卷與調查':'辨識題型：contingency(跳答)、probe(追問)、double-barrelled(一題兩問應避免)；pilot 檢驗題目可行性。','質性研究':'grounded theory 由資料浮現理論、理論飽和=無新類別；ethnography 長期參與觀察；focus group 有 moderator 引導。','理論與假設':'好理論可否證(falsifiable)且簡約(parsimony)；concept 自然形成、construct 為研究發明。','統計與測量':'Type I=棄真(無中生有)、Type II=取偽；名目用眾數、序位用中位數；相關≠因果。','研究流程與倫理':'研究流程=問題→文獻→設計→蒐集→分析→詮釋；涉及人類受試→IRB+知情同意。','其他':'回到題幹關鍵詞，先定義核心名詞，再用刪去法排除明顯錯誤選項。'};
 function RMTIP(c){return RMTIPS[c]||RMTIPS['其他'];}
 

 function cat(state){
  var body=state==='black'?'#4B4650':(state==='white'?'#FDFBF7':'#EFE7D8');
  var ln=state==='black'?'#332F39':(state==='white'?'#E6DDD0':'#D8CDB9');
  var pk='#F2B8C6',pkd='#E59AAC';var lv=level();
  var t='<svg viewBox="0 0 200 185" width="180" height="166" role="img" aria-label="珍珠貓">';
  // tail
  t+='<path class="'+(state==='black'?'tlf':'tl')+'" d="M30 122 q-26 -2 -24 -34 q1 -16 14 -16" fill="none" stroke="'+ln+'" stroke-width="13" stroke-linecap="round"/>';
  // body
  t+='<ellipse cx="100" cy="135" rx="56" ry="40" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/>';
  // paws
  if(state==='white'){t+='<ellipse cx="70" cy="104" rx="12" ry="9" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/><ellipse cx="130" cy="104" rx="12" ry="9" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/>';}
  else{t+='<ellipse cx="74" cy="160" rx="14" ry="10" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/><ellipse cx="126" cy="160" rx="14" ry="10" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/>';}
  // head
  t+='<circle cx="100" cy="74" r="50" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/>';
  // ears
  t+='<path d="M60 40 Q52 8 84 30 Q72 34 60 40Z" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/><path d="M140 40 Q148 8 116 30 Q128 34 140 40Z" fill="'+body+'" stroke="'+ln+'" stroke-width="2.5"/>';
  t+='<path d="M64 36 Q60 20 78 30Z" fill="'+pk+'"/><path d="M136 36 Q140 20 122 30Z" fill="'+pk+'"/>';
  // accessories (養成)
  if(lv>=3){t+='<path d="M62 112 q38 18 76 0 l-6 14 q-32 12 -64 0Z" fill="'+pkd+'" stroke="'+ln+'" stroke-width="1.5"/>';}
  if(lv>=5){t+='<path d="M78 30 l8 -16 l8 12 l8 -14 l8 16 Z" fill="#E9C46A" stroke="#C99A2E" stroke-width="1.5"/>';}if(lv>=7){t+='<path d="M46 122 q-26 -6 -20 -30 q16 4 24 26Z" fill="#F4E1C2" stroke="'+ln+'" stroke-width="1.5" opacity=".92"/><path d="M154 122 q26 -6 20 -30 q-16 4 -24 26Z" fill="#F4E1C2" stroke="'+ln+'" stroke-width="1.5" opacity=".92"/>';}if(lv>=9){t+='<ellipse cx="100" cy="13" rx="21" ry="6" fill="none" stroke="#E9C46A" stroke-width="3"/>';}
  // cheeks
  t+='<ellipse cx="64" cy="86" rx="10" ry="6.5" fill="'+pk+'" opacity=".75"/><ellipse cx="136" cy="86" rx="10" ry="6.5" fill="'+pk+'" opacity=".75"/>';
  // eyes
  if(state==='white'){
   t+='<g class="eyes"><path d="M68 74 q12 -12 24 0" stroke="'+ln+'" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M108 74 q12 -12 24 0" stroke="'+ln+'" stroke-width="4" fill="none" stroke-linecap="round"/></g>';
   t+='<path d="M92 86 q8 7 16 0" stroke="'+ln+'" stroke-width="2.6" fill="none" stroke-linecap="round"/>';
  } else if(state==='black'){
   t+='<g class="eyes"><path d="M70 76 q11 -5 22 -1" stroke="#F6EAD2" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M108 76 q11 -5 22 -1" stroke="#F6EAD2" stroke-width="4" fill="none" stroke-linecap="round"/></g>';
   t+='<circle cx="86" cy="79" r="3.6" fill="#F6EAD2"/><circle cx="118" cy="79" r="3.6" fill="#F6EAD2"/>';
   t+='<path d="M66 64 q10 -5 20 -1" stroke="'+ln+'" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
   t+='<path d="M92 92 q8 5 16 0" stroke="#F6EAD2" stroke-width="2.6" fill="none" stroke-linecap="round"/>';
   t+='<text x="150" y="50" font-size="18" fill="'+ln+'">💢</text>';
  } else {
   t+='<g class="eyes"><circle cx="80" cy="78" r="9.5" fill="'+ln+'"/><circle cx="120" cy="78" r="9.5" fill="'+ln+'"/>'+
      '<circle cx="83" cy="74" r="3.4" fill="#fff"/><circle cx="123" cy="74" r="3.4" fill="#fff"/><circle cx="77" cy="81" r="1.6" fill="#fff"/><circle cx="117" cy="81" r="1.6" fill="#fff"/></g>';
   t+='<path d="M94 90 q6 5 12 0" stroke="'+ln+'" stroke-width="2.4" fill="none" stroke-linecap="round"/>';
  }
  // nose
  t+='<path d="M97 84 l6 0 l-3 4 Z" fill="'+pkd+'"/>';
  // whiskers
  t+='<path d="M44 80 h20 M46 88 h18 M156 80 h-20 M154 88 h-18" stroke="'+ln+'" stroke-width="1.3" stroke-linecap="round" opacity=".7"/>';
  if(state==='white'){t+='<text class="hrt" x="150" y="60" font-size="17" fill="'+pkd+'">♥</text><text class="hrt" x="38" y="66" font-size="13" fill="'+pkd+'" style="animation-delay:1.1s">♥</text>';}
  t+='</svg>';
  return t;
 }
 function m(v,l,u){return '<div class="metric"><div class="v">'+v+'</div><div class="l">'+l+(u?' '+u:'')+'</div></div>';}

 function renderHome(){
  var td=todayDay(),hasE=todayEntry();
  var state=(hasE||(td&&st.done[td.id]))?'white':((td&&!st.done[td.id]&&now>=START&&now<=SEND)?'black':'neutral');
  var di=days.findIndex(function(x){return same(x.date,now);});
  var line=state==='black'?pick(TEASE,now.getDate()+(di<0?0:di)):(state==='white'?pick(WHITE,st.entries.length):pick(NEUT,now.getDate()));
  var unitsDone=0;for(var i=0;i<Math.min(CUR.length,days.length);i++)if(st.done[days[i].id])unitsDone++;
  var dExam=diff(now,EXAM),li=lvInfo(),H='';
  H+='<div style="text-align:center;margin-bottom:8px;"><h1>'+(SHARE?'資格考衝刺 · 珍珠':'珍珠日記')+'</h1><div class="sub">'+(SHARE?'研方刷題 · 統計練習 · 模擬考｜養成你的珍珠':'只記你已經做到的事 · 珍珠用動作陪你')+'</div></div>';
  H+='<div class="count"><div class="mini">距 11/20 資格考</div><div class="big">'+(dExam>=0?dExam:0)+' 天</div><div class="mini">約 '+Math.max(0,Math.ceil(dExam/7))+' 週 · 距開學 '+Math.max(0,diff(now,new Date(2026,8,1)))+' 天</div></div>';
  H+='<div class="card catwrap"><div class="cat" id="cat" data-cat="'+state+'">'+cat(state)+'</div>'+
     '<div class="sub" style="margin-top:2px;">'+(state==='black'?'黑珍珠（欠揍模式）':state==='white'?'白珍珠（撒嬌模式）':'珍珠 Lv.'+li.l)+'　<span id="purr" style="color:var(--pink);"></span></div>'+
     '<div style="font-size:14px;margin-top:4px;">'+line+'</div>'+
     '<div style="margin-top:10px;text-align:left;"><div class="mini" style="display:flex;justify-content:space-between;"><span>珍珠 Lv.'+li.l+'（'+(st.points||0)+' 珍珠值）</span><span>下一級還差 '+Math.max(0,li.nx-(st.points||0))+'</span></div><div class="lvbar" style="margin-top:4px;"><div class="lvfill" style="width:'+li.pct+'%"></div></div>'+
     '<div class="mini" style="margin-top:6px;">擼擼 '+(st.aff||0)+' 次　|　配件獎勵：'+accLine()+'</div></div>';
  H+='</div>';
  H+='<div class="metrics" style="margin-bottom:13px;">'+(SHARE?(m(unitsDone+'/'+CUR.length,'讀書進度','')+m((st.wrongRM.length+st.wrongStat.length),'錯題本','題')+m((st.points||0),'珍珠值','')+m('Lv.'+li.l,'等級','')):(m(streakE(),'連續記錄','天')+m(st.entries.length,'珍珠數','筆')+m(unitsDone+'/'+CUR.length,'讀書進度','')+m((st.wrongRM.length+st.wrongStat.length),'錯題本','題')))+'</div>';if(!SHARE)H+='<div class="card" style="padding:11px 13px;display:flex;align-items:center;gap:10px;"><span class="mini" style="flex:0 0 auto;">切換功能</span><select id="hubSel" style="flex:1;padding:9px;border-radius:9px;border:.5px solid var(--line);background:var(--surface);color:var(--ink);font-family:inherit;font-size:14.5px;"><option value="exam">🎯 資格考衝刺</option><option value="paper">📄 論文閱讀管理（讀完寫心得領珍珠）</option></select></div>';

  if(!SHARE){H+='<div class="card"><h2>記一筆珍珠　<span class="mini">+6 珍珠值</span></h2><div class="sub" style="margin-bottom:8px;">寫「事實」就好：今天做到、想到、注意到的。不用稱讚自己。</div><textarea id="inp" rows="2" placeholder="例如：今天把後驗機率默寫出來了，沒看解答。"></textarea><div class="row" style="margin-top:8px;"><button class="primary" id="addBtn" style="flex:1;">記下這筆</button><button id="filtBtn">濾鏡又開了</button></div><div id="filtPanel" style="display:none;margin-top:10px;" class="soft"><div style="font-size:14px;">抓到了，這就是進步。<b>你不用贏它，只要不再自動相信它。</b></div><div style="font-size:14px;margin-top:6px;color:var(--muted);">問自己：「如果詩涵是我的學生，我會跟她說什麼？」</div><div id="filtCnt" class="mini" style="margin-top:6px;"></div></div></div>';}

  H+='<div class="card"><h2>📌 當日任務　<span class="mini">今天該做的一件事</span></h2>';
  if(now<START)H+='<div class="sub">距開讀還有 '+diff(now,START)+' 天（'+md(START)+' 起）。先把講義與詳解放好。</div>';
  else if(now.getDay()===0)H+='<div class="sub">今天是休息日，讓大腦消化。明天再戰。</div>';
  else if(td){var on=!!st.done[td.id];
   H+='<div class="day" data-toggle="'+td.id+'" style="border-left:3px solid '+SCOL[td.subj]+';"><div class="chk '+(on?'on':'')+'">'+(on?'✓':'')+'</div><div><div class="mini">'+md(td.date)+' 週'+WD[td.date.getDay()]+' · '+td.est+'hr · 完成 +12</div><div style="font-size:15px;font-weight:500;'+(on?'text-decoration:line-through;opacity:.55;':'')+'"><span style="color:'+SCOL[td.subj]+';">'+td.subj+'</span> · '+td.title+'</div></div></div>';
   if(td.link)H+='<button id="goTask" data-link="'+td.link+'" style="width:100%;margin-top:8px;">'+(td.link.indexOf('plan')===0?'開始三階段練習 →':(td.link.indexOf('rm')===0?'在這裡刷研方題 →':'看這題型 · 作答對照 →'))+'</button>';
  } else if(now>SEND&&now<=EXAM)H+='<div class="sub">開學維持期：每天默寫一條核心公式 + 每週一回模擬。</div>';
  H+='</div>';
  if(!SHARE&&now>=START&&now<=SEND){var overdue=days.filter(function(x){return x.date<now&&!same(x.date,now)&&!st.done[x.id]&&x.subj!=='彈性';});if(overdue.length){H+='<div class="card" style="border-left:3px solid var(--clay);"><h2>🐢 待補進度　<span class="mini">落後 '+overdue.length+' 格</span></h2>';H+='<div class="sub" style="margin-bottom:8px;">進度落後很正常，不用一次補完。挑一格做完打勾，黑珍珠就會變白 🤍</div>';overdue.slice(0,6).forEach(function(x){var col=SCOL[x.subj];H+='<div class="day" data-toggle="'+x.id+'" style="border-left:3px solid '+col+';"><div class="chk"></div><div><div class="mini">'+md(x.date)+' 週'+WD[x.date.getDay()]+' · 補完 +12</div><div style="font-size:14px;font-weight:500;"><span style="color:'+col+';">'+x.subj+'</span> · '+esc(x.title)+'</div></div></div>';if(x.link)H+='<button class="gonav" data-gonav="'+x.link+'" style="width:100%;margin:-2px 0 8px;font-size:13px;padding:7px;">▶ 去做這格</button>';});if(overdue.length>6)H+='<div class="mini" style="text-align:center;margin-top:4px;">…還有 '+(overdue.length-6)+' 格，先補上面幾格 👆</div>';H+='</div>';}}

  var due=dueList();H+='<div class="card"><h2>今日複習　<span class="mini">間隔記憶</span></h2>';if(due.length){H+='<div class="sub" style="margin-bottom:6px;">這些題型到了回顧時間，趁還記得鞏固長期記憶：</div>';due.forEach(function(d){H+='<div class="ttl" data-review="'+d.key+'"><span>'+(d.ft.tp.star?"★ ":"")+esc(d.ft.tp.title)+'</span><span class="pill">第 '+(d.m.box+1)+' 階複習 →</span></div>';});}else H+='<div class="sub">今天沒有到期的複習，繼續往前推進 👍（完成或自評過的題型，會照記憶曲線排隊回來）。</div>';if(st.wrongRM.length)H+='<div class="ttl" data-gowrong="1" style="border-color:var(--no)"><span style="color:var(--no)">研方錯題 '+st.wrongRM.length+' 題</span><span class="pill">去重練 →</span></div>';H+='</div>';H+='<div class="card"><h2>練習區</h2><div class="row"><button id="pRM" class="primary" style="flex:1;min-width:46%;">研方刷題</button><button id="pST" style="flex:1;min-width:46%;">統計作答對照</button><button id="pPlan" style="flex:1;min-width:46%;">三階段練習</button><button id="pW" style="flex:1;min-width:46%;">錯題本 ('+(st.wrongRM.length+st.wrongStat.length)+')</button></div><div class="mini" style="margin-top:8px;">三階段＝前測→看重點→後測（也可從上方每日任務直接進入該題型）。</div></div>';H+='<div class="card"><h2>衝刺模擬考</h2><div class="sub" style="margin-bottom:8px;">研方選擇題＋統計題，做完給你預估成績（對照目標 研方70 / 統計50）。</div><button id="goMock" class="primary" style="width:100%;">開始模擬考 →</button></div>';H+='<div class="soft" style="margin-bottom:13px;text-align:center;"><a href="https://claude.ai/new" target="_blank" style="color:var(--purple);font-size:14px;font-weight:500;text-decoration:none;">💬 開啟 Claude 對話討論（評分 / 問問題）↗</a><div class="mini" style="margin-top:4px;">手機、平板也能直接和 Claude 討論考試重點</div></div>';

  if(!SHARE){var _rm=st.rem||{am:'08:00',pm:'21:00'};H+='<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><h2 style="margin:0;">📲 手機提醒</h2><span class="mini">早晚各一次 · 每次都不一樣</span></div>';H+='<div class="sub" style="margin:6px 0 9px;">'+(_rm.on?'已開啟 🔔 到時間會用一句新鮮的打氣陪你 —— 不管做了沒，都很有活力 🦪':'打開後，早上一句開場、晚上一句回顧，陪你每天養一顆珍珠 ✨')+'</div>';H+='<div class="row" style="gap:8px;margin-bottom:9px;"><label style="flex:1;font-size:14px;color:var(--muted);">☀️ 早上<input id="remAm" type="time" value="'+(_rm.am||'08:00')+'" style="width:100%;margin-top:4px;"></label><label style="flex:1;font-size:14px;color:var(--muted);">🌙 晚上<input id="remPm" type="time" value="'+(_rm.pm||'21:00')+'" style="width:100%;margin-top:4px;"></label></div>';if(_rm.on){H+='<div class="row"><button id="remOff" style="flex:1;">關閉提醒</button><button id="remTest" class="primary" style="flex:1;">試跳一次 ✨</button></div>';}else{H+='<button id="remOn" class="primary" style="width:100%;">開啟每日提醒</button>';}H+='<div class="ttl" data-remhelp="1" style="margin-top:9px;"><span style="font-size:13px;">📱 iPhone 怎麼讓它跳通知？</span><span class="pill">'+(_rm._help?'收合':'看步驟')+'</span></div>';if(_rm._help){H+='<div class="soft" style="margin-top:6px;font-size:13px;line-height:1.75;">① 用 <b>Safari</b> 開這個頁面<br>② 點底部<b>分享</b>鈕 → <b>加入主畫面</b><br>③ 從主畫面打開這個 App → 按「開啟每日提醒」並<b>允許通知</b><br>④ 之後開著或放背景，到時間就會跳；完全關掉時 iPhone 無法自動推播，<b>下次打開會幫你補一則</b>。<div class="mini" style="margin-top:5px;">放在主畫面第一頁，看到就想點開撈一顆 🦪</div></div>';}H+='</div>';H+='<div class="card"><div style="display:flex;justify-content:space-between;align-items:center;"><h2 style="margin:0;">珍珠日記</h2><span class="mini">最新在上</span></div><div style="margin-top:10px;">';
  var sorted=st.entries.slice().reverse();
  for(var e=0;e<sorted.length;e++){var en=sorted[e];H+='<div class="entry"><div class="t">'+(en.t||'')+'</div><div class="b">'+esc(en.b)+'</div><div style="margin-top:4px;"><a class="copy" data-copy="'+e+'">複製</a> · <a class="copy" data-del="'+e+'">刪除</a></div></div>';}
  H+='</div><div style="margin-top:10px;"><div class="mini" style="margin-bottom:6px;">創始珍珠（不會被歸零的事）</div>';
  for(var f=0;f<(st.pins||[]).length;f++)H+='<div class="entry pin"><div class="b">'+esc(st.pins[f])+'</div></div>';
  H+='</div></div>';}
  H+='<div class="card"><div class="wk" id="schToggle"><h2 style="margin:0;">暑假讀書排程</h2><span class="mini">展開 ▾</span></div><div id="sch" style="display:none;margin-top:10px;"></div></div>';
  if(!SHARE&&st.anchor){H+='<div class="soft" style="margin-bottom:13px;"><div style="font-size:14px;">「'+esc(st.anchor)+'」</div><div class="mini" style="margin-top:6px;">心虛的時候回來看一眼。這不是安慰，是你的證據。</div></div>';}
  H+='<div class="card"><h2>雲端同步　<span class="mini">換裝置自動帶回</span></h2>';if(!window._db){H+='<div class="sub">雲端尚未就緒(需要網路連線才能同步)。</div>';}else if(st._cloudPending){H+='<div class="sub" style="margin-bottom:8px;color:var(--no);">雲端「'+esc(st.syncCode)+'」已經有資料，要怎麼處理？</div><div class="row"><button id="useCloud" style="flex:1;">⬇ 用雲端蓋本機</button><button id="useLocal" style="flex:1;">⬆ 用本機蓋雲端</button></div>';}else if(st.syncCode){H+='<div class="sub">已連線同步碼：<b>'+esc(st.syncCode)+'</b>　'+esc(st._syncMsg||'')+'</div><div class="row" style="margin-top:8px;"><button id="syncNow" class="primary" style="flex:1;">立即同步</button><button id="syncOff" style="flex:1;">取消連線</button></div><div class="mini" style="margin-top:6px;">在另一台裝置輸入同一組同步碼，就會自動帶回所有資料。</div>';}else{if(SHARE)H+='<div class="sub" style="color:var(--clay);font-weight:600;margin-bottom:6px;">👉 第一次使用：請先設定你自己的同步碼，進度才會跨裝置保存。</div>';H+='<div class="sub" style="margin-bottom:8px;">設一組只有你知道的「同步碼」(建議長一點，例如 amy-stat-7k3p9)；每台裝置輸入同一組就會自動同步。</div><input id="syncIn" placeholder="輸入你的同步碼"><button id="syncConnect" class="primary" style="width:100%;margin-top:8px;">連線並同步</button>';}H+='</div>';H+='<div class="card"><h2>資料備份 / 換裝置</h2><div class="sub" style="margin-bottom:8px;">換電腦或平板前，先按「匯出」存成檔案(放 Google Drive 或寄給自己)；到新裝置打開後按「匯入」即可帶回所有進度與紀錄。</div><div class="row"><button id="expBtn" class="primary" style="flex:1;">匯出備份</button><label style="flex:1;display:inline-flex;align-items:center;justify-content:center;border:.5px solid var(--line);border-radius:10px;cursor:pointer;padding:10px;min-height:44px;">匯入備份<input id="impInput" type="file" accept="application/json,.json" style="display:none;"></label></div></div>';H+='<div style="text-align:center;"><a class="copy" id="rst">重置全部資料</a></div>';
  return H;
 }
 function schedHTML(){var H='',cw=curWeek();
  for(var w=0;w<nW;w++){var wd=days.filter(function(x){return x.week===w;});if(!wd.length)continue;var dn=wd.filter(function(x){return st.done[x.id];}).length,open=(w===cw||st.open[w]);
   H+='<div style="margin-bottom:8px;"><div class="wk" data-week="'+w+'"><span>第 '+(w+1)+' 週 <span class="mini">'+md(wd[0].date)+'–'+md(wd[wd.length-1].date)+'</span></span><span class="mini">'+dn+'/'+wd.length+'</span></div>';
   if(open)for(var q=0;q<wd.length;q++){var x=wd[q],on=!!st.done[x.id];H+='<div class="day" data-toggle="'+x.id+'" style="border-left:3px solid '+SCOL[x.subj]+';"><div class="chk '+(on?'on':'')+'">'+(on?'✓':'')+'</div><div><div class="mini">'+md(x.date)+' 週'+WD[x.date.getDay()]+' · '+x.est+'hr</div><div style="font-size:14px;'+(on?'text-decoration:line-through;opacity:.55;':'')+'"><span style="color:'+SCOL[x.subj]+';">'+x.subj+'</span> · '+x.title+'</div></div></div>';}
   H+='</div>';}
  return H;}

 function rmPool(round){var idxs=[],g={1:[0,1,2,3],2:[4,5,6,7],3:[8,9,10,11]};if(round.indexOf('sem:')===0){var syi=+round.slice(4);if(RM[syi])RM[syi].qs.forEach(function(q,qi){if(q.opts&&q.opts.length>=2)idxs.push([syi,qi]);});return idxs;}if(round.indexOf('cat:')===0){var cc=round.slice(4);RM.forEach(function(ss,si){ss.qs.forEach(function(q,qi){if(q.cat===cc&&q.opts&&q.opts.length>=2)idxs.push([si,qi]);});});return idxs;}
  if(round==='wrong'){return st.wrongRM.map(function(w){return w.slice();});}
  var ps=round==='all'?RM.map(function(_,i){return i;}):(g[round]||[]);
  ps.forEach(function(si){var s=RM[si];if(s)s.qs.forEach(function(qq,qi){if(qq.opts&&qq.opts.length>=2)idxs.push([si,qi]);});});return idxs;}
 function shuf(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1));var t=a[i];a[i]=a[j];a[j]=t;}return a;}
 function startRM(round){var pl=rmPool(round);if(round.indexOf('sem:')!==0)pl=shuf(pl);st.sess={pool:pl,i:0,score:0,picked:null,round:round};}
 function inWrong(si,qi){return st.wrongRM.some(function(w){return w[0]==si&&w[1]==qi;});}

 function rmCats(){var m={},o=[];RM.forEach(function(ss){ss.qs.forEach(function(q){if(q.opts&&q.opts.length>=2){var c=q.cat||'其他';if(!(c in m)){m[c]=0;o.push(c);}m[c]++;}});});return {m:m,o:o};}
 function renderRMmenu(){var rmode=st.rmMode||'sem';var H='<button id="back">← 回首頁</button><h2 style="margin-top:12px;">研方刷題</h2>';H+='<div class="row" style="margin-bottom:10px;"><button data-rmmode="sem" class="'+(rmode==='sem'?'primary':'')+'" style="flex:1;">歷屆</button><button data-rmmode="cat" class="'+(rmode==='cat'?'primary':'')+'" style="flex:1;">類別</button><button data-rmmode="day" class="'+(rmode==='day'?'primary':'')+'" style="flex:1;">當日任務</button></div>';H+='<div class="sub" style="margin-bottom:10px;">點選項立刻看對錯與解析；答錯自動進錯題本。</div>';if(rmode==='cat'){var rc=rmCats();rc.o.sort(function(a,b){return rc.m[b]-rc.m[a];});rc.o.forEach(function(c){H+='<div class="ttl" data-rm="cat:'+c+'"><span>'+esc(c)+'</span><span class="pill">'+rc.m[c]+' 題 →</span></div>';});return H;}if(rmode==='day'){H+='<div class="sub" style="margin-bottom:8px;">照排程列出研方任務，點有「去刷」的直接開始。</div>';days.forEach(function(x){if(x.subj==='研方'||x.subj==='模擬'){var on=st.done[x.id];if(x.link&&x.link.indexOf('plan')===0){H+='<div class="ttl" data-goplan="'+x.link+'"><span>'+(on?'✓ ':'')+md(x.date)+'（'+WD[x.date.getDay()]+'） '+esc(x.title)+(same(x.date,now)?' · 今天':'')+'</span><span class="pill">去三階段 →</span></div>';}else if(x.link&&x.link.indexOf('rm')===0){H+='<div class="ttl" data-rm="'+x.link.replace('rm:','')+'"><span>'+(on?'✓ ':'')+md(x.date)+'（'+WD[x.date.getDay()]+'） '+esc(x.title)+(same(x.date,now)?' · 今天':'')+'</span><span class="pill">去刷 →</span></div>';}else if(x.subj==='研方'){H+='<div class="ttl" style="opacity:.65;"><span>'+(on?'✓ ':'')+md(x.date)+'（'+WD[x.date.getDay()]+'） '+esc(x.title)+'</span><span class="pill">讀題庫</span></div>';}}});return H;}
  H+=sortBar();H+='<div class="sub" style="margin:2px 0 8px;">選一個年度，照原卷順序練那一年：</div>';var ord=RM.map(function(_,i){return i;});if(st.yearDesc)ord.reverse();ord.forEach(function(si){var ss=RM[si];var c=ss.qs.filter(function(q){return q.opts&&q.opts.length>=2;}).length;if(c)H+='<div class="ttl" data-rm="sem:'+si+'"><span>'+esc(ss.label.split('（')[0])+'　'+yname(ss.label.split('（')[0])+'</span><span class="pill">'+c+' 題 →</span></div>';});H+='<div class="row" style="margin-top:10px;"><button data-rm="all" style="flex:1;">全部隨機 290 題</button><button data-rm="wrong" class="primary" style="flex:1;">只練錯題（'+st.wrongRM.length+'）</button></div>';return H;}
 function renderRMq(){var s=st.sess;if(!s)return renderRMmenu();
  if(!s.pool.length)return '<button id="back">← 回首頁</button><div class="card" style="margin-top:14px;text-align:center;">錯題本是空的，太好了！'+cat('white')+'</div>';
  if(s.i>=s.pool.length){if(s.phase){var rec=st.phase['rm:'+s.cat]||{};var lbl=s.phase==='pre'?'前測':'後測';var PH='<button id="planback">← 回三階段</button><div class="card" style="text-align:center;margin-top:14px;"><h2>'+lbl+'完成！</h2><div class="sub">'+esc(s.cat)+'　研究方法</div><div style="font-size:34px;font-weight:600;color:var(--teal);">'+s.score+' / '+s.pool.length+'</div>'+(s.phase==='pre'?'<div class="sub">這是你的真實起點，錯很多也沒關係。接著去看 ②重點，再做 ③後測比較。</div>':'')+((rec.pre&&rec.post)?'<div class="sub" style="color:var(--clay);font-weight:500;">前測 '+rec.pre.s+'/'+rec.pre.t+' → 後測 '+rec.post.s+'/'+rec.post.t+'　'+deltaTxt(rec)+'</div>':'')+cat('white')+'<button id="planback2" class="primary" style="width:100%;margin-top:10px;">回三階段練習</button></div>';return PH;}var pct=Math.round(s.score/s.pool.length*100);
   return '<button id="back">← 回首頁</button><div class="card" style="text-align:center;margin-top:14px;"><h2>這輪完成！</h2><div style="font-size:34px;font-weight:600;color:var(--teal);">'+s.score+' / '+s.pool.length+'</div><div class="sub">答對率 '+pct+'%　+'+s.score+' 珍珠值</div>'+(s.markedToday?'<div class="sub" style="color:var(--teal)">今天的任務也幫你打勾了 ✓ +12</div>':'')+cat('white')+'<div class="mini">'+pick(WHITE,s.score)+'</div><div class="row" style="margin-top:10px;"><button class="primary" id="again" style="flex:1;">再來一輪</button><button id="logit" style="flex:1;">記成一筆珍珠</button></div></div>';}
  var pr=s.pool[s.i],sem=RM[pr[0]],q=sem.qs[pr[1]];var ansL=(q.ans||'').toUpperCase().replace(/[^A-E]/g,'').charAt(0);
  var H='<div style="display:flex;justify-content:space-between;align-items:center;"><button id="back">← 回首頁</button><span class="pill">'+(s.i+1)+' / '+s.pool.length+(s.phase==='pre'?'':' · 對 '+s.score)+'</span></div>';H+='<div class="lvbar" style="margin-top:10px;"><div class="lvfill" style="width:'+Math.round(s.i/s.pool.length*100)+'%;background:var(--teal)"></div></div>';
  H+='<div class="card" style="margin-top:12px;"><div class="mini">'+esc(sem.label.split('（')[0])+'　Q'+q.n+(inWrong(pr[0],pr[1])?' · 錯題':'')+'</div><div style="font-size:16px;font-weight:500;margin:6px 0 10px;">'+esc(q.q)+'</div>';
  for(var o=0;o<q.opts.length;o++){var L=q.opts[o].toUpperCase().replace(/[^A-E]/,'').charAt(0)||String.fromCharCode(65+o);var cls='opt';if(s.picked){if(s.phase==='pre'){if(L===s.picked)cls+=' selp';}else{if(L===ansL)cls+=' ok';else if(L===s.picked)cls+=' no';}}H+='<button class="'+cls+'" data-opt="'+L+'"'+(s.picked?' disabled':'')+'>'+esc(q.opts[o])+'</button>';}
  if(s.picked&&s.phase==='pre'){H+='<div class="soft" style="margin-top:10px;"><div style="font-size:14px;">已記下你的作答。<b>前測不公布答案</b>，等看完重點、做完後測再一起對照。</div></div><button class="primary" id="next" style="width:100%;margin-top:10px;">'+(s.i+1>=s.pool.length?'看前測結果 →':'下一題 →')+'</button>';}else if(s.picked){var right=s.picked===ansL;H+='<div class="soft" style="margin-top:10px;"><div style="font-weight:500;color:'+(right?'var(--ok)':'var(--no)')+';">'+(right?'答對了 ✓ +1':'答錯了（正解 '+ansL+'）· 已收進錯題本')+'</div>'+(q.note?'<div style="font-size:14px;margin-top:4px;">'+esc(q.note)+'</div>':'')+'<div style="font-size:13.5px;margin-top:6px;color:var(--olive);"><b>解題思路：</b>'+esc(RMTIP(q.cat))+'</div></div><button class="primary" id="next" style="width:100%;margin-top:10px;">下一題 →</button>';}
  H+='</div>';return H;}

 function statList(){return [['high','超高頻 / 高頻'],['mid','中頻'],['low','低頻']];}
 function findTopic(link){var mm=link.match(/^stat:(high|mid|low)(\d+)$/);if(!mm)return null;return {g:mm[1],i:+mm[2]};}
 function origQ(yr,qno){var q=''+qno;if(/名詞/.test(q)||/^一/.test(q))return null;var sem=(''+yr).split('/')[0].slice(0,4);var m=q.match(/\d+/);if(!m)return null;var lab=m[0];var qs=(window.STATFULL[sem]&&window.STATFULL[sem].qs)||[];for(var i=0;i<qs.length;i++){if(qs[i].sect==='問答'&&qs[i].label===lab)return qs[i].text;}return null;}
 function topicPanel(key){var fk=findKey(key);if(!fk)return '';var tp=fk.tp;var H='';H+='<div class="soft" style="margin:-3px 0 9px;">';H+='<div class="mini" style="margin-bottom:6px;">點開每個子題：先自己作答 → 顯示詳解對照（模擬正式考）</div>';tp.years.forEach(function(y,yi){var sk=key+'|'+yi,qo=st.statOpen[sk];var oq=origQ(y[0],y[1]);var disp=oq?(esc(oq)+' <span class="mini">（'+esc(y[2])+'）</span>'):esc(y[2]);H+='<div class="ttl" data-sq="'+sk+'"><span style="font-size:13.5px;"><b>'+esc(y[0])+'</b>（'+esc(y[1])+'） '+disp+'</span><span class="pill">'+(qo?'收合':'作答')+'</span></div>';if(qo){H+='<div style="padding:2px 2px 10px;"><textarea data-ans="'+sk+'" rows="3" placeholder="寫下你對這子題的解題過程…">'+esc(st.statAns[sk]||'')+'</textarea>';H+='<div class="row" style="margin-top:8px;"><button data-solq="'+sk+'" style="flex:1;">'+(st.statOpen[sk+'_s']?'隱藏詳解':'顯示詳解')+'</button><button data-copy3="'+sk+'" style="flex:1;">複製給 AI 評分</button></div>';if(st.statOpen[sk+'_s']){H+='<div class="soft" style="margin-top:8px;background:var(--surface);">';tp.sol.forEach(function(sl){H+='<div style="font-size:14px;margin-bottom:5px;"><b style="color:var(--clay);">◆ '+esc(sl[0])+'：</b>'+esc(sl[1])+'</div>';});H+='<div class="mini" style="margin-top:6px;">出處：'+esc(tp.lect)+'｜'+esc(tp.book)+'</div></div>';}H+='</div>';}});H+='<button data-copyall="'+key+'" style="width:100%;margin-top:10px;">複製本題型「全部作答」→ 請 AI 逐題評分</button>';H+='<div class="mini" style="margin:10px 0 4px;">整題型自評（影響間隔複習排程）</div><div class="row"><button data-sc="'+key+'|熟" style="flex:1;">熟 +8</button><button data-sc="'+key+'|普通" style="flex:1;">普通 +4</button><button data-sc="'+key+'|不熟" style="flex:1;">不熟 +2</button></div>';H+='</div>';return H;}
 function renderStat(focus){
  if(st.statSess)return renderStatSess();
  var H='<button id="back">← 回首頁</button><h2 style="margin-top:12px;">統計 · 作答對照</h2><div class="sub" style="margin-bottom:10px;">流程：看歷屆題 → 自己寫解題過程 → 看標準解法對照 → 自評（不熟會進錯題本，也可複製給 AI 評分）。</div>';var smode=st.statMode||'cat';H+='<div class="row" style="margin-bottom:10px;"><button data-smode="cat" class="'+(smode==='cat'?'primary':'')+'" style="flex:1;">類別</button><button data-smode="day" class="'+(smode==='day'?'primary':'')+'" style="flex:1;">當日任務題目</button><button data-smode="year" class="'+(smode==='year'?'primary':'')+'" style="flex:1;">歷屆</button></div>';if(smode==='day'){H+='<div class="sub" style="margin-bottom:8px;">照排程順序，點任一天直接在這裡展開作答（今天的預設展開）。</div>';days.forEach(function(x){if(x.subj==='統計'&&x.link&&x.link.indexOf('stat:')===0){var dk='d:'+x.id,kk=x.link.replace('stat:',''),op=(dk in st.statOpen)?st.statOpen[dk]:same(x.date,now),on=st.done[x.id];H+='<div class="ttl" data-dayexp="'+dk+'"><span>'+(on?'✓ ':'')+md(x.date)+'（'+WD[x.date.getDay()]+'） '+esc(x.title)+(same(x.date,now)?' · 今天':'')+'</span><span class="pill">'+(op?'收合':'作答')+'</span></div>';if(op)H+=topicPanel(kk);}else if(x.subj==='統計'&&x.link&&x.link.indexOf('plan')===0){var on2=st.done[x.id];H+='<div class="ttl" data-goplan="'+x.link+'"><span>'+(on2?'✓ ':'')+md(x.date)+'（'+WD[x.date.getDay()]+'） '+esc(x.title)+(same(x.date,now)?' · 今天':'')+'</span><span class="pill">去三階段 →</span></div>';}});return H;}if(smode==='year'){var by=statByYear();if(!st.statYear){H+=sortBar();H+='<div class="sub" style="margin:2px 0 8px;">選一個年度，看那一年統計考了哪些題：</div>';var yo=by.o.slice();if(st.yearDesc)yo.reverse();yo.forEach(function(sem){H+='<div class="ttl" data-statyear="'+sem+'"><span>'+sem+'　'+yname(sem)+'</span><span class="pill">'+by.m[sem].length+' 題 →</span></div>';});return H;}H+='<button data-statyear="" style="margin-bottom:8px;">← 選其他年度</button><button id="statstart" class="primary" style="width:100%;margin-bottom:8px;">▶ 整年連續作答（模擬）</button><div class="mini" style="margin:4px 0 8px;">'+st.statYear+'　'+yname(st.statYear)+'（點題目看解法）</div>';var fq=fullQs(st.statYear),tot=fq.reduce(function(a,b){return a+(b.pts||0);},0);H+='<div class="mini" style="margin:0 0 8px;">全卷約 '+tot+' 分（點題目看完整題目＋解法）</div>';fq.forEach(function(q,i){var ok='y:'+st.statYear+':'+i,op=st.statOpen[ok];H+='<div class="ttl" data-yq="'+ok+'"><span style="font-size:13px;"><b>'+esc(q.sect)+esc(q.label)+'</b>（'+q.pts+'分） '+esc(q.text)+'</span><span class="pill">'+(op?'收合':'解法')+'</span></div>';if(op){var k=statMatch(q.text);if(k)H+=solBlock(k);else H+='<div class="soft" style="margin-top:6px;"><div class="mini">此題型請到「類別」分頁查詳解。</div></div>';}});return H;}
  statList().forEach(function(g){H+='<div class="mini" style="margin:10px 0 6px;">'+g[1]+'</div>';
   STAT[g[0]].forEach(function(tp,ti){var key=g[0]+ti,open=!!st.statOpen[key]||(focus&&focus.g===g[0]&&focus.i===ti);
    var weak=st.wrongStat.indexOf(key)>=0;
    H+='<div class="ttl" data-stat="'+key+'"><span style="font-weight:500;">'+(tp.star?'★ ':'')+esc(tp.title)+(weak?' · <span style="color:var(--no)">弱點</span>':'')+'</span><span class="pill">'+esc(tp.tier.split('（')[0])+'</span></div>';
    if(open)H+=topicPanel(key);
   });});
  return H;}
 function renderWrong(){
  var H='<button id="back">← 回首頁</button><h2 style="margin-top:12px;">錯題本</h2>';
  var wt=st.wrongTab||'rm';
  H+='<div class="row" style="margin-bottom:10px;"><button data-wtab="rm" class="'+(wt==='rm'?'primary':'')+'" style="flex:1;">研究方法（'+st.wrongRM.length+'）</button><button data-wtab="stat" class="'+(wt==='stat'?'primary':'')+'" style="flex:1;">統計（'+st.wrongStat.length+'）</button></div>';
  if(wt==='rm'){H+='<div class="card"><h2>研方錯題（'+st.wrongRM.length+'）</h2>';
  if(!st.wrongRM.length)H+='<div class="sub">目前沒有研方錯題。</div>';
  else{H+='<button class="primary" id="practiceWrong" style="width:100%;margin-bottom:8px;">開始重練（答對就移除）</button>';
   st.wrongRM.slice(0,40).forEach(function(w){var q=RM[w[0]]&&RM[w[0]].qs[w[1]];if(!q)return;H+='<div class="entry" style="border-left-color:var(--no)"><div class="t">'+esc(RM[w[0]].label.split('（')[0])+' Q'+q.n+'　正解 '+esc((q.ans||'').toUpperCase().replace(/[^A-E]/g,'').charAt(0))+'</div><div class="b">'+esc(q.q)+'</div></div>';});}
  H+='</div>';}
  else{H+='<div class="card"><h2>統計弱點題型（'+st.wrongStat.length+'）</h2>';
  if(!st.wrongStat.length)H+='<div class="sub">目前沒有標記為不熟的統計題型。</div>';
  else st.wrongStat.forEach(function(k){var ft=findKey(k);if(!ft)return;H+='<div class="ttl" data-goweak="'+k+'"><span>'+(ft.tp.star?'★ ':'')+esc(ft.tp.title)+'</span><span class="pill">去複習 →</span></div>';});
  H+='</div>';}return H;}
 function findKey(key){var mm=key.match(/^(high|mid|low)(\d+)$/);if(!mm)return null;var tp=STAT[mm[1]][+mm[2]];return tp?{g:mm[1],i:+mm[2],tp:tp}:null;}

 function sortBar(){var d=st.yearDesc;return '<div class="row" style="margin-bottom:6px;"><button data-sortord="0" class="'+(!d?'primary':'')+'" style="flex:1;">舊 → 新</button><button data-sortord="1" class="'+(d?'primary':'')+'" style="flex:1;">新 → 舊</button></div>';}
 function solBlock(key){var fk=findKey(key);if(!fk)return '';var H='<div class="soft" style="margin-top:8px;background:var(--surface);">';fk.tp.sol.forEach(function(sl){H+='<div style="font-size:14px;margin-bottom:5px;"><b style="color:var(--clay);">◆ '+esc(sl[0])+'：</b>'+esc(sl[1])+'</div>';});H+='<div class="mini" style="margin-top:6px;">出處：'+esc(fk.tp.lect)+'｜'+esc(fk.tp.book)+'</div></div>';return H;}
 function statFlat(){var by=statByYear(),a=[];by.o.forEach(function(sm){by.m[sm].forEach(function(q){a.push({qno:q.qno,desc:q.desc,key:q.key,title:q.title,sem:sm});});});return a;}
 function fullQs(sem){return (window.STATFULL[sem]&&window.STATFULL[sem].qs)||[];}
 function statMatch(text){var t=(text||'').toLowerCase();var R=[['general linear test','high2'],['reduced model','high2'],['full model','high2'],['test h0','high2'],['coefficient of partial determination','high11'],['partial determination','high11'],['partial correlation','high11'],['hosmer','high5'],['logistic','high5'],['logit','mid4'],['odds','mid4'],['log-linear','mid4'],['log linear','mid4'],['poisson','mid4'],['classification rule','high4'],['posterior probab','high4'],['prior probabilit','high4'],['cochrane','high10'],['durbin','high10'],['autoregressive','high9'],['ar(1)','high9'],['autocorrelat','high9'],['analysis of covariance','high3'],['ancova','high3'],['covariate','high3'],['reduce experimental error','high3'],['blocking','high3'],['orthogonal factor','high0'],['factor loading','high0'],['factor score','high0'],['factor analysis','high0'],['factor model','high0'],['rotation','high0'],['principal component','high0'],['composite reliability','high0'],['rmsea','high0'],['confirmatory factor','high0'],['multivariate pair','high1'],['pair comparison','high1'],['paired comparison','high1'],['hotelling','high1'],['repeated-measure','mid5'],['repeated measure','mid5'],['contrast matrix','high7'],['manova','high7'],['profile','high7'],['interaction effect','low4'],['canonical','high8'],['t2-interval','high6'],['t2 interval','high6'],['t2-intervals','high6'],['paired-comparison','high1'],['paired- comparison','high1'],['contingency','low2'],['multinomial sampling','low2'],['chi-square','low2'],['卡方','low2'],['wilks','high6'],['simultaneous','high6'],['bonferroni','high6'],['mean vector','high6'],['confidence region','high6'],['constant probability density','high6'],['wishart','high6'],['multivariate central','low5'],['central limit','low5'],['blue','mid0'],['gauss-markov','mid0'],['gauss markov','mid0'],['box-cox','mid0'],['normality','mid0'],['常態性','mid0'],['assumptions of the model','mid0'],['standardized regression','mid1'],['partial regression plot','mid1'],['multiple correlation','mid1'],['piecewise','mid1'],['vif','mid1'],['cross-validation','mid2'],['discriminant','mid2'],['k-means','mid2'],['classification function','mid2'],['歸類','mid2'],['brown-forsythe','mid3'],['levene','mid3'],['homogeneity of var','mid3'],['variance同質','mid3'],['變異數同質','mid3'],['nested design','low1'],['crossed design','low1'],['cross and nested','low1'],['cross vs nested','low1'],['cross designs','low1'],['randomized block','low3'],['block design','low3'],['fixed-effect','low4'],['random-effect','low4'],['fixed effect','low4'],['random effect','low4'],['two-factor','low4'],['ridge','low7'],['multicollinear','low7'],['collinear','low7'],['bootstrap','low8'],['nonmetric','low9'],['multidimensional scaling','low9'],['standardized regression model','mid1'],['anova迴歸','low0'],['one-factor anova','low2'],['multiple regression','mid0'],['regression model','mid0'],['anova','low4']];for(var i=0;i<R.length;i++)if(t.indexOf(R[i][0])>=0)return R[i][1];return null;}
 function gradePrompt(title,desc,ans){return '請依詳解逐題批改這一題（不要只給總結）。請依序給：🏷️判定、得分(/10)、✅對的、❌關鍵失分點(踩到陷阱要點名)、🎯正確理由(白話)、✍️滿分版作答(可背)、💡口訣。\n\n【題型】'+title+'\n【題目】'+desc+'\n【我的作答】'+ans;}
 function renderStatSess(){var ss=st.statSess,fq=fullQs(ss.year),N=fq.length;if(ss.i>=N){var got=(ss.scores||[]).reduce(function(a,b){return a+b;},0),tot=fq.reduce(function(a,b){return a+(b.pts||0);},0),pct=tot?Math.round(got/tot*100):0;return '<button id="sback">← 結束</button><div class="card" style="text-align:center;margin-top:14px;"><h2>整年完成！</h2><div class="sub">'+ss.year+'　'+yname(ss.year)+'</div><div style="font-size:30px;font-weight:600;color:var(--clay);">預估 '+got+' / '+tot+' 分</div><div class="sub">自評估算約 '+pct+'%（實際請用「複製給 AI 評分」校準）</div>'+cat(pct>=50?'white':'neutral')+'<div class="row" style="margin-top:10px;"><button id="copyyear" class="primary" style="flex:1;">複製整年作答 → Claude 評分</button><button id="sback2" style="flex:1;">回題庫</button></div></div>';}var q=fq[ss.i],ak='ys:'+ss.year+':'+ss.i,k=statMatch(q.text);var H='<div style="display:flex;justify-content:space-between;align-items:center;"><button id="sback">← 結束</button><span class="pill">'+(ss.i+1)+' / '+N+'　'+q.pts+'分</span></div>';H+='<div class="lvbar" style="margin-top:10px;"><div class="lvfill" style="width:'+Math.round(ss.i/N*100)+'%;background:var(--teal)"></div></div>';H+='<div class="card" style="margin-top:12px;"><div class="mini">'+ss.year+'　'+esc(q.sect)+' 第'+esc(q.label)+' 題　('+q.pts+'分)</div><div style="font-size:16px;font-weight:500;margin:6px 0 10px;">'+esc(q.text)+'</div>';H+=handBar()+ansArea(ak);H+='<div class="row" style="margin-top:8px;"><button id="showsol" style="flex:1;">'+(ss.showSol?'隱藏詳解':'顯示詳解')+'</button><button data-copy3y="'+ak+'|'+(k||'')+'" style="flex:1;">複製給 AI 評分</button></div>';if(ss.showSol){if(k)H+=solBlock(k);else H+='<div class="soft" style="margin-top:8px;"><div class="mini">此題請參考「類別」分頁對應題型的詳解。</div></div>';}H+='<div class="mini" style="margin:10px 0 4px;">對照後自評（滿分 '+q.pts+'）</div><div class="row"><button data-ssc="'+q.pts+'|10" style="flex:1;">熟</button><button data-ssc="'+q.pts+'|6" style="flex:1;">普通</button><button data-ssc="'+q.pts+'|3" style="flex:1;">不熟</button></div>';H+='</div>';return H;}
  function ansArea(ak){if(st.handMode){return '<div class="soft" style="margin-top:4px;"><div class="mini">✍️ 手寫模式：在紙上或平板手寫app作答 → 拍照/截圖。評分時按下方「複製給 Claude」會複製題目，到 claude.ai 貼上並附這張照片，我就能看你的手寫批改。</div><input type="file" accept="image/*" capture="environment" data-photo="'+ak+'" style="margin-top:6px;"><img data-pv="'+ak+'" alt="" style="display:none;max-width:100%;border-radius:8px;margin-top:6px;"></div>';}return '<textarea data-ans="'+ak+'" rows="4" placeholder="在這裡打字作答…">'+esc(st.statAns[ak]||'')+'</textarea>';}
 function handBar(){return '<div class="row" style="margin-bottom:6px;"><button data-hand="0" class="'+(!st.handMode?'primary':'')+'" style="flex:1;">打字</button><button data-hand="1" class="'+(st.handMode?'primary':'')+'" style="flex:1;">手寫</button></div>';}
 function startMock(){var sel=st.mockSel;var rp=[];RM.forEach(function(ss,si){ss.qs.forEach(function(q,qi){if(q.opts&&q.opts.length>=2)rp.push([si,qi]);});});shuf(rp);rp=rp.slice(0,sel.rmN);var allF=[];for(var sm in window.STATFULL){window.STATFULL[sm].qs.forEach(function(q){allF.push({sem:sm,label:q.label,sect:q.sect,text:q.text,pts:q.pts});});}var noun=allF.filter(function(x){return x.sect==='名詞';}),qa=allF.filter(function(x){return x.sect==='問答';});shuf(noun);shuf(qa);var sf=noun.slice(0,sel.nN).concat(qa.slice(0,sel.qN));st.mock={phase:'rm',rp:rp,ri:0,rmScore:0,picked:null,sf:sf,si:0,sScores:[],showSol:false};}
 function renderMock(){var mk=st.mock;if(!mk){var sel=st.mockSel;var H='<button id="back">← 回首頁</button><div class="card" style="margin-top:12px;"><h2>衝刺模擬考</h2><div class="sub" style="margin-bottom:10px;">仿真實考卷：研方全選擇(自動算分)＋統計(名詞解釋5分/題＋問答10分/題，依配分)。做完給預估成績。</div>';H+='<div class="mini">研方題數(滿分100，每題約 '+(Math.round(100/sel.rmN*10)/10)+' 分)</div><div class="row" style="margin:4px 0 10px;">'+[30,40].map(function(v){return '<button data-rmn="'+v+'" class="'+(sel.rmN===v?'primary':'')+'" style="flex:1;">'+v+' 題</button>';}).join('')+'</div>';H+='<div class="mini">統計規模</div><div class="row" style="margin:4px 0 12px;"><button data-spreset="full" class="'+(sel.nN===8?'primary':'')+'" style="flex:1;">完整(名詞8+問答6)</button><button data-spreset="lite" class="'+(sel.nN===5?'primary':'')+'" style="flex:1;">精簡(名詞5+問答3)</button></div>';H+='<button id="startMock" class="primary" style="width:100%;">開始 →</button></div><div class="mini" style="text-align:center;">目標：研方 70 分、統計 50 分</div>';return H;}if(mk.phase==='rm'){var pr=mk.rp[mk.ri],sem=RM[pr[0]],q=sem.qs[pr[1]],aL=(q.ans||'').toUpperCase().replace(/[^A-E]/g,'').charAt(0);var H='<div style="display:flex;justify-content:space-between;align-items:center;"><button id="back">← 放棄</button><span class="pill">研方 '+(mk.ri+1)+' / '+mk.rp.length+'</span></div>';H+='<div class="lvbar" style="margin-top:10px;"><div class="lvfill" style="width:'+Math.round(mk.ri/mk.rp.length*100)+'%;background:var(--teal)"></div></div>';H+='<div class="card" style="margin-top:12px;"><div class="mini">'+esc(sem.label.split('（')[0])+' Q'+q.n+'</div><div style="font-size:16px;font-weight:500;margin:6px 0 10px;">'+esc(q.q)+'</div>';for(var o=0;o<q.opts.length;o++){var L=q.opts[o].toUpperCase().replace(/[^A-E]/,'').charAt(0)||String.fromCharCode(65+o);var cls='opt';if(mk.picked){if(L===aL)cls+=' ok';else if(L===mk.picked)cls+=' no';}H+='<button class="'+cls+'" data-mopt="'+L+'"'+(mk.picked?' disabled':'')+'>'+esc(q.opts[o])+'</button>';}if(mk.picked){H+='<div class="mini" style="margin-top:6px;color:'+(mk.picked===aL?'var(--ok)':'var(--no)')+';">'+(mk.picked===aL?'答對 ✓':'答錯（正解 '+aL+'）')+'</div><button id="mnext" class="primary" style="width:100%;margin-top:8px;">'+(mk.ri+1>=mk.rp.length?'進入統計題 →':'下一題 →')+'</button>';}H+='</div>';return H;}if(mk.phase==='stat'){if(!mk.sf.length){mk.phase='result';return renderMock();}var q=mk.sf[mk.si],ak='mk:'+mk.si;var H='<div style="display:flex;justify-content:space-between;align-items:center;"><button id="back">← 放棄</button><span class="pill">統計 '+(mk.si+1)+' / '+mk.sf.length+'　'+q.pts+'分</span></div>';H+='<div class="card" style="margin-top:12px;"><div class="mini">'+esc(q.sem)+'　'+esc(q.sect)+'（'+q.pts+'分）</div><div style="font-size:16px;font-weight:500;margin:6px 0 10px;">'+esc(q.text)+'</div>';H+=handBar()+ansArea(ak);H+='<button id="msol" style="width:100%;margin-top:8px;">'+(mk.showSol?'隱藏詳解':'顯示詳解(對照後自評)')+'</button>';if(mk.showSol){var k=statMatch(q.text);if(k)H+=solBlock(k);}H+='<div class="mini" style="margin:10px 0 4px;">自評(滿分'+q.pts+')</div><div class="row"><button data-msc="'+q.pts+'|10" style="flex:1;">熟</button><button data-msc="'+q.pts+'|6" style="flex:1;">普通</button><button data-msc="'+q.pts+'|3" style="flex:1;">不熟</button></div></div>';return H;}if(mk.phase==='result'){var rN=mk.rp.length||1,rF=Math.round(mk.rmScore/rN*100);var sTot=mk.sf.reduce(function(a,b){return a+(b.pts||0);},0)||1,sGot=mk.sScores.reduce(function(a,b){return a+b;},0),sF=Math.round(sGot/sTot*100);var H='<button id="back">← 回首頁</button><div class="card" style="text-align:center;margin-top:12px;"><h2>模擬考結果 · 預估成績</h2>'+cat(rF>=70&&sF>=50?'white':'neutral')+'</div>';H+='<div class="metrics" style="margin-bottom:12px;">'+m(rF,'研方預估','/100')+m(sF,'統計預估','/100')+m(mk.rmScore+'/'+rN,'研方答對','')+m(sGot+'/'+sTot,'統計配分','')+'</div>';H+='<div class="card"><div style="font-size:14px;">研方：'+rF+' 分　'+(rF>=70?'<b style=\"color:var(--ok)\">已達標(70) ✓</b>':'<b style=\"color:var(--no)\">距 70 還差 '+(70-rF)+' 分</b>')+'</div><div style="font-size:14px;margin-top:4px;">統計(自評)：'+sF+' 分　'+(sF>=50?'<b style=\"color:var(--ok)\">已達標(50) ✓</b>':'<b style=\"color:var(--no)\">距 50 還差 '+(50-sF)+' 分</b>')+'</div><div class="mini" style="margin-top:6px;">統計為自評估算(依配分加權)，實際請用「複製給 AI 評分」校準。</div></div>';H+='<div class="row"><button id="copymock" class="primary" style="flex:1;">複製統計作答 → Claude 評分</button><button id="remock" style="flex:1;">再考一次</button></div>';return H;}return '';}

 function rmCatPool(c){var p=[];RM.forEach(function(ss,si){ss.qs.forEach(function(q,qi){if(q.opts&&q.opts.length>=2&&(q.cat||'其他')===c)p.push([si,qi]);});});return p;}
 function rmHalf(c,phase){var p=rmCatPool(c);if(p.length<6)return p.slice();var h=Math.ceil(p.length/2);return phase==='pre'?p.slice(0,h):p.slice(h);}
 function startRMphase(c,phase){var pl=rmHalf(c,phase);shuf(pl);st.sess={pool:pl,i:0,score:0,picked:null,round:'phase',phase:phase,cat:c};st.view='rm';}
 function deltaTxt(rec){var a=rec.pre.s/rec.pre.t,b=rec.post.s/rec.post.t,d=Math.round((b-a)*100);return d>0?'進步 +'+d+'%':(d<0?d+'%':'持平');}
 function pBadge(rec,ph){if(!rec||!rec[ph])return '<span class="bdg off">'+(ph==='pre'?'前測 —':'後測 —')+'</span>';var r=rec[ph];return '<span class="bdg on">'+(ph==='pre'?'前測 ':'後測 ')+r.s+'/'+r.t+'</span>';}
 function pBadgeS(rec,ph){if(!rec||!rec[ph])return '<span class="bdg off">'+(ph==='pre'?'前測 —':'後測 —')+'</span>';return '<span class="bdg on">'+(ph==='pre'?'前測 ':'後測 ')+rec[ph].lv+'</span>';}
 function deltaTxtS(rec){return rec.post.s>rec.pre.s?'更熟了 ↑':(rec.post.s<rec.pre.s?'再加強':'持平');}
 function planCardRM(c,fo){var rec=st.phase['rm:'+c],full=rmCatPool(c).length,small=full<6;
  var H='<div class="card" style="padding:13px;'+(fo?'border:1.5px solid var(--sage);background:var(--surface2);':'')+'"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;"><b>'+esc(c)+'</b><span class="mini">'+full+' 題'+(small?' · 題量少，共用題':'')+'</span></div>';
  H+='<div style="margin:9px 0;">'+pBadge(rec,'pre')+'　'+pBadge(rec,'post')+((rec&&rec.pre&&rec.post)?'　<span class="mini" style="color:var(--clay);font-weight:500;">'+deltaTxt(rec)+'</span>':'')+'</div>';
  H+='<div class="row"><button data-rmpre="'+esc(c)+'" class="primary" style="flex:1;">① 前測</button><button data-rmtip="'+esc(c)+'" style="flex:1;">② 看重點</button><button data-rmpost="'+esc(c)+'" style="flex:1;">③ 後測</button></div>';
  if(st.planTip===c)H+='<div class="soft" style="margin-top:9px;font-size:13.5px;"><b style="color:var(--olive);">解題重點：</b>'+esc(RMTIP(c))+'</div>';
  return H+'</div>';}
 function planCardStat(key,tp,fo){var rec=st.phase['st:'+key];
  var H='<div class="card" style="padding:13px;'+(fo?'border:1.5px solid var(--sage);background:var(--surface2);':'')+'"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px;"><span style="font-weight:500;font-size:14px;">'+(tp.star?'★ ':'')+esc(tp.title)+'</span><span class="pill">'+esc(tp.tier.split('（')[0])+'</span></div>';
  H+='<div style="margin:9px 0;">'+pBadgeS(rec,'pre')+'　'+pBadgeS(rec,'post')+((rec&&rec.pre&&rec.post)?'　<span class="mini" style="color:var(--clay);font-weight:500;">'+deltaTxtS(rec)+'</span>':'')+'</div>';
  H+='<div class="row"><button data-stpre="'+key+'" class="primary" style="flex:1;">① 前測</button><button data-sttip="'+key+'" style="flex:1;">② 看詳解</button><button data-stpost="'+key+'" style="flex:1;">③ 後測</button></div>';
  if(st.planTip==='st:'+key)H+=solBlock(key);
  return H+'</div>';}
 function renderPlan(){
  if(st.planStat)return renderPlanStat();
  var pm=st.planMode||'rm';
  var H='<button id="back">← 回首頁</button><h2 style="margin-top:12px;">三階段練習</h2>';
  if(st.planFocus){var f=st.planFocus;
   H+='<div class="mini" style="margin:10px 0 6px;color:var(--clay);font-weight:600;">📌 今日任務題型 · 直接從 ① 前測開始</div>';
   if(f.sub==='rm')H+=planCardRM(f.key,true);else{var fk=findKey(f.key);if(fk)H+=planCardStat(f.key,fk.tp,true);}
   H+='<div class="wk" id="planShowAll" style="margin:8px 0 12px;"><span style="font-weight:600;font-size:14px;">看全部題型</span><span class="mini">'+(st.planAll?'收合 ▴':'展開 ▾')+'</span></div>';
   if(!st.planAll)return H;
  }
  H+='<div class="soft" style="margin-bottom:11px;font-size:13px;line-height:1.8;">①<b>前測</b>：還沒看重點就先做，量出真實起點（錯很多很正常）。<br>②讀統整重點 / 看詳解。<br>③<b>後測</b>：再測一次，看自己進步多少。<br>④累積幾輪後做 <b>實際模擬考</b>。<div class="mini" style="margin-top:5px;">前測 → 後測的分數差，就是你進步的證據。</div></div>';
  H+='<div class="row" style="margin-bottom:11px;"><button data-pmode="rm" class="'+(pm==='rm'?'primary':'')+'" style="flex:1;">研究方法</button><button data-pmode="stat" class="'+(pm==='stat'?'primary':'')+'" style="flex:1;">統計</button></div>';
  if(pm==='rm'){var rc=rmCats();rc.o.sort(function(a,b){return rc.m[b]-rc.m[a];});
   H+='<div class="sub" style="margin-bottom:8px;">每類題庫對半切：①前測用前半、③後測用後半（不同題、相同概念）。</div>';
   rc.o.forEach(function(c){H+=planCardRM(c,false);});
  }else{H+='<div class="sub" style="margin-bottom:8px;">統計用同一題：①前測憑記憶先寫 → ②看詳解 → ③後測再寫，比較熟練度。</div>';
   statList().forEach(function(g){H+='<div class="mini" style="margin:10px 0 6px;">'+g[1]+'</div>';STAT[g[0]].forEach(function(tp,ti){H+=planCardStat(g[0]+ti,tp,false);});});
  }
  H+='<div class="card"><h2>④ 實際模擬測驗</h2><div class="sub" style="margin-bottom:8px;">累積幾個題型後，用整卷模擬考檢驗（研方＋統計，給預估成績）。</div><button id="planMock" class="primary" style="width:100%;">開始模擬考 →</button></div>';
  return H;}
 function renderPlanStat(){var ps=st.planStat,fk=findKey(ps.key);if(!fk)return renderPlan();var tp=fk.tp,ak='plan:'+ps.key+':'+ps.phase;
  var H='<button id="planback">← 回三階段</button><div class="card" style="margin-top:12px;"><div class="mini">'+(ps.phase==='pre'?'① 前測（先別看詳解，憑記憶寫）':'③ 後測（讀完重點後再寫一次）')+'</div><div style="font-size:16px;font-weight:600;margin:6px 0;">'+(tp.star?'★ ':'')+esc(tp.title)+'</div><div class="sub" style="margin-bottom:8px;">寫出這個題型的解法步驟、關鍵公式或判斷邏輯。</div>';
  H+=handBar()+ansArea(ak);
  if(ps.phase==='pre'&&!st.planSol)H+='<div class="mini" style="margin-top:8px;color:var(--hint);">🔒 前測階段建議先不看詳解，寫完直接自評。</div>';
  H+='<div class="row" style="margin-top:8px;"><button data-plansol="1" style="flex:1;">'+(st.planSol?'隱藏詳解':'顯示詳解')+'</button><button data-plangrade="'+ak+'|'+ps.key+'" style="flex:1;">複製給 AI 評分</button></div>';
  if(st.planSol)H+=solBlock(ps.key);
  H+='<div class="mini" style="margin:11px 0 4px;">寫完自評（記錄到三階段）：</div><div class="row"><button data-plansc="熟" style="flex:1;">熟</button><button data-plansc="普通" style="flex:1;">普通</button><button data-plansc="不熟" style="flex:1;">不熟</button></div></div>';
  return H;}

 function _ptxt(v){if(v==null)return '';if(Array.isArray(v))return v.map(function(x){x=(''+x).trim();return x?(/^[・•-]/.test(x)?x:'・'+x):'';}).filter(Boolean).join('\n');if(typeof v==='object'){var a=[];for(var k in v){var t=_ptxt(v[k]);if(t)a.push(t);}return a.join('\n');}return ''+v;} function _normPaper(o){o=o||{};['summary','findings','contribution','method','gap','limit','future'].forEach(function(k){o[k]=_ptxt(o[k]);});['tldr','keywords','title','authors','year','journal','quartile','if'].forEach(function(k){o[k]=(o[k]==null?'':(''+o[k]));});return o;} function gkey(){return st.gkey||localStorage.getItem('pearl_gkey')||'';}
 function paperToast(m){var d=document.createElement('div');d.textContent=m;d.style.cssText='position:fixed;left:50%;top:16%;transform:translateX(-50%) scale(.9);background:var(--sage);color:#FAF6EF;font-weight:600;padding:12px 22px;border-radius:14px;z-index:9999;box-shadow:0 6px 24px rgba(0,0,0,.25);opacity:0;transition:all .3s;font-size:15px;';document.body.appendChild(d);requestAnimationFrame(function(){d.style.opacity='1';d.style.transform='translateX(-50%) scale(1)';});setTimeout(function(){d.style.opacity='0';setTimeout(function(){d.remove();},300);},2100);}
 function geminiAnalyze(file,cb){
  var fr=new FileReader();
  fr.onload=function(){
   var b64=(''+fr.result).split(',')[1]||'';
   var prompt='你是資深學術論文導讀者，讀者是博士生。請仔細閱讀整份 PDF，回傳純 JSON（不要 markdown 圍欄、不要多餘文字）。欄位：tldr, title, authors, year, journal, quartile, if, keywords, summary, findings, contribution, method, gap, limit, future。【tldr】用一兩句直白的繁體中文講清楚「這篇到底在研究什麼、最重要的發現是什麼」，讓人一眼看懂這篇在幹嘛。【keywords】3到6個關鍵詞，用逗號分隔。【summary/findings/contribution/method/gap/limit/future】一律繁體中文、寫得具體（盡量帶出研究對象/樣本數/變項/理論/方法名稱/關鍵數據與主要結果），每段 2到4 點、每點用「・」開頭；其中 findings 必須寫出論文實際的發現與結論（要有內容、不要空泛），summary 講清楚研究目的與脈絡，method 講資料來源/樣本/分析方法。title/authors/journal 照原文；quartile 如 Q1；if 為影響指數數字；不確定的數值就留空字串。';
   var body={contents:[{parts:[{text:prompt},{inline_data:{mime_type:'application/pdf',data:b64}}]}],generationConfig:{temperature:0.4,maxOutputTokens:8192,responseMimeType:'application/json'}};
   var MODELS=['gemini-2.5-flash','gemini-2.0-flash'];var busy=document.getElementById('paperBusy');
   function attempt(i){
    var model=MODELS[Math.min(i,MODELS.length-1)];
    if(busy&&i>0)busy.textContent='🤖 AI 忙線中，自動重試…（第 '+i+' 次，可能要等一下）';
    fetch('https://generativelanguage.googleapis.com/v1beta/models/'+model+':generateContent?key='+encodeURIComponent(gkey()),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})
     .then(function(r){return r.json().then(function(j){return {st:r.status,j:j};});})
     .then(function(res){var j=res.j;
      if(j&&j.candidates&&j.candidates[0]){try{cb(null,_normPaper(JSON.parse(j.candidates[0].content.parts[0].text)));}catch(e){cb('解析失敗：'+e,null);}return;}
      var msg=(j&&j.error&&j.error.message)||('HTTP '+res.st);
      var bz=(res.st===503||res.st===429||/high demand|overload|UNAVAILABLE|RESOURCE_EXHAUSTED|try again/i.test(msg));
      if(bz&&i<5){setTimeout(function(){attempt(i+1);},2000+i*2500);}
      else cb(bz?'😮\u200d💨 Gemini 現在流量爆滿（這是 Google 端暫時的狀況，不是你的問題）。等一兩分鐘再上傳一次就好。':'分析失敗：'+msg,null);})
     .catch(function(e){if(i<5){setTimeout(function(){attempt(i+1);},2000+i*2500);}else cb('呼叫失敗（網路或金鑰問題）：'+e,null);});
   }
   attempt(0);
  };
  fr.readAsDataURL(file);
 }
 function analyzePdf(file){if(!file)return;if(!gkey()){alert('請先設定 Gemini 金鑰');return;}_pendingErr='';_pendingPdf=file;var b=document.getElementById('paperBusy');if(b){b.style.display='block';b.textContent='🤖 AI 分析中…（約 20–40 秒，請勿關閉）';}geminiAnalyze(file,function(err,o){if(err){_pendingErr=err;render();return;}_pendingPdf=null;_pendingErr='';o=o||{};var id=nowMs();st.papers.push({id:id,title:o.title||file.name,authors:o.authors||'',year:o.year||'',journal:o.journal||'',quartile:o.quartile||'',ifv:o.if||'',tldr:o.tldr||'',keywords:o.keywords||'',summary:o.summary||'',findings:o.findings||'',contribution:o.contribution||'',method:o.method||'',gap:o.gap||'',limit:o.limit||'',future:o.future||'',reflection:'',read:false,awarded:false});st.curPaper=id;save();render();paperToast('🤖 分析完成！整合成你的心得就能領珍珠');});}
 function renderPaper(){
  if(st.curPaper!=null)return renderPaperDetail();
  var H='<button id="back">← 回首頁</button><h2 style="margin-top:12px;">📄 論文閱讀管理</h2>';
  H+='<div class="sub" style="margin-bottom:10px;">上傳論文 PDF → AI 自動分析 → 你把重點整合成自己的心得 → 領珍珠 🦪（珍珠值與資格考共用）</div>';
  if(!gkey()){H+='<div class="card" style="border-color:var(--no);"><div class="sub" style="color:var(--no);">⚠️ 還沒設定 Gemini API 金鑰，無法 AI 分析。</div><button id="setKey" class="primary" style="margin-top:8px;width:100%;">🔑 設定 Gemini API 金鑰</button></div>';}
  else{H+='<div class="row" style="margin-bottom:6px;"><label class="primary" style="flex:1;text-align:center;cursor:pointer;padding:11px 14px;border-radius:10px;font-size:15px;">➕ 上傳 PDF 分析<input id="pdfIn" type="file" accept="application/pdf" style="display:none;"></label><button id="setKey" style="flex:0 0 auto;">🔑</button></div>';}
  H+='<div id="paperBusy" class="sub" style="display:none;color:var(--clay);margin:6px 0 8px;">🤖 AI 分析中…（約 20–40 秒，請勿關閉）</div>';if(_pendingPdf&&_pendingErr)H+='<div class="card" style="border-color:var(--no);"><div style="color:var(--no);font-size:13px;white-space:pre-wrap;line-height:1.6;">❌ '+esc(_pendingErr)+'</div><div class="mini" style="margin:6px 0;">檔案還在（'+esc((_pendingPdf.name||'').slice(0,28))+'），不用重選</div><button id="pdfRetry" class="primary" style="width:100%;">🔄 重試</button></div>';
  var read=st.papers.filter(function(p){return p.read;}).length;
  var _ym=ymd(now).slice(0,7);function _rd(p){return p.readDate||'';}
  var mY=st.papers.filter(function(p){return p.read&&_rd(p).slice(0,7)===_ym;}).length;
  var wZ=st.papers.filter(function(p){return p.read&&_rd(p)&&diff(new Date(_rd(p)+'T00:00:00'),now)>=0&&diff(new Date(_rd(p)+'T00:00:00'),now)<=6;}).length;
  if(st.papers.length){var stt='📚 已讀 '+read+' 篇　·　本月 '+mY+' 篇';if(mY>=4)stt+='　·　本週 '+wZ+' 篇';H+='<div class="card" style="padding:11px 14px;text-align:center;font-weight:600;color:var(--clay);">'+stt+'</div>';}
  if(!st.papers.length)H+='<div class="card" style="text-align:center;color:var(--muted);">還沒有論文～上傳第一篇 PDF 開始吧！</div>';
  else st.papers.slice().reverse().forEach(function(p){H+='<div class="ttl" data-paper="'+p.id+'"><span style="font-size:13.5px;">'+(p.read?'✅ ':'⭕ ')+esc(p.title||'(未命名)')+'<div class="mini">'+esc(p.authors||'')+(p.year?' · '+p.year:'')+(p.journal?' · '+esc(p.journal):'')+'</div></span><span class="pill">'+(p.read?'看心得':'寫心得 →')+'</span></div>';});
  return H;}
 function renderPaperDetail(){
  var p=st.papers.filter(function(x){return x.id===st.curPaper;})[0];if(!p)return renderPaper();
  var H='<button id="paperBack">← 論文清單</button><div class="card" style="margin-top:12px;"><h2 style="font-size:16px;">'+esc(p.title||'(未命名)')+'</h2><div class="mini" style="margin-top:3px;">'+esc(p.authors||'')+(p.year?' · '+p.year:'')+'</div>';
  if(p.journal||p.quartile||p.ifv)H+='<div class="mini" style="margin-top:3px;color:var(--clay);">'+esc(p.journal||'')+(p.quartile?' · '+esc(p.quartile):'')+(p.ifv?' · IF '+esc(p.ifv):'')+'</div>';
  H+='</div>';
  function fld(l,v){return v?('<div class="card" style="padding:12px;"><div class="mini" style="color:var(--clay);font-weight:600;margin-bottom:5px;">'+l+'</div><div style="font-size:14px;white-space:pre-wrap;line-height:1.7;">'+esc(v)+'</div></div>'):'';}
  H+=(p.tldr?'<div class="soft" style="border-left:3px solid var(--clay);font-size:15px;font-weight:600;margin-bottom:11px;line-height:1.75;">📌 一句話看懂：'+esc(p.tldr)+'</div>':'');if(p.keywords)H+='<div style="margin-bottom:11px;">'+esc(p.keywords).split(/[,，、;；]/).map(function(k){k=k.trim();return k?'<span style="display:inline-block;font-size:12px;background:var(--surface2);color:var(--muted);border-radius:8px;padding:2px 9px;margin:0 5px 5px 0;">#'+k+'</span>':'';}).join('')+'</div>';H+=fld('📑 研究摘要（在做什麼）',p.summary)+fld('🔑 主要發現／結果',p.findings)+fld('💡 主要貢獻',p.contribution)+fld('🔬 研究方法',p.method)+fld('🕳️ 研究缺口',p.gap)+fld('⚠️ 研究限制',p.limit)+fld('🔮 未來方向',p.future);
  H+='<div class="card"><h2>✍️ 我的心得　<span class="mini">把 AI 重點整合成你自己的理解</span></h2><div class="sub" style="margin-bottom:6px;">這篇跟你研究（AgeTech／高齡福祉）的關聯？你的評價？可借鑑之處？</div>';
  H+='<textarea id="reflIn" rows="5" placeholder="用自己的話寫下整合後的心得…">'+esc(p.reflection||'')+'</textarea>';
  H+='<div class="mini" style="margin:8px 0 4px;">'+(p.awarded?'🦪 已領珍珠 +20':'寫完心得按下方，領 20 珍珠值')+'</div>';
  H+='<button id="finishPaper" class="primary" style="width:100%;">'+(p.read?'💾 更新心得':'✅ 完成閱讀，領珍珠 🦪')+'</button>';H+='<button id="gradeRefl" style="width:100%;margin-top:8px;">📤 請 AI 評我的心得（給回饋）</button>';
  H+='<button id="delPaper" style="width:100%;margin-top:8px;color:var(--no);">🗑️ 刪除這篇</button></div>';
  return H;}
 function aiOpen(txt){try{if(navigator.clipboard)navigator.clipboard.writeText(txt);}catch(e){}var old=document.getElementById('aiPick');if(old)old.remove();var d=document.createElement('div');d.id='aiPick';d.style.cssText='position:fixed;left:50%;bottom:16px;transform:translateX(-50%);background:var(--surface);border:.5px solid var(--line);border-radius:16px;padding:12px 14px;z-index:9999;box-shadow:0 8px 30px rgba(0,0,0,.28);max-width:94vw;';d.innerHTML='<div class="mini" style="text-align:center;margin-bottom:8px;">✅ 已複製評分內容，選一個 AI 貼上即可評分</div><div class="row" style="justify-content:center;flex-wrap:nowrap;"><button data-ai="https://chatgpt.com/" style="flex:1;">🟢 ChatGPT</button><button data-ai="https://gemini.google.com/app" style="flex:1;">🔷 Gemini</button><button data-ai="https://claude.ai/new" class="primary" style="flex:1;">🟣 Claude</button></div><div style="text-align:center;margin-top:7px;"><a class="copy" id="aiClose" style="cursor:pointer;">關閉</a></div>';document.body.appendChild(d);d.querySelectorAll('[data-ai]').forEach(function(b){b.onclick=function(){window.open(b.getAttribute('data-ai'),'_blank');d.remove();};});var c=document.getElementById('aiClose');if(c)c.onclick=function(){d.remove();};}
  function render(){var app=document.getElementById('app');
  if(st.view==='home')app.innerHTML=renderHome();
  else if(st.view==='rm')app.innerHTML=(st.sess?renderRMq():renderRMmenu());
  else if(st.view==='stat')app.innerHTML=renderStat(st._focus);
  else if(st.view==='wrong')app.innerHTML=renderWrong();
  else if(st.view==='mock')app.innerHTML=renderMock();
  else if(st.view==='plan')app.innerHTML=renderPlan();
  else if(st.view==='paper')app.innerHTML=renderPaper();
  st._focus=null;bind();}
 function bind(){var app=document.getElementById('app');function on(id,fn){var el=document.getElementById(id);if(el)el.onclick=fn;}
  on('back',function(){st.view='home';st.sess=null;st.statSess=null;st.mock=null;st.planStat=null;st.planFocus=null;render();});on('planback',function(){st.view='plan';st.sess=null;st.planStat=null;st.planSol=false;render();});on('planback2',function(){st.view='plan';st.sess=null;st.planStat=null;st.planSol=false;render();});app.querySelectorAll('[data-sortord]').forEach(function(el){el.onclick=function(){st.yearDesc=el.getAttribute('data-sortord')==='1';render();};});app.querySelectorAll('[data-hand]').forEach(function(el){el.onclick=function(){var ta=app.querySelector('[data-ans]');if(ta)st.statAns[ta.getAttribute('data-ans')]=ta.value;st.handMode=el.getAttribute('data-hand')==='1';render();};});app.querySelectorAll('[data-photo]').forEach(function(el){el.onchange=function(){if(!el.files||!el.files[0])return;var fr=new FileReader();fr.onload=function(){var img=app.querySelector('img[data-pv="'+el.getAttribute('data-photo')+'"]');if(img){img.src=fr.result;img.style.display='block';}};fr.readAsDataURL(el.files[0]);};});app.querySelectorAll('[data-goplan]').forEach(function(el){el.onclick=function(){var pp=el.getAttribute('data-goplan').split(':');st.view='plan';st.planMode=(pp[1]==='rm'?'rm':'stat');st.planFocus=pp[2]?{sub:pp[1],key:pp[2]}:null;st.planAll=false;render();};});
  if(st.view==='home'){
   var ce=document.getElementById('cat');if(ce&&ce.getAttribute('data-cat')==='black'){ce.style.animation='none';ce.style.transition='transform .2s cubic-bezier(.34,1.56,.64,1)';ce.style.willChange='transform';var dn=0;var dz=function(cx,cy){ce.style.transform='none';var r=ce.getBoundingClientRect();var hx=r.left+r.width/2,hy=r.top+r.height/2;var a=Math.atan2(hy-cy,hx-cx),nx=Math.cos(a)*72,ny=Math.sin(a)*32;nx=Math.max(-95,Math.min(95,nx));ny=Math.max(-46,Math.min(46,ny));ce.style.transform='translate('+Math.round(nx)+'px,'+Math.round(ny)+'px) rotate('+(nx>0?7:-7)+'deg)';dn++;var pe=document.getElementById('purr');if(pe)pe.textContent=(dn>=5?'好啦…想摸我，就先把今天那格打勾嘛 😼':pick(DODGE,dn));clearTimeout(ce._dt);ce._dt=setTimeout(function(){ce.style.transform='translate(0,0)';},800);};ce.onmousemove=function(e){dz(e.clientX,e.clientY);};ce.onmouseenter=function(e){dz(e.clientX,e.clientY);};ce.onclick=function(e){dz(e.clientX,e.clientY);};ce.ontouchstart=function(e){var t=e.touches&&e.touches[0];if(t)dz(t.clientX,t.clientY);if(e.cancelable)e.preventDefault();};}else if(ce){ce.onclick=function(){ce.classList.remove('wig');void ce.offsetWidth;ce.classList.add('wig');st.aff=(st.aff||0)+1;save();var pe=document.getElementById('purr');if(pe)pe.textContent=pick(PURR,st.aff);};}
   on('addBtn',function(){var v=document.getElementById('inp').value.trim();if(!v)return;var d=new Date();st.entries.push({date:ymd(d),t:stamp(d),b:v});pts(6);save();render();});
   var _ra=document.getElementById('remAm');if(_ra)_ra.onchange=function(){st.rem.am=_ra.value||'08:00';st.rem.fired={};save();};
   var _rp=document.getElementById('remPm');if(_rp)_rp.onchange=function(){st.rem.pm=_rp.value||'21:00';st.rem.fired={};save();};
   on('remOn',function(){st.rem.on=true;st.rem.fired={};st.rem.day=ymd(new Date());if(_ra)st.rem.am=_ra.value||st.rem.am;if(_rp)st.rem.pm=_rp.value||st.rem.pm;save();var done=function(){render();if(window._pearlRemCheck)window._pearlRemCheck();};if(window.Notification&&Notification.requestPermission){try{var pr=Notification.requestPermission(done);if(pr&&pr.then)pr.then(done);}catch(e){done();}}else done();});
   on('remOff',function(){st.rem.on=false;save();render();});
   on('remTest',function(){if(window._pearlPreview)window._pearlPreview();});
   app.querySelectorAll('[data-remhelp]').forEach(function(el){el.onclick=function(){st.rem._help=!st.rem._help;save();render();};});
   on('filtBtn',function(){var k=ymd(new Date());st.filter[k]=(st.filter[k]||0)+1;pts(1);save();var pn=document.getElementById('filtPanel');pn.style.display='block';document.getElementById('filtCnt').textContent='你今天已經抓到濾鏡 '+st.filter[k]+' 次——每抓到一次，你就離它遠半步。';});
   on('pRM',function(){st.view='rm';st.sess=null;render();});
   on('pST',function(){st.view='stat';render();});on('pPlan',function(){st.view='plan';st.planFocus=null;st.planAll=false;st.planMode='rm';render();});var hs=document.getElementById('hubSel');if(hs)hs.onchange=function(){if(hs.value==='paper'){st.view='paper';st.curPaper=null;render();}};
   on('pW',function(){st.view='wrong';render();});on('goMock',function(){st.view='mock';st.mock=null;render();});
   var gt=document.getElementById('goTask');if(gt)gt.onclick=function(){var lk=gt.getAttribute('data-link');if(lk.indexOf('plan')===0){var pp=lk.split(':');st.view='plan';st.planMode=(pp[1]==='rm'?'rm':'stat');st.planFocus=pp[2]?{sub:pp[1],key:pp[2]}:null;st.planAll=false;}else if(lk.indexOf('rm')===0){st.view='rm';if(lk==='rm:wrong'){startRM('wrong');}else{st.sess=null;}}else{st.view='stat';st._focus=findTopic(lk);}render();};
   app.querySelectorAll('[data-gonav]').forEach(function(el){el.onclick=function(){var lk=el.getAttribute('data-gonav');if(lk.indexOf('plan')===0){var pp=lk.split(':');st.view='plan';st.planMode=(pp[1]==='rm'?'rm':'stat');st.planFocus=pp[2]?{sub:pp[1],key:pp[2]}:null;st.planAll=false;}else if(lk.indexOf('rm')===0){st.view='rm';if(lk==='rm:wrong'){startRM('wrong');}else{st.sess=null;}}else{st.view='stat';st._focus=findTopic(lk);}render();};});
   on('schToggle',function(){var sc=document.getElementById('sch');if(sc.style.display==='none'){sc.style.display='block';sc.innerHTML=schedHTML();bindSched();}else sc.style.display='none';});
   on('rst',function(){if(confirm('確定清空所有資料（珍珠、進度、珍珠值、錯題本）？')){st={entries:SEED.slice(),done:{},open:{},filter:{},statOpen:{},statAns:{},wrongRM:[],wrongStat:[],points:0,aff:0,view:'home',sess:null,awd:{},mem:{},phase:{}};save();render();}});on('expBtn',function(){var data=localStorage.getItem(KEY)||'{}';var blob=new Blob([data],{type:'application/json'});var a=document.createElement('a');a.href=URL.createObjectURL(blob);var d=new Date();a.download=(SHARE?'資格考備份_':'珍珠日記備份_')+d.getFullYear()+p2(d.getMonth()+1)+p2(d.getDate())+'.json';document.body.appendChild(a);a.click();a.remove();});var imp=document.getElementById('impInput');if(imp)imp.onchange=function(){if(!imp.files||!imp.files[0])return;var fr=new FileReader();fr.onload=function(){try{JSON.parse(fr.result);localStorage.setItem(KEY,fr.result);alert('匯入成功！將重新載入頁面。');location.reload();}catch(e){alert('檔案格式不正確，請選擇正確的備份檔。');}};fr.readAsText(imp.files[0]);};on('syncConnect',function(){var v=document.getElementById('syncIn');var code=v?v.value.trim():'';if(!code){alert('請先輸入同步碼');return;}st.syncCode=code;st._cloudPending=null;cloudPull(function(c){if(c&&c.data){st._cloudPending=c;render();}else{save();st._syncMsg='已連線，已上傳本機';render();}});});on('useCloud',function(){if(st._cloudPending)applyCloud(st._cloudPending);st._cloudPending=null;st._syncMsg='已下載雲端';render();});on('useLocal',function(){st._cloudPending=null;cloudPush();st._syncMsg='已上傳本機';render();});on('syncNow',function(){cloudPull(function(c){if(c&&(c.ts||0)>(st._ts||0)){applyCloud(c);st._syncMsg='已拉回雲端較新版';}else{cloudPush();st._syncMsg='已同步';}render();});});on('syncOff',function(){st.syncCode='';st._cloudPending=null;save();render();});
   app.querySelectorAll('[data-toggle]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-toggle');if(st.done[k]){delete st.done[k];pts(-12);}else{st.done[k]=1;pts(12);var dy=days.filter(function(x){return x.id===k;})[0];if(dy&&dy.link&&dy.link.indexOf('stat:')===0)seedMem(dy.link.replace('stat:',''));}save();render();};});
   app.querySelectorAll('[data-copy]').forEach(function(el){el.onclick=function(){var i=+el.getAttribute('data-copy');var en=st.entries.slice().reverse()[i];var t=(en.t?en.t+'　':'')+en.b;if(navigator.clipboard)navigator.clipboard.writeText(t);el.textContent='已複製';setTimeout(function(){el.textContent='複製';},1200);};});
   app.querySelectorAll('[data-del]').forEach(function(el){el.onclick=function(){var i=+el.getAttribute('data-del');if(confirm('刪除這一筆？')){st.entries.splice(st.entries.length-1-i,1);save();render();}};});app.querySelectorAll('[data-review]').forEach(function(el){el.onclick=function(){st.view='stat';st._focus=findKey(el.getAttribute('data-review'));render();};});app.querySelectorAll('[data-gowrong]').forEach(function(el){el.onclick=function(){st.view='wrong';render();};});
  } else if(st.view==='rm'){
   app.querySelectorAll('[data-rmmode]').forEach(function(el){el.onclick=function(){st.rmMode=el.getAttribute('data-rmmode');render();};});app.querySelectorAll('[data-rm]').forEach(function(el){el.onclick=function(){startRM(el.getAttribute('data-rm'));render();};});
   app.querySelectorAll('[data-opt]').forEach(function(el){el.onclick=function(){var s=st.sess;if(s.picked)return;s.picked=el.getAttribute('data-opt');var pr=s.pool[s.i],q=RM[pr[0]].qs[pr[1]];var ansL=(q.ans||'').toUpperCase().replace(/[^A-E]/g,'').charAt(0);
    if(s.picked===ansL){s.score++;pts(1);if(s.round==='wrong'){st.wrongRM=st.wrongRM.filter(function(w){return!(w[0]==pr[0]&&w[1]==pr[1]);});pts(2);}}
    else{if(s.phase!=='pre'&&!inWrong(pr[0],pr[1]))st.wrongRM.push([pr[0],pr[1]]);}save();render();};});
   on('next',function(){st.sess.i++;st.sess.picked=null;if(st.sess.i>=st.sess.pool.length){if(st.sess.phase){st.phase['rm:'+st.sess.cat]=st.phase['rm:'+st.sess.cat]||{};st.phase['rm:'+st.sess.cat][st.sess.phase]={s:st.sess.score,t:st.sess.pool.length};}var td=todayDay();if(td&&!st.done[td.id]&&(td.subj==='研方'||(td.subj==='模擬'&&td.link&&td.link.indexOf('rm')===0))){st.done[td.id]=1;pts(12);st.sess.markedToday=true;}save();}render();});
   on('again',function(){startRM(st.sess.round);render();});
   on('logit',function(){var d=new Date();st.entries.push({date:ymd(d),t:stamp(d),b:'今天刷了一輪研方選擇題，答對 '+st.sess.score+'/'+st.sess.pool.length+'。'});pts(6);save();st.view='home';st.sess=null;render();});
  } else if(st.view==='stat'){
   app.querySelectorAll('[data-smode]').forEach(function(el){el.onclick=function(){st.statMode=el.getAttribute('data-smode');if(st.statMode!=='year')st.statYear=null;render();};});app.querySelectorAll('[data-statyear]').forEach(function(el){el.onclick=function(){var v=el.getAttribute('data-statyear');st.statYear=v||null;render();};});on('statstart',function(){st.statSess={year:st.statYear,i:0,showSol:false,scores:[]};render();});function saveTA(){var ta=app.querySelector('[data-ans]');if(ta)st.statAns[ta.getAttribute('data-ans')]=ta.value;}on('sback',function(){saveTA();st.statSess=null;save();render();});on('sback2',function(){st.statSess=null;render();});on('showsol',function(){saveTA();st.statSess.showSol=!st.statSess.showSol;save();render();});on('statnext',function(){saveTA();st.statSess.i++;st.statSess.showSol=false;save();render();});app.querySelectorAll('[data-ssc]').forEach(function(el){el.onclick=function(){saveTA();var pr=el.getAttribute('data-ssc').split('|'),pts=+pr[0],lv=+pr[1];st.statSess.scores=st.statSess.scores||[];st.statSess.scores.push(Math.round(pts*lv/10));st.statSess.i++;st.statSess.showSol=false;save();render();};});on('copyyear',function(){var ss=st.statSess,fq=fullQs(ss.year),L=[];fq.forEach(function(q,i){var a=st.statAns['ys:'+ss.year+':'+i];if(a&&a.trim())L.push(q.sect+q.label+'('+q.pts+'分) '+q.text+'\n我的作答：'+a);});var txt='請依詳解「逐題分開」批改'+ss.year+'整年統計作答，依各題配分給分，並給：🏷️判定/得分/✅對的/❌失分點/🎯正確理由/✍️滿分版/💡口訣，最後給總分。\n\n'+L.join('\n\n');aiOpen(txt);});app.querySelectorAll('[data-copy3y]').forEach(function(el){el.onclick=function(){saveTA();var pr=el.getAttribute('data-copy3y').split('|'),ak=pr[0],key=pr[1],y=ak.split(':');var q=fullQs(y[1])[+y[2]];var title=key?findKey(key).tp.title:'統計';var txt=gradePrompt(title,q.sect+q.label+'('+q.pts+'分) '+q.text,(st.handMode?'(我已在 Claude 對話附上手寫照片)':(st.statAns[ak]||'(尚未作答)')));if(navigator.clipboard)navigator.clipboard.writeText(txt);aiOpen(txt);el.textContent='已複製 ✓';setTimeout(function(){el.textContent='複製給 AI 評分';},2000);};});app.querySelectorAll('[data-yq]').forEach(function(el){el.onclick=function(){var v=el.getAttribute('data-yq');st.statOpen[v]=!st.statOpen[v];save();render();};});
   app.querySelectorAll('[data-dayexp]').forEach(function(el){el.onclick=function(){var dk=el.getAttribute('data-dayexp');var dy=days.filter(function(x){return 'd:'+x.id===dk;})[0];var cur=(dk in st.statOpen)?st.statOpen[dk]:(dy?same(dy.date,now):false);st.statOpen[dk]=!cur;save();render();};});
   app.querySelectorAll('[data-stat]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-stat');st.statOpen[k]=!st.statOpen[k];save();render();};});app.querySelectorAll('[data-sq]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-sq');st.statOpen[k]=!st.statOpen[k];save();render();};});app.querySelectorAll('[data-solq]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-solq');st.statOpen[k+'_s']=!st.statOpen[k+'_s'];save();render();};});app.querySelectorAll('[data-copy3]').forEach(function(el){el.onclick=function(){var sk=el.getAttribute('data-copy3'),pr=sk.split('|'),fk=findKey(pr[0]),y=fk.tp.years[+pr[1]],ans=st.statAns[sk]||'(尚未作答)';var txt='請依詳解逐題批改這一題（不要只給總結）。請依序給：🏷️判定(一句話標籤，如「方向對、理由錯」)、得分(/10)、✅對的地方、❌關鍵失分點(若踩到常見陷阱要點名並引用詳解的陷阱提醒)、🎯正確理由(白話)、✍️滿分版作答(可直接背的完整範例)、💡口訣。用白話、鼓勵但誠實。\n\n【題型】'+fk.tp.title+'\n【題目】'+y[0]+'('+y[1]+') '+y[2]+'\n【我的作答】'+ans;if(navigator.clipboard)navigator.clipboard.writeText(txt);aiOpen(txt);el.textContent='已複製 ✓';setTimeout(function(){el.textContent='複製給 AI 評分';},2200);};});app.querySelectorAll('[data-copyall]').forEach(function(el){el.onclick=function(){var key=el.getAttribute('data-copyall'),fk=findKey(key),lines=[];fk.tp.years.forEach(function(y,yi){var a=st.statAns[key+'|'+yi];if(a&&a.trim())lines.push('第'+(yi+1)+'題 '+y[0]+'('+y[1]+') '+y[2]+'\n我的作答：'+a);});if(!lines.length){el.textContent='（這題型還沒有作答）';setTimeout(function(){el.textContent='複製本題型「全部作答」→ 請 AI 逐題評分';},1800);return;}var txt='請依詳解「逐題分開」批改(不要只給一個總結)。每一子題都依序給：🏷️判定、得分(/10)、✅對的地方、❌關鍵失分點(踩到陷阱要點名並引用詳解的陷阱提醒)、🎯正確理由(白話)、✍️滿分版作答(可直接背)、💡口訣；最後再給總分與「今天最該補強的一點」。用白話、鼓勵但誠實。\n\n題型：'+fk.tp.title+'\n\n'+lines.join('\n\n');if(navigator.clipboard)navigator.clipboard.writeText(txt);aiOpen(txt);el.textContent='已複製 ✓';setTimeout(function(){el.textContent='複製本題型「全部作答」→ 請 AI 逐題評分';},2300);};});
   app.querySelectorAll('[data-sol]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-sol');st.statOpen[k+'_s']=!st.statOpen[k+'_s'];save();render();};});
   app.querySelectorAll('[data-ans]').forEach(function(el){el.onblur=function(){st.statAns[el.getAttribute('data-ans')]=el.value;save();};});
   app.querySelectorAll('[data-copy2]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-copy2');var ft=findKey(k);var ans=st.statAns[k]||'(尚未作答)';var txt='請依詳解幫我評分這題統計作答。\\n題型：'+ft.tp.title+'\\n我的作答：\\n'+ans;if(navigator.clipboard)navigator.clipboard.writeText(txt);aiOpen(txt);el.textContent='已複製 ✓';setTimeout(function(){el.textContent='複製給 AI 評分';},2200);};});
   app.querySelectorAll('[data-sc]').forEach(function(el){el.onclick=function(){var v=el.getAttribute('data-sc').split('|'),k=v[0],lvl=v[1];pts(lvl==='熟'?8:lvl==='普通'?4:2);schedRev(k,lvl);
    if(lvl==='不熟'){if(st.wrongStat.indexOf(k)<0)st.wrongStat.push(k);}else{st.wrongStat=st.wrongStat.filter(function(x){return x!==k;});}
    var td=todayDay();if(td&&!st.done[td.id]&&td.link==='stat:'+k){st.done[td.id]=1;pts(12);}save();render();};});
  } else if(st.view==='wrong'){
   app.querySelectorAll('[data-wtab]').forEach(function(el){el.onclick=function(){st.wrongTab=el.getAttribute('data-wtab');render();};});
   on('practiceWrong',function(){startRM('wrong');st.view='rm';render();});
   app.querySelectorAll('[data-goweak]').forEach(function(el){el.onclick=function(){st.view='stat';st._focus=findKey(el.getAttribute('data-goweak'));render();};});
  } else if(st.view==='mock'){app.querySelectorAll('[data-rmn]').forEach(function(el){el.onclick=function(){st.mockSel.rmN=+el.getAttribute('data-rmn');render();};});app.querySelectorAll('[data-stn]').forEach(function(el){el.onclick=function(){st.mockSel.stN=+el.getAttribute('data-stn');render();};});on('startMock',function(){startMock();render();});app.querySelectorAll('[data-mopt]').forEach(function(el){el.onclick=function(){var mk=st.mock;if(mk.picked)return;mk.picked=el.getAttribute('data-mopt');var pr=mk.rp[mk.ri],q=RM[pr[0]].qs[pr[1]],aL=(q.ans||'').toUpperCase().replace(/[^A-E]/g,'').charAt(0);if(mk.picked===aL)mk.rmScore++;render();};});on('mnext',function(){var mk=st.mock;mk.ri++;mk.picked=null;if(mk.ri>=mk.rp.length)mk.phase='stat';render();});on('msol',function(){var ta=app.querySelector('[data-ans]');if(ta)st.statAns[ta.getAttribute('data-ans')]=ta.value;st.mock.showSol=!st.mock.showSol;render();});app.querySelectorAll('[data-spreset]').forEach(function(el){el.onclick=function(){if(el.getAttribute('data-spreset')==='full'){st.mockSel.nN=8;st.mockSel.qN=6;}else{st.mockSel.nN=5;st.mockSel.qN=3;}render();};});app.querySelectorAll('[data-msc]').forEach(function(el){el.onclick=function(){var mk=st.mock;var ta=app.querySelector('[data-ans]');if(ta)st.statAns[ta.getAttribute('data-ans')]=ta.value;var pr=el.getAttribute('data-msc').split('|');mk.sScores.push(Math.round((+pr[0])*(+pr[1])/10));mk.si++;mk.showSol=false;if(mk.si>=mk.sf.length)mk.phase='result';save();render();};});on('copymock',function(){var mk=st.mock,L=[];mk.sf.forEach(function(q,i){var a=st.statAns['mk:'+i];if(a&&a.trim())L.push('第'+(i+1)+'題('+q.title.split('（')[0]+') '+q.desc+'\n我的作答：'+a);});var txt='請依詳解逐題批改模擬考統計作答，每題給判定/得分(/10)/對的/失分點/正確理由/滿分版/口訣，最後總分。\n\n'+L.join('\n\n');aiOpen(txt);});on('remock',function(){st.mock=null;render();});} else if(st.view==='plan'){function saveTAp(){var ta=app.querySelector('[data-ans]');if(ta)st.statAns[ta.getAttribute('data-ans')]=ta.value;}
   app.querySelectorAll('[data-pmode]').forEach(function(el){el.onclick=function(){saveTAp();st.planMode=el.getAttribute('data-pmode');st.planTip=null;render();};});
   app.querySelectorAll('[data-rmtip]').forEach(function(el){el.onclick=function(){var c=el.getAttribute('data-rmtip');st.planTip=(st.planTip===c?null:c);render();};});
   app.querySelectorAll('[data-rmpre]').forEach(function(el){el.onclick=function(){startRMphase(el.getAttribute('data-rmpre'),'pre');render();};});
   app.querySelectorAll('[data-rmpost]').forEach(function(el){el.onclick=function(){startRMphase(el.getAttribute('data-rmpost'),'post');render();};});
   app.querySelectorAll('[data-sttip]').forEach(function(el){el.onclick=function(){var k='st:'+el.getAttribute('data-sttip');st.planTip=(st.planTip===k?null:k);render();};});
   app.querySelectorAll('[data-stpre]').forEach(function(el){el.onclick=function(){st.planStat={key:el.getAttribute('data-stpre'),phase:'pre'};st.planSol=false;render();};});
   app.querySelectorAll('[data-stpost]').forEach(function(el){el.onclick=function(){st.planStat={key:el.getAttribute('data-stpost'),phase:'post'};st.planSol=false;render();};});
   app.querySelectorAll('[data-plansol]').forEach(function(el){el.onclick=function(){saveTAp();st.planSol=!st.planSol;render();};});
   app.querySelectorAll('[data-ans]').forEach(function(el){el.onblur=function(){st.statAns[el.getAttribute('data-ans')]=el.value;save();};});
   app.querySelectorAll('[data-plangrade]').forEach(function(el){el.onclick=function(){saveTAp();var pr=el.getAttribute('data-plangrade').split('|'),ak=pr[0],fk=findKey(pr[1]);var ans=(st.handMode?'(我已在 Claude 對話附上手寫照片)':(st.statAns[ak]||'(尚未作答)'));var txt=gradePrompt(fk.tp.title,fk.tp.title+'：請寫出完整解法步驟與關鍵概念',ans);if(navigator.clipboard)navigator.clipboard.writeText(txt);aiOpen(txt);el.textContent='已複製 ✓';setTimeout(function(){el.textContent='複製給 AI 評分';},2000);};});
   app.querySelectorAll('[data-plansc]').forEach(function(el){el.onclick=function(){saveTAp();var lv=el.getAttribute('data-plansc'),sc=lv==='熟'?10:lv==='普通'?6:3,key=st.planStat.key,ph=st.planStat.phase;st.phase['st:'+key]=st.phase['st:'+key]||{};st.phase['st:'+key][ph]={lv:lv,s:sc};pts(ph==='post'?(lv==='熟'?8:lv==='普通'?4:2):2);if(ph==='post'){schedRev(key,lv);if(lv==='不熟'){if(st.wrongStat.indexOf(key)<0)st.wrongStat.push(key);}else st.wrongStat=st.wrongStat.filter(function(x){return x!==key;});}var td=todayDay();if(td&&!st.done[td.id]&&td.link==='plan:stat:'+key){st.done[td.id]=1;pts(12);}st.planStat=null;st.planSol=false;save();render();};});
   on('planShowAll',function(){st.planAll=!st.planAll;render();});on('planMock',function(){st.view='mock';st.mock=null;render();});} else if(st.view==='paper'){var sk=document.getElementById('setKey');if(sk)sk.onclick=function(){var k=prompt('貼上你的 Gemini API 金鑰（會跟著你的同步碼自動帶到其他裝置）：',gkey());if(k!=null){k=k.trim();st.gkey=k;localStorage.setItem('pearl_gkey',k);save();render();}};var pin=document.getElementById('pdfIn');if(pin)pin.onchange=function(){var fl=pin.files&&pin.files[0];if(fl)analyzePdf(fl);pin.value='';};on('pdfRetry',function(){if(_pendingPdf)analyzePdf(_pendingPdf);});app.querySelectorAll('[data-paper]').forEach(function(el){el.onclick=function(){st.curPaper=+el.getAttribute('data-paper');render();};});on('paperBack',function(){st.curPaper=null;render();});var rf=document.getElementById('reflIn');on('finishPaper',function(){var p=st.papers.filter(function(x){return x.id===st.curPaper;})[0];if(!p)return;var v=(rf?rf.value:'').trim();p.reflection=v;if(v&&!p.awarded){pts(20);p.awarded=true;p.read=true;p.readDate=ymd(now);save();render();paperToast('🦪 +20 珍珠值！讀完一篇又前進了～');}else{if(v)p.read=true;save();render();paperToast('💾 心得已更新');}});on('gradeRefl',function(){var p=st.papers.filter(function(x){return x.id===st.curPaper;})[0];if(!p)return;var rf=document.getElementById('reflIn');var refl=(rf?rf.value:(p.reflection||'')).trim();if(!refl){alert('先寫一點心得，再請 AI 給回饋喔 🙂');return;}if(rf){p.reflection=refl;save();}var txt='我讀完這篇論文後寫了心得，請幫我看：①我的理解有沒有錯或遺漏 ②可以補強或延伸的點 ③用一句話肯定我做得好的地方。請具體、鼓勵但誠實，用繁體中文。\n\n【論文】'+(p.title||'')+'\n【期刊】'+(p.journal||'')+'\n【一句話】'+(p.tldr||'')+'\n【AI整理的重點】\n・摘要：'+(p.summary||'')+'\n・主要發現：'+(p.findings||'')+'\n・貢獻：'+(p.contribution||'')+'\n・方法：'+(p.method||'')+'\n\n【我的心得】\n'+refl;aiOpen(txt);});on('delPaper',function(){if(confirm('刪除這篇論文與心得？')){st.papers=st.papers.filter(function(x){return x.id!==st.curPaper;});st.curPaper=null;save();render();}});}
 }
 function bindSched(){var sc=document.getElementById('sch');
  sc.querySelectorAll('[data-week]').forEach(function(el){el.onclick=function(){var w=el.getAttribute('data-week');st.open[w]=!(st.open[w]||w==curWeek());sc.innerHTML=schedHTML();bindSched();};});
  sc.querySelectorAll('[data-toggle]').forEach(function(el){el.onclick=function(){var k=el.getAttribute('data-toggle');if(st.done[k]){delete st.done[k];pts(-12);}else{st.done[k]=1;pts(12);var dy=days.filter(function(x){return x.id===k;})[0];if(dy&&dy.link&&dy.link.indexOf('stat:')===0)seedMem(dy.link.replace('stat:',''));}save();sc.innerHTML=schedHTML();bindSched();};});}
 render();
 if(window._db&&st.syncCode){cloudPull(function(c){if(c){if((c.ts||0)>(st._ts||0)){applyCloud(c);st._syncMsg='已從雲端帶回';if(SEEDLOCAL)save();render();}else{if((st._ts||0)>(c.ts||0))cloudPush();else if(SEEDLOCAL)save();}}else if(SEEDLOCAL){save();}});}
 if(!SHARE){(function(){function getPool(){var p=(st.pins||[]).slice().concat(st.entries.map(function(e){return e.b;}));if(st.anchor)p.push(st.anchor);return p.length?p:['你已經很棒了，慢慢來。'];}var idx=Math.floor(Math.random()*97);var box=document.createElement('div');box.id='selfTalk';box.style.cssText='position:fixed;right:12px;bottom:12px;max-width:235px;font-size:12.5px;line-height:1.55;background:var(--surface2);color:var(--ink);border:.5px solid var(--line);border-radius:14px;padding:8px 13px;z-index:99;box-shadow:0 2px 8px rgba(0,0,0,.14);cursor:pointer;';function show(){var pool=getPool();var raw=pool[((idx%pool.length)+pool.length)%pool.length];var isT=(!!st.anchor&&raw===st.anchor);var t=raw;if(!isT&&t.length>44)t=t.slice(0,44)+'…';box.innerHTML='<span style="opacity:.55;font-size:11px;">'+(isT?'💚 老師說':'🤍 我對自己說')+'</span><br>'+esc(t);}function nextOne(){idx++;show();}box.onclick=nextOne;show();document.body.appendChild(box);setInterval(nextOne,18000);})();}
 if(!SHARE){(function(){
  var GO=['還沒開始？完美，最好的起點就是現在這一秒 🚀','撈一顆珍珠就好 —— 一題、一行、一個名詞，都算數 🦪','不用全做完，先做「一點點」，動起來身體就醒了 ⚡','嘿，未來的你正在謝謝現在願意翻開書的你 💪','今天的份還在等你，三分鐘也好，我們開工！🔥','別想太多，先坐下、打開、寫下第一個字 ✍️','進度落後很正常，挑一格做完就贏過昨天 🐢→🐇','你不用贏過誰，只要比剛剛多動一下下 🌱','一題研方、一個統計名詞，珍珠值馬上 +6 ✨','狀態不好也能做 —— 降低標準，先求有再求好 🍃','現在的一小步，是考場上的一大口氣 🫧','翻開它，珍珠在海裡等你撈，下海吧 🌊','給自己 5 分鐘，做完再決定要不要停 ⏱️','今天還沒記錄，沒關係，從這一刻重新開始最帥 😎','哪怕只是複習昨天的錯題，也是往前一步 🔁','深呼吸，你準備好了，比你以為的更準備好 🌬️','把「等一下」換成「就現在」，你會回不去的 ✅','慢慢來比較快，但先開始才有得慢慢來 🛟'];
  var YAY=['你今天已經為珍珠動手了，這就是複利 🤍','看到沒？你說到做到，繼續閃閃發光 ✨','今天這一筆，未來會變成考場上的底氣 💎','已經有進度了！要不要再撈一顆當 bonus？🦪','你正在養成一顆珍珠，每天一點，超穩 🌟','做到了就是做到了，給自己一個大大的讚 👏','連續努力的人最迷人，今天的你很迷人 😏','進度入袋 ✓ 休息也是計畫的一部分，安心睡 😴','這份堅持，三個月後一定會回來謝謝你 🙏','你今天比昨天更靠近珍珠了，真的 💪','小小一步也算數，而你今天已經跨出去了 🏁','穩穩的，不用衝太快，你已經在路上了 🛤️','今日達成！把這份手感帶到明天 🔥','看你這麼努力，我也想替你開瓶香檳 🥂','已完成今日打卡，珍珠又亮了一階 🐚','你對自己的承諾，今天又兌現了一次 💛','這種一天一點的累積，最後會嚇到你 📈','辛苦了，今天的你值得被好好誇一下 🌸'];
  function rDays(){return Math.max(0,Math.ceil((EXAM-new Date())/86400000));}
  function activeToday(){var k=ymd(new Date());if(st.done&&st.done[k])return true;var es=st.entries||[];for(var i=0;i<es.length;i++){if(es[i].date===k)return true;}return false;}
  function pickFrom(pool){var n=((st.rem.seq||0)%pool.length+pool.length)%pool.length;st.rem.seq=(st.rem.seq||0)+1;return pool[n];}
  function remMsg(slot){var act=activeToday();var line=pickFrom(act?YAY:GO);var title=slot==='am'?'☀️ 早安，珍珠':'🌙 晚安前，珍珠';return {title:title,body:line,sub:'距資格考剩 '+rDays()+' 天 · 珍珠值 '+(st.points||0),act:act};}
  function osNotify(m){try{if(navigator.serviceWorker&&navigator.serviceWorker.controller){navigator.serviceWorker.ready.then(function(reg){reg.showNotification(m.title,{body:m.body+'\n'+m.sub,tag:'pearl-rem',renotify:true});})['catch'](function(){});return;}if(window.Notification&&Notification.permission==='granted'){new Notification(m.title,{body:m.body+'\n'+m.sub,tag:'pearl-rem'});}}catch(e){}}
  function fireBanner(m){var old=document.getElementById('pearlRem');if(old&&old.parentNode)old.parentNode.removeChild(old);var b=document.createElement('div');b.id='pearlRem';b.style.cssText='position:fixed;left:50%;top:14px;transform:translateX(-50%) translateY(-150%);width:min(94vw,420px);z-index:9999;background:linear-gradient(135deg,#7c6cf0,#39c2b3);color:#fff;border-radius:16px;padding:14px 16px;box-shadow:0 12px 34px rgba(0,0,0,.28);transition:transform .55s cubic-bezier(.34,1.56,.64,1);';b.innerHTML='<div style="font-size:13px;opacity:.92;margin-bottom:3px;">'+esc(m.title)+(m.act?'　🤍 你今天動手了':'')+'</div><div style="font-weight:600;font-size:15.5px;line-height:1.5;">'+esc(m.body)+'</div><div style="font-size:12px;opacity:.85;margin-top:6px;">'+esc(m.sub)+'</div><div style="display:flex;gap:8px;margin-top:11px;"><button id="_remGo" style="flex:1;border:none;border-radius:10px;padding:10px;font-size:14px;font-weight:600;background:#fff;color:#6b5bd6;cursor:pointer;">'+(m.act?'再撈一顆 →':'好，去做一題 →')+'</button><button id="_remX" style="border:none;border-radius:10px;padding:10px 13px;font-size:14px;background:rgba(255,255,255,.22);color:#fff;cursor:pointer;">知道了</button></div>';document.body.appendChild(b);requestAnimationFrame(function(){b.style.transform='translateX(-50%) translateY(0)';});function close(){b.style.transform='translateX(-50%) translateY(-150%)';setTimeout(function(){if(b.parentNode)b.parentNode.removeChild(b);},520);}var gx=b.querySelector('#_remX');if(gx)gx.onclick=close;var gg=b.querySelector('#_remGo');if(gg)gg.onclick=function(){close();st.view='plan';st.planFocus=null;st.planAll=false;st.planMode='rm';render();};clearTimeout(b._t);b._t=setTimeout(close,14000);}
  function fire(slot){var m=remMsg(slot);save();osNotify(m);fireBanner(m);}
  window._pearlPreview=function(){fire((new Date()).getHours()<14?'am':'pm');};
  function parseT(t){var p=(t||'0:0').split(':');return {h:+p[0]||0,mi:+p[1]||0};}
  function check(){if(!st.rem||!st.rem.on)return;var d=new Date(),k=ymd(d);if(st.rem.day!==k){st.rem.day=k;st.rem.fired={};save();}var slots=[['am',st.rem.am],['pm',st.rem.pm]],over=[];for(var i=0;i<slots.length;i++){var pt=parseT(slots[i][1]),w=new Date(d);w.setHours(pt.h,pt.mi,0,0);if(d>=w&&!st.rem.fired[k+'|'+slots[i][0]])over.push(slots[i][0]);}if(!over.length)return;for(var j=0;j<over.length;j++)st.rem.fired[k+'|'+over[j]]=1;save();fire(over[over.length-1]);}
  window._pearlRemCheck=check;
  setTimeout(check,1600);setInterval(check,30000);
 })();}
})();
</script></body></html>'''

RMCATS=[('研究哲學',['positivism','post-positivism','ontolog','epistemolog','paradigm','empiric','deductive','inductive','nomothetic','idiographic','methodolog']),
 ('抽樣',['sampling','stratified','cluster','quota','convenience','snowball','systematic','sampling frame','random sample','sample size']),
 ('信度',['reliab','test-retest','split-half','inter-rater','internal consist','cronbach','kappa']),
 ('效度',['validity','content valid','construct valid','criterion','convergent','discriminant','face valid','ecological']),
 ('因素分析',['factor','loading','rotation','eigen','communalit','varimax','oblique','principal component','scree','exploratory factor','confirmatory factor']),
 ('實驗設計',['experiment','factorial','main effect','interaction','random assign','manipulation','pretest','posttest','quasi','control group','field experiment','natural experiment','confound']),
 ('問卷與調查',['questionnaire','survey','double-barrel','contingency','probe','structured','pilot','response set','social desirab','non-response','nonresponse','interview']),
 ('質性研究',['grounded theory','ethnograph','interpretive','focus group','qualitative','case study','observation','secondary','content analysis','triangulation','field interview','saturation']),
 ('理論與假設',['theory','hypothes','falsifia','parsimony','agency theory','planned behavior','reasoned action','elaboration likelihood','construct is','proposition']),
 ('統計與測量',['type i error','type ii error','type-i','type-ii','skewed','correlation','regression','nominal','ordinal','parameter','univariate','bivariate','descriptive','significance','central tendency','median','levels of measurement']),
 ('研究流程與倫理',['research process','research proposal','replicat','ethic','irb','institutional review','informed consent'])]
def _rmcat(q):
    t=(q['q']+' '+' '.join(q.get('opts',[]))).lower()
    for nm,kws in RMCATS:
        for k in kws:
            if k in t:return nm
    return '其他'
for _sem in RM:
    for _q in _sem['qs']:
        _q['cat']=_rmcat(_q)
base = T.replace('__STATFULL__', json.dumps(STATFULL, ensure_ascii=False)).replace('__RM__', json.dumps(RM, ensure_ascii=False)).replace('__STAT__', json.dumps(STAT, ensure_ascii=False))
PERSONAL_SCRUB=['我想到一個很棒的日記 app 點子（後來命名為「珍珠日記」）；並且透過對話，看見了真實的自己。','我替這本日記取了名字「珍珠日記」；並且第一次主動對自己說：我想學著被稱讚。','珍珠陪我看清「我是什麼樣的人」——一個被自己低估、卻又柔軟又有力量的人。這次我沒有反駁。','我「沒想過」，卻讀到了博士班。','我「沒想過」，卻考進了博士班。','我「沒想過」，卻留下來了。','「詩涵，不要給自己那麼大的壓力。我們都在旁邊支持你，不用擔心，你已經很棒了。老師以你為榮！」','詩涵，不要給自己那麼大的壓力。我們都在旁邊支持你，不用擔心，你已經很棒了。老師以你為榮！','心虛的時候回來看一眼。這不是安慰，是你的證據。','問自己：「如果詩涵是我的學生，我會跟她說什麼？」','抓到了，這就是進步。','寫「事實」就好：今天做到、想到、注意到的。不用稱讚自己。','昨天可是把我擼到翻肚的人耶，今天這點事難得倒你？']
# 主版（個人完整，有硬寫種子）
io.open(OUT,'w',encoding='utf-8').write(base.replace('__SHARE__','false').replace('__SEEDLOCAL__','true'))
# 分享版（無個資、考試功能）
SHAREOUT=r"C:\Users\Cindy\Downloads\Cindy's Agent\資格考衝刺_珍珠版.html"
_sh=base.replace('__SHARE__','true').replace('__SEEDLOCAL__','false')
for _p in PERSONAL_SCRUB: _sh=_sh.replace(_p,'')
_sh=_sh.replace('建議長一點，例如 amy-stat-7k3p9','建議用「英文名-科目-隨機碼」，例如 amy-stat-7k3p9，長一點別人才猜不到')
_sh=_sh.replace('</body>','<div style="text-align:center;font-size:11px;color:#A89E8C;padding:8px 0 30px;letter-spacing:.5px;">NYCU 經管所 · 詩涵 ✕ Claude · 2026</div><div style="position:fixed;right:10px;bottom:10px;font-size:12px;color:#7A5C3A;background:rgba(240,224,208,.92);border:.5px solid #E2D9CA;border-radius:20px;padding:5px 13px;z-index:99;box-shadow:0 1px 5px rgba(0,0,0,.1);">祝順利上岸 💪</div></body>')
io.open(SHAREOUT,'w',encoding='utf-8').write(_sh)
io.open(r"C:\Users\Cindy\Downloads\Cindy's Agent\index.html",'w',encoding='utf-8').write(_sh)
# 乾淨外殼版（個人功能、但檔案內無任何個資文字；資料靠同步碼從雲端帶回）
_shell=base.replace('__SHARE__','false').replace('__SEEDLOCAL__','false')
for _p in PERSONAL_SCRUB: _shell=_shell.replace(_p,'')
import os as _os
_pdir=r"C:\Users\Cindy\Downloads\Cindy's Agent\個人版上架"
_os.makedirs(_pdir,exist_ok=True)
io.open(_pdir+r"\index.html",'w',encoding='utf-8').write(_shell)
_repo=r"C:\Users\Cindy\Downloads\pearl-deploy"
_os.makedirs(_repo+r"\share",exist_ok=True)
_os.makedirs(_repo+r"\personal",exist_ok=True)
io.open(_repo+r"\share\index.html",'w',encoding='utf-8').write(_sh)
io.open(_repo+r"\personal\index.html",'w',encoding='utf-8').write(_shell)  # Git 自動部署用（無個資）
print('saved 3:', OUT, '|', SHAREOUT, '|', _pdir+r"\index.html")
