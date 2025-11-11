/**
 * ------------------------------------------------------------------
 * Part 1: 核心环境设置 (V8引擎技巧与原型链伪装)
 * ------------------------------------------------------------------
 */

// 引入Node.js核心模块，用于创建无法被 typeof 检测到的特殊对象
const v8 = require('v8');
const vm = require('vm');
v8.setFlagsFromString('--allow-natives-syntax');
const undetectable = vm.runInThisContext("%GetUndetectable()");
v8.setFlagsFromString('--no-allow-natives-syntax');

// [关键修复]
// 设置全局 window 对象，让它和 Node.js 的 global 指向同一个对象。
// 绝对不要 delete global，否则会破坏 Node.js 内部模块的依赖。
window = global;

// 伪装 window 的类型，使其通过 Object.prototype.toString.call(window) 检测
function Window(){};
window.Window = Window;
window.__proto__ = Window.prototype;
Object.defineProperties(window, {
    [Symbol.toStringTag]: {
        value: 'Window',
        configurable: true
    }
});

// 伪装 document 的类型和原型链
function Document(){}
function HTMLDocument(){}
Object.setPrototypeOf(HTMLDocument.prototype, Document.prototype);
const document = new HTMLDocument();

// 将 require 放在这里，因为它可能需要 window 和 document
require("./content"); // 假设这个文件定义了全局变量 content

/**
 * ------------------------------------------------------------------
 * Part 2: 模拟的DOM元素对象池
 * ------------------------------------------------------------------
 */

// 用于模拟 document.getElementsByTagName('script') 的返回值
const scripts = [
    {
        type: "text/javascript", r: 'm',
        parentElement: {
            getAttribute: function(args) { if (args == 'r') return 'm'; },
            removeChild: function () {}
        },
        getAttribute: function(args) { if (args == 'r') return 'm'; }
    },
    {
        type: "text/javascript", r: 'm',
        src: "/fpqQrgG7L6po/eaKJbLE9bqof.294cc83.js",
        parentElement: {
            getAttribute: function() {},
            removeChild: function () {}
        },
        getAttribute: function(args) { if (args == 'r') return 'm'; }
    }
];

// 模拟页面上的 meta 标签
const meta1 = {
    content: content, // 使用 content.js 中定义的变量
    r: 'm',
    getAttribute: function(tag){
        if (tag === 'r') return 'm';
        console.log("meta1 => getAttribute", tag);
    },
    parentNode:{ removeChild: function() {} }
};

// 模拟 div > i 结构
const i1 = { length: 0 };
const div1 = {
    getElementsByTagName: function (tag){
        if (tag === 'i') return i1;
        console.log("div1 => getElementsByTagName", tag);
    }
};

// 模拟 a 标签
const a1 = {
    href: 'datasearch/home-index.html',
    protocol: 'https:',
    hostname: 'www.nmpa.gov.cn',
    pathname: 'datasearch/home-index.html'
};

// 准备多个 input 对象，因为 createElement 每次调用都应返回新对象
const l_input = {}, l2_input = {}, l3_input = {};

// 准备 form 对象，并为其关键属性设置 getter/setter 钩子，用于调试和绕过检测
const form1 = {};
let form_action_storage = '';
Object.defineProperty(form1, 'action', {
    get() {
        console.log('HOOK: form.action 被读取, 返回第一个input对象');
        return l_input;
    },
    set(v) {
        console.log('HOOK: form.action 被设置为 ->', v);
        form_action_storage = v;
    }
});
Object.defineProperty(form1, 'textContent', {
    get() {
        console.log('HOOK: form.textContent 被读取, 返回第二个input对象');
        return l2_input;
    },
    set(v) {
        console.log('HOOK: form.textContent 被设置为 ->', v);
    }
});

/**
 * ------------------------------------------------------------------
 * Part 3: 定义 Document.prototype 上的方法和属性
 * ------------------------------------------------------------------
 */
document.cookie = ''; // 初始化 cookie

// [关键] 伪装 document.all，使其 typeof 结果为 'undefined'
Object.defineProperty(Document.prototype, 'all', {
    configurable: true, enumerable: true,
    value: undetectable, writable: true,
});

