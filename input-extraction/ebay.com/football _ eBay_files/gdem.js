(function(){'use strict';function aa(a){var b=0;return function(){return b<a.length?{done:!1,value:a[b++]}:{done:!0}}}function l(a){var b="undefined"!=typeof Symbol&&Symbol.iterator&&a[Symbol.iterator];return b?b.call(a):{next:aa(a)}}var ba="function"==typeof Object.defineProperties?Object.defineProperty:function(a,b,c){a!=Array.prototype&&a!=Object.prototype&&(a[b]=c.value)},ca="undefined"!=typeof window&&window===this?this:"undefined"!=typeof global&&null!=global?global:this;
function da(a,b){if(b){var c=ca;a=a.split(".");for(var e=0;e<a.length-1;e++){var d=a[e];d in c||(c[d]={});c=c[d]}a=a[a.length-1];e=c[a];b=b(e);b!=e&&null!=b&&ba(c,a,{configurable:!0,writable:!0,value:b})}}da("Object.entries",function(a){return a?a:function(b){var c=[],e;for(e in b)Object.prototype.hasOwnProperty.call(b,e)&&c.push([e,b[e]]);return c}});var n=this||self,ea=Date.now||function(){return+new Date};var p=document,fa=window;var ha=Array.prototype.forEach?function(a,b){Array.prototype.forEach.call(a,b,void 0)}:function(a,b){for(var c=a.length,e="string"==typeof a?a.split(""):a,d=0;d<c;d++)d in e&&b.call(void 0,e[d],d,a)};function q(a){q[" "](a);return a}q[" "]=function(){};var r={},t=null;
function ia(a){for(var b=[],c=0,e=0;e<a.length;e++){var d=a.charCodeAt(e);255<d&&(b[c++]=d&255,d>>=8);b[c++]=d}a=3;!1===a||void 0===a?a=0:!0===a&&(a=3);if(!t)for(t={},c="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789".split(""),e=["+/=","+/","-_=","-_.","-_"],d=0;5>d;d++){var f=c.concat(e[d].split(""));r[d]=f;for(var g=0;g<f.length;g++){var h=f[g];void 0===t[h]&&(t[h]=g)}}a=r[a];c=[];for(e=0;e<b.length;e+=3){var m=b[e],k=(d=e+1<b.length)?b[e+1]:0;h=(f=e+2<b.length)?b[e+2]:0;g=m>>2;
m=(m&3)<<4|k>>4;k=(k&15)<<2|h>>6;h&=63;f||(h=64,d||(k=64));c.push(a[g],a[m],a[k]||"",a[h]||"")}return c.join("")};function u(a){try{var b;if(b=!!a&&null!=a.location.href)a:{try{q(a.foo);b=!0;break a}catch(c){}b=!1}return b}catch(c){return!1}}function v(a,b){if(a)for(var c in a)Object.prototype.hasOwnProperty.call(a,c)&&b.call(void 0,a[c],c,a)}function ja(a){var b=a.length;if(0==b)return 0;for(var c=305419896,e=0;e<b;e++)c^=(c<<5)+(c>>2)+a.charCodeAt(e)&4294967295;return 0<c?c:4294967296+c};function ka(a){n.google_image_requests||(n.google_image_requests=[]);var b=n.document.createElement("img");b.src=a;n.google_image_requests.push(b)};function w(a){return!(!a||!a.call)&&"function"===typeof a}var x=!!window.google_async_iframe_id,y=x&&window.parent||window;function z(){if(x&&!u(y)){var a="."+p.domain;try{for(;2<a.split(".").length&&!u(y);)p.domain=a=a.substr(a.indexOf(".")+1),y=window.parent}catch(b){}u(y)||(y=window)}return y};function A(a,b){var c=void 0===c?{}:c;this.error=a;this.context=b.context;this.msg=b.message||"";this.id=b.id||"jserror";this.meta=c};var la=/^https?:\/\/(\w|-)+\.cdn\.ampproject\.(net|org)(\?|\/|$)/;function B(a){a=a||C();for(var b=new D(n.location.href,!1),c=null,e=a.length-1,d=e;0<=d;--d){var f=a[d];!c&&la.test(f.url)&&(c=f);if(f.url&&!f.g){b=f;break}}c=null;d=a.length&&a[e].url;0!=b.depth&&d&&(c=a[e]);return new ma(b,c)}
function C(a){var b=a||n,c=[],e=null;do{var d=b;if(u(d)){var f=d.location.href;e=d.document&&d.document.referrer||null}else f=e,e=null;c.push(new D(f||""));try{b=d.parent}catch(g){b=null}}while(b&&d!=b);d=0;for(b=c.length-1;d<=b;++d)c[d].depth=b-d;d=a||n;if(d.location&&d.location.ancestorOrigins&&d.location.ancestorOrigins.length==c.length-1)for(a=1;a<c.length;++a)b=c[a],b.url||(b.url=d.location.ancestorOrigins[a-1]||"",b.g=!0);return c}function ma(a,b){this.b=a;this.a=b}
function D(a,b){this.url=a;this.g=!!b;this.depth=null};function E(){this.c="&";this.f=!1;this.b={};this.h=0;this.a=[]}function F(a,b){var c={};c[a]=b;return[c]}function G(a,b,c,e,d){var f=[];v(a,function(g,h){(g=H(g,b,c,e,d))&&f.push(h+"="+g)});return f.join(b)}
function H(a,b,c,e,d){if(null==a)return"";b=b||"&";c=c||",$";"string"==typeof c&&(c=c.split(""));if(a instanceof Array){if(e=e||0,e<c.length){for(var f=[],g=0;g<a.length;g++)f.push(H(a[g],b,c,e+1,d));return f.join(c[e])}}else if("object"==typeof a)return d=d||0,2>d?encodeURIComponent(G(a,b,c,e,d+1)):"...";return encodeURIComponent(String(a))}function I(a,b,c,e){a.a.push(b);a.b[b]=F(c,e)}
function na(a,b,c){b=b+"//pagead2.googlesyndication.com"+c;var e=oa(a)-c.length;if(0>e)return"";a.a.sort(function(ua,va){return ua-va});c=null;for(var d="",f=0;f<a.a.length;f++)for(var g=a.a[f],h=a.b[g],m=0;m<h.length;m++){if(!e){c=null==c?g:c;break}var k=G(h[m],a.c,",$");if(k){k=d+k;if(e>=k.length){e-=k.length;b+=k;d=a.c;break}else a.f&&(d=e,k[d-1]==a.c&&--d,b+=k.substr(0,d),d=a.c,e=0);c=null==c?g:c}}a="";null!=c&&(a=d+"trn="+c);return b+a}
function oa(a){var b=1,c;for(c in a.b)b=c.length>b?c.length:b;return 3997-b-a.c.length-1};function J(a,b,c,e){if(Math.random()<(e||.01))try{if(c instanceof E)var d=c;else d=new E,v(c,function(g,h){var m=d,k=m.h++;g=F(h,g);m.a.push(k);m.b[k]=g});var f=na(d,a.a,"/pagead/gen_204?id="+b+"&");f&&ka(f)}catch(g){}};var K=null;function L(){var a=n.performance;return a&&a.now&&a.timing?Math.floor(a.now()+a.timing.navigationStart):ea()}function M(){var a=void 0===a?n:a;return(a=a.performance)&&a.now?a.now():null};function pa(a,b,c){this.label=a;this.type=b;this.value=c;this.duration=0;this.uniqueId=Math.random();this.slotId=void 0};var N=n.performance,qa=!!(N&&N.mark&&N.measure&&N.clearMarks),O=function(a){var b=!1,c;return function(){b||(c=a(),b=!0);return c}}(function(){var a;if(a=qa){var b;if(null===K){K="";try{a="";try{a=n.top.location.hash}catch(c){a=n.location.hash}a&&(K=(b=a.match(/\bdeid=([\d,]+)/))?b[1]:"")}catch(c){}}b=K;a=!!b.indexOf&&0<=b.indexOf("1337")}return a});
function P(){var a=Q;this.b=[];this.c=a||n;var b=null;a&&(a.google_js_reporting_queue=a.google_js_reporting_queue||[],this.b=a.google_js_reporting_queue,b=a.google_measure_js_timing);this.a=O()||(null!=b?b:1>Math.random())}function R(a){a&&N&&O()&&(N.clearMarks("goog_"+a.label+"_"+a.uniqueId+"_start"),N.clearMarks("goog_"+a.label+"_"+a.uniqueId+"_end"))}
P.prototype.start=function(a,b){if(!this.a)return null;var c=M()||L();a=new pa(a,b,c);b="goog_"+a.label+"_"+a.uniqueId+"_start";N&&O()&&N.mark(b);return a};function S(){var a=T;this.c=U;this.f=this.b;this.a=void 0===a?null:a}S.prototype.b=function(a,b,c,e,d){d=d||"jserror";try{var f=new E;f.f=!0;I(f,1,"context",a);b.error&&b.meta&&b.id||(b=new A(b,{message:V(b)}));b.msg&&I(f,2,"msg",b.msg.substring(0,512));var g=b.meta||{};if(e)try{e(g)}catch(m){}b=[g];f.a.push(3);f.b[3]=b;var h=B();h.a&&I(f,4,"top",h.a.url||"");I(f,5,"url",h.b.url||"");J(this.c,d,f,c)}catch(m){try{J(this.c,d,{context:"ecmserr",rctx:a,msg:V(m),url:h&&h.b.url},c)}catch(k){}}return!0};
function V(a){var b=a.toString();a.name&&-1==b.indexOf(a.name)&&(b+=": "+a.name);a.message&&-1==b.indexOf(a.message)&&(b+=": "+a.message);if(a.stack){a=a.stack;try{-1==a.indexOf(b)&&(a=b+"\n"+a);for(var c;a!=c;)c=a,a=a.replace(/((https?:\/..*\/)[^\/:]*:\d+(?:.|\n)*)\2/,"$1");b=a.replace(/\n */g,"\n")}catch(e){}}return b};var U,W,Q=z(),T=new P;function ra(){if(!Q.google_measure_js_timing){var a=T;a.a=!1;a.b!=a.c.google_js_reporting_queue&&(O()&&ha(a.b,R),a.b.length=0)}}U=new function(){var a=void 0===a?fa:a;this.a="http:"===a.location.protocol?"http:":"https:"};W=new S;if("complete"==Q.document.readyState)ra();else if(T.a){var sa=function(){ra()},ta=Q;ta.addEventListener&&ta.addEventListener("load",sa,!1)};function wa(a){var b=a.indexOf("?");0<=b&&(a=a.substring(0,b));b=a.indexOf("#");0<=b&&(a=a.substring(0,b));return a}
function xa(a){var b={},c=C(a);c=B(c);b.url=wa(c.a?c.a.url:c.b.url);try{var e=a.history.length}catch(d){e=0}b.u_his=e;e=0;c=a;do{e++;try{c=c.parent!==c?c.parent:null}catch(d){c=null}}while(c&&20>=e);b.nhd=e;a.screen&&(b.u_w=a.screen.width,b.u_h=a.screen.height,b.u_aw=a.screen.availWidth,b.u_ah=a.screen.availHeight);a.navigator&&a.navigator.plugins&&(b.u_nplug=a.navigator.plugins.length);a=u(a.top)&&a.top.document?wa(a.top.document.referrer):null;b.ref=a;return b}
function ya(){var a=void 0===a?window:a;a=xa(a);if(a=Object.entries(a).filter(function(b){b=l(b);b.next();return(b=b.next().value)||0===b}).map(function(b){var c=l(b);b=c.next().value;c=c.next().value;return encodeURIComponent(String(b))+"="+encodeURIComponent(String(c))}).join("&"))a=a+"&gdemsign="+String(ja(a)),a=ia(a);return a};function za(){if(!n.gDemandSignals){n.gDemandSignals=ya();var a=window,b=z();try{if(p.createEvent){var c=p.createEvent("CustomEvent");c.initCustomEvent("googledemandsignals",!0,!0,"");a.dispatchEvent(c)}else if(w(b.CustomEvent)){var e=new b.CustomEvent("googledemandsignals",{bubbles:!0,cancelable:!0,detail:""});a.dispatchEvent(e)}else if(w(b.Event)){var d=new Event("googledemandsignals",{bubbles:!0,cancelable:!0});a.dispatchEvent(d)}}catch(f){}}}var X;
try{if(W.a&&W.a.a){X=W.a.start((478).toString(),3);za();var Y=W.a,Z=X;if(Y.a&&"number"==typeof Z.value){var Aa=M()||L();Z.duration=Aa-Z.value;var Ba="goog_"+Z.label+"_"+Z.uniqueId+"_end";N&&O()&&N.mark(Ba);!Y.a||2048<Y.b.length||Y.b.push(Z)}}else za()}catch(a){var Ca=!0;try{R(X),Ca=W.f(478,new A(a,{message:V(a)}),void 0,void 0)}catch(b){W.b(217,b)}if(!Ca)throw a;};}).call(this);