# 晴天预约指南

公开网站：**https://www.zhiyuxuan.click**

网站源码现存放在 `awesome-sean/cqu-sunny-reservation`，与 iPhone、安卓教程和脚本共同维护。部署根目录为仓库根目录，生成的 HTML 已提交。

## 页面

| 地址 | 内容 |
| --- | --- |
| `/` | 教程与软件下载入口 |
| `/cqu/` | 重庆大学晴天预约提醒介绍 |
| `/cqu/iphone/` | iPhone 配置步骤、截图与代码复制 |
| `/cqu/android/` | 安卓安装、权限、定时提醒与小组件教程 |
| `/scriptable/` | Scriptable Android 介绍和 APK 下载 |

所有页面、图片、样式、脚本、脚本包和 APK 均在本站提供。页面加载不依赖 Google 字体、第三方 JavaScript 或 GitHub 图片；外部链接仅用于官方应用、预约入口和源码参考。

当前 APK 的应用内更新仍查询 GitHub。网站提供独立的 APK 下载，不会改变 APK 内部的更新源。

## 维护

修改 `content/` 内的 Markdown 后生成 HTML：

```sh
python -m pip install -r tools/requirements-build.txt
python tools/build_site.py
```

样式位于 `assets/site.css`，复制代码交互位于 `assets/site.js`。生成的 HTML 已提交，线上按静态站点部署，不需要额外构建依赖。

本地预览：

```sh
node tools/serve.cjs
```

更新 APK 时需同步 `downloads/` 文件、SHA-256 校验、`tools/build_site.py` 和 `content/app.md` 的版本文字，以及 `vercel.json` 中的下载文件头，然后重新生成静态页面。

## 来源与许可

- 天气教程与脚本：[awesome-sean/cqu-sunny-reservation](https://github.com/awesome-sean/cqu-sunny-reservation)，[MIT 许可](downloads/WEATHER-LICENSE.txt)。
- 安卓 APK：[awesome-sean/scriptable-android](https://github.com/awesome-sean/scriptable-android)，基于 [EdenleeGitHub/scriptable-android](https://github.com/EdenleeGitHub/scriptable-android) v0.2.1 派生维护；保留其 [MIT](downloads/ANDROID-LICENSE.txt) 和 [第三方声明](downloads/ANDROID-THIRD-PARTY-NOTICES.txt)。
- APK 内同样包含完整许可。本站为独立教程项目，与重庆大学、Scriptable、Apple 没有官方隶属或合作关系。
