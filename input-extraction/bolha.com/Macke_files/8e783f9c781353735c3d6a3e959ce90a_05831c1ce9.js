(window.webpackJsonp=window.webpackJsonp||[]).push([[13],{756:function(e,t){var a=/^(?:submit|button|image|reset|file)$/i,i=/^(?:input|select|textarea|keygen)/i,n=/(\[[^\[\]]*\])/g;function r(e,t,a){if(t.match(n)){!function e(t,a,i){if(0===a.length)return t=i;var n=a.shift(),r=n.match(/^\[(.+?)\]$/);if("[]"===n)return t=t||[],Array.isArray(t)?t.push(e(null,a,i)):(t._values=t._values||[],t._values.push(e(null,a,i))),t;if(r){var s=r[1],c=+s;isNaN(c)?(t=t||{})[s]=e(t[s],a,i):(t=t||[])[c]=e(t[c],a,i)}else t[n]=e(t[n],a,i);return t}(e,function(e){var t=[],a=new RegExp(n),i=/^([^\[\]]*)/.exec(e);for(i[1]&&t.push(i[1]);null!==(i=a.exec(e));)t.push(i[1]);return t}(t),a)}else{var i=e[t];i?(Array.isArray(i)||(e[t]=[i]),e[t].push(a)):e[t]=a}return e}function s(e,t,a){return a=a.replace(/(\r)?\n/g,"\r\n"),a=(a=encodeURIComponent(a)).replace(/%20/g,"+"),e+(e?"&":"")+encodeURIComponent(t)+"="+a}e.exports=function(e,t){"object"!=typeof t?t={hash:!!t}:void 0===t.hash&&(t.hash=!0);for(var n=t.hash?{}:"",c=t.serializer||(t.hash?r:s),o=e&&e.elements?e.elements:[],l=Object.create(null),u=0;u<o.length;++u){var h=o[u];if((t.disabled||!h.disabled)&&h.name&&(i.test(h.nodeName)&&!a.test(h.type))){var d=h.name,f=h.value;if("checkbox"!==h.type&&"radio"!==h.type||h.checked||(f=void 0),t.empty){if("checkbox"!==h.type||h.checked||(f=""),"radio"===h.type&&(l[h.name]||h.checked?h.checked&&(l[h.name]=!0):l[h.name]=!1),null==f&&"radio"==h.type)continue}else if(!f)continue;if("select-multiple"!==h.type)n=c(n,d,f);else{f=[];for(var v=h.options,b=!1,p=0;p<v.length;++p){var m=v[p],S=t.empty&&!m.value,g=m.value||S;m.selected&&g&&(b=!0,n=t.hash&&"[]"!==d.slice(d.length-2)?c(n,d+"[]",m.value):c(n,d,m.value))}!b&&t.empty&&(n=c(n,d,""))}}}if(t.empty)for(var d in l)l[d]||(n=c(n,d,""));return n}},834:function(e,t,a){"use strict";a.r(t);var i=a(42),n=a(9),r=a(12),s=a(10),c=a(6),o=a(24),l=a(11),u=a(4),h=a(7),d=a(20),f=a(0),v=a(27),b=a.n(v),p=a(43),m=a.n(p),S=a(15),g=a(39),O=a(16),j=a(13),C=a(756),y=a.n(C),N=a(23),_=a(34),k=a(5),x=a.n(k),A=a(19),E=a(3),$=a(41),F=a(31);function T(){var e=Object(i.a)(['\n\t\t\t<div class="notification notification--','">\n\t\t\t\t<p>',"</p>\n\t\t\t</div>\n\t\t"]);return T=function(){return e},e}function w(){var e=Object(i.a)(['\n\t\t\t<div class="notification notification--','">\n\t\t\t\t<p>',"</p>\n\t\t\t</div>\n\t\t"]);return w=function(){return e},e}function L(){var e=Object(i.a)(['\n\t\t\t\t\t<a\n\t\t\t\t\t\thref="','"\n\t\t\t\t\t\tclass="SavedSearchCreate-baseAction SavedSearchCreate-baseAction--edit"\n\t\t\t\t\t\tdata-test-id="saved_search.create.go_to_edit"\n\t\t\t\t\t>\n\t\t\t\t\t\t<span class="TextWithIcon"\n\t\t\t\t\t\t\t><i\n\t\t\t\t\t\t\t\tclass="icon icon--xs icon--saved-search-create"\n\t\t\t\t\t\t\t\taria-hidden="true"\n\t\t\t\t\t\t\t\trole="presentation"\n\t\t\t\t\t\t\t></i\n\t\t\t\t\t\t\t>',"</span\n\t\t\t\t\t\t>\n\t\t\t\t\t</a>\n\t\t\t\t"]);return L=function(){return e},e}function P(e){return Object.entries(e).map((function(e){var t=Object(d.a)(e,2),a=t[0],i=t[1];return"category_id"===a?["categoryId",i]:[a,i]})).reduce((function(e,t){var a=Object(d.a)(t,2),i=a[0],n=a[1];return Object(h.a)({},e,Object(u.a)({},i,n))}),{})}var R=function(e){function t(e){var a;return Object(n.a)(this,t),(a=Object(s.a)(this,Object(c.a)(t).call(this,e))).setupElements(),a.setupComponentDisplay(),a}return Object(l.a)(t,e),Object(r.a)(t,[{key:"setupElements",value:function(){this.$form=document.querySelector("#".concat(this.props.formId))}},{key:"preventFormSubmit",value:function(){var e=this;x.a.publish("entityListFormHandler",(function(t){t.preventDefault(),e.submitFormEvent()}))}},{key:"unpreventFormSubmit",value:function(){x.a.publish("entityListFormHandler",null)}},{key:"setupComponentDisplay",value:Object(f.a)((function(){var e=this;if(e.setState({receiveNotifications:e.$receiveNotifications.checked,notificationChannel:e.$notificationChannel.find((function(e){return e.checked})).value,notificationFrequency:e.$notificationFrequency.find((function(e){return e.checked})).value}),N.a.isLoggedIn())return e.setState({disableExpand:!0}),Object(f.j)((function(){return Object(f.b)(e.checkIfSavedSearchExists(!0),(function(t){if(e.setState({expand:!1,disableExpand:t,savedSearchExists:t}),!t)return e.setState({loading:!0}),Object(f.b)(e.getSuggestedTitle(!0),(function(t){e.setState({title:t})}))}))}),(function(t,a){return e.setState({loading:!1}),Object(f.m)(t,a)}));e.setState({disableExpand:!1,title:e.props.defaultSuggestedTitle})}))},{key:"submitFormEvent",value:Object(f.a)((function(){var e=this;return e.setState({loading:!0}),Object(f.g)(Object(f.j)((function(){return Object(f.e)((function(){return Object(f.b)(e.submitForm(),(function(){e.trackEvent(),e.setState({genericError:!1,savedSearchExists:!0,expand:!1})}))}),(function(t){Object(A.a)(t),e.setState({genericError:t.errors[0].title})}))}),(function(t,a){return e.setState({loading:!1}),Object(f.m)(t,a)})))}))},{key:"trackEvent",value:function(){var e=this.props.searchContext,t="".concat("").concat("Email"," Notification ").concat(e," saved");Object(_.b)(["_trackEvent","Saved Searches",t,this.props.searchUrl,0,!0])}},{key:"getSearchParameters",value:function(e){var t,a=arguments.length>1&&void 0!==arguments[1]&&arguments[1],i=b.a.parse(e,!0),n=i.query,r=m.a.parse(y()(this.$form)),s=[];a?(s.push(r),s.push(this.props.searchParameters)):(s.push(this.props.searchParameters),s.push(r)),s.push(null!==(t=n)&&void 0!==t?t:{});var c=s.reduce((function(e,t){return Object(h.a)({},e,{},P(t))}),{});return delete c.ctl,delete c["saved_search_create[notificationChannel]"],m.a.stringify(c)}},{key:"getSuggestedTitle",value:Object(f.a)((function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0],a=new j.Model("saved-search");a.setAttribute("searchContext",e.props.searchContext),a.setAttribute("searchParameters",e.getSearchParameters(e.props.searchUrl,t));var i=a.serialize();return Object(f.b)(Object(O.default)({url:"/ccapi/v2/user/me/saved-searches/suggest-title",method:"POST",data:i}),(function(e){var t=new j.Store;return t.sync(e),t.find("saved-search").title}))}))},{key:"checkIfSavedSearchExists",value:Object(f.a)((function(){var e=this,t=arguments.length>0&&void 0!==arguments[0]&&arguments[0],a=new j.Model("saved-search");a.setAttribute("searchContext",e.props.searchContext),a.setAttribute("searchParameters",e.getSearchParameters(e.props.searchUrl,t));var i=a.serialize();return Object(f.e)((function(){return Object(f.b)(Object(O.default)({url:"/ccapi/v2/user/me/saved-searches/exists",method:"POST",data:i,dataType:"text"}),(function(){return!1}))}),(function(){return!0}))}))},{key:"submitForm",value:Object(f.a)((function(){var e=new j.Model("saved-search");e.setAttribute("title",this.state.title),e.setAttribute("receiveNotifications",this.state.receiveNotifications),e.setAttribute("notificationChannel",this.state.notificationChannel),e.setAttribute("searchContext",this.props.searchContext),e.setAttribute("searchParameters",this.getSearchParameters(this.props.searchUrl));var t=e.serialize();return Object(f.c)(Object(O.default)({url:"/ccapi/v2/user/me/saved-searches",method:"POST",data:t}))}))},{key:"render",value:function(e,t){if("loading"===e&&(this.$title.disabled=t,this.$cancel.disabled=t,this.$receiveNotifications.closest(".form-label").classList.toggle("is-disabled",t),this.$receiveNotifications.disabled=t,this.$notificationChannel.forEach((function(e){e.closest(".form-label").classList.toggle("is-disabled",t),e.disabled=t})),this.$notificationFrequency.forEach((function(e){e.closest(".form-label").classList.toggle("is-disabled",!0),e.disabled=!0}))),"title"===e&&(this.$title.value=t),"title"===e||"loading"===e){var a=""===this.state.title||!0===this.state.loading;null!==this.$submit&&(this.$submit.disabled=a)}if("disableExpand"===e&&(this.$expand.disabled=t),"savedSearchExists"===e&&t){var i=Object(g.b)(L(),this.props.savedSearchEditUrl,Object(E.b)("ad_search.saved_search.create.success"));this.$expand.replaceWith(i)}if("expand"===e&&(t?this.$information.classList.remove("hidden"):(this.$information.classList.add("hidden"),this.renderRemoveNotifications())),"genericError"===e&&(!0===t?this.renderAddNotifications(Object(E.b)("ad_search.saved_search.create.error"),"invalid"):t?this.renderAddNotifications(Object(E.b)("ad_search.".concat(t)),"invalid"):this.renderRemoveNotifications()),"estimatedNumberOfResults"===e)if(""!==t){var n=t;"search"===this.props.searchContext&&this.isSearchTooGenericForNotifications&&(n="".concat(Object(E.b)("ad_search.saved_search.create.precise_results"),"<br /><br />").concat(t)),this.renderAddNotifications(n,"info")}else this.renderRemoveNotifications();if("notificationChannel"===e)if("push_notification"===t){var r=this.resolveMobileAppStoreLink(),s=r.url,c=r.external;this.renderAddNotificationChannelNotifications("".concat(Object(E.b)("ad_search.saved_search.create.push_notification_usage_notice"),"<br /><br />").concat(Object(E.b)("ad_search.saved_search.create.push_notification_usage_notice_app_link",{linkStartTag:'<a href="'.concat(s,'"').concat(c?' target="_blank" rel="noopener nofollow"':"",">"),linkEndTag:"</a>"}),"."),"info")}else this.renderRemoveNotificationChannelNotifications()}},{key:"resolveMobileAppStoreLink",value:function(){return Object($.b)()?{url:this.props.mobileAppIosAppStoreUrl,external:!0}:Object($.a)()?{url:this.props.mobileAppAndroidAppStoreUrl,external:!0}:{url:Object(F.b)({name:"mobile_app_information"}),external:!1}}},{key:"renderAddNotifications",value:function(e,t){var a=Object(g.b)(w(),t,e);this.$notifications.classList.remove("hidden"),this.$notifications.innerHTML="",this.$notifications.appendChild(a)}},{key:"renderRemoveNotifications",value:function(){this.$notifications.classList.add("hidden"),this.$notifications.innerHTML=""}},{key:"renderAddNotificationChannelNotifications",value:function(e,t){var a=Object(g.b)(T(),t,e);this.$notificationChannelNotifications.classList.remove("hidden"),this.$notificationChannelNotifications.innerHTML="",this.$notificationChannelNotifications.appendChild(a)}},{key:"renderRemoveNotificationChannelNotifications",value:function(){this.$notificationChannelNotifications.classList.add("hidden"),this.$notificationChannelNotifications.innerHTML=""}},{key:"remove",value:function(){Object(o.a)(Object(c.a)(t.prototype),"remove",this).call(this),this.unpreventFormSubmit()}},{key:"handleReceiveNotifications",value:Object(f.a)((function(e){var t=this;if(e){t.setState({loading:!0});var a=new j.Model("notification-search-result-estimate");a.setAttribute("searchContext",t.props.searchContext),a.setAttribute("searchParameters",t.getSearchParameters(t.props.searchUrl));var i=a.serialize();return Object(f.b)(Object(O.default)({url:"/ccapi/v2/notification-search-result-estimate",method:"POST",data:i}),(function(a){var i=new j.Store;i.sync(a);var n=i.findAll("notification-search-result-estimate"),r=Object(d.a)(n,1)[0];t.isSearchTooGenericForNotifications=r.isSearchTooGenericForNotifications;var s=t.getEstimatedNumberOfResultsForDaysMessage(r.resultCountForTimeWindow,r.timeWindowInDays);t.setState({loading:!1,receiveNotifications:e,estimatedNumberOfResults:s})}))}t.setState({receiveNotifications:e,estimatedNumberOfResults:""})}))},{key:"getEstimatedNumberOfResultsForDaysMessage",value:function(e,t){var a=e/t;return 0===a?Object(E.b)("ad_search.saved_search.create.no_results_in_last_two_weeks"):a>=1.8?Object(E.b)("ad_search.saved_search.create.results_per_day",{results:Math.round(a)}):a<1.8?Object(E.b)("ad_search.saved_search.create.results_per_week",{results:Math.round(7*a)}):""}}]),t}(S.a);Object(u.a)(R,"el",".SavedSearchCreate"),Object(u.a)(R,"events",{"input .SavedSearchCreate-title":function(e){this.setState({title:e.target.value})},"click .SavedSearchCreate-baseAction--expand":function(){this.setState({expand:!this.state.expand})},"click .SavedSearchCreate-action--cancel":function(){this.setState({expand:!1})},"click .SavedSearchCreate-action--submit":function(){this.submitFormEvent()},"change .SavedSearchCreate-receiveNotifications":function(e){this.handleReceiveNotifications(e.target.checked)},"change .SavedSearchCreate-notificationChannel":function(e){this.setState({notificationChannel:e.target.value})},"change .SavedSearchCreate-notificationFrequency":function(e){this.setState({notificationFrequency:e.target.value})},"focus .SavedSearchCreate-title":"preventFormSubmit","blur .SavedSearchCreate-title":"unpreventFormSubmit"}),Object(u.a)(R,"childrenEl",{expand:".SavedSearchCreate-baseAction--expand",information:".SavedSearchCreate-information",title:".SavedSearchCreate-title",submit:".SavedSearchCreate-action--submit",cancel:".SavedSearchCreate-action--cancel",notifications:".SavedSearchCreate-notifications",notificationChannelNotifications:".SavedSearchCreate-notificationChannelNotifications",receiveNotifications:".SavedSearchCreate-receiveNotifications","notificationChannel[]":".SavedSearchCreate-notificationChannel","notificationFrequency[]":".SavedSearchCreate-notificationFrequency"}),Object(u.a)(R,"defaultProps",{searchContext:"",searchParameters:{},searchUrl:"",savedSearchEditUrl:"",loginUrl:"",formId:"",defaultSuggestedTitle:"",hasMobilePushNotificationsSupport:!0,mobileAppIosAppStoreUrl:"",mobileAppAndroidAppStoreUrl:""}),t.default=R}}]);