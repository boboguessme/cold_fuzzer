# -*- coding: utf-8 -*-

import utils

## js变量类型转换
#  @todo 考虑是否把declare、assign、invoke_function包装成一个statement类
#  @todo 支持赋值语句定义匿名函数
class TYPE(object):

	## JavaScript NULL显示形式
	NULL = 0
	## JavaScript 数字显示形式
	NUMBER = 1
	## JavaScript 字符串显示形式
	STRING = 2
	## JavaScript 变量显示形式
	VARIABLE = 3
	## JavaScript 函数显示形式
	FUNCTION = 4
	## 原始显示
	RAW = 5
	
	## 构造函数
	def __init__(self):
		pass
		
	## 将类型转换成显示形式
	#  @param value 显示值
	#  @param type 显示类型
	#  @return 对应值的显示形式
	#  @return 如果不支持的显示类型，返回'null'
	#  @remark 没有列表类型，补充的话应该可以直接str()转换
	@staticmethod
	def convert(value, type):
		if type == TYPE.NULL:
			return 'null'
		elif type == TYPE.NUMBER:
			return str(value)
		elif type == TYPE.STRING:
			return '"%s"' % value
		elif type == TYPE.VARIABLE:
			return value
		elif type == TYPE.RAW:
			return value
		else:
			return 'null'
			