// 伪装 document 的类型字符串
Object.defineProperty(Document.prototype, 'toString', {
    value: function() { return '[object HTMLDocument]'; },
});

// 模拟 createElement，使用计数器返回不同的 input 对象
let input_count = 0;
Document.prototype.createElement = function(tag) {
    console.log("document => createElement", tag);
    if (tag === 'div') return div1;
    if (tag === 'a') return a1;
    if (tag === 'form') return form1;
    if (tag === 'input') {
        input_count++;
        if (input_count === 1) return l_input;
        if (input_count === 2) return l2_input;
        return l3_input;
    }
    return {};
};

// 模拟 getElementsByTagName，第一次调用返回 script 列表，之后返回空
let script_first_call = true;
Document.prototype.getElementsByTagName = function(tag) {
    console.log("document => getElementsByTagName", tag);
    if (tag === 'script') {
        if (script_first_call) {
            script_first_call = false;
            return scripts;
        }
        return [];
    }
    if (tag === 'base') return { length: 0 };
    if (tag === 'meta') return [meta1];
    return [];
};

Document.prototype.getElementById = function(id) {
    console.log("document => getElementById", id);
    if (id === 'meta') return meta1;
    if (id === 'root-hammerhead-shadow-ui') return null; // 常见检测
    return null;
};

// 其他 document 属性和方法
Document.prototype.body = null;
Document.prototype.documentElement = {};
Document.prototype.visibilityState = 'visible';
Document.prototype.appendChild = function() {};
Document.prototype.removeChild = function() {};
Document.prototype.addEventListener = function() {};
Document.prototype.attachEvent = undefined; // IE 特有，通常为 undefined

/**
 * ------------------------------------------------------------------
 * Part 4: 定义 window 上的其他全局对象和属性
 * ------------------------------------------------------------------
 */

// [关键] 伪装 navigator.webdriver
function Navigator(){};
function webdriver_func() { return false; }
webdriver_func.toString = function() { return 'function webdriver() { [native code] }'; };
Object.defineProperty(Navigator.prototype, 'webdriver', {
    configurable: true, enumerable: true,
    get: webdriver_func
});
const navigator = new Navigator();
Object.assign(navigator, {
    appCodeName: "Mozilla", appName: "Netscape",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    cookieEnabled: true, deviceMemory: 8, language: "zh-CN", languages: ["zh-CN", "en", "zh"],
    onLine: true, platform: "Win32", product: "Gecko", productSub: '20030107',
    userAgent: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    vendor: "Google Inc.", vendorSub: ""
});

// location 对象
const location = {
    "href": "https://www.nmpa.gov.cn/datasearch/home-index.html",
    "origin": "https://www.nmpa.gov.cn", "protocol": "https:", "host": "www.nmpa.gov.cn",
    "hostname": "www.nmpa.gov.cn", "port": "", "pathname": "/datasearch/home-index.html",
    "search": "", "hash": ""
};

// 其他全局 API
window.document = document;
window.navigator = navigator;
window.clientInformation = navigator;
window.location = location;
window.top = window;
window.self = window;
window.screen = { availHeight: 1392, availWidth: 2560, height: 1440, width: 2560, colorDepth: 24, pixelDepth: 24 };
window.history = { length: 2 };
window.chrome = {};
window.ActiveXObject = undefined;
window.localStorage = { setItem:function(){}, getItem:function(){} };
window.sessionStorage = { setItem:function(){}, getItem:function(){} };
window.setTimeout = function() {};
window.setInterval = function() {};
window.addEventListener = function() {};
window.attachEvent = undefined;
window.MutationObserver = function() { return { observe: function() {} } };
window.XMLHttpRequest = function() {};

/**
 * ------------------------------------------------------------------
 * Part 5: 加载目标JS并执行
 * ------------------------------------------------------------------
 */

// 依次加载网站的JS文件
require("./ts");
require("./func");

// 定义获取cookie的函数并执行
function get_cookie(){
    return document.cookie;
}
