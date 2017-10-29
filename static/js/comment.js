// function insertUbbUrl(n){var i=prompt("显示链接的文本.\n如果为空，那么将只显示超级链接地址",""),t;i!=null&&(t=prompt("http:// 超级链接","http://"),t!=""&&t!="http://"&&(i!=""?$("#"+n).parseHtml("[url="+t+"]"+i+"[/url]"):$("#"+n).parseHtml("[url]"+t+"[/url]")))}
//
// function insertUbbImg(n){var t=prompt("请先将图片上传到您的图库中，然后将图片地址拷下粘贴在此：","http://");t!=null&&$.trim(t)!=""&&t.toLowerCase()!="http://"&&$("#"+n).parseHtml("[img]"+t+"[/img]")}
//
// function insertUploadImg(n){$("#tbCommentBody").parseHtml("[img]"+n+"[/img]\n");$("#tbCommentBody").focus()}
//
// function insertUbbCode(){var n=450,t=400,r=(screen.width-n)/2,u=(screen.height-t)/2,i;document.domain="cnblogs."+location.hostname.substring(location.hostname.lastIndexOf(".")+1,location.hostname.length);i=window.open("/SyntaxHighlighter.htm","_blank","width="+n+",height="+t+",toolbars=0,resizable=1,left="+r+",top="+u);i.focus()}
// insertUBB=function(n,t){var r=$("#"+n).selection(),i;r==""?$("#tip_comment").html("请选择文字"):(i=t,t.indexOf("=")>=0&&(i=t.substring(0,t.indexOf("="))),$("#"+n).parseHtml("["+t+"]"+r+"[/"+i+"]"))}

//--------失败的作品------