/**
 * @license text 2.0.16 Copyright jQuery Foundation and other contributors.
 * Released under MIT license, http://github.com/requirejs/text/LICENSE
 */
/*jslint regexp: true */
/*global require, XMLHttpRequest, ActiveXObject,
  define, window, process, Packages,
  java, location, Components, FileUtils */
define(["module"], function(e) {
    "use strict";
    var n, r, t, o, i, a = ["Msxml2.XMLHTTP", "Microsoft.XMLHTTP", "Msxml2.XMLHTTP.4.0"],
        s = /^\s*<\?xml(\s)+version=[\'\"](\d)*.(\d)*[\'\"](\s)*\?>/im,
        u = /<body[^>]*>\s*([\s\S]+)\s*<\/body>/im,
        c = "undefined" != typeof location && location.href,
        l = c && location.protocol && location.protocol.replace(/\:/, ""),
        f = c && location.hostname,
        p = c && (location.port || void 0),
        d = {},
        m = e.config && e.config() || {};

    function v(e, n) {
        return void 0 === e || "" === e ? n : e
    }
    return n = {
        version: "2.0.16",
        strip: function(e) {
            if (e) {
                var n = (e = e.replace(s, "")).match(u);
                n && (e = n[1])
            } else e = "";
            return e
        },
        jsEscape: function(e) {
            return e.replace(/(['\\])/g, "\\$1").replace(/[\f]/g, "\\f").replace(/[\b]/g, "\\b").replace(/[\n]/g, "\\n").replace(/[\t]/g, "\\t").replace(/[\r]/g, "\\r").replace(/[\u2028]/g, "\\u2028").replace(/[\u2029]/g, "\\u2029")
        },
        createXhr: m.createXhr || function() {
            var e, n, r;
            if ("undefined" != typeof XMLHttpRequest) return new XMLHttpRequest;
            if ("undefined" != typeof ActiveXObject)
                for (n = 0; n < 3; n += 1) {
                    r = a[n];
                    try {
                        e = new ActiveXObject(r)
                    } catch (e) {}
                    if (e) {
                        a = [r];
                        break
                    }
                }
            return e
        },
        parseName: function(e) {
            var n, r, t, o = !1,
                i = e.lastIndexOf("."),
                a = 0 === e.indexOf("./") || 0 === e.indexOf("../");
            return -1 !== i && (!a || i > 1) ? (n = e.substring(0, i), r = e.substring(i + 1)) : n = e, -1 !== (i = (t = r || n).indexOf("!")) && (o = "strip" === t.substring(i + 1), t = t.substring(0, i), r ? r = t : n = t), {
                moduleName: n,
                ext: r,
                strip: o
            }
        },
        xdRegExp: /^((\w+)\:)?\/\/([^\/\\]+)/,
        useXhr: function(e, r, t, o) {
            var i, a, s, u = n.xdRegExp.exec(e);
            return !u || (i = u[2], s = (a = (a = u[3]).split(":"))[1], a = a[0], (!i || i === r) && (!a || a.toLowerCase() === t.toLowerCase()) && (!s && !a || function(e, n, r, t) {
                if (n === t) return !0;
                if (e === r) {
                    if ("http" === e) return v(n, "80") === v(t, "80");
                    if ("https" === e) return v(n, "443") === v(t, "443")
                }
                return !1
            }(i, s, r, o)))
        },
        finishLoad: function(e, r, t, o) {
            t = r ? n.strip(t) : t, m.isBuild && (d[e] = t), o(t)
        },
        load: function(e, r, t, o) {
            if (o && o.isBuild && !o.inlineText) t();
            else {
                m.isBuild = o && o.isBuild;
                var i = n.parseName(e),
                    a = i.moduleName + (i.ext ? "." + i.ext : ""),
                    s = r.toUrl(a),
                    u = m.useXhr || n.useXhr;
                0 !== s.indexOf("empty:") ? !c || u(s, l, f, p) ? n.get(s, function(r) {
                    n.finishLoad(e, i.strip, r, t)
                }, function(e) {
                    t.error && t.error(e)
                }) : r([a], function(e) {
                    n.finishLoad(i.moduleName + "." + i.ext, i.strip, e, t)
                }, function(e) {
                    t.error && t.error(e)
                }) : t()
            }
        },
        write: function(e, r, t, o) {
            if (d.hasOwnProperty(r)) {
                var i = n.jsEscape(d[r]);
                t.asModule(e + "!" + r, "define(function () { return '" + i + "';});\n")
            }
        },
        writeFile: function(e, r, t, o, i) {
            var a = n.parseName(r),
                s = a.ext ? "." + a.ext : "",
                u = a.moduleName + s,
                c = t.toUrl(a.moduleName + s) + ".js";
            n.load(u, t, function(r) {
                var t = function(e) {
                    return o(c, e)
                };
                t.asModule = function(e, n) {
                    return o.asModule(e, c, n)
                }, n.write(e, u, t, i)
            }, i)
        }
    }, "node" === m.env || !m.env && "undefined" != typeof process && process.versions && process.versions.node && !process.versions["node-webkit"] && !process.versions["atom-shell"] ? (r = require.nodeRequire("fs"), n.get = function(e, n, t) {
        try {
            var o = r.readFileSync(e, "utf8");
            "\ufeff" === o[0] && (o = o.substring(1)), n(o)
        } catch (e) {
            t && t(e)
        }
    }) : "xhr" === m.env || !m.env && n.createXhr() ? n.get = function(e, r, t, o) {
        var i, a = n.createXhr();
        if (a.open("GET", e, !0), o)
            for (i in o) o.hasOwnProperty(i) && a.setRequestHeader(i.toLowerCase(), o[i]);
        m.onXhr && m.onXhr(a, e), a.onreadystatechange = function(n) {
            var o, i;
            4 === a.readyState && ((o = a.status || 0) > 399 && o < 600 ? ((i = new Error(e + " HTTP status: " + o)).xhr = a, t && t(i)) : r(a.responseText), m.onXhrComplete && m.onXhrComplete(a, e))
        }, a.send(null)
    } : "rhino" === m.env || !m.env && "undefined" != typeof Packages && "undefined" != typeof java ? n.get = function(e, n) {
        var r, t, o = new java.io.File(e),
            i = java.lang.System.getProperty("line.separator"),
            a = new java.io.BufferedReader(new java.io.InputStreamReader(new java.io.FileInputStream(o), "utf-8")),
            s = "";
        try {
            for (r = new java.lang.StringBuffer, (t = a.readLine()) && t.length() && 65279 === t.charAt(0) && (t = t.substring(1)), null !== t && r.append(t); null !== (t = a.readLine());) r.append(i), r.append(t);
            s = String(r.toString())
        } finally {
            a.close()
        }
        n(s)
    } : ("xpconnect" === m.env || !m.env && "undefined" != typeof Components && Components.classes && Components.interfaces) && (t = Components.classes, o = Components.interfaces, Components.utils.import("resource://gre/modules/FileUtils.jsm"), i = "@mozilla.org/windows-registry-key;1" in t, n.get = function(e, n) {
        var r, a, s, u = {};
        i && (e = e.replace(/\//g, "\\")), s = new FileUtils.File(e);
        try {
            (r = t["@mozilla.org/network/file-input-stream;1"].createInstance(o.nsIFileInputStream)).init(s, 1, 0, !1), (a = t["@mozilla.org/intl/converter-input-stream;1"].createInstance(o.nsIConverterInputStream)).init(r, "utf-8", r.available(), o.nsIConverterInputStream.DEFAULT_REPLACEMENT_CHARACTER), a.readString(r.available(), u), a.close(), r.close(), n(u.value)
        } catch (e) {
            throw new Error((s && s.path || "") + ": " + e)
        }
    }), n
});