"""Generate the committed static pages. Build dependency: Markdown==3.8.2."""
from pathlib import Path
from html import escape
import json,re,zipfile,hashlib
import markdown

ROOT=Path(__file__).resolve().parent.parent
DOMAIN='https://www.zhiyuxuan.click'
APK='/downloads/Scriptable-Android-0.2.3.apk'
VERSION='0.2.3'
def icon(name):
    paths={'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M19 5l-1.5 1.5m-11 11L5 19"/>','phone':'<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M10 5h4m-3 14h2"/>','clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v6l4 2"/>','book':'<path d="M12 5c-3-2-6-2-9-1v15c3-1 6-1 9 1 3-2 6-2 9-1V4c-3-1-6-1-9 1v15"/>'}
    return '<svg viewBox="0 0 24 24" aria-hidden="true">'+paths[name]+'</svg>'
def button(label,url,primary=False,download=False):return f'<a class="button{" primary" if primary else ""}" href="{url}"'+(' download' if download else '')+'>'+label+'</a>'
def header(active):
    links=[('/','首页','home'),('/cqu/','天气教程','weather'),('/scriptable/','软件','app')]
    return '<a class="skip" href="#main">跳到正文</a><header class="site-header"><div class="shell header-inner"><a class="brand" href="/"><span class="brand-mark">'+icon('sun')+'</span>晴天预约指南</a><nav class="header-nav" aria-label="主导航">'+''.join(f'<a href="{url}"'+(' class="active" aria-current="page"' if key==active else '')+'>'+label+'</a>' for url,label,key in links)+'</nav></div></header>'
def footer():return '''<footer class="site-footer"><div class="shell footer-inner"><div>由 awesome-sean 整理维护。<br>独立教程项目，与重庆大学、Scriptable、Apple 没有官方隶属或合作关系。</div><div class="footer-links"><a href="/cqu/iphone/">iPhone 教程</a><a href="/cqu/android/">安卓教程</a><a href="https://github.com/awesome-sean/cqu-sunny-reservation">天气脚本源码</a><a href="https://github.com/awesome-sean/scriptable-android">APK 源码</a></div></div></footer>'''
def page(title,description,body,path,active):
    html='<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f6f8fc"><meta name="description" content="'+escape(description,quote=True)+'"><link rel="canonical" href="'+DOMAIN+path+'"><link rel="icon" type="image/svg+xml" href="/assets/favicon.svg"><link rel="stylesheet" href="/assets/site.css?v=20261123"><script src="/assets/site.js?v=20261123" defer></script><title>'+escape(title)+' · 晴天预约指南</title></head><body data-site-version="guides-20261123">'+header(active)+'<main id="main" class="shell">'+body+'</main>'+footer()+'</body></html>'
    target=ROOT/(path.strip('/')+'/index.html' if path!='/' else 'index.html');target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf8')
