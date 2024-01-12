import{a as w,r as E,o as y,c as v,b as r,d as l,w as p,e as _,f as $,g as I,h as R,i as O,j as A,k as T}from"./vendor-3743131b.js";(function(){const i=document.createElement("link").relList;if(i&&i.supports&&i.supports("modulepreload"))return;for(const s of document.querySelectorAll('link[rel="modulepreload"]'))a(s);new MutationObserver(s=>{for(const e of s)if(e.type==="childList")for(const n of e.addedNodes)n.tagName==="LINK"&&n.rel==="modulepreload"&&a(n)}).observe(document,{childList:!0,subtree:!0});function t(s){const e={};return s.integrity&&(e.integrity=s.integrity),s.referrerPolicy&&(e.referrerPolicy=s.referrerPolicy),s.crossOrigin==="use-credentials"?e.credentials="include":s.crossOrigin==="anonymous"?e.credentials="omit":e.credentials="same-origin",e}function a(s){if(s.ep)return;s.ep=!0;const e=t(s);fetch(s.href,e)}})();const d="/api",h="/auth",k={login:`${h}/login/`,signup:`${h}/signup/`,isLoggedIn:`${h}/is-logged-in/`,activate:`${h}/activate/`,me:`${h}/me/`,trip:`${d}/trip/`,userTrips:`${d}/user-trips/`,deleteTripRequest:`${d}/delete-trip-request/`,joinRequests:`${d}/join-requests/`,joinSelectedTrips:`${d}/join-selected-trips/`,tripList:`${d}/trip-list/`};const C=(o,i)=>{const t=o.__vccOpts||o;for(const[a,s]of i)t[a]=s;return t},S={data(){return{isLoggedIn:!1}},created(){this.checkLoginStatus()},methods:{async checkLoginStatus(){const o=k.isLoggedIn,i=await w.get(o);this.isLoggedIn=i.data.isAuthenticated},toggleMenu(){this.showMenu=!this.showMenu;var o=document.getElementById("rightNav");o.style.display==="block"?o.style.display="none":o.style.display="block"}}},N={id:"app",class:"box"},V={class:"navbar"},B={class:"nav-content"},q={class:"brand-and-menu"},D={key:0},j={class:"text-size"},M={key:1},z={class:"text-size"},U=r("div",null,null,-1),W=r("div",null,null,-1),F=r("div",null,null,-1),H=[U,W,F],K={class:"right",id:"rightNav"},X=r("a",{href:"/tutorial"},"Tutorial",-1);function G(o,i,t,a,s,e){const n=E("router-link"),g=E("router-view");return y(),v("div",N,[r("nav",V,[r("div",B,[r("div",q,[s.isLoggedIn?(y(),v("div",D,[r("span",j,[l(n,{to:"/"},{default:p(()=>[_("findaride")]),_:1})])])):(y(),v("div",M,[r("span",z,[l(n,{to:"/"},{default:p(()=>[_("findaride")]),_:1})])])),r("div",{class:"hamburger",onClick:i[0]||(i[0]=(...b)=>e.toggleMenu&&e.toggleMenu(...b))},H)]),r("div",K,[l(n,{to:"/about"},{default:p(()=>[_("About")]),_:1}),X,l(n,{to:"/dashboard"},{default:p(()=>[_("Dashboard")]),_:1}),l(n,{to:"/profile"},{default:p(()=>[_("Profile")]),_:1})])])]),l(g,{class:"full-height pt-8",style:{overflow:"auto"}})])}const J=C(S,[["render",G]]),Q="modulepreload",Y=function(o){return"/static/"+o},L={},f=function(i,t,a){if(!t||t.length===0)return i();const s=document.getElementsByTagName("link");return Promise.all(t.map(e=>{if(e=Y(e),e in L)return;L[e]=!0;const n=e.endsWith(".css"),g=n?'[rel="stylesheet"]':"";if(!!a)for(let u=s.length-1;u>=0;u--){const m=s[u];if(m.href===e&&(!n||m.rel==="stylesheet"))return}else if(document.querySelector(`link[href="${e}"]${g}`))return;const c=document.createElement("link");if(c.rel=n?"stylesheet":Q,n||(c.as="script",c.crossOrigin=""),c.href=e,document.head.appendChild(c),n)return new Promise((u,m)=>{c.addEventListener("load",u),c.addEventListener("error",()=>m(new Error(`Unable to preload CSS for ${e}`)))})})).then(()=>i()).catch(e=>{const n=new Event("vite:preloadError",{cancelable:!0});if(n.payload=e,window.dispatchEvent(n),!n.defaultPrevented)throw e})},Z=[{path:"/",name:"home",component:()=>f(()=>import("./HomeView-298011c4.js"),["assets/HomeView-298011c4.js","assets/vendor-3743131b.js","assets/vendor-86a04bde.css","assets/HomeView-e4c169b1.css"])},{path:"/about/",name:"about",component:()=>f(()=>import("./AboutView-d46917be.js"),["assets/AboutView-d46917be.js","assets/vendor-3743131b.js","assets/vendor-86a04bde.css","assets/AboutView-d155bbfc.css"])},{path:"/profile/",name:"profile",component:()=>f(()=>import("./ProfileView-b2de96d5.js"),["assets/ProfileView-b2de96d5.js","assets/axios_service-eba734f5.js","assets/vendor-3743131b.js","assets/vendor-86a04bde.css","assets/ProfileView-8e3965cf.css"])},{path:"/dashboard/",name:"dashboard",component:()=>f(()=>import("./DashboardView-e83f2956.js"),["assets/DashboardView-e83f2956.js","assets/vendor-3743131b.js","assets/vendor-86a04bde.css","assets/axios_service-eba734f5.js","assets/DashboardView-a5544f66.css"])},{path:"/tutorial/",name:"tutorial",component:()=>f(()=>import("./TutorialView-1bc34939.js"),["assets/TutorialView-1bc34939.js","assets/vendor-3743131b.js","assets/vendor-86a04bde.css","assets/TutorialView-cf5b1278.css"])}];async function ee(){const o=k.isLoggedIn;return(await w.get(o)).data.isAuthenticated}const te=["dashboard","profile"],x=$({history:I("/"),routes:Z});x.beforeEach(async(o,i,t)=>{if(te.includes(o.name))if(await ee())t();else{let e=`/accounts/login/?next=${encodeURIComponent(o.path)}`;window.location.href=e}else t()});const oe=R({components:A,directives:T}),P=O(J).use(oe).use(x);P.directive("tooltip",{mounted(o,i){o.style.position="relative";const t=document.createElement("span");t.textContent=i.value,t.style.visibility="hidden",t.style.position="absolute",t.style.bottom="100%",t.style.left="50%",t.style.transform="translateX(-50%)",t.style.backgroundColor="black",t.style.color="white",t.style.padding="5px 10px",t.style.borderRadius="4px",t.style.fontSize="14px",t.style.whiteSpace="nowrap",o.appendChild(t),o.onmouseenter=()=>t.style.visibility="visible",o.onmouseleave=()=>t.style.visibility="hidden"}});P.mount("#app");export{C as _,k as e};
