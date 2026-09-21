const canvas=document.getElementById("game"),ctx=canvas.getContext("2d");
const N=30,S=canvas.width/N;
let snake,dir,nextDir,food,powers=[],obstacles=[],score,level,combo,paused,running,startTime,lastTick,elapsed,missionTarget;
let high=Number(localStorage.getItem("vivekSnakeHigh")||0);
document.getElementById("high").textContent=high;
const achievements=[
  ["first","FIRST BITE",s=>s>=10],["speed","SPEED DEMON",s=>level>=5],
  ["hunter","HUNTER",s=>s>=500],["survivor","SURVIVOR",s=>s>=1000]
];
function reset(){
 snake=[{x:15,y:15},{x:14,y:15},{x:13,y:15}];dir={x:1,y:0};nextDir=dir;
 food=null;powers=[];obstacles=[];score=0;level=1;combo=1;paused=false;running=false;elapsed=0;missionTarget=250;
 for(let i=0;i<12;i++) spawnObstacle(); spawnFood();
 updateUI(); draw();
}
function rand(n){return Math.floor(Math.random()*n)}
function free(x,y){return !snake?.some(p=>p.x===x&&p.y===y)&&!obstacles.some(p=>p.x===x&&p.y===y)}
function spawnFood(){
 let f; do f={x:rand(N),y:rand(N),type:"apple"}; while(!free(f.x,f.y));
 const r=Math.random(); if(r<.10)f.type="star"; else if(r<.28)f.type="gold"; else if(r>.92)f.type="poison"; food=f;
}
function spawnObstacle(){
 let p; do p={x:rand(N),y:rand(N)}; while(!free(p.x,p.y)||Math.abs(p.x-15)+Math.abs(p.y-15)<7); obstacles.push(p)
}
function spawnPower(){
 if(powers.length>=2)return;
 let p;do p={x:rand(N),y:rand(N),type:["shield","slow","double"][rand(3)],ttl:10000};while(!free(p.x,p.y));
 powers.push(p)
}
function setDir(d){
 const map={up:{x:0,y:-1},down:{x:0,y:1},left:{x:-1,y:0},right:{x:1,y:0}};
 const v=map[d]; if(v&&!(v.x===-dir.x&&v.y===-dir.y))nextDir=v;
}
document.addEventListener("keydown",e=>{
 const k=e.key.toLowerCase();
 if(["arrowup","w"].includes(k))setDir("up"); if(["arrowdown","s"].includes(k))setDir("down");
 if(["arrowleft","a"].includes(k))setDir("left"); if(["arrowright","d"].includes(k))setDir("right");
 if(k===" "&&running){paused=!paused;showOverlay(paused,"PAUSED","Press SPACE to continue","RESUME")}
 if(k==="r")start(); if(["arrowup","arrowdown","arrowleft","arrowright"," "].includes(k))e.preventDefault();
});
document.querySelectorAll("[data-dir]").forEach(b=>b.onclick=()=>setDir(b.dataset.dir));
document.getElementById("startBtn").onclick=start;
function start(){reset();running=true;startTime=performance.now();lastTick=performance.now();document.getElementById("overlay").classList.add("hidden");requestAnimationFrame(loop)}
function speed(){return Math.max(45,145-(level-1)*10)}
function loop(t){
 if(!running)return;
 if(!paused){
  elapsed=(t-startTime)/1000;
  if(t-lastTick>=speed()){step();lastTick=t}
  draw();updateUI()
 }
 requestAnimationFrame(loop)
}
function step(){
 dir=nextDir;
 const head={x:snake[0].x+dir.x,y:snake[0].y+dir.y};
 if(head.x<0||head.x>=N||head.y<0||head.y>=N||obstacles.some(p=>p.x===head.x&&p.y===head.y)||snake.some((p,i)=>i>0&&p.x===head.x&&p.y===head.y)){gameOver();return}
 snake.unshift(head);
 let ate=head.x===food.x&&head.y===food.y;
 if(ate){
  let gain=food.type==="apple"?10:food.type==="gold"?30:food.type==="star"?75:-25;
  if(food.type==="poison"){snake.splice(-2,Math.min(2,snake.length-2));combo=1}else{score=Math.max(0,score+gain*combo);combo=Math.min(9,combo+1)}
  if(score>high){high=score;localStorage.setItem("vivekSnakeHigh",high)}
  if(score>level*100){level++;for(let i=0;i<2;i++)spawnObstacle()}
  if(Math.random()<.25)spawnPower();spawnFood()
 }else{snake.pop();combo=Math.max(1,combo-0.02)}
 powers=powers.filter(p=>{p.ttl-=speed();return p.ttl>0});
 for(const p of powers)if(p.x===head.x&&p.y===head.y){if(p.type==="shield"){score+=20}else if(p.type==="slow"){score+=15}else score+=30;p.ttl=0}
}
function gameOver(){running=false;showOverlay(false,"GAME OVER",`Score ${score} • Level ${level}`,"PLAY AGAIN")}
function showOverlay(paused,title,text,button){const o=document.getElementById("overlay");o.classList.remove("hidden");document.getElementById("overlayTitle").textContent=title;document.getElementById("overlayText").textContent=text;document.getElementById("startBtn").textContent=button}
function updateUI(){
 document.getElementById("score").textContent=score;document.getElementById("high").textContent=high;document.getElementById("level").textContent=level;document.getElementById("combo").textContent="x"+Math.max(1,Math.floor(combo));
 const sec=Math.floor(elapsed),m=String(Math.floor(sec/60)).padStart(2,"0"),s=String(sec%60).padStart(2,"0");document.getElementById("time").textContent=`${m}:${s}`;
 document.getElementById("mission").textContent=`Reach ${missionTarget} points.`;
 document.getElementById("missionBar").style.width=Math.min(100,score/missionTarget*100)+"%";
 document.getElementById("powers").innerHTML=powers.length?powers.map(p=>`<div class="power active">${p.type.toUpperCase()} • ${(p.ttl/1000).toFixed(1)}s</div>`).join(""):'<div class="power empty">Collect power-ups</div>';
 document.getElementById("achievements").innerHTML=achievements.map(([id,name,fn])=>`<div class="achievement ${fn(score)?"unlocked":""}">${fn(score)?"✓":"○"} ${name}</div>`).join("")
}
function draw(){
 ctx.clearRect(0,0,canvas.width,canvas.height);
 ctx.strokeStyle="rgba(38,75,102,.22)";ctx.lineWidth=1;
 for(let i=0;i<=N;i++){ctx.beginPath();ctx.moveTo(i*S,0);ctx.lineTo(i*S,canvas.height);ctx.stroke();ctx.beginPath();ctx.moveTo(0,i*S);ctx.lineTo(canvas.width,i*S);ctx.stroke()}
 obstacles.forEach(p=>{ctx.fillStyle="#263d50";ctx.shadowColor="#355a75";ctx.shadowBlur=8;round(p.x*S+3,p.y*S+3,S-6,S-6,5);ctx.shadowBlur=0});
 if(food){const col={apple:"#ff5577",gold:"#ffd34d",star:"#b77cff",poison:"#ff304f"}[food.type];ctx.fillStyle=col;ctx.shadowColor=col;ctx.shadowBlur=18;const cx=food.x*S+S/2,cy=food.y*S+S/2,r=food.type==="star"?S*.32:S*.28;ctx.beginPath();ctx.arc(cx,cy,r,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0}
 powers.forEach(p=>{ctx.strokeStyle=p.type==="shield"?"#4ab8ff":p.type==="slow"?"#bd8cff":"#ffd34d";ctx.lineWidth=3;ctx.beginPath();ctx.arc(p.x*S+S/2,p.y*S+S/2,S*.32,0,Math.PI*2);ctx.stroke()});
 snake.forEach((p,i)=>{const col=i===0?"#65e7ad":"#2fa7ff";ctx.fillStyle=col;ctx.shadowColor=col;ctx.shadowBlur=i===0?18:7;round(p.x*S+2,p.y*S+2,S-4,S-4,6);ctx.shadowBlur=0});
 if(snake[0]){ctx.fillStyle="#071019";const h=snake[0],ex=h.x*S+S/2+(dir.x?dir.x*5:0),ey=h.y*S+S/2+(dir.y?dir.y*5:0);ctx.beginPath();ctx.arc(ex-dir.y*4,ey+dir.x*4,2.3,0,7);ctx.fill();ctx.beginPath();ctx.arc(ex+dir.y*4,ey-dir.x*4,2.3,0,7);ctx.fill()}
}
function round(x,y,w,h,r){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill()}
reset();
