define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/_base/array",
	"dojo/dom-construct",
	"dojo/on",
	"dojo/query",
	"./GreetingView",
	"../GuestbookStore",
	"./_ViewBaseMixin",
	"dojo/text!./templates/Guestbook.html",
	"dijit/form/ValidationTextBox",
	"dijit/form/Button",
	"dijit/registry"
], function(declare, lang, array, domConstruct, on, query, Greeting, GuestbookStore, _ViewBaseMixin, template, ValidationTextBox,
			_WidgetsInTemplateMixin, registry) {

	return declare([_ViewBaseMixin], {

		templateString: template,
		guestbookName: "",
		guestbookStore: null,

		postCreate: function(data) {
			this.inherited(arguments);
			this.refreshGreetings();

			this.own(
				on(this.switchGuestbookButton,
					"click", lang.hitch(this, "changeGuestBook")),
				on(this.submitNewGreetingButton,
					"click", lang.hitch(this, "addNewGreeting"))
			);
		},

		changeGuestBook: function() {
			this.guestbookName = this.contentSwitchGuestbook.get("value");
			this.refreshGreetings();
		},

		clearGreetings: function() {
			array.forEach(query(".greetingView"), function(greetingNode){
				var widget = registry.byNode(greetingNode);
				widget.destroy();
			})
		},

		getGreetings: function() {
			//console.log(this.guestbookName);
			this.guestbookStore.getGreetings(this.guestbookName)
				.then(
					lang.hitch(this, function(result){
						var greetings = result.greetings;
						var docFragment = document.createDocumentFragment();
						var arrayWidgetGreeting = [];
						array.forEach(greetings, lang.hitch(this, function(item) {
							var data = {
								"guestbook_store": this.guestbookStore,
								"guestbook_name": result.guestbook_name,
								"greeting_id": item.greeting_id,
								"updated_by": item.updated_by !== "" ? item.updated_by:"Anonymous Person",
								"content": item.content,
								"date": item.date
							};
							var greeting = new Greeting(data);
							docFragment.appendChild(greeting.domNode);
							arrayWidgetGreeting.push(greeting);
						}));
						domConstruct.place(docFragment, "greetings", "before");
						array.forEach(arrayWidgetGreeting, lang.hitch(this, function(greeting) {
							greeting.startup();
						}));
					}),
					lang.hitch(this,function(error) {
						alert(error);
					})
				);
		},

		refreshGreetings: function() {
			this.clearGreetings();
			this.getGreetings();
		},

		addNewGreeting: function() {
			if (this.contentNewGreeting.validate() == true) {
				var messageGreeting = this.contentNewGreeting.get("value");
				this.guestbookStore.set("guestbookName", this.guestbookName);
				this.guestbookStore.addGreeting(messageGreeting)
					.then(
						lang.hitch(this, function (data) {
							alert("Insert Success");
							this.contentNewGreeting.set("value", "");
							this.refreshGreetings();
						}),
						lang.hitch(this,function(error) {
							alert(error);
						})
					)
			} else {
				alert("Form invalid");
			}
		}
	});
});