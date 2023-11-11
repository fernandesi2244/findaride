import{l as u,k as f,m as v,o as h,c as C,a as o,u as y,v as d,x as r,p as T,i as b}from"./vendor-1c2b7f9b.js";import{_ as P}from"./index-9e0a4d45.js";const c=n=>(T("data-v-52828319"),n=n(),b(),n),q={class:"modal-overlay"},A={class:"modal"},x=c(()=>o("h3",null,"Add a new trip request",-1)),R=["onSubmit"],k={class:"form-group"},w={class:"form-group"},F={class:"form-group"},I={class:"form-group"},S={class:"form-group"},B={class:"form-group"},D=c(()=>o("button",{type:"submit",class:"btn"},"Add Trip Request",-1)),V={__name:"AddTripForm",emits:["addTripRequest","close"],setup(n,{emit:l}){const p=u(),i=u(),e=f({from:"",fromPostalCode:"",to:"",toPostalCode:"",departureDate:"",departureTime:"",luggageCount:0,comments:"",status:"Pending"});function _(){console.log("Submitting trip:",e),l("addTripRequest",{...e}),m()}function g(){l("close"),m()}function m(){e.from="",e.fromPostalCode="",e.to="",e.toPostalCode="",e.departureDate="",e.departureTime="",e.luggageCount=0,e.comments=""}return v(()=>{const a=new google.maps.places.Autocomplete(p.value,{types:["transit_station"],fields:["address_components"]}),t=new google.maps.places.Autocomplete(i.value,{types:["transit_station"],fields:["address_components"]});google.maps.event.addListener(a,"place_changed",()=>{console.log(a.getPlace().address_components);let s=a.getPlace().address_components.pop();e.fromPostalCode=s.long_name,e.from=document.getElementById("from").value}),google.maps.event.addListener(t,"place_changed",()=>{let s=t.getPlace().address_components.pop();e.toPostalCode=s.long_name,e.to=document.getElementById("to").value})}),(a,t)=>(h(),C("div",q,[o("div",A,[x,o("form",{onSubmit:y(_,["prevent"])},[o("div",k,[o("input",{id:"from",ref_key:"fromRef",ref:p,placeholder:"From",required:""},null,512)]),o("div",w,[o("input",{id:"to",ref_key:"toRef",ref:i,placeholder:"To",required:""},null,512)]),o("div",F,[d(o("input",{"onUpdate:modelValue":t[0]||(t[0]=s=>e.departureDate=s),type:"date",required:""},null,512),[[r,e.departureDate]])]),o("div",I,[d(o("input",{"onUpdate:modelValue":t[1]||(t[1]=s=>e.departureTime=s),type:"time",required:""},null,512),[[r,e.departureTime]])]),o("div",S,[d(o("input",{"onUpdate:modelValue":t[2]||(t[2]=s=>e.luggageCount=s),type:"number",min:"0",required:""},null,512),[[r,e.luggageCount,void 0,{number:!0}]])]),o("div",B,[d(o("textarea",{"onUpdate:modelValue":t[3]||(t[3]=s=>e.comments=s),placeholder:"Other comments"},null,512),[[r,e.comments]])]),D],40,R),o("button",{onClick:g,class:"btn cancel-btn"},"Cancel")])]))}},E=P(V,[["__scopeId","data-v-52828319"]]);export{E as A};
