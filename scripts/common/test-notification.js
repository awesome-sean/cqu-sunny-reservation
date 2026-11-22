const now = new Date();
const time = new Date(now.getTime() + 8 * 3600000)
  .toISOString().slice(0, 19).replace("T", " ");
const automatic = typeof config !== "undefined" && config.runsInAutomation;
const source = automatic ? "安卓后台自动化" : "Scriptable 脚本执行";

const notification = new Notification();
notification.title = "定时通知测试成功";
notification.body = "执行方式：" + source + "\n北京时间：" + time
  + "\n本测试不判断天气，也不请求网络。";
notification.sound = "default";
await notification.schedule();

const message = "已提交测试通知；北京时间 " + time;
console.log(message);
Script.setShortcutOutput(message);
Script.complete();
