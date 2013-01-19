if(!ThunderSpy) var ThunderSpy = {};

ThunderSpy.log = function(str) {
  econsole = Components.classes["@mozilla.org/consoleservice;1"]
    .getService(Components.interfaces.nsIConsoleService);
  econsole.logStringMessage("ThunderSpy: "+str);
}