## js代码生成		
#  @remark 分支和循环太高级，就不支持了 - -#	
#  @attention 为了简单起见，每一个元素的引用变量和id一致
#  @remark fuzz代码结构可以在最后生成出代码，之前代码序列存到单独变量
#  @remark 里方便调整。比如函数体就用list保存，每一个函数是个dict，内
#  @remark 部字段是name, args, statements，然后在最后生成函数代码；另
#  @remark 外还有全局代码序列等等
#  @remark 不过目前没有这种方式的需求
#  @todo 需要相关配置文件，适应多种浏览器、不同版本的变化
#  @todo 很多DOM方法并没有应用，比如所列在http://msdn.microsoft.com/en-us/library/ie/hh773165%28v=vs.85%29.aspx
#  @todo 所以cloneNode等类型漏洞没有办法跑出来
class JsGen(object):
	
	## @var ELEMENTS
	#  元素列表
	#  @remark 收集完整IE元素
	ELEMENTS = [
		"a",
		"abbr",
		"address",
		"area",
		"article",
		"aside",
		"audio",
		"b",
		"base",
		"bdo",
		"blockQuote",
		"body",
		"br",
		"button",
		"caption",
		"cite",
		"code",
		"col",
		"colGroup",
		"comment",
		"custom",
		"datalist",
		"dd",
		"del",
		"dfn",
		"div",
		"dl",
		"dt",
		"em",
		"embed",
		"fieldSet",
		"figcaption",
		"figure",
		"footer",
		"form",
		"head",
		"header",
		"hgroup",
		"h1",
		"hr",
		"html",
		#"HTML Comment",
		"i",
		"iframe",
		"img",
		"input",
		"ins",
		"kbd",
		"label",
		"legend",
		"li",
		"link",
		"map",
		"mark",
		"media",
		"menu",
		"meta",
		"nav",
		"noScript",
		"object",
		"ol",
		"optGroup",
		"option",
		"p",
		"param",
		"pre",
		"progress",
		"q",
		"rt",
		"ruby",
		"s",
		"samp",
		#"script",
		"section",
		"select",
		"small",
		"source",
		"span",
		"strong",
		"style",
		"sub",
		"sup",
		"table",
		"tBody",
		"td",
		"textArea",
		"tFoot",
		"th",
		"tHead",
		"title",
		"tr",
		"track",
		"u",
		"ul",
		"var",
		"video",
		"xml",
		### IE反对使用的元素开始
		"acronym",
		"wbr",
		"align",
		"aLink",
		"applet",
		"axis",
		"background",
		"baseFont",
		"bgColor",
		"bgSound",
		"big",
		"cellPadding",
		"cellSpacing",
		"center",
		"classid",
		"code",
		"codeBase",
		"codeType",
		"compact",
		"declare",
		"dir",
		"event",
		"face",
		"fgColor",
		"font",
		"frame",
		"frameBorder",
		"frameSet",
		"hspace",
		"HTMLFrameElement",
		"HTMLNextIdElement",
		"isIndex",
		"language",
		"link",
		"listing",
		"marginHeight",
		"marginWidth",
		"marquee",
		"nextID",
		"noBR",
		"noFrames",
		"noShade",
		"noWrap",
		#"plainText", 会把代码变成文本
		"rev",
		"rules",
		"scheme",
		"scope",
		"scrolling",
		"size",
		"standby",
		"start",
		"strike",
		"summary",
		"text",
		"tt",
		"type",
		"vAlign",
		"value",
		"valueType",
		"version",
		"vLink",
		"vrml",
		"vspace",
		"width",
		"xmp",
		### IE反对元素结束
	]
	
	## @var EVENTS
	#  事件列表
	#  @remark 收集完整IE事件
	EVENTS = [
		"compositionend",
		"compositionstart",
		"compositionupdate",
		"drag",
		"dragend",
		"dragenter",
		"dragleave",
		"dragover",
		"dragstart",
		"drop",
		"blur",
		"focus",
		"focusin",
		"focusout",
		"keydown",
		"keypress",
		"keyup",
		"message",
		"click",
		"dblclick",
		"mousedown",
		"mousemove",
		"mouseout",
		"mouseover",
		"mouseup",
		"mousewheel",
		"DOMSubtreeModified",
		"DOMNodeInserted",
		"DOMNodeRemoved",
		"DOMAttrModified",
		"DOMCharacterDataModified",
		"storage",
		"SVGZoom",
		"textInput",
		"abort",
		"error",
		"load",
		"select",
		"resize",
		### IE反对事件开始
		"afterupdate",
		"beforecopy",
		"beforecut",
		"beforeeditfocus",
		"beforepaste",
		"beforeupdate",
		"cellchange",
		"controlselect",
		"copy",
		"cut",
		"dataavailable",
		"datasetchanged",
		"datasetcomplete",
		"errorupdate",
		"filterchange",
		"help",
		"layoutcomplete",
		"losecapture",
		"mousewheel",
		"move",
		"moveend",
		"movestart",
		"propertychange",
		"resizeend",
		"resizestart",
		"rowenter",
		"rowexit",
		"rowsdelete",
		"rowsinserted",
		"selectionchange",
		"selectstart",
		"stop",
		"storagecommit",
		### IE反对事件结束
	]
	
	## @var COMMANDS
	#  命令列表
	#  @todo 补齐列表
	#  未使用
	COMMANDS = [
		'delete', 'insertButton', 
	]
	
	## @var PROPERTIES
	#  属性列表
	#  @remark 收集完整IE属性
	PROPERTIES = [
		"abbr",
		"accept",
		"acceptCharset",
		"accessKey",
		"action",
		"activeElement",
		"ActiveXObject",
		"alinkColor",
		"all",
		"allowfullscreen",
		"allowTransparency",
		"alt",
		"altHtml",
		"anchorNode",
		"anchorOffset",
		"anchors",
		"applets",
		"applicationName",
		"archive",
		"async",
		"ATOMICSELECTION",
		"attributes",
		"autocomplete",
		"autofocus",
		"background",
		"balance",
		"BaseHref",
		"BGCOLOR",
		"bgProperties",
		"body",
		"border",
		"borderColor",
		"borderColorDark",
		"borderColorLight",
		"bottom",
		"bottomMargin",
		"boundElements",
		"browserLanguage",
		"canHaveChildren",
		"canHaveHTML",
		"caption",
		"cellIndex",
		"cells",
		"ch",
		"characterSet",
		"charset",
		"checked",
		"children",
		"chOff",
		"cite",
		"class",
		"classList",
		"className",
		"clear",
		"clientHeight",
		"clientLeft",
		"clientTop",
		"clientWidth",
		"color",
		"cols",
		"colSpan",
		"compatible",
		"compatMode",
		"complete",
		"content",
		"contentDocument",
		"contentEditable",
		"contentWindow",
		"controlRange",
		"cookie",
		"coords",
		"Count",
		"customError",
		"data",
		"dataFld",
		"dataFormatAs",
		"dataPageSize",
		"dataSrc",
		"dateTime",
		"defaultCharset",
		"defaultChecked",
		"defaultSelected",
		"defaultValue",
		"defaultView",
		"defer",
		"designMode",
		"dir",
		"disabled",
		"doctype",
		"documentElement",
		"documentMode",
		"domain",
		"draggable",
		"dropEffect",
		"effectAllowed",
		"elements",
		"embeds",
		"encoding",
		"enctype",
		"fgColor",
		"FieldDelim",
		"fileCreatedDate",
		"fileModifiedDate",
		"files",
		"fileSize",
		"fileUpdatedDate",
		"focusNode",
		"focusOffset",
		"form",
		"formAction",
		"formEnctype",
		"formMethod",
		"formNoValidate",
		"forms",
		"formTarget",
		"frameElement",
		"frames",
		"frameSpacing",
		"head",
		"headers",
		"height",
		"hidden",
		"hideFocus",
		"href",
		"hreflang",
		"htmlFor",
		"httpEquiv",
		"id",
		"images",
		"implementation",
		"indeterminate",
		"index",
		"isCollapsed",
		"isContentEditable",
		"isDisabled",
		"isMap",
		"isMultiLine",
		"isOpen",
		"label",
		"lazyload",
		"lang",
		"lastModified",
		"leftMargin",
		"length",
		"linkColor",
		"links",
		"list",
		"longDesc",
		"loop",
		"lowsrc",
		"max",
		"maxConnectionsPerServer",
		"maxLength",
		"method",
		"Methods",
		"min",
		# "x-ms-AcceleratorKey",  js语法错误 需要改用setAttribute
		"msCapsLockWarningOff",
		"multiple",
		"naturalHeight",
		"naturalWidth",
		"noHref",
		"noResize",
		"noValidate",
		"object",
		"offscreenBuffering",
		"offsetHeight",
		"offsetLeft",
		"offsetParent",
		"offsetTop",
		"offsetWidth",
		"onLine",
		"options",
		"palette",
		"parentWindow",
		"pathname",
		"pattern",
		"patternMismatch",
		"placeholder",
		"pluginspage",
		"position",
		"rangeCount",
		"rangeOverflow",
		"rangeUnderflow",
		"readOnly",
		"readyState",
		"referrer",
		"rel",
		"required",
		"rightMargin",
		"role",
		"rowIndex",
		"rows",
		"rowSpan",
		"sandbox",
		"screenLeft",
		"screenTop",
		"scripts",
		"scroll",
		"scrollHeight",
		"scrollLeft",
		"scrollTop",
		"scrollWidth",
		"sectionRowIndex",
		"SECURITY",
		"selected",
		"selectedIndex",
		"selectionEnd",
		"selectionStart",
		"self",
		"shape",
		"size",
		"sourceIndex",
		"span",
		"specified",
		"spellcheck",
		"src",
		"start",
		"status",
		"step",
		"stepMismatch",
		"style",
		"tabIndex",
		"tabStop",
		"tagName",
		"tagUrn",
		"target",
		"tBodies",
		"text",
		"tFoot",
		"tHead",
		"title",
		"tooLong",
		"top",
		"topMargin",
		"type",
		"typeMismatch",
		"uniqueID",
		"uniqueNumber",
		"units",
		"URLUnencoded",
		"urn",
		"useMap",
		"userAgent",
		"valid",
		"validationMessage",
		"validity",
		"vAlign",
		"value",
		"valueAsNumber",
		"valueMissing",
		"vcard_name",
		"version",
		"viewLink",
		"viewMasterTab",
		"vlinkColor",
		"volume",
		"width",
		"willValidate",
		"wrap",
		#"x-ms-format-detection",  js语法错误 需要改用setAttribute
	]
	
	## @var BLACK_PROPERTIES
	#  清空元素内容的属性列表
	#  @todo 补齐列表
	BLACK_PROPERTIES = [
		'nodeName',
		'nodeValue',
		'nodeType',
		'childNodes',
		'location',
		'name',
		'opener',
		'URL',
		'onbeforeunload',
		'onunload',
		'innerHTML',
		'outerHTML',
		'innerText',
		"outerText",
		'textContent',
		'Components',
		'controllers',
		'lastChild',
		'previousSibling',
		'previousElementSibling',
		'parentNode',
		'parentTextEdit',
		'parentElement',
		'ownerDocument',
		'document' ,
		'cloneNode',
		'open',
		'close',
		'print',	
	]
	
	## @var STYLES
	#  样式属性
	#  @remark 这是一个字典
	#  @remark key默认是style标签或者属性可直接使用的，在js语句中需要做转换	
	STYLES = {
		"align-content": ["stretch", "center", "flex-start", "flex-end", "space-between", "space-around", "initial", "inherit"],
		"align-items": ["stretch", "center", "flex-start", "flex-end", "baseline", "initial", "inherit"],
		"align-self": ["auto", "stretch", "center", "flex-start", "flex-end", "baseline", "initial", "inherit"],
		"animation-delay": ["1s", "1073741823s", "initial", "inherit"],
		"animation-direction": ["normal", "reverse", "alternate", "alternate-reverse", "initial", "inherit"],
		"animation-duration": ["1s", "1073741823s", "initial", "inherit"],
		"animation-fill-mode": ["none", "forwards", "backwards", "both", "initial", "inherit"],
		"animation-iteration-count": ["1", "1073741823", "infinite", "initial", "inherit"],
		"animation-name": ["Oops", "none", "initial", "inherit"], # 不清楚怎么构造
		"animation-play-state": ["none", "initial", "inherit"],
		"animation-timing-function": ["linear", "ease", "ease-in", "ease-out", "cubic-bezier(0.25, 0.1, 0.25, 1)", "initial", "inherit"],
		"backface-visibility": ["visible", "hidden", "initial", "inherit"],
		"background-attachment": ["scroll", "fixed", "local", "initial", "inherit"],
		"background-clip": ["border-box", "padding-box", "content-box", "initial", "inherit"],
		"background-color": ["#ffc00c", "transparent", "initial", "inherit"],
		"background-image": ["url('cold_fuzz.jpg')", "none", "initial", "inherit"],
		"background-origin": ["padding-box", "border-box", "content-box", "initial", "inherit"],
		"background-position": ["left top", "right center", "center bottom", "2% 3%", "2px 3px", "initial", "inherit"],
		"background-repeat": ["repeat", "repeat-x", "repeat-y", "no-repeat", "initial", "inherit"],
		"background-size": ["auto", "12", "1073741823", "cover", "contain", "intial", "inherit"],
		"border-bottom-color": ["blue", "transparent", "initial", "inherit"],
		"border-bottom-left-radius": ["25px," "12%", "initial", "inherit"],
		"border-bottom-right-radius": ["25px," "12%", "initial", "inherit"],
		"border-bottom-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"border-bottom-width": ["medium", "thin", "thick", "10px", "initial", "inherit"],
		"border-collapse": ["separate", "collapse", "initial", "inherit"],
		"border-color": ["blue", "transparent", "initial", "inherit"],
		"border-image-outset": ["4", "1073741823", "initial", "inherit"],
		"border-image-repeat": ["stretch", "repeat", "round", "initial", "inherit"],
		"border-image-slice": ["50%", "fill", "initial", "inherit"],
		"border-image-source": ["none", "url('cold_fuzz.jpg')", "initial", "inherit"],
		"border-image-width": ["20px 30px", "20% 30%", "auto", "initial", "inherit"],
		"border-left-color": ["blue", "transparent", "initial", "inherit"],
		"border-left-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"border-left-width": ["medium", "thin", "thick", "0px", "initial", "inherit"],
		"border-right-color": ["blue", "transparent", "initial", "inherit"],
		"border-right-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"border-right-width": ["medium", "thin", "thick", "0px", "initial", "inherit"],
		"border-spacing": ["15px 10px", "initial", "inherit"],
		"border-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"border-top-color": ["blue", "transparent", "initial", "inherit"],
		"border-top-left-radius": ["25px," "12%", "initial", "inherit"],
		"border-top-right-radius": ["25px," "12%", "initial", "inherit"],
		"border-top-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"border-top-width": ["medium", "thin", "thick", "10px", "initial", "inherit"],
		"bottom": ["auto", "10px", "initial", "inherit"],
		"box-shadow": ["none", "10px 20px 30px blue", "inset", "initial", "inherit"],
		"box-sizing": ["content-box", "border-box", "initial", "inherit"],
		"break-after": ["auto", "always", "avoid", "left", "right", "page", "column", "avoid-page", "avoid-column"], # IE独有
		"break-before": ["auto", "always", "avoid", "left", "right", "page", "column", "avoid-page", "avoid-column"], # IE独有
		"break-inside": ["auto", "avoid", "avoid-page", "avoid-column"], # IE独有
		"caption-side": ["top", "bottom", "initial", "inherit"],
		"clear": ["none", "left", "right", "both", "initial", "inherit"],
		"clip": ["auto", "rect(0px, 50px, 50px, 0px)", "initial", "inherit"],
		"clip-path": ["none", "Oops"], # IE独有 不知道怎么构造
		"clip-rule": ["nonzero", "evenodd", "inherit"], # IE独有
		"color": ["blue", "#fc0fff"],
		"column-count": ["3", "1073741823", "auto", "initial", "inherit"], # 这个3是数字类型，这里暂时用字符串
		"column-fill": ["balance", "auto", "initial", "inherit"],
		"column-gap": ["50px", "normal", "initial", "inherit"],
		"column-rule-color": ["blue", "initial", "inherit"],
		"column-rule-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"column-rule-width": ["medium", "thin", "thick", "10px", "initial", "inherit"],
		"column-span": ["3", "1073741823", "all", "initial", "inherit"],
		"column-width": ["auto", "100px", "initial", "inherit"],
		# "content": normal, 据说不能用js直接赋值 http://www.w3schools.com/cssref/pr_gen_content.asp
		"counter-increment": ["none", "3", "1073741823", "initial", "inherit"],
		"counter-reset": ["none", "3", "1073741823", "initial", "inherit"],
		"cursor": ["alias", "all-scroll", "auto", "cell", "context-menu", "col-resize", "copy", "crosshair", "default", "e-resize", "ew-resize", "help", "move", "n-resize", "ne-resize", "nesw-resize", "ns-resize", "nw-resize", "nwse-resize", "no-drop", "none", "not-allowed", "pointer", "progress", "row-resize", "s-resize", "se-resize", "sw-resize", "text", "url('cold_fuzz.jpg')", "vertical-text", "w-resize", "wait", "zoom-in", "zoom-out", "initial", "inherit"],
		"direction": ["ltr", "rtl", "initial", "inherit"],
		"display": ["inline", "block", "flex", "inline-block", "inline-flex", "inline-table", "list-item", "run-in", "table", "table-caption", "table-column-group", "table-header-group", "table-footer-group", "table-row-group", "table-cell", "table-column", "table-row", "none", "initial", "inherit"],
		"dominant-baseline": ["auto", "use-script", "no-change", "reset-size", "ideographic", "alphabetic", "hanging", "mathematical", "central", "middle", "text-after-edge", "text-before-edge", "inherit"], # IE独有
		"empty-cells": ["show", "hide", "initial", "inherit"],
		"enable-background": ["accumulate", "inherit", "new 20 30 100 200"], # IE独有 这个new瞎写的
		"fill": ["none", "currentColor", "funciri", "inherit"], # IE独有
		"fill-opacity": ["0.5", "0.3999999999", "inherit"], # IE独有
		"fill-rule": ["nonzero", "evenodd", "inherit"], # IE独有
		#"filter": ["none"], # IE独有 貌似挺复杂，先不用
		"flex-basis": ["10px", "20%", "auto", "initial", "inherit"],
		"flex-direction": ["row", "row-reverse", "column", "column-reverse", "initial", "inherit"],
		"flex-grow": ["5", "1073741823", "initial", "inherit"],
		"flex-shrink": ["5", "1073741823", "initial", "inherit"],
		"flex-wrap": ["nowrap", "wrap", "wrap-reverse", "initial", "inherit"],
		"float": ["none", "left", "right", "initial", "inherit"],
		"flood-color": ["blue", "currentColor", "inherit"], # IE独有
		"flood-opacity": ["0.5", "0.3999999999", "inherit"], # IE独有
		"font-family": ["arial", "Verdana,sans-serif", "initial", "inherit"],
		"font-feature-settings": ["normal", "kern, dlig", "tnum, ss01", "kern", "smcp", "liga", "dlig", "ss01", "ss10", "ss20", "swsh", "tnum", "lnum", "onum"], # IE独有
		"font-size": ["medium", "xx-small", "x-small", "small", "large", "x-large", "xx-large", "smaller", "larger", "14px", "initial", "inherit"],
		"font-size-adjust": ["0.58", "none", "initial", "inherit"],
		"font-stretch": ["wider", "narrower", "ultra-condensed", "extra-condensed", "condensed", "semi-condensed", "normal", "semi-expanded", "expanded", "extra-expanded", "ultra-expanded", "initial", "inherit"],
		"font-style": ["normal", "italic", "oblique", "initial", "inherit"],
		"font-variant": ["normal", "small-caps", "initial", "inherit"],
		"font-weight": ["normal", "bold", "bolder", "lighter", "888", "1073741823", "initial", "inherit"],
		"glyph-orientation-horizontal": ["80deg", "inherit"], # IE独有
		"glyph-orientation-vertical": ["auto", "80deg", "inherit"], # IE独有
		"height": ["auto", "500px", "initial", "inherit"],
		"ime-mode": ["auto", "active", "inactive", "disabled"], # IE独有
		"justify-content": ["flex-start", "flex-end", "center", "space-between", "space-around", "initial", "inherit"],
		"kerning": ["auto", "inherit", "3", "1073741823"], # IE独有
		"layout-flow": ["horizontal", "vertical-ideographic"], # IE独有
		"layout-grid-char": ["none", "auto", "20px", "33%"], # IE独有
		"layout-grid-line": ["none", "auto", "20px", "33%"], # IE独有
		"layout-grid-mode": ["both", "none", "line", "char"], # IE独有
		"layout-grid-type": ["loose", "strict", "fixed"], # IE独有
		"left": ["auto", "100px", "initial", "inherit"],
		"letter-spacing": ["normal", "3px", "initial", "inherit"],
		"lighting-color": ["blue", "rgb(30,22,40)", "currentColor", "inherit"], # IE独有
		"line-break": ["normal", "strict"], # IE独有
		"line-height": ["normal", "30px", "6", "1073741823", "length", "initial", "inherit"],
		"list-style-image": ["none", "url('cold_fuzz.jpg')", "initial", "inherit"],
		"list-style-position": ["inside", "outside", "initial", "inherit"],
		"list-style-type": ["disc", "armenian", "circle", "cjk-ideographic", "decimal", "decimal-leading-zero", "georgian", "hebrew", "hiragana", "hiragana-iroha", "katakana", "katakana-iroha", "lower-alpha", "lower-greek", "lower-latin", "lower-roman", "none", "square", "upper-alpha", "upper-latin", "upper-roman", "initial", "inherit"],
		"margin-bottom": ["100px", "auto", "initial", "inherit"],
		"margin-left": ["100px", "auto", "initial", "inherit"],
		"margin-right": ["100px", "auto", "initial", "inherit"],
		"margin-top": ["100px", "auto", "initial", "inherit"],
		"marker": ["none", "url('cold_fuzz.jpg')", "inherit"], # IE独有
		"marker-end": ["none", "url('cold_fuzz.jpg')", "inherit"], # IE独有
		"marker-mid": ["none", "url('cold_fuzz.jpg')", "inherit"], # IE独有
		"marker-start": ["none", "url('cold_fuzz.jpg')", "inherit"], # IE独有
		"mask": ["none", "url('cold_fuzz.jpg')", "inherit"], # IE独有
		"max-height": ["100px", "none", "initial", "inherit"],
		"max-width": ["100px", "none", "initial", "inherit"],
		"min-height": ["20px", "initial", "inherit"],
		"min-width": ["20px", "auto", "initial", "inherit"],
		"opacity": ["0.5", "initial", "inherit"],
		"order": ["2", "1073741823", "initial", "inherit"],
		"orphans": ["2", "1073741823"], # IE独有
		"outline-color": ["transparent", "invert", "#FF00CC", "initial", "inherit"],
		"outline-style": ["none", "hidden", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset", "initial", "inherit"],
		"outline-width": ["medium", "thin", "thick", "2px", "initial", "inherit"],
		"overflow": ["visible", "hidden", "scroll", "auto", "initial", "inherit"],
		"overflow-x": ["visible", "hidden", "scroll", "auto", "initial", "inherit"],
		"overflow-y": ["visible", "hidden", "scroll", "auto", "initial", "inherit"],
		"padding-bottom": ["50px", "50%", "50cm", "50pt", "initial", "inherit"],
		"padding-left": ["50px", "50%", "50cm", "50pt", "initial", "inherit"],
		"padding-right": ["50px", "50%", "50cm", "50pt", "initial", "inherit"],
		"padding-top": ["50px", "50%", "50cm", "50pt", "initial", "inherit"],
		"page-break-after": ["auto", "always", "avoid", "left", "right", "initial", "inherit"],
		"page-break-before": ["auto", "always", "avoid", "left", "right", "initial", "inherit"],
		"page-break-inside": ["auto", "avoid", "initial", "inherit"],
		"perspective": ["50px", "none"],
		"perspective-origin": ["10px 5px", "10px 50%", "top 25%", "left center", "35px bottom", "initial", "inherit"],
		"pointer-events": ["visiblePainted", "visibleFill", "visibleStroke", "visible", "painted", "fill", "stroke", "all", "none", "inherit"], # IE独有
		"position": ["static", "absolute", "fixed", "relative", "initial", "inherit"],
		"quotes": ["none", "<<' '>>", "initial", "inherit"],
		"right": ["auto", "200px", "initial", "inherit"],
		"ruby-align": ["auto", "left", "center", "right", "distribute-letter", "distribute-space", "line-edge"], # IE独有
		"ruby-overhang": ["auto", "whitespace", "none"], # IE独有
		"ruby-position": ["above", "inline"], # IE独有
		"scrollbar-3dlight-color": ["#000000", "#e3e3e3"], # IE独有
		"scrollbar-arrow-color": ["#000000", "#f2c083"], # IE独有
		"scrollbar-base-color": ["#000000", "#f2c083"], # IE独有
		"scrollbar-darkshadow-color": ["#000000", "#696969"], # IE独有
		"scrollbar-face-color": ["#000000", "#f0f0f0"], # IE独有
		"scrollbar-highlight-color": ["#000000", "#ffffff"], # IE独有
		"scrollbar-shadow-color": ["#000000", "#a0a0a0"], # IE独有
		"scrollbar-track-color": ["#000000", "#0a0a0a"], # IE独有
		"stop-color": ["currentColor", "inherit"], # IE独有
		"stop-opacity": ["0.33", "inherit"], # IE独有
		"stroke": ["none", "currentColor", "inherit", "#000000", "#ffc00c", "url('cold_fuzz.jpg')"], # IE独有
		"stroke-dasharray": ["none", "inherit", "2,30%,1.5,120%"], # IE独有
		"stroke-dashoffset": ["20px", "20%", "inherit", "120%"], # IE独有
		"stroke-linecap": ["butt", "round", "bevel"], # IE独有
		"stroke-linejoin": ["miter", "round", "bevel", "inherit"], # IE独有
		"stroke-miterlimit": ["4", "inherit", "20", "1073741823"], # IE独有
		"stroke-opacity": ["0.3", "inherit"], # IE独有
		"stroke-width": ["0.01px", "30cm", "20%", "inherit"], # IE独有
		"table-layout": ["auto", "fixed", "initial", "inherit"],
		"text-align": ["left", "right", "center", "justify", "initial", "inherit"],
		"text-align-last": ["auto", "left", "right", "center", "justify", "start", "end", "initial", "inherit"],
		"text-anchor": ["start", "middle", "end", "inherit"], # IE独有
		"text-autospace": ["none", "ideograph-alpha", "ideograph-numeric", "ideograph-parenthesis", "ideograph-space"], # IE独有
		"text-decoration": ["none", "underline", "overline", "line-through", "initial", "inherit"],
		"text-indent": ["50px", "initial", "inherit"],
		"text-justify": ["auto", "inter-word", "inter-ideograph", "inter-cluster", "distribute", "kashida", "trim", "initial", "inherit"],
		#"text-justify-trim": ["auto"], # IE独有 msdn没查到
		#"text-kashida": ["0%"], # IE独有 msdn没查到
		"text-kashida-space": ["20%", "200%"], # IE独有
		"text-overflow": ["clip", "ellipsis", "string", "initial", "inherit"],
		"text-shadow": ["2px 5px 5px red", "none", "initial", "inherit"],
		"text-transform": ["none", "capitalize", "uppercase", "lowercase", "initial", "inherit"],
		"text-underline-position": ["above", "below", "auto", "auto-pos"], # IE独有
		"top": ["auto", "length", "initial", "inherit"],
		"touch-action": ["auto", "none", "pan-x", "pan-y", "pinch-zoom", "manipulation", "double-tap-zoom", "cross-slide-x", "cross-slide-y"], # IE独有
		"transform": ["matrix(0.866,0.5,-0.5,0.866,0,0)", "matrix3d(0.866,0.5,-0.5,0.866,0,0,0,0,0,0,0,0,0,0,0,0)", "translate(20px,10px)", "translate3d(20px,10px, 5px)", "translateX(-25px)", "translateY(-25px)", "translateZ(-25px)", "scale(0.5,2)", "scale3d(0.5,2,1)", "scaleX(3)", "scaleY(3)", "scaleZ(3)", "rotate(170deg)", "rotate3d(0.4, 0.2, 0.5, 20deg)", "rotateX(120deg)", "rotateY(40deg)", "rotateZ(90deg)", "skew(50deg,50deg)", "skewX(80deg)", "skewY(80deg)", "perspective(2)", "none", "initial", "inherit"], #WARNING: 3d结尾函数参数都是瞎写的
		"transform-origin": ["3px 8px", "3px 8px 2px", "left 50%", "2px bottom 1px", "initial", "inherit"],
		"transform-style": ["flat", "preserve-3d", "initial", "inherit"],
		"transition-delay": ["2ms", "1s", "1073741823s", "initial", "inherit"],
		"transition-duration": ["2ms", "1s", "1073741823s", "initial", "inherit"],
		"transition-property": ["one", "all", "width,height", "initial", "inherit"],
		"transition-timing-function": ["ease", "linear", "ease-in", "ease-out", "ease-in-out", "cubic-bezier(0.25, 0.1, 0.25, 1)", "initial", "inherit"],
		"unicode-bidi": ["normal", "embed", "bidi-override", "intitial", "inherit"],
		"vertical-align": ["baseline", "10px", "10%", "sub", "super", "top", "text-top", "middle", "bottom", "text-bottom", "initial", "inherit"],
		"visibility": ["visible", "hidden", "collapse", "initial", "inherit"],
		"white-space": ["normal", "nowrap", "pre", "pre-line", "pre-wrap", "initial", "inherit"],
		"widows": ["2", "200", "1073741823"], # IE独有
		"width": ["auto", "300px", "20%", "initial", "inherit"],
		"word-break": ["normal", "break-all", "keep-all", "initial", "inherit"],
		"word-spacing": ["normal", "20px", "initial", "inherit"],
		"word-wrap":  ["normal", "break-word", "initial", "inherit"],
		"writing-mode": ["lr-tb", "rl-tb", "tb-rl", "bt-rl", "tb-lr", "bt-lr", "lr-bt", "rl-bt", "lr", "rl", "tb"], # IE独有
		"z-index": ["auto", "-1", "1073741823", "initial", "inherit"],
		"zoom": ["normal", "0.4", "20%", "2.6", "250%"], # IE独有
	}
	
	## @var INTERESTING_VALUES
	#  特殊值列表
	INTERESTING_VALUES = [
		TYPE.convert(0, TYPE.NUMBER),
		TYPE.convert('null', TYPE.NULL),
	]
	
	## @var MAX_OPERATIONS
	#  fuzz最大操作上限
	MAX_OPERATIONS = 20
	
	## @var MAX_ELEMENTS
	#  添加元素数量随机mod
	#  @todo 未使用
	MAX_ELEMENTS = 20
	
	## @var MAX_PROPERTY
	#  添加属性数量随机mod
	#  @todo 未使用	
	MAX_PROPERTY = 9
	
	## @var MAX_LISTENERS
	#  添加事件数量随机mod
	#  @todo 未使用	
	MAX_LISTENERS = 5
	
	## @var ids
	#  页面元素id列表	
	## @var rand
	#  随机数据对象
	
	## 构造函数
	#  @param ids 页面元素id列表
	def __init__(self, ids):
		self.ids = ids
		self.rand = utils.Rand()
		self.global_vars = self.init_vars()
		
	## 初始化分配html元素变量引用
	#  @return 声明已存在元素的js代码序列
	#  @remark 这一会因为invoke_function自动添加';'导致每条语句多出一个';'
	def init_vars(self):
		js_content = []
		for id in self.ids:
			js_content.append(self.declare(
						id,
						self.invoke_function(
							'document', 'getElementById', [[id,TYPE.STRING]]),
						TYPE.RAW))
		return js_content
		
	## fuzz策略生成
	#  @return fuzz操作js代码
	#  @remark 起点函数是cold_start
	def fuzz(self):	
		js_content = []
		cold_start = self.create_function(
				'cold_start', [], self.random_js_contents())
		js_content.append(cold_start)
		timer_code = self.set_timer()
		js_content.append(timer_code)
		return '\n\n'.join(self.global_vars + js_content);
	
	## 创建setTimeout
	#  @return 相应js代码
	#  @attention 包含相关函数定义
	def set_timer(self):
		js_content = self.random_js_contents(True)
		# 自刷新进行fuzz
		js_content.append('window.location.reload();')
		callback_func = self.create_function(
				'timer_handler', [], js_content)
		return self.invoke_function('window', 'setTimeout', 
				[[callback_func,TYPE.RAW], [100,TYPE.NUMBER]])
				
	## 创建随机js代码序列
	#  @param is_timer True在setTimeout内调用
	#  @param is_event True在event响应函数内调用
	#  @return js代码序列
	def random_js_contents(self, is_timer=False, is_event=False):
		# 不能同时存在既在timer内又在event内
		assert(not is_timer or not is_event)
		js_content = []
		operation_counts = self.rand.rint(self.MAX_OPERATIONS)
		for current_operation_count in xrange(operation_counts):
			js_content.append(self.random_operate(is_timer, is_event))
		return js_content
		
	## 创建事件响应js代码序列
	#  @return js代码序列
	def random_event_contents(self):
		return self.random_js_contents(False, True)
	
	## 随机操作
	#  @param is_timer True在setTimeout内调用
	#  @param is_event True在event响应函数内调用
	#  @return 随机操作的js代码
	def random_operate(self, is_timer=False, is_event=False):
		type_mod = 4
		type = self.rand.rint(type_mod)
		# 事件操作
		if type == 0:
			if is_event:
				# 极端条件下貌似会死循环
				return self.random_operate(is_timer, is_event)
			return self.random_event_operate(is_timer)
		# 样式操作
		elif type == 1:
			return self.random_style_operate()
		# 元素操作
		elif type == 2:
			return self.random_element_operate(is_timer)
		# 全局操作
		else:
			return self.random_global_operate()
		
	## 生成触发事件的js代码
	#  @param target 事件发生宿主
	#  @param event_type 事件类型
	#  @return js代码
	def fire_event(self, target, event_type):
		""" 非IE以外的浏览器支持
		return self.invoke_function(
					target, 
					'dispatchEvent',
					[['new Event("%s")' % event_type, TYPE.RAW]])
		"""		
		js_content = []
		# @attention 事件名统一是e
		evt_var_name = 'e'
		js_content.append(self.declare(
				evt_var_name, 
				self.invoke_function(
					'document', 
					'createEvent', 
					[['Event', TYPE.STRING]]),
				TYPE.RAW))
		js_content.append(self.invoke_function(
				evt_var_name,
				'initEvent',
				[[event_type, TYPE.STRING], 
				 [self.rand.rbool(), TYPE.VARIABLE],
				 [self.rand.rbool(), TYPE.VARIABLE]
				]))
		js_content.append(self.invoke_function(
				target,
				'dispatchEvent',
				[[evt_var_name, TYPE.VARIABLE]]))
		return self.generate_js_code(js_content, False)
				
			
	## 随机事件操作
	#  @param is_timer True在setTimeout内调用
	#  @return 相应js代码
	#  @todo 对事件的初始化进行处理，如果处理，需要修改self.EVENTS结构，对每一类事件类型有不同的初始化方式
	#  @attention 包含相关函数定义
	#  @attention IE6-IE9 需要使用attachEvent而不是addEventListener
	#  @attention 现在事件对象是默认初始化
	#  @remark 参考https://developer.mozilla.org/en-US/docs/Web/Reference/Events?redirectlocale=en-US&redirectslug=DOM%2FMozilla_event_reference
	def random_event_operate(self, is_timer=False):
		target = self.random_item(self.ids)
		event = self.random_item(self.EVENTS)
		if is_timer:
			return self.fire_event(target, event)
		else:
			return self.invoke_function(target, 'addEventListener', 
					[[event, TYPE.STRING],
					[self.create_function(target, ['evt'], 
						self.random_event_contents()), TYPE.RAW],
					[self.rand.rbool(), TYPE.VARIABLE]
					])
		
	## 随机样式操作
	#  @return 相应js代码
	def random_style_operate(self):
		target = self.random_item(self.ids)
		style = self.random_item(self.STYLES.keys())
		# 转换style名称  例如letter-scaping转成letterScaping
		style_name = ''.join(map(lambda x: x.capitalize(), style.split('-')))
		style_name = '%s%s' % (style_name[0].lower(), style_name[1:])
		style_value = self.random_item(self.STYLES[style])
		return self.assign('.'.join((target, 'style', style_name)), 
					style_value, TYPE.STRING)
		
	## 随机元素操作
	#  @param enable_clean_property 允许清空元素的操作
	#  @return 相应js代码
	def random_element_operate(self, enable_clean_property=False):
		type_mod = 6
		type = self.rand.rint(type_mod)
		# 增加元素，并随机添加到tree中
		if type == 0:
			js_content = []
			js_content.append(self.setup_element(self.random_item(self.ELEMENTS)))
			# 添加的元素id应该是ids的最后一个元素
			element_id = self.ids[-1]
			js_content.append(self.invoke_function(
					self.random_item(self.ids),
					'appendChild',
					[[element_id,TYPE.VARIABLE]]))
			return ''.join(js_content)		
		# 删除元素
		elif type == 1:
			# @todo removeNode貌似只有IE支持，以后考虑考虑
			# 现在只用了removeChild
			current_element = self.random_item(self.ids)
			return self.invoke_function(
					'.'.join((current_element, 'parentNode')),
					'removeChild', [[current_element,TYPE.VARIABLE]])
		# 清空元素内容
		elif type == 2:
			if not enable_clean_property:
				# 极端条件下貌似会死循环，可以买彩票了吧？
				return self.random_element_operate(enable_clean_property)
			return self.assign(
					'.'.join((self.random_item(self.ids), self.random_item(self.BLACK_PROPERTIES))),
					'null', TYPE.NULL)		
		# 元素相互引用
		# 随机选取元素添加到另一随意元素
		elif type == 3:
			child_element = self.random_item(self.ids)
			parent_element = self.random_item(self.ids)
			return self.invoke_function(
					parent_element, 'appendChild', [[child_element,TYPE.VARIABLE]])
		#  赋值元素属性
		elif type == 4:
			current_element = self.random_item(self.ids)
			return self.assign(
					'.'.join((current_element, self.random_item(self.PROPERTIES))), 
					self.random_item(self.INTERESTING_VALUES), TYPE.RAW)
		# 引用属性
		else:
			return self.ref('.'.join((self.random_item(self.ids), 
						self.random_item(self.PROPERTIES))))
		
	## 随机全局操作
	#  @return 相应js代码
	#  @todo 不知道都有啥操作，IE可能有createTextRange等函数
	def random_global_operate(self):
		return 'CollectGarbage();'
		
	## 创建元素，赋值变量并且设置元素id为对应变量名
	#  @param element_tag 元素tag名称
	#  @param id_len id长度，默认10
	#  @return 相应js代码
	#  @todo  这种方式fuzz不出来same id那种漏洞
	def setup_element(self, element_tag, id_len=10):
		element_id = self.rand.rstr(id_len)
		self.ids.append(element_id)
		self.global_vars.append('var %s;' % element_id)
		return '%s = %s;%s' % (element_id, 
				self.create_element(element_tag),
				self.set_element_id(element_id))
		
	## 随机创建元素
	#  @return 相应js代码
	def random_create_element(self):
		return self.create_element(self.random_item(self.ELEMENTS))
		
	## 创建元素
	#  @param element_tag 元素tag名称
	#  @return 相应js代码
	def create_element(self, element_tag):
		return 'document.createElement("%s")' % element_tag

	## 随机挑选元素添加随机子元素
	#  @return 相应js代码
	def random_append_element(self):
		return self.append_element(self.random_item(self.ids),
				self.random_item(self.ids))
	
	## 添加子元素
	#  @param parent 父元素变量名
	#  @param child 子元素变量名
	#  @return 相应js代码
	def append_element(self, parent, child):
		return '%s.appendChild(%s);' % (parent, child)
	
	## 设置元素id
	#  @param element_id 元素变量名也是对应id
	#  @return 相应js代码
	def set_element_id(self, element_id):
		lvalue = ''.join((element_id, '.id'))
		return self.assign(lvalue, element_id, TYPE.STRING)
		
	## 随机获取给定列表元素
	#  @param items
	#  @return 相应js代码
	def random_item(self, items):
		return items[self.rand.rint(len(items))]
		
	## 产生DOM style属性值
	#  @param count 样式个数
	#  @return 形如 position:static;...
	def generate_style_attribute(self, count=1):
		if count < 1:
			count = 1
		result = []
		for i in xrange(count):
			style = self.random_item(self.STYLES.keys())
			value = self.random_item(self.STYLES[style])
			result.append('%s:%s;' % (style, value))
		return ''.join(result)
		
	## 生成变量声明语句
	#  @param name 变量名
	#  @param value 变量值
	#  @param type js.TYPE 支持类型
	#  @return 变量声明语句
	#  @remark 代码已经添加';'
	@staticmethod
	def declare(name, value=None, type=None):
		if value is None:
			return 'var %s;' % name
		else:
			# assign函数已经添加了';'，所以这里不需要追加
			return 'var %s' % JsGen.assign(name, value, type)
		
	## 生成赋值语句
	#  @param lvalue 赋值左值
	#  @param rvalue 赋值右值
	#  @param type js.TYPE 支持类型
	#  @return 赋值语句
	#  @remark 代码已经添加';'
	@staticmethod
	def assign(lvalue, rvalue, type):
		return '%s = %s;' % (lvalue, TYPE.convert(rvalue, type))
		
	## 生成引用变量语句
	#  @param var 变量
	#  @return 引用变量语句
	@staticmethod
	def ref(var):
		return '%s;' % var
		
	## 生成函数调用语句
	#  @param invoker 函数所属对象 
	#  @param function 函数名
	#  @param args 函数参数 [[参数值,js.TYPE 支持类型], ...]
	#  @return 函数调用语句
	#  @remark 代码已经添加';'
	#  @attention invoker不可为空，比如alert应以window.alert形式调用
	@staticmethod
	def invoke_function(invoker, function, args=[]):
		args_helper = []
		for value, type in args:
			args_helper.append(TYPE.convert(value, type))
		args_str = ', '.join(args_helper)
		
		return '%s.%s(%s);' % (invoker, function, args_str)
		
	## 生成函数定义
	#  @param name 函数名
	#  @param arg_names 函数参数表
	#  @param statements 函数的语句序列
	#  @return 函数定义代码
	@staticmethod
	def create_function(name, arg_names=[], statements=[]):
		return 'function %s(%s){%s}' % \
			(name, ', '.join(arg_names), JsGen.generate_js_code(statements))
			
	## 生成指定js代码序列的js代码
	#  @param js_sets js代码序列
	#  @param wrap True添加try/catch
	#  @return js代码
	@staticmethod
	def generate_js_code(js_sets, wrap=True):
		if wrap:
			return ''.join(map(JsGen.wrapper, js_sets))
		else:
			return ''.join(js_sets)
			
	## try/catch包装语句
	#  @param statement js语句
	#  @return 包装语句
	@staticmethod
	def wrapper(statement):
		return 'try{%s}catch(exception){};' % statement
		
		
if __name__ == '__main__':
	print 'declare has tested assign'
	print 'declare("test")\n%s\n\n' % JsGen.declare('test')
	print 'declare("test", 12, TYPE.NUMBER)\n%s\n\n' % JsGen.declare('test', 12, TYPE.NUMBER)
	print 'declare("test", "null", TYPE.NULL)\n%s\n\n' % JsGen.declare('test', 'null', TYPE.NULL)
	print 'declare("test", "test_str", TYPE.STRING)\n%s\n\n' % JsGen.declare('test', 'test_str', TYPE.STRING)
	print 'declare("test", "test", TYPE.VARIABLE)\n%s\n\n' % JsGen.declare('test', 'test', TYPE.VARIABLE)
	print 'invoke_function("document", "createRange")\n%s\n\n' % JsGen.invoke_function('document', 'createRange')
	print 'invoke_function("window", "alert", [["hello world!" , TYPE.STRING]])\n%s\n\n' % JsGen.invoke_function('window', 'alert', [['hello world!', TYPE.STRING]])
	print 'invoke_function("div_s", "setAttribute", [["test_attr",TYPE.STRING, "test_value",TYPE.STRING]])\n%s\n\n' % JsGen.invoke_function('div_s', 'setAttribute', [['test_attr',TYPE.STRING, 'test_value', TYPE.STRING]])
	print 'create_function("test_func")\n%s\n\n' % JsGen.create_function('test_func')
	print 'create_function("test_func", ["a","b","c"])\n%s\n\n' % JsGen.create_function('test_func', ['a','b','c'])
	print 'create_function("test_func", statements=[declare("test", "test_str", TYPE.STRING), invoke_function("document", "createRange")])\n%s\n\n' % JsGen.create_function('test_func', statements=[JsGen.declare('test', 'test_str', TYPE.STRING), JsGen.invoke_function('document', 'createRange')])
	print 'create_function("test_func", ["a","b","c"], [declare("test", "test_str", TYPE.STRING), invoke_function("document", "createRange")])\n%s\n\n' % JsGen.create_function('test_func', ['a', 'b', 'c'], [JsGen.declare('test', 'test_str', TYPE.STRING), JsGen.invoke_function('document', 'createRange')])
	
	jg = JsGen(['a', 'b'])
	print 'random_append_element()\n%s\n\n' % jg.random_append_element()
	print 'setup_element("div")\n%s\n\n' % jg.setup_element('div')
	print 'fuzz()\n%s\n\n' % jg.fuzz()
		