/**
 * Created by Adm on 04.08.2016.
 */
if (typeof common == 'undefined')
  common = {};
if (typeof common.funcs == 'undefined')
  common.funcs = {};

(function() {
    this.getRandomInt = function(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    };

    this.visibilityChanged = function(show, hide) {
        var hidden, visibilityState, visibilityChange;

        if (typeof document.hidden !== "undefined")
            hidden = "hidden", visibilityChange = "visibilitychange", visibilityState = "visibilityState";
        else if (typeof document.msHidden !== "undefined")
            hidden = "msHidden", visibilityChange = "msvisibilitychange", visibilityState = "msVisibilityState";

        document.addEventListener(visibilityChange, function () {
            if (document[hidden] && hide)
                hide();
            else if (!document[hidden] && show)
                show();
        });
    };

    this.shuffle = function(array) {
        var copy = [], n = array.length, i;
        while (n) {
            i = Math.floor(Math.random() * array.length);
            if (i in array) {
                copy.push(array[i]);
                delete array[i];
                n--;
            }
        }
        return copy;
    }

}).call(common.funcs);