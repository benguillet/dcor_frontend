// static/js/hipercicUtilities.js
// 6/28/11

// Contains utility functions and support for the "console" jscript object

// create an HttpObject -- different for different browsers //
function makeHttpObject() {
    try {return new XMLHttpRequest();}
    catch (error) {}
    try {return new ActiveXObject("Msxml2.XMLHTTP");}
    catch (error) {}
    try {return new ActiveXObject("Microsoft.XMLHTTP");}
    catch (error) {}
    throw new Error("Could not create HTTP request object.");
      }

// an XML utility function
function getNodeValue(obj,tag) {
    return obj.getElementsByTagName(tag)[0].firstChild.nodeValue;
}

// make an XML DOM object from an XML string (see w3schools.com/xmL/xml_parser.asp)
function parseXMLString(XMLstring)
{
    if(window.DOMParser) // for most browsers
	{
	    parser=new DOMParser();
	    return parser.parseFromString(XMLstring,"text/xml");
	}
    else // Internet Explorer
	{
	    xmlDoc=new ActiveXObject("Microsoft.XMLDOM");
	    xmlDoc.async="false";
	    xmlDoc.loadXML(XMLstring);
	    return xmlDoc;
	}
}


// print to a console line if there is one
// this is sort of a "debugging printf" method.
// Works with this line of HTML: <br><br><br>Console Output:<input type="text" id="consoleOutputBox" value="" readonly="readonly" size="50" />
function console(str) {
    try {
	document.getElementById("consoleOutputBox").value = str;
    }
    catch(err) {} // fail silently
}
