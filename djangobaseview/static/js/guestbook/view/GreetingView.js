define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/on",
	"dojo/dom-style",
	"./_ViewBaseMixin",
	"../models/Greeting",
	"dojo/text!./templates/Greeting.html",


], function(declare, lang, on, domStyle, _ViewBaseMixin, Greeting, template) {

		return declare("GreetingView", [_ViewBaseMixin], {

			templateString: template,
			guestbookStore: null,
			model : new Greeting(),

			constructor: function(data) {
				this.model.guestbookName = data.guestbook_name;
				this.model.greeting_id = data.greeting_id;
				this.model.content = data.content;
				this.model.date = data.date;
				if (data.updated_by !== "None") {
					this.model.author = data.updated_by;
				} else {
					this.model.author = "Anonymous Person";
				}
				this.guestbookStore = data.guestbook_store;
			},

			postCreate: function(data) {
				this.inherited(arguments);

				this.own(
					on(this.deleteButton,
						"click", lang.hitch(this, "deleteGreeting")),
					on(this.openEditFormButton,
						"click", lang.hitch(this, "openEditForm")),
					on(this.submitUpdateGreetingButton,
						"click", lang.hitch(this, "updateGreeting"))
				);
			},

			deleteGreeting: function() {
				this.guestbookStore.deleteGreeting(this.model.greeting_id, this.model.guestbookName)
					.then(
						lang.hitch(this, function(data) {
							alert("Delete Success");
							this.destroyRecursive();
						}),
						lang.hitch(this,function(error) {
							alert(error);
						})
					);
			},

			openEditForm: function() {
				this.guestbookStore.getGreetingDetail(this.model.greeting_id, this.model.guestbookName)
					.then(
						lang.hitch(this, function(data) {
							var formNode = this.editFormNode;
							domStyle.set(formNode, {"display": "block"});
							this.contentTextbox.set("value", data.content);
						}),
						lang.hitch(this,function(error) {
							alert(error);
						})
					);
			},

			updateGreeting: function() {
				if (this.contentTextbox.validate() == true) {
					this.model.content = this.contentTextbox.value

					this.guestbookStore.updateGreeting(this.model.greeting_id, this.model.content,this.model.guestbookName )
						.then(
							lang.hitch(this, function () {
								alert("Update Success");
								console.log(this.contentNode)
								this.contentNode.innerHTML = this.model.content
								var formNode = this.editFormNode;
								domStyle.set(formNode, {"display": "none"});
							}),
							lang.hitch(this,function(error) {
								alert(error);
							})
						)
				} else {
					alert("Form Invalid");
				}
			}
		});
});