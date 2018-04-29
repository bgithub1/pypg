ace.define("ace/mode/duval2_highlight_rules",[], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

var Duval2HighlightRules = function() {

    this.$rules = {
        "start" : [ 
                   {
                       token : "keyword", // 
                       regex : /[ ^-]{0,2}201[0-9][ ]{1,10}[0-9]{1,8}[ ]{1,10}[0-9]{7}[.][0-9]{4}[ ]{1,10}[A-Z][a-z]{2}[-][0-9]{2}[-]201[0-9][ ]{1,10}[0-9]{4,9}[.][0-9]{4}[ ]{1,10}[0-9]{1,10}[.][0-9]{2}[ ]{1,10}[0-9]{1,10}[.][0-9]{2}[ ]{1,10}[0-9]{1,10}[.][0-9]{2}[ ]{1,10}[0-9]{1,10}[.][0-9]{2}/
                   }, {
                       token : "string", // 
                       regex : /[ ][0-9]{6}[-][0-9]{4}[ ]/
                   }
                   
//        {
//            token : "comment",
//            regex : "\\*.*$"
//        }, {
//            token : "string",           // " string
//            regex : '".*?"'
//        }
       ]
    };
};

Duval2HighlightRules.metaData = {
	    fileTypes: ['text'],
	    name: 'Text'
	};

oop.inherits(Duval2HighlightRules, TextHighlightRules);

exports.Duval2HighlightRules = Duval2HighlightRules;
});

//hello
ace.define("ace/mode/duval2",[], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var Duval2HighlightRules = require("./duval2_highlight_rules").Duval2HighlightRules;

var Mode = function() {
    this.HighlightRules = Duval2HighlightRules;
    this.$behaviour = this.$defaultBehaviour;
};
oop.inherits(Mode, TextMode);

(function() {

    this.lineCommentStart = "*";

    this.$id = "ace/mode/duval2";
}).call(Mode.prototype);

exports.Mode = Mode;

});
                (function() {
                    ace.require(["ace/mode/duval2"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            