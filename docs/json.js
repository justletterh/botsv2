/*
 * @license
 * RequireJS plugin for loading JSON files
 * - depends on Text plugin and it was HEAVILY "inspired" by it as well.
 * Author: Miller Medeiros
 * Version: 0.4.0 (2014/04/10)
 * Released under the MIT license
 */
define(["text"],function(text){var CACHE_BUST_QUERY_PARAM="bust",CACHE_BUST_FLAG="!bust",jsonParse="undefined"!=typeof JSON&&"function"==typeof JSON.parse?JSON.parse:function(val){return eval("("+val+")")},buildMap={};function cacheBust(n){return n=n.replace(CACHE_BUST_FLAG,""),(n+=n.indexOf("?")<0?"?":"&")+CACHE_BUST_QUERY_PARAM+"="+Math.round(2147483647*Math.random())}return{load:function(t,n,i,r){r.isBuild&&(!1===r.inlineJSON||-1!==t.indexOf(CACHE_BUST_QUERY_PARAM+"="))||0===n.toUrl(t).indexOf("empty:")?i(null):text.get(n.toUrl(t),function(n){var e;if(r.isBuild)buildMap[t]=n,i(n);else{try{e=jsonParse(n)}catch(n){i.error(n)}i(e)}},i.error,{accept:"application/json"})},normalize:function(n,e){return-1!==n.indexOf(CACHE_BUST_FLAG)&&(n=cacheBust(n)),e(n)},write:function(n,e,t){e in buildMap&&t('define("'+n+"!"+e+'", function(){ return '+buildMap[e]+";});\n")}}});