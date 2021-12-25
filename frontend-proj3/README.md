# 前端运行方法(frontend-proj3)
安装 node.js，详见：[安装教程](https://zhuanlan.zhihu.com/p/82347262)

安装 Quasar CLI，详见：http://www.quasarchs.com/quasar-cli/installation#introduction


# 技术转移文档（`篇幅限制的都写了"详见参考"`）
代码目录结构说明：

详见：http://www.quasarchs.com/quasar-cli/directory-structure#introduction

代码必要说明：

见代码注释

部署过程、启动运行流程：


**Install the dependencies**
```bash
npm install
```

**Start the app in development mode (hot-code reloading, error reporting, etc.)**
```bash
quasar dev
```

依赖的第三方库的目录及版本：
```json
{
  "name": "frontend-proj3",
  "author": "otrap",
  "scripts": {
    "lint": "eslint --ext .js,.vue ./",
    "test": "echo \"No test specified\" && exit 0"
  },
  "dependencies": {
    "@quasar/extras": "^1.0.0",
    "axios": "^0.21.1",
    "core-js": "^3.6.5",
    "echarts": "^5.2.2",
    "quasar": "^1.0.0"
  },
  "devDependencies": {
    "@quasar/app": "^2.0.0",
    "babel-eslint": "^10.0.1",
    "eslint": "^7.21.0",
    "eslint-config-prettier": "^8.1.0",
    "eslint-plugin-vue": "^7.7.0",
    "eslint-webpack-plugin": "^2.4.0"
  },
  "browserslist": [
    "last 10 Chrome versions",
    "last 10 Firefox versions",
    "last 4 Edge versions",
    "last 7 Safari versions",
    "last 8 Android versions",
    "last 8 ChromeAndroid versions",
    "last 8 FirefoxAndroid versions",
    "last 10 iOS versions",
    "last 5 Opera versions"
  ],
  "engines": {
    "node": ">= 10.18.1",
    "npm": ">= 6.13.4",
    "yarn": ">= 1.21.1"
  }
}

```
