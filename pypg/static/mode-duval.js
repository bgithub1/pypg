ace.define("ace/mode/duval_highlight_rules",[], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;

var DuvalHighlightRules = function() {
    this.$rules = {
        "start" : [
            {
                token : "keyword", // 
                regex : /[ ^-]{0,2}201[0-9][ ]{1,20}[0-9]{1,8}[ ]{1,20}[0-9]{7}[.][0-9]{4}[ ]{1,20}[A-Z][a-z]{2}[-][0-9]{2}[-]201[0-9][ ]{1,20}[0-9]{4,9}[.][0-9]{4}[ ]{1,30}[0-9]{1,20}[.][0-9]{2}[ ]{1,20}[0-9]{1,20}[.][0-9]{2}[ ]{1,20}[0-9]{1,20}[.][0-9]{2}[ ]{1,20}[0-9]{1,20}[.][0-9]{2}/
            }, {
                token : "keyword", // 
                regex : /^[ ]+[0-9]{6}[-][0-9]{4}[ ]+$/
            }
        ]
    };
    
    this.normalizeRules();
};

DuvalHighlightRules.metaData = {
    fileTypes: ['text'],
    name: 'Text'
};

oop.inherits(DuvalHighlightRules, TextHighlightRules);

exports.DuvalHighlightRules = DuvalHighlightRules;
});

ace.define("ace/mode/duval",[], function(require, exports, module) {
"use strict";

var oop = require("../lib/oop");
var TextMode = require("./text").Mode;
var DuvalHighlightRules = require("./duval_highlight_rules").DuvalHighlightRules;

var Mode = function() {
    this.HighlightRules = DuvalHighlightRules;
    this.$behaviour = this.$defaultBehaviour;
};
oop.inherits(Mode, TextMode);

(function() {
    this.lineCommentStart = "#";
    this.$id = "ace/mode/duval";
}).call(Mode.prototype);

exports.Mode = Mode;
});
                (function() {
                    ace.require(["ace/mode/duval"], function(m) {
                        if (typeof module == "object" && typeof exports == "object" && module) {
                            module.exports = m;
                        }
                    });
                })();
            