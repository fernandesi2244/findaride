import{c as l,g as p,a as T,n as P}from"./axios_service-eba734f5.js";import{e as u}from"./index-ca3c2a3e.js";import{m as h,n as m,p as V,a as g,o as a,c as o,b as s,t as e,F as b,q as v,u as n,e as x,d as B}from"./vendor-3743131b.js";const D={class:"container-xl pt-4"},L={class:"narrow-container-profile"},N={class:"text-start"},j=s("div",{class:"mt-4"},[s("h4",{class:"text-start"}," Thank you for using findaride! "),s("h5",{class:"text-start mt-3"}," During your time with us, you have ")],-1),E={class:"row mt-4 mb-3"},F={class:"col-4 col-padding px-4"},M=s("p",{class:"text-start"}," been on ",-1),O={class:"big-text"},S=s("p",{class:"text-end"}," trips ",-1),U={class:"col-4 col-padding"},Y=s("p",{class:"text-start"}," traveled ",-1),$={class:"big-text"},q=s("p",{class:"text-end"}," miles ",-1),I={class:"col-4 col-padding"},z=s("p",{class:"text-start"}," shared rides with ",-1),A={class:"big-text"},C=s("p",{class:"text-end"}," people ",-1),G=s("h4",null,"Your past trips",-1),H={key:0,class:"past-trips accordion",id:"accordion"},J={class:"accordion-header accordion-profile-header"},K=["data-bs-target"],Q=["id"],R={class:"accordion-body"},W={class:"mb-2"},X={class:"flex"},Z=s("h5",{class:"text-start margin-right-1 header-border"},[x("Members"),s("br")],-1),ss={class:"text-start"},ts={class:"text-start"},es={key:1},as={__name:"Profile",setup(f){const r=h({first_name:"",id:-1}),i=h({number_riders:0,number_trips:0,miles_ridden:0,past_riders:0,id:-1}),_=m([]);m(null),V(async()=>{await y(),await w()});async function y(){const d=u.me,c=await g.get(d);Object.assign(r,c.data),Object.assign(i,c.data.user_stats)}async function w(){const d=`${u.userTrips}`,c=await g.get(d,{params:{when:"past"}});_.value=c.data.trips}return(d,c)=>(a(),o("div",D,[s("div",L,[s("h2",N,e(r.first_name)+" "+e(r.last_name),1),j,s("div",E,[s("div",F,[M,s("p",O,e(i.number_trips),1),S]),s("div",U,[Y,s("p",$,e(i.miles_ridden),1),q]),s("div",I,[z,s("p",A,e(i.number_riders),1),C])]),G,_.value.length>0?(a(),o("div",H,[(a(!0),o(b,null,v(_.value,t=>(a(),o("div",{key:t.college+t.id,class:"accordion-item accordion-profile-item"},[s("h2",J,[s("button",{class:"accordion-button accordion-profile-button collapsed",type:"button","data-bs-toggle":"collapse","data-bs-target":"#"+t.college+t.id},e(n(l)(t.departure_location))+" → "+e(n(l)(t.arrival_location))+" between "+e(n(p)(t.earliest_departure_time))+" and "+e(n(p)(t.latest_departure_time))+" "+e(n(T)(t.earliest_departure_time,t.latest_departure_time)),9,K)]),s("div",{id:t.college+t.id,class:"accordion-collapse collapse"},[s("div",R,[s("div",W,[s("div",X,[Z,s("div",ss,[x("Luggage bags: "),s("span",null,e(t.num_luggage_bags),1)])]),(a(!0),o(b,null,v(t.participant_list,k=>(a(),o("h6",ts,e(n(P)(k)),1))),256))])])],8,Q)]))),128))])):(a(),o("div",es," You do not have any past trips. "))])]))}},cs={__name:"ProfileView",setup(f){return(r,i)=>(a(),o("main",null,[B(as)]))}};export{cs as default};
