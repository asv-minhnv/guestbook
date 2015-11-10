define([
	"dojo/_base/config",
	"dojo/parser",
	"dojo/ready",
	"dojo/dom",
	"./view/GuestbookView",
	"./GuestbookStore"
], function(config, parser, ready, dom, GuestbookView, GuestbookStore) {

	ready(function() {
		if (!config.parseOnLoad) {
			parser.parse();
		}
		var guestbookName = "default_guestbook";
		var store = new GuestbookStore({"guestbookName": guestbookName});
		var guestbook = new GuestbookView({
			"guestbookName": guestbookName,
			"guestbookStore": store
		});
		var result = dom.byId("result");
		guestbook.placeAt(result);
	});

});