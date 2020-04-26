
           (function () {
    var pvs = window.top.location == window.self.location ? 1 : 2;
    if (window.DotMetricsInitScript == undefined) {
        window.DotMetricsInitScript = true;

        var rand=new Date().getTime();
        var pvid = (Date.now().toString(36) + Math.random().toString(36).substr(2, 24));
        var domain = window.location.hostname;
        var pageUrl = encodeURIComponent(window.location);
        var imgUrl = "https://script.dotmetrics.net/hit.gif?id=2095&url=" + pageUrl + "&dom=" + domain + "&r=" + rand + "&pvs=" + pvs + "&pvid=" + pvid;

        var im=new Image;
        im.src = imgUrl;
        im.onload = function (){im.onload=null};
        if(pvs==2){return;}

        function NewDotMetricsLoad(DotMetricsContentLoadedFunction) {
            if (document.readyState != undefined && document.readyState != 'loading') {
                setTimeout(function () {
                    DotMetricsContentLoadedFunction();
                }, 100);
            } else if (document.addEventListener) {
                document.addEventListener("DOMContentLoaded", DotMetricsContentLoadedFunction, false);
            } else if (document.attachEvent) {
                document.attachEvent("onreadystatechange", DotMetricsContentLoadedFunction);
            } else if (window.addEventListener) {
                window.addEventListener("load", DotMetricsContentLoadedFunction, false);
            } else if (window.attachEvent) {
                window.attachEvent("onload", DotMetricsContentLoadedFunction);
            }
            if (window.location.href.indexOf('dotmetrics_debug=true') >= 0){
                DotMetricsContentLoadedFunction();
            }
        }

        NewDotMetricsLoad(function () {
            if (document.createElement) {
                if (typeof window.DotMetricsSettings == 'undefined') {
                    window.DotMetricsSettings =
                                {
                                    CurrentPage: window.location,
                                    Debug: false,
                                    DataUrl: "https://script.dotmetrics.net/SiteEvent.dotmetrics",
                                    PostUrl: "https://script.dotmetrics.net/DeviceInfo.dotmetrics",
                                    ScriptUrl:  "https://script.dotmetrics.net/Scripts/script.v62.js?v=144",
                                    ScriptDebugUrl:  "https://demo-script.dotmetrics.net/Scripts/script.debug-css-test.js?v=dc3a6548-ea35-4ba9-b63d-fab27a6c71c0",
                                    PingUrl: "https://script.dotmetrics.net/Ping.dotmetrics",
                                    AjaxEventUrl: "https://script.dotmetrics.net/AjaxEvent.dotmetrics",
                                    SiteSectionId: 2095,
                                    SiteId: 475,
                                    FlashUrl: "https://script.dotmetrics.net/Scripts/DotMetricsFlash.swf",
                                    TimeOnPage: 'DotMetricsTimeOnPage',
                                    AjaxEventTimeout: 2000,
                                    AdexEnabled: false,
                                    AdexConfigUrl: "https://adex.dotmetrics.net/adexConfig.js?v=144&id=2095",
                                    BeaconUrl: "https://script.dotmetrics.net/BeaconEvent.dotmetrics",
                                    PVID:pvid
                                };

                    var scriptUrl = window.DotMetricsSettings.ScriptUrl;
                    if (window.location.href.indexOf('dotmetrics_debug=true') >= 0){
                        scriptUrl = window.DotMetricsSettings.ScriptDebugUrl;
                    }

                    var fileref = document.createElement('script');
                        fileref.setAttribute("type", "text/javascript");
                        fileref.setAttribute("src", scriptUrl);
                        fileref.setAttribute("async", "async");
                        if (typeof fileref != "undefined") {
                            document.getElementsByTagName("head")[0].appendChild(fileref);
                        }

                    window.postMessage({ type: 'DotmetricsDoorEvent', siteId: DotMetricsSettings.SiteId, sectionId: DotMetricsSettings.SiteSectionId},'*');

                    

                    if(window.DotMetricsSettings.AdexEnabled){
	                    fileref = document.createElement('script');
	                    fileref.setAttribute("type", "text/javascript");
	                    fileref.setAttribute("src", window.DotMetricsSettings.AdexConfigUrl);
	                    fileref.setAttribute("async", "async");
	                    if (typeof fileref != "undefined") {
	                         document.getElementsByTagName("head")[0].appendChild(fileref);
                        }
                    }
                }
            }
        });
    }
})(window);