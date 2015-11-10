define([
	"dojo/_base/declare",
	"dojo/store/JsonRest",
	"dojo/cookie",
	"dojo/Stateful"
], function(declare, JsonRest, cookie, Stateful) {
	return declare([Stateful], {
		jsonRest: null,
		guestbookName: null,

		constructor: function() {
			this.watch("guestbookName", function(name, oldValue, value) {
				if (oldValue !== value){
					this.jsonRest = new JsonRest({
						target: "/api/guestbook/" + this.guestbookName + "/greeting/",
						headers: {"X-CSRFToken": cookie("csrftoken")}
					});
				}
			});
		},

		getGreetings: function(guestbookName, cursor) {
			this.guestbookName = guestbookName;
			return this.jsonRest.query({
				"guestbook_name": this.guestbookName,
				"cursor" : cursor
			});
		},

		addGreeting: function(guestbookMesage) {
			return this.jsonRest.add({
				"guestbook_name": this.guestbookName,
				"guestbook_mesage": guestbookMesage
			});
		},

		deleteGreeting: function(greetingId, guestbookName) {
			this.set("guestbookName", guestbookName);
			return this.jsonRest.remove(greetingId);
		},

		getGreetingDetail: function(greetingId, guestbookName){
			this.set("guestbookName", guestbookName);
			return this.jsonRest.get(greetingId);
		},

		updateGreeting: function(greetingId, guestbookMesage, guestbookName) {
			this.set("guestbookName", guestbookName);
			return this.jsonRest.put({
				"guestbook_name": this.guestbookName,
				"guestbook_mesage": guestbookMesage,
				"greeting_id": greetingId
			});
		}
	});
});