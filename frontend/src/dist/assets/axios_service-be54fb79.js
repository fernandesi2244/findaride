import{a as f}from"./vendor-4c76fc02.js";function c(e){if(typeof e=="string")return e;try{let t="",a=1;for(const[o,r]of Object.entries(e))t+=`${a++} ${r}
`;return t}catch{return JSON.stringify(e)}}function m(e,t){const a=new Date(e),o=new Date(t),r=Math.round((o-a)/(1e3*60*60*24));return r>0?"+"+String(r):""}const s={1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"};function l(e,t){return u(e)+" – "+u(t)}function n(e){const t=new Date(e);return s[t.getMonth()]+". "+t.getDate()+" "+t.getFullYear()}function g(e,t){return n(e)===n(t)?n(e):`${n(e)} - ${n(t)}`}function $(e,t){return n(e)===n(t)?"on "+n(e):`(${n(e)}-${n(t)})`}function u(e){return new Date(e).toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"})}function d(e){return e.split(",")[0]}function h(e){return`${e.first_name} ${e.last_name} (${e.email})`}f.defaults.xsrfCookieName="csrftoken";f.defaults.xsrfHeaderName="X-CSRFTOKEN";export{$ as a,n as b,d as c,l as d,m as e,c as f,u as g,g as h,h as n};