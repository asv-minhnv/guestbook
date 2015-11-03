define([
	"dojo/_base/declare",
	"dojo/store/JsonRest",
	"dojo/cookie",
	"dojo/Stateful"
], function(declare, JsonRest, cookie, Stateful){
	return declare([Stateful],{
		jsonRest: null,
		guestbookName: null,

		_guestbookNameGetter: function(){
			return this.guestbookName;
		},

		_guestbookNameSetter: function(guestbook_name){
			this.guestbookName = guestbook_name;
		},

		constructor: function(){
			this.watch("guestbookName", function(name, oldValue, value){
				if (oldValue !== value){
					this.guestbookName = value;
					this.jsonRest = new JsonRest({
						target: "/api/guestbook/" + this.guestbookName + "/greeting/",
						headers: {"X-CSRFToken": cookie("csrftoken")}
					});
				}
			});
		},

		getGreetings: function(guestbook_name, cursor){
			return this.jsonRest.query({
				"cursor" : cursor
			});
		},

		addGreeting: function(guestbook_mesage){
			return this.jsonRest.add({
				"guestbook_name": this.guestbookName,
				"guestbook_mesage": guestbook_mesage
			});
		},

		deleteGreeting: function(greeting_id){
			return this.jsonRest.remove(greeting_id);
		},

		getGreetingDetail: function(greeting_id){
			console.log(this.jsonRest.get(greeting_id))
			return this.jsonRest.get(greeting_id);
		},

		updateGreeting: function(greeting_id, guestbook_mesage){
			return this.jsonRest.put({
				"guestbook_name": this.guestbookName,
				"guestbook_mesage": guestbook_mesage,
				"id": greeting_id
			});
		}
	});
});