def platforms():return '<div class="cards"><section class="card"><div class="card-icon">'+icon('phone')+'</div><h3>iPhone 使用教程</h3><p>安装 Scriptable，用快捷指令设置每天的天气检查。可选添加桌面小组件。</p>'+button('开始 iPhone 设置','/cqu/iphone/')+'</section><section class="card"><div class="card-icon">'+icon('clock')+'</div><h3>安卓使用教程</h3><p>安装 Scriptable Android，导入脚本，在应用内设置每天的执行时间。</p>'+button('开始安卓设置','/cqu/android/')+'</section></div>'
rules='''<div class="step-flow"><div><strong>每天检查</strong><p>按你设置的时间，查询北京时间后天的天气。</p></div><div><strong>晴天提醒</strong><p>白天预报严格为“晴”时，发送预约提醒。</p></div><div><strong>自行预约</strong><p>点击通知打开学校预约页面，登录并完成预约。</p></div></div>'''
hero='''<section class="hero"><div><p class="eyebrow">iPhone 与安卓使用指南</p><h1>重庆大学<br>晴天预约提醒</h1><p class="lead">每天看看后天的天气。白天预报为晴时，提醒你提前预约；从安装脚本到设置自动化，一步步完成。</p><div class="actions">'''+button('iPhone 教程','/cqu/iphone/',True)+button('安卓教程','/cqu/android/')+'''</div><p class="micro">支持定时通知，也可添加桌面天气小组件。</p></div><div class="hero-preview"><img src="/assets/iphone-widget.jpg" width="675" height="665" alt="天气小组件示例，展示后天的天气、温度与提醒状态"><p>桌面展示示例，天气以实际查询为准</p></div></section>'''
appstrip='<div class="app-strip"><img src="/assets/app-icon.png" width="76" height="76" alt="Scriptable Android 应用图标"><div><h2>Scriptable Android</h2><p>安卓端的脚本、小组件与自动化运行环境。</p></div>'+button('软件下载与说明','/scriptable/')+'</div>'
home=hero+'<section class="section"><div class="section-heading"><div><h2>按你的手机开始</h2><p>两套操作步骤，同一个晴天提醒。</p></div></div>'+platforms()+'</section><section class="section"><div class="section-heading"><div><h2>提醒是怎样触发的？</h2><p>例如 22 日检查 24 日的天气，晴天时提醒预约 24 日。</p></div></div>'+rules+'<p class="micro" style="margin-top:18px">预报来自 UAPI 的重庆市沙坪坝区，不是校园独立气象观测。项目只做提醒，不自动提交预约。</p></section><section class="section">'+appstrip+'</section>'
page('首页','重庆大学晴天预约提醒双平台教程、Scriptable Android 软件和脚本下载。',home,'/','home')
overview='<header class="page-head"><p class="breadcrumb"><a href="/">首页</a> / 天气预约提醒</p><p class="eyebrow">先选平台，再按步骤设置</p><h1>重庆大学晴天预约提醒</h1><p class="lead">检查北京时间后天的白天天气，严格为“晴”时提醒预约。不是检查未来两天中任意一天，也不把“多云转晴”算作晴天。</p></header>'+platforms()+'<section class="section" style="margin-top:38px"><h2>从检查到预约</h2>'+rules+'<div class="notice">小组件只展示天气。要收到通知，请在对应教程中完成定时自动化；学校可预约日期和开放时间以预约页面为准。</div><div class="actions">'+button('下载全部脚本','/downloads/cqu-weather-scripts.zip',False,True)+button('打开学校预约页面','https://mobilereserve.cqu.edu.cn/#/login')+'</div><p class="micro">脚本包包含两端脚本、通知测试脚本和使用说明，不含安卓 APK。</p></section><section class="section faq"><h2>先了解这几件事</h2><details><summary>为什么运行了，没有收到通知？</summary><p>天气脚本只有在后天白天预报为“晴”时才提醒。其他天气不提醒是正常的；还需检查通知权限以及自动化参数 notify。</p></details><details><summary>现在不是晴天，如何测试？</summary><p>每份教程都提供不判断天气、不联网的通知测试脚本。先手动运行，再设置 3～5 分钟后的定时任务，检查真实的通知触发时间。</p></details><details><summary>小组件多久刷新一次？</summary><p>刷新由系统与后台策略安排，不能代替定时通知。省电、网络或厂商限制可能导致延迟。</p></details></section>'
page('天气预约教程','重庆大学提前两天的晴天预约提醒：iPhone、安卓教程和脚本下载。',overview,'/cqu/','weather')

