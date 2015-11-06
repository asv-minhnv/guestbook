define([
	"dojo/_base/config",
	"dojo/parser",
	"dojo/ready",
	"dojo/dom",
	"./view/Guestbook",
], function(config, parser, ready, dom, Guestbook) {

	ready(function() {
		if (!config.parseOnLoad) {
			parser.parse();
		}

		var guestbook = new Guestbook({"guestbook_name": "default_guestbook"});
		var result = dom.byId("result");
		guestbook.placeAt(result);
	});

});