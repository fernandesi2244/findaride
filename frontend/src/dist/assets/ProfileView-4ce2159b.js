import{c as p,g as D,n as N}from"./axios_service-69da3fda.js";import{e as m}from"./index-2a08fece.js";import{k as g,l as d,m as V,n as B,g as v,o as a,c as o,a as s,d as _,t as e,F as x,q as b,u as l,b as P}from"./vendor-51ff1aab.js";const S={class:"container-xl pt-4"},$={class:"narrow-container"},j={class:"text-start"},E={class:"text-secondary text-small"},F=s("div",{class:"mt-4"},[s("h4",{class:"text-start"}," Thank you for using findaride! "),s("h5",{class:"text-start mt-3"}," During your time with us, you have ")],-1),I={class:"row mt-3"},L={class:"col-4 px-4"},M=s("p",{class:"text-start"}," been on ",-1),O={class:"big-text"},U=s("p",{class:"text-end"}," trips ",-1),Y={class:"col-4"},q=s("p",{class:"text-start"}," traveled ",-1),z={class:"big-text"},A=s("p",{class:"text-end"}," miles ",-1),C={class:"col-4"},G=s("p",{class:"text-start"}," shared rides with ",-1),H={class:"big-text"},J=s("p",{class:"text-end"}," people ",-1),K=s("h4",null,"Your past trips",-1),Q={key:0,class:"accordion",id:"accordion"},R={class:"accordion-header"},W=["data-bs-target"],X=["id"],Z={class:"accordion-body"},ss={class:"mb-2"},ts={class:"flex"},es=s("h5",{class:"text-start"},[_("Members:"),s("br")],-1),as={class:"text-start"},os=s("br",null,null,-1),ns={class:"text-start"},cs={key:1},is={__name:"Profile",setup(f){const n=g({first_name:"",id:-1}),r=g({number_riders:0,number_trips:0,miles_ridden:0,past_riders:0,id:-1}),u=d([]),y=d(0),h=V(()=>u.value.filter(c=>!c.is_active));d(null),B(async()=>{await w(),await k()});async function w(){const c=m.me,i=await v.get(c);Object.assign(n,i.data),Object.assign(userStast,i.data.user_stats)}async function k(){const c=`${m.userTrips}${n.id}/`,i=await v.get(c);u.value=i.data.trips,y.value=i.data.id}return(c,i)=>(a(),o("div",S,[s("div",$,[s("h2",j,[_(e(n.first_name)+" "+e(n.last_name)+" ",1),s("span",E,"("+e(n.college_display)+")",1)]),F,s("div",I,[s("div",L,[M,s("p",O,e(r.number_trips),1),U]),s("div",Y,[q,s("p",z,e(r.miles_ridden),1),A]),s("div",C,[G,s("p",H,e(r.number_riders),1),J])]),K,h.value.length>0?(a(),o("div",Q,[(a(!0),o(x,null,b(h.value,t=>(a(),o("div",{key:t.college+t.id,class:"accordion-item"},[s("h2",R,[s("button",{class:"accordion-button collapsed",type:"button","data-bs-toggle":"collapse","data-bs-target":"#"+t.college+t.id},e(l(p)(t.departure_location))+" → "+e(l(p)(t.arrival_location))+" on "+e(l(D)(t.latest_departure_time)),9,W)]),s("div",{id:t.college+t.id,class:"accordion-collapse collapse"},[s("div",Z,[s("div",ss,[s("div",ts,[s("div",null,[es,(a(!0),o(x,null,b(t.participant_list,T=>(a(),o("h6",as,e(l(N)(T)),1))),256))])]),os,s("h5",ns,[_("Number of luggage bags: "),s("span",null,e(t.num_luggage_bags),1)])])])],8,X)]))),128))])):(a(),o("div",cs," You do not have any past trips. "))])]))}},_s={__name:"ProfileView",setup(f){return(n,r)=>(a(),o("main",null,[P(is)]))}};export{_s as default};