def guide(kind,title,description):
    md=markdown.Markdown(extensions=['tables','fenced_code','toc'])
    body=md.convert((ROOT/'content'/f'{kind}.md').read_text(encoding='utf8'))
    body=body.replace('<table>','<div class="table-wrap"><table>').replace('</table>','</table></div>')
    body=re.sub(r'<a href="(/downloads/[^\"]+\.(?:apk|js|zip))">',r'<a href="\1" download>',body)
    toc=''.join('<a href="#'+escape(x['id'],quote=True)+'">'+escape(x['name'])+'</a>' for x in md.toc_tokens if x['level']==2)
    if kind=='iphone':
        actions='<button class="button primary" data-copy-code="/downloads/cqu-weather-ios.txt">复制 iPhone 代码</button>'+button('打开代码 TXT','/downloads/cqu-weather-ios.txt')
        download=button('下载 iPhone JS','/downloads/cqu-weather-ios.js',False,True)
    else:
        actions=button('下载 Android APK',APK,True,True)+button('下载天气脚本','/downloads/cqu-weather-android.js',False,True)
        download=button('下载通知测试脚本','/downloads/test-notification.js',False,True)
    intro='<header class="page-head"><p class="breadcrumb"><a href="/cqu/">天气预约提醒</a> / '+title+'</p><h1>'+title+'</h1><p class="lead">'+description+'</p><div class="actions">'+actions+'</div><span id="copy-status" class="copy-status" aria-live="polite"></span></header>'
    layout='<div class="guide-layout"><aside class="toc"><p>本页步骤</p><nav aria-label="本页目录">'+toc+'</nav><div class="toc-download">'+download+'</div></aside><article class="guide-body">'+body+'</article></div>'
    page(title,description,intro+layout,'/cqu/'+kind+'/','weather')
guide('iphone','iPhone 设置教程','使用 Scriptable 与快捷指令，设置每天的晴天预约提醒。')
guide('android','安卓设置教程','安装 Scriptable Android，导入天气脚本，在应用内设置定时提醒。')

appcontent=markdown.markdown((ROOT/'content/app.md').read_text(encoding='utf8'),extensions=['tables','fenced_code'])
size=(ROOT/APK.lstrip('/')).stat().st_size/1024/1024
apphero='<section class="app-hero"><div><p class="breadcrumb"><a href="/">首页</a> / 软件下载</p><img class="app-icon" src="/assets/app-icon.png" width="84" height="84" alt="Scriptable Android 图标"><h1>Scriptable Android</h1><p class="lead">在安卓手机上运行 JavaScript，创建桌面小组件，让脚本按设定的时间自动执行。</p><div class="tags"><span class="tag">v'+VERSION+'</span><span class="tag">Android 8.0 及以上</span><span class="tag">MIT 许可</span></div><div class="actions">'+button('下载 APK · 0.2.3',APK,True,True)+button('查看安卓天气教程','/cqu/android/')+'</div><p class="download-meta">安装包约 '+f'{size:.2f}'+' MB · 原签名覆盖更新<br><a href="/downloads/SHA256.txt">查看 SHA-256 校验值</a></p></div><img class="app-shot" src="/assets/app-scripts.png" width="780" height="1688" alt="Scriptable Android 脚本列表界面"></section>'
page('Scriptable Android 下载','Scriptable Android 0.2.3 安卓 APK 下载、使用说明与开源来源。',apphero+'<section class="guide-body" style="margin-bottom:56px">'+appcontent+'</section>','/scriptable/','app')
paths=['/','/cqu/','/cqu/iphone/','/cqu/android/','/scriptable/']
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+DOMAIN+p+'</loc></url>' for p in paths)+'</urlset>',encoding='utf8')
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+DOMAIN+'/sitemap.xml\n')
with zipfile.ZipFile(ROOT/'downloads/cqu-weather-scripts.zip','w',zipfile.ZIP_DEFLATED) as archive:
    for file in ['cqu-weather-ios.js','cqu-weather-ios.txt','cqu-weather-android.js','test-notification.js','test-notification.txt','WEATHER-LICENSE.txt']:
        archive.write(ROOT/'downloads'/file,file)
    archive.writestr('使用说明.txt','重庆大学晴天预约提醒\n\niPhone 教程：'+DOMAIN+'/cqu/iphone/\n安卓教程：'+DOMAIN+'/cqu/android/\n\n天气任务参数填写 notify，小组件参数留空。\n测试脚本不判断天气，运行就提交测试通知。\n此包不含 APK；安卓安装包见 '+DOMAIN+'/scriptable/\n')
assert hashlib.sha256((ROOT/APK.lstrip('/')).read_bytes()).hexdigest()=='91d9dc82b93cfb3fbbfd349d0e5343f6a217e2ec378d61a80711b757cc96ec0a'
print('Generated five static pages, sitemap and downloadable script bundle. APK checksum verified.')
